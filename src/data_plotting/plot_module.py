import numpy as np
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

def make_bar_plot_percent(values: list, labels: list, colors: list, title: str, x_name: str, y_name: str):
    bars = plt.bar(labels, height=values, color=colors, width=0.2)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .005, str(round(yval, 1)) + "%")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def make_bar_plot_counts(values: list, labels: list, colors: list, title: str, x_name: str, y_name: str):
    bars = plt.bar(labels, height=values, color=colors, width=0.2)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .005, str(round(yval, 1)))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def make_scatter_plot(values_x: list, values_y: list, sizes: list, xticks: list, title: str, x_name: str, y_name: str):
    plt.scatter(values_x, values_y, s=sizes, alpha=0.5)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.xticks(xticks)
    plt.title(title)
    plt.tight_layout()
    plt.show()

def make_heatmap(data_array: np.array, x_list, y_list, title: str, x_name: str, y_name: str):
    plt.imshow(data_array)
    # plt.xticks(np.arange(len(unique_age_values)), labels=unique_age_values)
    plt.xticks(np.arange(len(x_list)), labels=x_list)
    # plt.yticks(np.arange(len(no_show_values)), labels=no_show_values)
    plt.yticks(np.arange(len(y_list)), labels=y_list)
    for y in range(len(y_list)):
        for x in range(len(x_list)):
            val = data_array[y, x]
            plt.text(x, y, val, ha="center", va="center", color="black")
            # text = ax.text(j, i, harvest[x, y],
            #                ha="center", va="center", color="w")
    plt.colorbar(label="Frequency", shrink=0.7, aspect=10 * 0.7)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    plt.tight_layout()
    plt.show()
