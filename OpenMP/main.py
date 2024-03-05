import matplotlib.pyplot as plt
import subprocess
import itertools as it
import logging

NS = [1, 10, 100, 1000, 10_000]
THREAD_NOS = [1, 2, 4, 8, 12, 24]
COMP = "clang"
# CFLAGS = ["-xHost", "-qopenmp", "-std=c99", "-fast"]

# COMP = "icc"
CFLAGS = ["-fopenmp", "-std=c99", "-fast"]


def compile(in_file_path: str, out_file_path: str, n: int, thread_no: int):
    logging.info(
        f"Compiling {in_file_path} to {out_file_path} with N={n} and THREAD_NO={thread_no}"
    )
    res = subprocess.run(
        [
            COMP,
            *CFLAGS,
            in_file_path,
            "-o",
            out_file_path,
            f"-DN={n}",
            f"-DTHREAD_NO={thread_no}",
        ]
    )


def main():
    for n, thread_no in it.product(NS, THREAD_NOS):
        compile("main.c", f"main_{n}_{thread_no}", n, thread_no)


if __name__ == "__main__":
    main()
