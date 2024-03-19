import subprocess
import itertools as it
import logging
import csv

NS = [2_000, 4_000, 8_000, 16_000, 32_000, 48_000]
THREAD_NOS = [1, 2, 4, 8, 16, 24]
RUNS = 10

COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-O3", "-xHost"]

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
    print(f"N={n} THREAD_NO={thread_no} TIMING: {float(timing)}")
    return float(timing)

def main():
    with open('data.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'n', 'thread_no', 'time', 'speedup', 'efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        time = dict()
        for n, thread_no in it.product(NS, THREAD_NOS):
            print(time)
            for run in range(1, RUNS + 1):
                curr_time = compile("src/omp_homework_vect_final.c", f"main_{n}_{thread_no}", n, thread_no)
                if thread_no == 1:
                    time[run] = curr_time
                    speedup = 1
                else:
                    speedup = (sum(time.values())/RUNS) / curr_time
                efficiency = speedup / thread_no
                writer.writerow({'run': run, 'n':n, 'thread_no':thread_no, 'time':curr_time, 'speedup':speedup, 'efficiency': efficiency})
               
if __name__ == "__main__":
    main()
