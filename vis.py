import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def vis(title: str, episodes: pd.DataFrame):
    print("Visualizing")
    plt.figure(figsize=(10.0, 10.0))
    plt.title(title)
    plt.grid(True, axis='y', linestyle='-')
    plt.ylim(-0.5, 10.5)
    cleaned = episodes.dropna(axis=0, subset=["seasonNumber", "episodeNumber"])
    sorted = cleaned.sort_values(["seasonNumber", "episodeNumber"])
    sorted["counter"] = range(1, len(sorted) + 1)
    palette = sns.color_palette()
    for season in set(sorted["seasonNumber"]):
        color = palette[(season - 1) % len(palette)]
        epidoes_from_this_season = sorted[sorted["seasonNumber"] == season]
        sns.regplot(x="counter", y="averageRating", data=epidoes_from_this_season)
        label_points(epidoes_from_this_season, plt.gca(), color, season)

    plt.xticks([], [])
    plt.xlabel("")

    for season in set(sorted["seasonNumber"]):
        min_counter = sorted[sorted["seasonNumber"] == season]["counter"].min()
        label_season(season, min_counter, plt.gca())

    print(episodes.groupby("seasonNumber")["averageRating"].mean())
    print(episodes.sample(5))

def show():
    print("Showing")
    plt.show()


def label_points(episodes, ax, color, season):
    labelled_episodes = []

    min_rating = episodes["averageRating"].idxmax()
    if not pd.isnull(min_rating):
        labelled_episodes.append(episodes.loc[min_rating])
    max_rating = episodes["averageRating"].idxmin()
    if not pd.isnull(max_rating):
        labelled_episodes.append(episodes.loc[max_rating])

    for row in labelled_episodes:
        ax.text(row["counter"] + 0.02,
                row["averageRating"],
                f"{row['seasonNumber']}x{row['episodeNumber']} {row['primaryTitle']}",
                fontsize=6)

    min_counter = episodes["counter"].min() - 0.5
    max_counter = episodes["counter"].max() + 0.5
    plt.axvspan(min_counter, max_counter, facecolor=color, alpha=0.25)


def label_season(season, x, ax):
    y = ax.get_ylim()[0]
    ax.text(x, y, str(season), color='black', alpha=0.5, fontsize=18)
