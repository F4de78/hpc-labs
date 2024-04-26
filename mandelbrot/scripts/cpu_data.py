import subprocess
import itertools as it
import csv

RESOLUTION = [500, 1000, 1500, 2000]
THREADS = [1, 2, 4, 8, 16, 24]
RUNS = 3

COMP = "icpx"
CFLAGS = ["-fast", "-xHost", "-qopenmp"]
SRC = "src/mandelbrot_cpu_omp.cpp"


def compile(resolution: int, thread: int, schedule: str):
    out_file_name = "cpu"

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            SRC,
            "-o",
            f"bin/{out_file_name}",
            f"-DRESOLUTION={resolution}",
            f"-DTHREAD_NO={thread}",
            f"-DOMP_SCHEDULE={schedule}",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_name}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing


def main():
    with open("report/data_cpu.csv", "w", newline="") as csvfile:
        fieldnames = [
            "run",
            "res",
            "thread_no",
            "omp_schedule",
            "time",
            "speedup",
            "efficiency",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for thread_no, res, omp_scheduler in it.product(
            THREADS,
            RESOLUTION,
            ["dynamic", "static"],  # OMP_SCHEDULE
        ):
            print(f"{res=}, {omp_scheduler=}, {thread_no=}")
            for run in range(1, RUNS + 1):
                curr_time = compile(res, thread_no, omp_schedule)
                writer.writerow(
                    {
                        "run": run,
                        "res": res,
                        "thread_no": thread_no,
                        "omp_schedule": omp_schedule,
                        "time": curr_time,
                    }
                )


if __name__ == "__main__":
    main()
