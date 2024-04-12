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
    ax.legend(title="Resolution")
    #plt.xscale('log')
    fig.savefig("report/img_cpu/time.pdf") 

def plot_speedup(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="speedup",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    ax.set_ylabel("Average speedup")
    ax.set_xlabel("#Thread")
    ax.set_title("Average speedup")
    ax.legend(title="Resolution")
    #plt.xscale('log')
    fig.savefig("report/img_cpu/speedup.pdf") 

def plot_efficiency(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="efficiency",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    ax.set_ylabel("Average efficiency")
    ax.set_xlabel("#Thread")
    ax.set_title("Average efficiency")
    ax.legend(title="Resolution")
    #plt.xscale('log')
    fig.savefig("report/img_cpu/efficiency.pdf") 

def main():
    data = pd.read_csv('report/data_cpu.csv')
    data['average_time'] = data.groupby(['n', 'thread_no'])['time'].transform('mean')
    data = data[['n', 'thread_no', 'average_time']].drop_duplicates()
    data['speedup'] = data.apply(lambda row: data[(data['n'] == row['n']) & (data['thread_no'] == 1)]['average_time'].iloc[0] / row['average_time'], axis=1)
    data['efficiency'] = data['speedup'] / data['thread_no']
    print(data)
    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)


if __name__ == "__main__":
    main()
