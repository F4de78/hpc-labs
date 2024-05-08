import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sns.set_theme()


def plot_heatmap(data, n: int):
    fig, ax = plt.subplots(figsize=(10, 10))
    data = data[data["resolution"] == n]
    data = data.pivot(index="thread_y", columns="thread_x", values="average_time_gpu")
    sns.heatmap(data, annot=True, fmt=".2f", linewidths=0, ax=ax, cmap="magma_r")
    ax.set_xlabel("#Thread per block (x)")
    ax.set_ylabel("#Thread per block (y)")
    ax.set_title(f"Heatmap of execution times for n = {n}")
    fig.savefig(f"report/img_gpu/heatmap_{n}.pdf")


def plot_line(data, n: int):
    data = data[data["resolution"] == n]
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(
        data=data,
        x="thread_x",
        y="average_time_gpu",
        hue="thread_y",
        ax=ax,
        marker="o",
        palette="tab10",
    )
    ax.set_title(f"Lineplot of execution times for n = {n}")
    ax.legend(title="#Thread per block (y)")
    ax.set_xlabel("#Thread per block (x)")
    ax.set_ylabel("Average time (ms)")
    fig.savefig(f"report/img_gpu/lineplot_{n}.pdf")


# plot a lineplot where on the x axys  there are the tuple (x_thread,y_thread), on the y axys the average time for every resolution
def plot_gpu_square(data):
    fig, ax = plt.subplots(figsize=(10, 10))
    data = data[data["thread_x"] == data["thread_y"]]
    # for every resolution plot the average time
    for n in data["resolution"].unique():
        data_n = data[data["resolution"] == n]
        sns.lineplot(
            data=data_n,
            x="thread_x",
            y="average_time_gpu",
            ax=ax,
            marker="o",
            label=f"{n}",
        )
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str((x, x))))
    # plt.yscale("log")
    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("Thread number")
    ax.set_title(f"Lineplot of execution times for every resolution")
    fig.savefig(f"report/img_gpu/square.pdf")


def plot_time(data):
    fig = plt.figure(figsize=(10, 10))

    data = data[data["thread_x"] == data["thread_y"]]
    for n in data["thread_x"].unique():
        ax = sns.lineplot(
            data=data[data["thread_x"] == n],
            x="resolution",
            y="average_time_gpu",
            label=f"({n},{n})",
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["resolution"].unique())
    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("Resolution")
    ax.set_title("Average execution time")
    ax.legend(title="#Thread")
    fig.savefig(f"report/img_gpu/gpu_time.pdf")


def plot_line_3d(data, n: int):
    data = data[data["resolution"] == n]
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(
        data["thread_x"], data["thread_y"], data["average_time_gpu"], cmap="vlag"
    )
    ax.set_xlabel("#Thread per block (x)")
    ax.set_ylabel("#Thread per block (y)")
    ax.set_zlabel("Average time (ms)")
    ax.invert_yaxis()  # Reverse the order of the y-axis
    ax.set_title(f"3D plot of execution times for n = {n}")
    fig.savefig(f"report/img_gpu/lineplot3d_{n}.pdf")


def main():
    data = pd.read_csv("report/data_gpu.csv")
    data = data[data["ftype"] == "double"]
    data["average_time_gpu"] = data.groupby(["resolution", "thread_x", "thread_y"])[
        "time_gpu"
    ].transform("mean")
    data = data[
        ["resolution", "thread_x", "thread_y", "average_time_gpu"]
    ].drop_duplicates()
    data.to_csv("report/data_graph_gpu.csv", index=False)

    for n in data['resolution'].unique():
        plot_heatmap(data, n)
    #     plot_line(data, n)
    plot_time(data)
    plot_gpu_square(data)
    # plot_line_3d(data, n)


if __name__ == "__main__":
    main()


def print_aggregate_table():
    data = pd.read_csv("report/data_gpu.csv")

    data = data[(data["thread_x"] == 16) & (data["thread_y"] == 16)][
        ["resolution", "time_gpu", "ftype"]
    ]

    data["average_time"] = data.groupby(["resolution", "ftype"])["time_gpu"].transform(
        "mean"
    )

    data = data[["resolution", "average_time", "ftype"]].drop_duplicates()

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(data)
