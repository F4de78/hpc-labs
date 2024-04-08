import argparse


def main(afn: str, bfn: str):
    with open(afn, encoding="utf-8") as af, open(bfn, encoding="utf-8") as bf:
        a = af.readlines()
        b = bf.readlines()
        for line_idx, (aline, bline) in enumerate(zip(a, b)):
            if aline != bline:
                for col, (ac, bc) in enumerate(zip(aline.split(","), bline.split(","))):
                    if ac != bc:
                        print(f"Line={line_idx + 1}, Col={col + 1}. Ref={ac}, GPU={bc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", type=str, default="../report/out_ref")
    parser.add_argument("--gpu", type=str, default="../report/out_gpu")
    args = parser.parse_args()
    main(args.ref, args.gpu)
