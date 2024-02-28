import datetime
import os
import sys
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


def plot(
    df: pd.DataFrame,
    names: List[str],
    name_key: str,
    filename: str,
    finishes: List[datetime.date],
):
    hue_order = names
    plt.figure()
    plt.grid()
    ax = sns.lineplot(
        data=df,
        x="datetime",
        y="wordcount",
        hue=name_key,
        hue_order=hue_order,
        style=name_key,
        style_order=hue_order,
        drawstyle="steps-post",
    )
    ax.set_xlim(
        df["datetime"].min() - datetime.timedelta(days=10),
        df["datetime"].max() + datetime.timedelta(days=60),
    )
    ax.axhline(60, color="gray", label="Word limit")
    for line, finish in zip(ax.get_lines(), finishes):
        ax.axvline(finish, color=line.get_color(), linestyle=line.get_linestyle())
    for finish in finishes:
        ax.annotate(" 3y", (finish, 55))
    ax.set(xlabel="Date & time", ylabel="Word count (K)")
    plt.xticks(rotation=30)
    plt.legend(loc="upper left")
    plt.tight_layout()
    print(f"Saving to {filename}")
    plt.savefig(filename)


def main():
    names = [
        "apj39",
        "cjj39",
        "af691",
        "jb2328",
    ]
    data_paths = get_data_paths("data")
    df = get_dataframe(data_paths)
    df_names = list(df["name"].unique())
    if set(names) != set(df_names):
        print(f"Names not equal to those found: {names} vs {df_names}")
        sys.exit(1)

    finishes = [datetime.date(2024, 4, 1), datetime.date(2024, 2, 1)]

    plot(
        df,
        names,
        "name",
        "plot.svg",
        finishes,
    )

    # make an anonymous version for publishing
    rename_map = {
        "apj39": "apj39",
        "cjj39": "cjj39",
        "af691": "af691",
        "jb2328": "jb2328",
    }
    if set(names) != set(rename_map.keys()):
        print(
            f"Not all names found in the rename_map: {names} vs {list(rename_map.keys())}"
        )
        sys.exit(1)

    anon_names = list(rename_map.values())
    df["anon_name"] = df["name"].map(rename_map)
    plot(df, anon_names, "anon_name", "docs/anon.svg", finishes)


main()
