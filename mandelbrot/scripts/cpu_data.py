import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS = [1,2,4,8,16,24]
RUNS = 3

COMP = "icpx"
CFLAGS = ["-fast", "-xHost", "-qopenmp"]
SRC = "src/mandelbrot_cpu_omp.cpp"

def compile(in_file_path: str, out_file_path: str, resolution: int, thread: int, scheduler: str):

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-o",
            "bin/" + out_file_path,
            f"-DRESOLUTION={resolution}",
            f"-DTHREAD_NO={thread}",
            f"-DOMP_SCHEDULE={scheduler}"
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing

def main():
    with open('report/data_cpu.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'res', 'thread_no', 'omp_scheduler', 'time', 'speedup', 'efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        time = dict()

        for run in range(1, RUNS + 1):
            for res in RESOLUTION:
                if res in time:
                    time[res].append(compile(SRC, f"mbcpu", res, 1, 'static'))
                else:
                    time[res] = [compile(SRC, f"mbcpu", res, 1, 'static')]


        for thread_no, res, omp_scheduler in it.product(THREADS, RESOLUTION, ['dynamic','static']):
            print(res, omp_scheduler, thread_no, time)
            for run in range(1, RUNS + 1):
                curr_time = compile(SRC, f"mbcpu", res, thread_no, omp_scheduler)
                speedup = (sum(time[res])/RUNS) / curr_time
                efficiency = speedup / thread_no
                writer.writerow({'run': run, \
                                 'res':res, \
                                 'thread_no':thread_no, \
                                 'omp_scheduler': omp_scheduler, \
                                 'time':curr_time, \
                                 'speedup':speedup, \
                                 'efficiency': efficiency
                                })

               
if __name__ == "__main__":
    main()
