import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from typing import Any, Tuple
import os

matplotlib.use('agg')
output_folder = 'plots'
EXT = 'svg'

def create_folder_if_not_exists(lang: str) -> None:
    os.makedirs(os.path.dirname('{}/{}'.format(output_folder, lang)), exist_ok=True)
    output_folder = '/'.join([output_folder, lang])

def user_data_extraction(user: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieves warnings date and user's activity count per month 

    Args:
        user (pd.DataFrame): user 

    Returns:
        pd.DataFrame: user data with info about the warnings
    """
    user_data = list()
    data = user['edit_history']
    warning_data = user['warnings_history']
    for year in data:
        year = str(year)
        for month in data[year]:
            if not year in warning_data or not month in warning_data[year]:
                warnings_value = {
                    'serious_transcluded': 0,
                    'warning_transcluded': 0, 
                    'not_serious_transcluded': 0
                }
            else:   
                warnings_value = {
                    'serious_transcluded': warning_data[year][month]['serious_transcluded'],
                    'warning_transcluded': warning_data[year][month]['warning_transcluded'], 
                    'not_serious_transcluded': warning_data[year][month]['not_serious_transcluded']
                }
            user_data.append({
                'date': datetime(int(year), int(month), 1), 
                'activities count': data[year][month], 
                'serious warnings': warnings_value['serious_transcluded'],
                'warnings': warnings_value['warning_transcluded'],
                'not serious warnings': warnings_value['not_serious_transcluded'],
                'serious_line': datetime(int(year), int(month), 1) if warnings_value['serious_transcluded'] else None,
                'warning_line': datetime(int(year), int(month), 1) if warnings_value['warning_transcluded'] else None,
                'not_serious_line': datetime(int(year), int(month), 1) if warnings_value['not_serious_transcluded'] else None
            })
    user_data = pd.DataFrame(user_data).reset_index(drop=True).sort_values(by='date')
    return user_data

def get_file_path(lang: str) -> str:
    """
    Gets the file given the Wikipedia language
    Args:
        lang (str): Wikipedia language
    Returns:
        str: file path of the compressed json file
    """
    file_path = 'output/{}wiki_users.features.json.gz'.format(lang)
    return file_path

def plot_pie_chart(title: str, data: list[float], labels: list[str]) -> None:
    """
    Plots a basic pie chart in a figure
    Args:
        title (str): title
        data (list[float]): data
        labels (list[str]): labels
    """
    plt.figure(figsize=(16, 8))
    plt.title(title)
    plt.pie(data, labels, autopct='%1.1f%%')
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))

def plot_bar_chart(title: str, y: list[int], x: list[Any]) -> None:
    """
    Plots a basic bar chart in a figure
    Args:
        title (str): title
        y (list[int]): y
        x (list[Any]): x
    """
    plt.figure(figsize=(20, 8))
    plt.title(title)
    plt.bar(y, x)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))

def plot_line_chart(x: pd.Series, y: list[Tuple[pd.Series, str]], title: str, ylabel: str, xlabel: str) -> None:
    """
    Plots a basic line chart in a figure

    Args:
        x (pd.Series): x
        y (list[Tuple[pd.Series, str]]): list of lines and associated labels
        title (str): title
        ylabel (str): y axis label
        xlabel (str): x axis label
    """
    plt.figure(figsize=(16,8))
    for line, label in y:
        plt.plot(x, line, label = label)
    plt.legend()
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))

def plot_line_chart_with_vertical_lines(x: pd.Series, y: list[Tuple[pd.Series, str]], title: str, ylabel: str, xlabel: str, vlinesx: list[Tuple[pd.Series, str]], ymin: int, ymax: int) -> None:
    """
    Plots a basic line chart in a figure

    Args:
        x (pd.Series): x
        y (list[Tuple[pd.Series, str]]): list of lines and associated labels
        title (str): title
        ylabel (str): y axis label
        xlabel (str): x axis label
        vlinesx (list[Tuple[pd.Series, str]]): set of vertical lines
        ymin (int): minimum y value for the vertical line
        ymax (int): maximum y value for the vertical line
    """
    plt.figure(figsize=(16,8))
    for line, label in y:
        plt.plot(x, line, label = label)
    for x, color in vlinesx:
        plt.vlines(x = x, ymin = ymin, ymax = ymax, color = color)
    plt.legend()
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))