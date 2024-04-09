from typing import List
import sys
from mandelplot import write_matrix_to_file, matrix_from_file


def matrix_diff(ref: List[List[int]], other: List[List[int]]) -> List[List[int]]:
    return [
        [abs(ref[y][x] - other[y][x]) for x in range(len(ref[y]))]
        for y in range(len(ref))
    ]


def matmul(matrix: List[List[int]], scalar: int, clamp_max=255) -> List[List[int]]:
    return [
        [
            matrix[y][x] * scalar if matrix[y][x] * scalar < clamp_max else clamp_max
            for x in range(len(matrix[y]))
        ]
        for y in range(len(matrix))
    ]


def main(ref: str, other: str):
    ref_m = matrix_from_file(ref)
    other_m = matrix_from_file(other)
    matrix = matrix_diff(ref_m, other_m)
    matrix = matmul(matrix, 10)
    write_matrix_to_file(matrix, f"{other}-diff-img.ppm")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python mandelplot.py <ref> <other>")
        sys.exit(1)

    main(args[0], args[1])
