import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS_X = [1,2,4,8,16]
THREADS_Y = [1,2,4,8,16]
RUNS = 1

COMP = "nvc++"
CFLAGS = []

def compile(in_file_path: str, out_file_path: str, resoultion: int, thread_x: int, thread_y: int, ftype: str):

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-o",
            "bin/" + out_file_path,
            f"-DTHREADS_X={thread_x}",
            f"-DTHREADS_Y={thread_y}",
            f"-DRESOLUTION={resoultion}",
            "-DDOUBLE" if ftype == "double" else "",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)

    output = res.stdout.decode("utf-8")
    try:
        timing = float(output.split("Time elapsed: ")[1].split(" ")[0])
    except Exception:
        print("Got exception. Output was: ", output)
        raise
    
    print(f"GPU: {timing}")
    return timing

def main():
    with open('report/data_gpu.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'resolution', 'thread_x', 'thread_y', 'time_gpu', 'ftype']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for resolution, thread_x, thread_y, ftype in it.product(RESOLUTION, THREADS_X, THREADS_Y, ["float", "double"]):
            print(resolution, thread_x, thread_y, ftype)
            for run in range(1, RUNS + 1):
                curr_time_gpu = compile("src/mandelbrot_gpu.cu", "mbgpu", resolution, thread_x, thread_y, ftype)
                writer.writerow({'run': run, 'resolution':resolution, 'thread_x':thread_x, 'thread_y':thread_y, 'time_gpu': curr_time_gpu, "ftype": ftype})
               
if __name__ == "__main__":
    main()
