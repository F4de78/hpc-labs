import pandas as pd


def get_data():
    data = pd.read_csv("report/data_cpu_norm_optim.csv")

    data["average_time"] = data.groupby(["res", "optim"])["time"].transform("mean")
    data["time"] = data["average_time"]
    data = data[["res", "optim", "time"]].drop_duplicates()

    return data


def main():
    data = get_data()
    print(data)


if __name__ == "__main__":
    main()
