import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme()

def plot_heatmap(data):
    fig, ax = plt.subplots(figsize=(10, 10))
    data = data.pivot("thread_y", "thread_x", "average_time_gpu")
    sns.heatmap(data, annot=True, fmt=".2f", linewidths=0, ax=ax, cmap="vlag")
    ax.set_title("Heatmap of execution times")
    fig.savefig("report/img/heatmap.pdf")

def plot_line(data):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(data=data, x="thread_x", y="average_time_gpu", hue="thread_y", ax=ax, marker="o", palette="tab10")
    ax.set_title("Lineplot of execution times")
    fig.savefig("report/img/lineplot.pdf")

# plot a graph where n = 1000 and the x axis is pair (thread_x, thread_y) and the y axis is the average gpu time for the tuple (thread_x, thread_y)
def plot_cpu_gpu(data, n: int):
    fig, ax = plt.subplots(figsize=(10, 10))
    data = data[data['n'] == n]
    # gropuby and mean to get the average time for each pair where thread_x = thread_y
    data = data[data['thread_x'] == data['thread_y']]
    data = data.groupby(['thread_x', 'thread_y']).mean().reset_index()
    sns.lineplot(data=data, x="thread_x", y="average_time_cpu", ax=ax, marker="o", label="CPU", color="tab:blue")
    ax = sns.lineplot(data=data, x="thread_x", y="average_time_gpu", ax=ax, marker="o", label="GPU", color="tab:orange")
    plt.yscale('log')
    ax.set_xticks([1,2,4,8,16])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str((x,x))))
    ax.set_ylabel("Average time (s)")
    ax.set_xlabel("Thread number")
    ax.set_title(f"Lineplot of execution times for n = {n}")
    fig.savefig("report/img/cpu_gpu.pdf")

def main():
    data = pd.read_csv('report/data.csv')
    data['average_time_gpu'] = data.groupby(['n', 'thread_x', 'thread_y'])['time_gpu'].transform('mean')
    data['average_time_cpu'] = data.groupby(['n'])['time_cpu'].transform('mean')
    data = data[['n', 'thread_x', 'thread_y', 'average_time_gpu', 'average_time_cpu']].drop_duplicates()
    print(data)
    plot_heatmap(data)
    plot_line(data)
    plot_cpu_gpu(data, 1000)


if __name__ == "__main__":
    main()
