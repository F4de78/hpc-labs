import subprocess
import itertools as it
import logging
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import csv

NS = [2_000, 4_000, 8_000, 16_000, 32_000, 48_000]
THREAD_NOS = [1, 2, 4, 8, 16, 24]
# COMP = "clang"
CFLAGS = ["-xHost", "-qopenmp", "-std=c99", "-fast"]

COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-O3"]
sns.set_theme()



def plot(data: list):
    plt.xticks(THREAD_NOS)
    for n in NS:
        print(n)
        df = pd.DataFrame(data[n], columns =['Threads', 'Time'])
        time_plot = sns.lineplot(data=df, x="Threads", y="Time",label=n, marker='o', markers=True, dashes=False)
    fig = time_plot.get_figure()
    fig.savefig("out.pdf") 

    #sns.lineplot(df)

def main():
    data = {}
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            if int(row['n']) in data:
                data[int(row['n'])].append((int(row['thread_no']), float(row['time'])))
            else:
                data[int(row['n'])] = [(int(row['thread_no']), float(row['time']))]
    print(data)
    plot(data)

if __name__ == "__main__":
    main()
