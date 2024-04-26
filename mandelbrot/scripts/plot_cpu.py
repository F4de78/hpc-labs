import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


sns.set_theme()


def plot_time_inv(data):
    fig = plt.figure()

    for n in data["res"].unique():
        ax = sns.lineplot(
            data=data[data["res"] == n],
            x="thread_no",
            y="average_time",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["thread_no"].unique())

    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("#Thread")
    ax.set_title("Average execution time")
    ax.legend(title="Resolution")
    plt.yscale("log")
    fig.savefig("report/img_cpu/time-inv.pdf")


def plot_time(data, fname="time.pdf"):
    fig = plt.figure()

    for n in data["thread_no"].unique():
        ax = sns.lineplot(
            data=data[data["thread_no"] == n],
            x="res",
            y="average_time",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["res"].unique())

    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("Resolution")
    ax.set_title("Average execution time")
    ax.legend(title="#Thread")
    # plt.xscale('log')
    fig.savefig(f"report/img_cpu/{fname}")


def plot_speedup(data, fname="speedup.pdf"):
    fig = plt.figure()
    for n in data["res"].unique():
        ax = sns.lineplot(
            data=data[data["res"] == n],
            x="thread_no",
            y="speedup",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["thread_no"].unique())
    ax.set_ylabel("Average speedup")
    ax.set_xlabel("#Thread")
    ax.set_title("Average speedup")
    ax.legend(title="Resolution")
    # plt.xscale('log')
    fig.savefig(f"report/img_cpu/{fname}")


def plot_efficiency(data, fname="efficiency.pdf"):
    fig = plt.figure()
    for n in data["res"].unique():
        ax = sns.lineplot(
            data=data[data["res"] == n],
            x="thread_no",
            y="efficiency",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["thread_no"].unique())
    ax.set_ylabel("Average efficiency")
    ax.set_xlabel("#Thread")
    ax.set_title("Average efficiency")
    ax.legend(title="Resolution")
    # plt.xscale('log')
    fig.savefig(f"report/img_cpu/{fname}")


def plot_diff(data, vect_data):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(18, 8))

    for n in data["thread_no"].unique():
        ax = sns.lineplot(
            data=data[data["thread_no"] == n],
            x="res",
            y="average_time",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
            ax=ax1,
        )
    ax.set_xticks(data["res"].unique())

    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("Resolution")
    ax.set_title("Not vectorized")
    # ax.legend(title="#Thread")

    for n in data["thread_no"].unique():
        ax = sns.lineplot(
            data=vect_data[vect_data["thread_no"] == n],
            x="res",
            y="average_time",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
            ax=ax2,
        )
    ax.set_xticks(vect_data["res"].unique())

    ax2.set_ylabel("Average time (ms)")
    ax2.set_xlabel("Resolution")
    ax2.set_title("Vectorized")
    ax2.legend(title="#Thread")

    fig.suptitle("Average execution time")

    fig.savefig("report/img_cpu/time-diff.pdf")


def plot_time_ratio(data):
    fig = plt.figure()

    for n in data["res"].unique():
        ax = sns.lineplot(
            data=data[data["res"] == n],
            x="thread_no",
            y="time_ratio",
            label=n,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["thread_no"].unique())

    ax.set_ylabel("Average time ratio")
    ax.set_xlabel("#Thread")
    ax.set_title("Average time ratio")
    ax.legend(title="Resolution")

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    fig.savefig("report/img_cpu/time-ratio.pdf")

def plot_vectorization_only_speedup(data, vect_data):
    fig = plt.figure()

    ax = sns.lineplot(
        data=data[data["thread_no"] ==1],
        x="res",
        y="average_time",
        label="Reference",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax = sns.lineplot(
        data=vect_data[(vect_data["thread_no"] ==1) & (vect_data["fma"] == False)],
        x="res",
        y="average_time",
        label="Vectorized",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax = sns.lineplot(
        data=vect_data[(vect_data["thread_no"] ==1) & (vect_data["fma"] == True)],
        x="res",
        y="average_time",
        label="Vectorized + FMA",
        marker="o",
        markers=True,
        dashes=False,
    )

    ax.set_xticks(data["res"].unique())

    ax.set_ylabel("Average time (ms)")
    ax.set_xlabel("Resolution")
    ax.set_title("Average execution time")
    ax.legend(title="Program")
    # plt.xscale('log')
    fig.savefig("report/img_cpu/vect_gains.pdf")


def get_vect_data():
    data = pd.read_csv("report/data_cpu_vect.csv")
    # only keep the optimal configuration
    print(data)
    data = data[
        (data["ftype"] == "float")
        & (data["omp_scheduler"] == "dynamic")
    ]
    print(data)
    data["average_time"] = data.groupby(["res", "thread_no", "fma"])["time"].transform("mean")

    data = data[["res", "thread_no", "average_time", "fma"]].drop_duplicates()

    data["speedup"] = data.apply(
        lambda row: data[(data["res"] == row["res"]) & (data["thread_no"] == 1) & (data["fma"] == row["fma"])][
            "average_time"
        ].iloc[0]
        / row["average_time"],
        axis=1,
    )
    data["efficiency"] = data["speedup"] / data["thread_no"]
    return data


def get_data():
    data = pd.read_csv("report/data_cpu.csv")
    # only keep the optimal configuration
    data = data[data["omp_scheduler"] == "dynamic"]
    data["average_time"] = data.groupby(["res", "thread_no"])["time"].transform("mean")

    data = data[["res", "thread_no", "average_time"]].drop_duplicates()

    data["speedup"] = data.apply(
        lambda row: data[(data["res"] == row["res"]) & (data["thread_no"] == 1)][
            "average_time"
        ].iloc[0]
        / row["average_time"],
        axis=1,
    )
    data["efficiency"] = data["speedup"] / data["thread_no"]

    return data


def main():
    vect_data = get_vect_data()
    print(vect_data)

    fma_vect_data = vect_data[vect_data["fma"] == True][["res", "thread_no", "average_time", "speedup", "efficiency"]].drop_duplicates()

    plot_time(fma_vect_data, fname="time-vect.pdf")
    plot_time_inv(fma_vect_data)
    plot_speedup(fma_vect_data, fname="speedup-vect.pdf")
    plot_efficiency(fma_vect_data, fname="efficiency-vect.pdf")

    data = get_data()
    plot_diff(data, fma_vect_data)
    plot_vectorization_only_speedup(data, vect_data)
    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)

    # Merge the two dataframes on 'thread_no' and 'res'
    merged_data = pd.merge(
        data, fma_vect_data, on=["thread_no", "res"], suffixes=("_data", "_vect_data")
    )

    # Calculate the ratio and store it in a new column
    merged_data["time_ratio"] = (
        merged_data["average_time_data"] / merged_data["average_time_vect_data"]
    )
    plot_time_ratio(merged_data)


if __name__ == "__main__":
    main()
