import subprocess
import itertools as it
import csv

NS = [2_000, 4_000, 8_000, 16_000, 32_000, 48_000]
RUNS = 10

COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-O3", "-march=alderlake"]

def compile(n: int, cache_trig: bool):
    in_file_path = "src/omp_homework.c"
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
            "-DCACHE_TRIG" if cache_trig else "",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_path}"], stdout=subprocess.PIPE)
    timing = res.stdout.decode("utf-8").split("\n")[1]
    timing = timing[len("DFTW computation in ") : -len(" seconds")]
    print(f"TIMING: {float(timing)}")
    return float(timing)

def main():
    with open('report/cache_trig_data.csv', 'w',  newline='') as csvfile:
        fieldnames = ['run', 'n', 'cache_trig', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n, cache_trig in it.product(NS, [False, True]):
            print(f"{n=}, {cache_trig=}")
            for run in range(1, RUNS + 1):
                curr_time = compile(n, cache_trig)
                writer.writerow({
                    'run': run, 
                    'n':n, 
                    'cache_trig': cache_trig, 
                    'time':curr_time
                })
               
if __name__ == "__main__":
    main()
