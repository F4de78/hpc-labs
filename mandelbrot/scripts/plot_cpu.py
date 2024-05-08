import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


sns.set_theme()


def plot_time_inv(data):
    fig = plt.figure(figsize=(10, 6))

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
    fig = plt.figure(figsize=(10, 6))

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
    fig.savefig(f"report/img_cpu/{fname}")


def plot_speedup(data, fname="speedup.pdf"):
    fig = plt.figure(figsize=(10, 6))
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

    fig.savefig(f"report/img_cpu/{fname}")


def plot_efficiency(data, fname="efficiency.pdf"):
    fig = plt.figure(figsize=(10, 6))
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
    fig = plt.figure(figsize=(10, 6))

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


def plot_vectorization_only_speedup(data, vect_data, no_fma_data):
    fig = plt.figure()

    ax = sns.lineplot(
        data=data[data["thread_no"] == 1],
        x="res",
        y="average_time",
        label="Reference",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax = sns.lineplot(
        data=no_fma_data[no_fma_data["thread_no"] == 1],
        x="res",
        y="average_time",
        label="Vectorized",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax = sns.lineplot(
        data=vect_data[vect_data["thread_no"] == 1],
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

    fig.savefig("report/img_cpu/vect_gains.pdf")


def plot_single_threaded_time_ratios(data):
    fig = plt.figure(figsize=(10, 6))

    ax = sns.lineplot(
        data=data[data["thread_no"] == 1],
        x="res",
        y="time_ratio",
        label="Vect + FMA / Baseline",
        marker="o",
        markers=True,
        dashes=False,
    )

    ax = sns.lineplot(
        data=data[data["thread_no"] == 1],
        x="res",
        y="time_ratio_no_fma",
        label="Vect / Baseline",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax.set_xticks(data["res"].unique())

    ax.set_ylabel("Average time ratio")
    ax.set_xlabel("Resolution")
    ax.set_title("Average single threaded time ratio")
    ax.legend(title="Code version")

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    fig.savefig("report/img_cpu/time-single-thread-ratio.pdf")


def plot_double_vs_float(float_data, double_data):
    fig = plt.figure()

    ax = sns.lineplot(
        data=float_data[float_data["thread_no"] == 1],
        x="res",
        y="average_time",
        label="float",
        marker="o",
        markers=True,
        dashes=False,
    )

    ax = sns.lineplot(
        data=double_data[double_data["thread_no"] == 1],
        x="res",
        y="average_time",
        label="double",
        marker="o",
        markers=True,
        dashes=False,
    )
    ax.set_xticks(float_data["res"].unique())

    ax.set_ylabel("Average execution time (ms)")
    ax.set_xlabel("Resolution")
    ax.set_title("Average single threaded time")
    ax.legend(title="Code version")

    fig.savefig("report/img_cpu/float_vs_double.pdf")


def get_vect_data():
    data = pd.read_csv("report/data_cpu_vect.csv")

    # only keep the optimal configuration
    data = data[
        (data["ftype"] == "double")
        & (data["fma"] == True)
        & (data["omp_schedule"] == "dynamic")
    ]

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


def get_float_vect_data():
    data = pd.read_csv("report/data_cpu_vect.csv")

    # only keep the optimal configuration
    data = data[
        (data["ftype"] == "float")
        & (data["fma"] == True)
        & (data["omp_schedule"] == "dynamic")
    ]

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


def get_vect_data_no_fma():
    data = pd.read_csv("report/data_cpu_vect.csv")

    # only keep the optimal configuration
    data = data[
        (data["ftype"] == "double")
        & (data["fma"] == False)
        & (data["omp_schedule"] == "dynamic")
    ]

    data["average_time"] = data.groupby(["res", "thread_no"])["time"].transform("mean")

    data = data[["res", "thread_no", "average_time", "fma"]].drop_duplicates()

    data["speedup"] = data.apply(
        lambda row: data[
            (data["res"] == row["res"])
            & (data["thread_no"] == 1)
            & (data["fma"] == row["fma"])
        ]["average_time"].iloc[0]
        / row["average_time"],
        axis=1,
    )
    data["efficiency"] = data["speedup"] / data["thread_no"]
    return data


def get_data():
    data = pd.read_csv("report/data_cpu.csv")

    # only keep the optimal configuration
    data = data[data["omp_schedule"] == "dynamic"]
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
    data = get_data()
    vect_data = get_vect_data()
    vect_no_fma = get_vect_data_no_fma()
    vect_float_data = get_float_vect_data()

    print("vect_data:\n", vect_data)
    plot_time(vect_data, fname="time-vect.pdf")
    plot_time_inv(vect_data)
    plot_speedup(vect_data, fname="speedup-vect.pdf")
    plot_efficiency(vect_data, fname="efficiency-vect.pdf")

    plot_double_vs_float(vect_float_data, vect_data)

    plot_diff(data, vect_data)
    plot_vectorization_only_speedup(data, vect_data, vect_no_fma)
    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)

    # Merge the two dataframes on 'thread_no' and 'res'
    merged_data = pd.merge(
        data, vect_data, on=["thread_no", "res"], suffixes=("_data", "_vect_data")
    )

    # Calculate the ratio and store it in a new column
    merged_data["time_ratio"] = (
        merged_data["average_time_data"] / merged_data["average_time_vect_data"]
    )
    plot_time_ratio(merged_data)

    merged_data = pd.merge(merged_data, vect_no_fma, on=["thread_no", "res"])

    # Calculate the ratio and store it in a new column
    merged_data["time_ratio_no_fma"] = (
        merged_data["average_time_data"] / merged_data["average_time"]
    )

    plot_single_threaded_time_ratios(merged_data)


if __name__ == "__main__":
    main()
