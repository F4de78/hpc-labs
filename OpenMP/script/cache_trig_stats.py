import pandas as pd


def main():
    data = pd.read_csv("report/cache_trig_data.csv")
    data["average_time"] = data.groupby(["n", "cache_trig"])["time"].transform("mean")
    data = data[["n", "cache_trig", "average_time"]].drop_duplicates()
    data["optim"] = data.apply(
        lambda row: data[
            (data["n"] == row["n"]) & (data["cache_trig"] != row["cache_trig"])
        ]["average_time"].iloc[0]
        / row["average_time"],
        axis=1,
    )

    with pd.option_context("display.max_rows", None):
        print("FLOAT only data:\n", data)


if __name__ == "__main__":
    main()
