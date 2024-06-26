import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme()


def plot_time(data):
    fig = plt.figure(figsize=(10, 7))

    for thread_no in data["thread_no"].unique():
        ax = sns.lineplot(
            data=data[data["thread_no"] == thread_no],
            x="n",
            y="average_time",
            label=thread_no,
            marker="o",
            markers=True,
            dashes=False,
        )
    ax.set_xticks(data["n"].unique())
    ax.set_ylabel("Average time (s)")
    ax.set_xlabel("N")
    ax.set_title("Average execution time")

    ax.tick_params(axis="x", labelrotation=45)

    ax.legend(title="#Thread")

    fig.savefig("report/img/time.pdf")


def plot_speedup(data):
    fig = plt.figure()
    for n in data["n"].unique():
        ax = sns.lineplot(
            data=data[data["n"] == n],
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

    ax.legend(title="N")

    fig.savefig("report/img/speedup.pdf")


def plot_efficiency(data):
    fig = plt.figure()
    for n in data["n"].unique():
        ax = sns.lineplot(
            data=data[data["n"] == n],
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

    ax.legend(title="N")

    fig.savefig("report/img/efficiency.pdf")


def plot_double_vs_float(data):
    fig = plt.figure(figsize=(10, 7))

    ax = sns.lineplot(
        data=data[(data["thread_no"] == 1) & (data["ftype"] == "float")],
        x="n",
        y="average_time",
        label="float",
        marker="o",
        markers=True,
        dashes=False,
    )

    ax = sns.lineplot(
        data=data[(data["thread_no"] == 1) & (data["ftype"] == "double")],
        x="n",
        y="average_time",
        label="double",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax.set_xticks(data["n"].unique())

    ax.set_ylabel("Average execution time (ms)")
    ax.set_xlabel("N")

    ax.tick_params(axis="x", labelrotation=45)

    ax.set_title("Average single threaded time")
    ax.legend(title="Floating point type")

    fig.savefig("report/img/float_vs_double.pdf")


def main():
    data = pd.read_csv("report/data.csv")
    data["average_time"] = data.groupby(["n", "thread_no"])["time"].transform("mean")
    data = data[["n", "thread_no", "average_time"]].drop_duplicates()
    data["speedup"] = data.apply(
        lambda row: data[(data["n"] == row["n"]) & (data["thread_no"] == 1)][
            "average_time"
        ].iloc[0]
        / row["average_time"],
        axis=1,
    )
    data["efficiency"] = data["speedup"] / data["thread_no"]

    with pd.option_context("display.max_rows", None):
        print(data)

    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)


if __name__ == "__main__":
    main()
