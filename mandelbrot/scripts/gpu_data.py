import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS_X = [1,2,4,8,16]
THREADS_Y = [1,2,4,8,16]
RUNS = 3

COMP = "nvcc"
CFLAGS = []

def compile(in_file_path: str, out_file_path: str, resoultion: int, thread_x: int, thread_y: int):

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-o",
            "bin/" + out_file_path,
            f"-DTHREADS_X={thread_x}",
            f"-DTHREADS_Y={thread_y}",
            f"-DRESOLUTION={resoultion}"
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)

    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"GPU: {timing}")
    return timing

def main():
    with open('report/data_gpu.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'resolution', 'thread_x', 'thread_y', 'time_gpu']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for resolution, thread_x, thread_y in it.product(RESOLUTION, THREADS_X, THREADS_Y):
            print(resolution, thread_x, thread_y)
            for run in range(1, RUNS + 1):
                curr_time_gpu = compile("src/mandelbrot_gpu.cu", f"mbgpu_{resolution}_{thread_x}_{thread_y}", resolution, thread_x, thread_y)
                writer.writerow({'run': run, 'resolution':resolution, 'thread_x':thread_x, 'thread_y':thread_y, 'time_gpu': curr_time_gpu})
               
if __name__ == "__main__":
    main()
