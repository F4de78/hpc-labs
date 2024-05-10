import subprocess
import itertools as it
import csv

NS = [2_000, 4_000, 8_000, 16_000, 32_000, 48_000]
THREAD_NOS = [1, 2, 4, 8, 16, 24]
RUNS = 10

COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-O3", "-march=alderlake"]

def compile(n: int, thread_no: int, use_double: bool):
    in_file_path = "src/omp_homework_vect.c"
    out_file_path = "dft"

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
            "-DDOUBLE" if use_double else "",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = res.stdout.decode("utf-8").split("\n")[1]
    timing = timing[len("DFTW computation in ") : -len(" seconds")]
    print(f"TIMING: {float(timing)}")
    return float(timing)

def main():
    with open('report/data.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'n', 'thread_no', 'ftype', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n, thread_no, use_double in it.product(NS, THREAD_NOS, [False, True]):
            print(f"{n=}, {thread_no=}, {use_double=}")
            for run in range(1, RUNS + 1):
                curr_time = compile(n, thread_no, use_double)
                writer.writerow({
                    'run': run, 
                    'n':n, 
                    'thread_no':thread_no, 
                    'ftype': "double" if use_double else "float", 
                    'time':curr_time
                })
               
if __name__ == "__main__":
    main()
