from typing import List
import sys


def write_matrix_to_file(matrix: List[List[int]], file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"P3\n{len(matrix[0])} {len(matrix)}\n255\n")
        for row in matrix:
            for idx, g in enumerate(row):
                if idx != 0:
                    file.write(" ")
                file.write(f"{g} {g} {g}")
            file.write("\n")


def matrix_from_file(filename: str) -> List[List[int]]:
    with open(filename, "r", encoding="utf-8") as file:
        file_content = file.readlines()
        return [
            [int(digit.strip()) for digit in line.split(",")] for line in file_content
        ]


def main(file_path: str):
    matrix = matrix_from_file(file_path)
    write_matrix_to_file(matrix, f"{file_path}-img.ppm")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python mandelplot.py <output_file>")
        sys.exit(1)

    main(args[0])
