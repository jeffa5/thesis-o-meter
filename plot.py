import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
    df["wordcount"] /= 1_000
    return df


def plot(df: pd.DataFrame, names: List[str], name_key: str, filename: str):
    hue_order = names
    plt.figure()
    ax = sns.lineplot(
        data=df, x="datetime", y="wordcount", hue=name_key, hue_order=hue_order
    )
    ax.axhline(60, color="gray", label="Word limit")
    ax.set(xlabel="Date & time", ylabel="Word count (K)")
    plt.xticks(rotation=30)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig(filename)


def main():
    data_paths = get_data_paths("data")
    df = get_dataframe(data_paths)
    names = sorted(list(df["name"].unique()))
    plot(df, names, "name", "plot.svg")

    # make an anonymous version for publishing
    anon_names = range(1, len(names)+1)
    rename_map = dict(zip(names, anon_names))
    df["anon_name"] = df["name"].map(rename_map)
    plot(df, anon_names, "anon_name", "docs/anon.svg")


main()
