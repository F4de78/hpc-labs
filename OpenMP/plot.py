import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme()



def plot_time(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="time",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    #plt.xscale('log')
    fig.savefig("time.pdf") 

def plot_speedup(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="speedup",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    #plt.xscale('log')
    fig.savefig("speedup.pdf") 

def plot_efficiency(data):
    fig = plt.figure()
    for n in data['n'].unique():
        ax = sns.lineplot(data=data[data['n']==n], x="thread_no", y="efficiency",label=n, marker='o', markers=True, dashes=False)
    ax.set_xticks(data['thread_no'].unique())
    #plt.xscale('log')
    fig.savefig("efficiency.pdf") 

def main():
    data = pd.read_csv('data.csv')
    plot_time(data)
    plot_speedup(data)
    plot_efficiency(data)


if __name__ == "__main__":
    main()
