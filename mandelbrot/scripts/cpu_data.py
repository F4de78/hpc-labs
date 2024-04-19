import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS = [1,2,4,8,16,24]
RUNS = 3

COMP = "icpx"
CFLAGS = ["-fast", "-qopenmp"]
SRC = "src/mandelbrot_cpu_vect_omp.cpp"

def compile(in_file_path: str, out_file_path: str, resolution: int, thread: int, fma: bool, ftype: str):

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-xHost",
            "-o",
            "bin/" + out_file_path,
            f"-DRESOLUTION={resolution}",
            f"-DTHREAD_NO={thread}",
            "-DFMA" if fma else "",
            f"-DFTYPE={ftype}"
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing

def main():
    with open('report/data_cpu.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'n', 'thread_no', 'fma', 'ftype', 'time', 'speedup', 'efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        time = []
        for n, thread_no, fma, ftype in it.product(RESOLUTION, THREADS, [True, False], ["float", "double"]):
            print(time)
            for run in range(1, RUNS + 1):
                curr_time = compile(SRC, f"mbcpu", n, thread_no, fma, ftype)
                if thread_no == 1:
                    time[run - 1] = curr_time
                    speedup = 1
                else:
                    speedup = (sum(time)/RUNS) / curr_time
                efficiency = speedup / thread_no
                writer.writerow({'run': run, 'n':n, 'thread_no':thread_no, 'fma':fma,'ftype':ftype,'time':curr_time, 'speedup':speedup, 'efficiency': efficiency})

               
if __name__ == "__main__":
    main()
