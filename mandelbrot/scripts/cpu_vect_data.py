import subprocess
import itertools as it
import logging
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS = [1, 2, 4, 8, 16, 24]
RUNS = 3

COMP = "icpx"
CFLAGS = ["-fast", "-xHost", "-qopenmp"]
SRC = "src/mandelbrot_cpu_vect_omp.cpp"


def compile(
    resolution: int,
    thread: int,
    fma: bool,
    ftype: str,
    scheduler: str,
):
    out_file = "vect_cpu"

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            SRC,
            "-o",
            f"bin/{out_file}",
            f"-DRESOLUTION={resolution}",
            f"-DTHREAD_NO={thread}",
            "-DFMA" if fma else "",
            f"-DFTYPE={ftype}",
            f"-DOMP_SCHEDULE={scheduler}",
        ]
    )

    res = subprocess.run([f"./bin/{out_file}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing


def main():
    with open("report/data_cpu_vect.csv", "w", newline="") as csvfile:
        fieldnames = [
            "run",
            "res",
            "thread_no",
            "fma",
            "ftype",
            "omp_scheduler",
            "time",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        time = dict()

        for thread_no, res, fma, ftype, omp_scheduler in it.product(
            THREADS,
            RESOLUTION,
            [True, False],  # FMA
            ["float", "double"],  # FTYPE
            ["dynamic", "static"],  # OMP_SCHEDULE
        ):
            print(f"{res=}, {fma=}, {ftype=}, {omp_scheduler=}, {thread_no=}, {time=}")
            for run in range(1, RUNS + 1):
                curr_time = compile(res, thread_no, fma, ftype, omp_scheduler)
                writer.writerow(
                    {
                        "run": run,
                        "res": res,
                        "thread_no": thread_no,
                        "fma": fma,
                        "ftype": ftype,
                        "omp_scheduler": omp_scheduler,
                        "time": curr_time,
                    }
                )


if __name__ == "__main__":
    main()
