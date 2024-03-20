import pandas as pd
from matplotlib import pyplot as plt


def show_histogram(input_df: pd.DataFrame, columns_to_show: list):
    input_df[columns_to_show].hist(figsize=(10, 10))
    plt.show()

def make_pie_chart_percent(values: list, labels: list, colors: list, title: str):
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def make_bar_plot_percent(values: list, labels: list, colors: list, title: str):
    bars = plt.bar(labels, height=values, color=colors, width=0.2)
    plt.title(title)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .005, str(round(yval, 1)) + "%")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def make_bar_plot_counts(values: list, labels: list, colors: list, title: str):
    bars = plt.bar(labels, height=values, color=colors, width=0.2)
    plt.title(title)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .005, str(round(yval, 1)))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

