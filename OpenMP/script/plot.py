import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme()

def plot_time(data):
    fig = plt.figure()

    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="average_time",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    ax.set_ylabel("Average time (s)")
    ax.set_xlabel("#Thread")
    ax.set_title("Average execution time")
    #plt.xscale('log')
    fig.savefig("time.pdf") 

def plot_speedup(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="speedup",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    ax.set_ylabel("Average speedup")
    ax.set_xlabel("#Thread")
    ax.set_title("Average speedup")
    #plt.xscale('log')
    fig.savefig("speedup.pdf") 

def plot_efficiency(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="efficiency",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    ax.set_ylabel("Average efficiency")
    ax.set_xlabel("#Thread")
    ax.set_title("Average efficiency")
    #plt.xscale('log')
    fig.savefig("efficiency.pdf")

def plot_double_vs_float(data):
    fig = plt.figure()

    ax = sns.lineplot(
        data=data[(data["thread_no"] == 1) & (data["ftype"] == "float")],
        x="res",
        y="average_time",
        label="float",
        marker="o",
        markers=True,
        dashes=False,
    )

    ax = sns.lineplot(
        data=data[(data["thread_no"] == 1) & (data["ftype"] == "double")],
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

def main():
    data = pd.read_csv('report/data.csv')
    data['average_time'] = data.groupby(['n', 'thread_no', 'ftype'])['time'].transform('mean')
    data = data[['n', 'thread_no', 'ftype', 'average_time']].drop_duplicates()
    data['speedup'] = data.apply(lambda row: data[(data['n'] == row['n']) & (data['thread_no'] == 1) & (data['ftype'] == row['ftype'])]['average_time'].iloc[0] / row['average_time'], axis=1)
    data['efficiency'] = data['speedup'] / data['thread_no']
    print(data)

    plot_double_vs_float(data)

    data = data[data['ftype'] == 'float']

    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)


if __name__ == "__main__":
    main()
