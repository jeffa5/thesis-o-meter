import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

import pandas as pd


def get_data_paths(root: str) -> List[str]:
    return [os.path.join(root, f) for f in os.listdir(root)]


def get_dataframe_single(data_path: str) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    username = data_path.split("/")[-1].split(".")[0]
    df["name"] = username
    return df


def get_dataframe(data_paths: List[str]) -> pd.DataFrame:
    dfs = [get_dataframe_single(path) for path in data_paths]
    df = pd.concat(dfs)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

def plot(df: pd.DataFrame):
    hue_order = sorted(list(df["name"].unique()))
    ax = sns.lineplot(data=df, x="datetime", y="wordcount", hue="name", hue_order=hue_order)
    ax.axhline(60_000, color="gray")
    plt.tight_layout()
    plt.grid()
    plt.savefig("plot.svg")


def main():
    data_paths = get_data_paths("data")
    df = get_dataframe(data_paths)
    plot(df)

main()
