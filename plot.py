import datetime
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

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
    given_names: List[str],
    name_key: str,
    filename: str,
    finishes: Dict[str, datetime.date],
    submissions: List[Tuple[datetime.date, int, str]],
):
    names = []
    # don't include names for those that have no line yet
    for name in given_names:
        data = df[df["name"] == name]
        if len(data) > 1:
            names.append(name)

    df = df[df["name"].isin(names)]

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
        df["datetime"].min() - datetime.timedelta(days=7),
        df["datetime"].max() + datetime.timedelta(days=7),
    )
    ax.axhline(60, color="gray", label="Word limit")
    for line, name in zip(ax.get_lines(), names):
        if name in finishes:
            finish = finishes[name]
            ax.axvline(finish, color="gray", linestyle=line.get_linestyle())
            ax.annotate(f" 3y {name}", (finish, 55))

    ax.set(xlabel="Date & time", ylabel="Word count (K)")

    subs_by_color = defaultdict(list)
    for sub in submissions:
        subs_by_color[sub[2]].append([sub[0], sub[1]])

    for color, subs in subs_by_color.items():
        plt.scatter(
            [s[0] for s in subs],
            [s[1] for s in subs],
            marker="*",
            color=color,
            zorder=5,
            s=100,
            edgecolors="black",
            linewidths=0.5,
        )

    plt.xticks(rotation=30)
    plt.legend(loc="upper left")
    plt.tight_layout()
    print(f"Saving to {filename}")
    plt.savefig(filename)


def main():
    names = [
        "apj39",
        "cjj39",
        "jb2328",
        "aati2",
        "af691",
    ]
    data_paths = get_data_paths("data")
    df = get_dataframe(data_paths)
    df_names = list(df["name"].unique())
    if set(names) != set(df_names):
        print(f"Names not equal to those found: {names} vs {df_names}")
        sys.exit(1)

    finishes = {
        "apj39": datetime.date(2024, 4, 1),
        "cjj39": datetime.date(2024, 2, 1),
        "aati2": datetime.date(2024, 10, 1),
        "jb2328": datetime.date(2025, 10, 1),
    }

    def get_submission_row(name, year, month, day):
        d = df
        d = d[d["name"] == name]
        d = d[
            d["datetime"]
            < pd.Timestamp(year=year, month=month, day=day + 1, tz="UTC", unit="ns")
        ]  # plus one day
        return d.tail(1)

    submission_dates = {"apj39": (2024, 8, 7)}
    submission_rows = [
        get_submission_row(n, y, m, d) for n, (y, m, d) in submission_dates.items()
    ]
    submissions = [(s["datetime"], s["wordcount"], "silver") for s in submission_rows]

    correction_dates = {}
    correction_rows = [
        get_submission_row(n, y, m, d) for n, (y, m, d) in correction_dates.items()
    ]
    submissions += [(s["datetime"], s["wordcount"], "gold") for s in correction_rows]

    plot(
        df,
        names,
        "name",
        "plot.svg",
        finishes,
        submissions,
    )

    # make an anonymous version for publishing
    rename_map = {
        "apj39": "apj39",
        "cjj39": "cjj39",
        "aati2": "anon",
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
    plot(df, anon_names, "anon_name", "docs/anon.svg", finishes, submissions)


main()
