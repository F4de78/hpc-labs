import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme()


def plot_time(data):
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
    fig.savefig("report/img_cpu/time.pdf")


def plot_speedup(data):
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
    fig.savefig("report/img_cpu/speedup.pdf")


def plot_efficiency(data):
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
    fig.savefig("report/img_cpu/efficiency.pdf")


def main():
    data = pd.read_csv("report/data_cpu_vect.csv")
    # filter the optimal configuration
    print(data)
    data = data[
        (data["ftype"] == "float")
        & (data["fma"] == True)
        & (data["omp_scheduler"] == "dynamic")
    ]
    print(data)
    data["average_time"] = data.groupby(["res", "thread_no"])["time"].transform("mean")
    data = data[
        ["res", "thread_no", "average_time", "speedup", "efficiency"]
    ].drop_duplicates()
    print(data)
    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)


if __name__ == "__main__":
    main()
