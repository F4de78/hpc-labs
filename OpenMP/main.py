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

def compile(in_file_path: str, out_file_path: str, n: int, thread_no: int):
    logging.info(
        f"Compiling {in_file_path} to {out_file_path} with N={n} and THREAD_NO={thread_no}"
    )

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            "-diag-disable=10441",
            in_file_path,
            "-o",
            "bin/" + out_file_path,
            f"-DN={n}",
            f"-DTHREAD_NO={thread_no}",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = res.stdout.decode("utf-8").split("\n")[1]
    timing = timing[len("DFTW computation in ") : -len(" seconds")]
    print(f"\n\nTIMING: {float(timing)}\n\n")
    return float(timing)

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
    with open('data.csv', 'w',  newline='') as csvfile:
        fieldnames = ['n', 'thread_no', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n, thread_no in it.product(NS, THREAD_NOS):
            writer.writerow({'n':n, 'thread_no':thread_no, 'time':compile("src/omp_homework_vect_final.c", f"main_{n}_{thread_no}", n, thread_no)})
               

if __name__ == "__main__":
    main()
