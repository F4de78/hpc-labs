import subprocess
import itertools as it
import csv

RESOLUTION = [500, 1000, 1500, 2000]
RUNS = 10

COMP = "icpx"
CFLAGS = ["-fast", "-xHost"]
SRC = "src/mandelbrot_cpu_omp.cpp"


def compile(resolution: int, optim: bool):
    out_file_name = "cpu"

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            SRC,
            "-o",
            f"bin/{out_file_name}",
            f"-DRESOLUTION={resolution}",
            "-DNORM_OPTIM" if optim else "",
        ]
    )

    res = subprocess.run([f"./bin/{out_file_name}"], stdout=subprocess.PIPE)
    timing = float(res.stdout.decode("utf-8").split("Time elapsed: ")[1].split(" ")[0])
    print(f"CPU: {timing}")
    return timing


def main():
    with open("report/data_cpu_norm_optim.csv", "w", newline="") as csvfile:
        fieldnames = [
            "run",
            "res",
            "optim",
            "time",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for res, optim in it.product(
            RESOLUTION,
            [True, False]
        ):
            print(f"{res=}, {optim=}")
            for run in range(1, RUNS + 1):
                curr_time = compile(res, optim)
                writer.writerow(
                    {
                        "run": run,
                        "res": res,
                        "optim": optim,
                        "time": curr_time,
                    }
                )


if __name__ == "__main__":
    main()
