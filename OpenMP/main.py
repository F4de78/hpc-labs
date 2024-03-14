import subprocess
import itertools as it
import logging
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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
    # ret = {'run_10000_1': 1.045192, 'run_10000_2': 0.525527, 'run_10000_4': 0.263874, 'run_10000_8': 0.134413, 'run_10000_12': 0.111495, 'run_10000_24': 0.089743, 'run_20000_1': 4.171668, 'run_20000_2': 2.095489, 'run_20000_4': 1.04992, 'run_20000_8': 0.535378, 'run_20000_12': 0.426402, 'run_20000_24': 0.339003, 'run_30000_1': 9.394479, 'run_30000_2': 4.699974, 'run_30000_4': 2.354223, 'run_30000_8': 1.179246, 'run_30000_12': 0.950071, 'run_30000_24': 0.758242, 'run_40000_1': 16.67007, 'run_40000_2': 8.336538, 'run_40000_4': 4.170657, 'run_40000_8': 2.091124, 'run_40000_12': 1.688673, 'run_40000_24': 1.381817}
    #ret = {10000: [(1, 1.048207), (2, 0.525167), (4, 0.268448), (8, 0.144054), (16, 0.099496), (24, 0.088811)], 20000: [(1, 4.172614), (2, 2.088615), (4, 1.051734), (8, 0.528246), (16, 0.36481), (24, 0.331546)], 30000: [(1, 9.390293), (2, 4.691887), (4, 2.36499), (8, 1.179665), (16, 0.81942), (24, 0.734957)], 40000: [(1, 16.672223), (2, 8.356542), (4, 4.191016), (8, 2.167108), (16, 1.4345), (24, 1.316893)]}
    ret = {}
    for n, thread_no in it.product(NS, THREAD_NOS):
        if n in ret:
            ret[n].append((thread_no, compile("src/omp_homework_vect_final.c", f"main_{n}_{thread_no}", n, thread_no)))
        else:
            print(n)
            ret[n] = [(thread_no, compile("src/omp_homework_vect_final.c", f"main_{n}_{thread_no}", n, thread_no))]
    plot(ret)

if __name__ == "__main__":
    main()
