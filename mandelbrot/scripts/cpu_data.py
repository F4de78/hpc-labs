import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS = [1,2,4,8,16,24]
RUNS = 3

COMP = "icpx"
CFLAGS = ["-fast", "-qopenmp"]

def compile(in_file_path: str, out_file_path: str, resolution: int, thread: int):

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-o",
            "bin/" + out_file_path,
            f"-DRESOLUTION={resolution}",
            f"-DTHREAD_NO={thread}"
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing

def main():
    with open('report/data_cpu.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'n', 'thread_no', 'time', 'speedup', 'efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        time = dict()
        for n, thread_no in it.product(RESOLUTION, THREADS):
            print(time)
            for run in range(1, RUNS + 1):
                curr_time = compile("src/mandelbrot_cpu.cpp", f"mbcpu_{n}_{thread_no}", n, thread_no)
                if thread_no == 1:
                    time[run] = curr_time
                    speedup = 1
                else:
                    speedup = (sum(time.values())/RUNS) / curr_time
                efficiency = speedup / thread_no
                writer.writerow({'run': run, 'n':n, 'thread_no':thread_no, 'time':curr_time, 'speedup':speedup, 'efficiency': efficiency})

               
if __name__ == "__main__":
    main()
