import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sns.set_theme()

def plot_heatmap(data, n: int):
    fig, ax = plt.subplots(figsize=(10, 10))
    data = data[data['resolution'] == n]
    data = data.pivot(index='thread_y', columns='thread_x', values='average_time_gpu')
    sns.heatmap(data, annot=True, fmt=".2f", linewidths=0, ax=ax, cmap="magma_r")
    ax.set_xlabel('#Thread per block (x)')
    ax.set_ylabel('#Thread per block (y)')
    ax.set_title(f"Heatmap of execution times for n = {n}")
    fig.savefig(f"report/img_gpu/heatmap_{n}.pdf")

def plot_line(data, n: int):
    data = data[data['resolution'] == n]
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(data=data, x="thread_x", y="average_time_gpu", hue="thread_y", ax=ax, marker="o", palette="tab10")
    ax.set_title(f"Lineplot of execution times for n = {n}")
    ax.legend(title='#Thread per block (y)')
    ax.set_xlabel('#Thread per block (x)')
    ax.set_ylabel('Average time (ms)')
    fig.savefig(f"report/img_gpu/lineplot_{n}.pdf")

def plot_line_3d(data, n: int):
    data = data[data['resolution'] == n]
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(data['thread_x'], data['thread_y'], data['average_time_gpu'], cmap="vlag")
    ax.set_xlabel('#Thread per block (x)')
    ax.set_ylabel('#Thread per block (y)')
    ax.set_zlabel('Average time (ms)')
    ax.invert_yaxis()  # Reverse the order of the y-axis
    ax.set_title(f"3D plot of execution times for n = {n}")
    fig.savefig(f"report/img_gpu/lineplot3d_{n}.pdf")


def main():
    data = pd.read_csv('report/data_gpu.csv')
    data['average_time_gpu'] = data.groupby(['resolution', 'thread_x', 'thread_y'])['time_gpu'].transform('mean')
    data = data[['resolution', 'thread_x', 'thread_y', 'average_time_gpu']].drop_duplicates()
    data.to_csv('report/data_graph_gpu.csv', index=False)
    for n in data['resolution'].unique():
        plot_heatmap(data, n)
        plot_line(data, n)
        plot_line_3d(data, n)

if __name__ == "__main__":
    main()
