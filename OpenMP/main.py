import subprocess
import itertools as it
import logging

NS = [1, 10, 100, 1000, 10_000]
THREAD_NOS = [1, 2, 4, 8, 12, 24]
# COMP = "clang"
# CFLAGS = ["-xHost", "-qopenmp", "-std=c99", "-fast"]

COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-fast"]


def compile(in_file_path: str, out_file_path: str, n: int, thread_no: int):
    logging.info(
        f"Compiling {in_file_path} to {out_file_path} with N={n} and THREAD_NO={thread_no}"
    )

    subprocess.run(
        [
            COMP,
            *CFLAGS,
            "-diag-disable=10441",
            in_file_path,
            "-o",
            out_file_path,
            f"-DN={n}",
            f"-DTHREAD_NO={thread_no}",
        ]
    )

    res = subprocess.run([f"./{out_file_path}"], stdout=subprocess.PIPE)
    timing = res.stdout.decode("utf-8").split("\n")[1]
    timing = timing[len("DFTW computation in ") : -len(" seconds")]
    print(f"\n\nTIMING: {float(timing)}\n\n")
    return float(timing)


def main():
    for n, thread_no in it.product(NS, THREAD_NOS):
        compile("omp_homework_vect_final.c", f"main_{n}_{thread_no}", n, thread_no)


if __name__ == "__main__":
    main()
