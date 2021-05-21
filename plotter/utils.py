import pandas as pd
import os
import math
import calendar
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse
from typing import Any, Tuple

matplotlib.use('agg')
output_folder = 'plots'
EXT = 'png'

def monthdelta(date, delta):
    """
    Subtract a month amont from a date

    Args:
        date ([datetime]): date
        delta ([int]): month count

    Returns:
        return date [datetime]: date after the subtraction
    """
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)

def create_folder_if_not_exists(lang: str) -> None:
    """
    It creates a folder if it do not exists

    Args:
        lang (str): Wikipedia community language
    """
    global output_folder
    if not os.path.exists('{}/{}'.format(output_folder, lang)):
        os.mkdir('{}/{}'.format(output_folder, lang))
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
        if int(year) > user['last_edit_year']:
            break
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
    plt.close()

def plot_bar_chart(title: str, y: list[int], x: list[Any], ylabel: str, xlabel: str) -> None:
    """
    Plots a basic bar chart in a figure
    Args:
        title (str): title
        y (list[int]): y
        x (list[Any]): x
    """
    plt.figure(figsize=(20, 8))
    plt.title(title)
    plt.bar(x, y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

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
    plt.close()

def plot_line_chart_with_vertical_lines(x: pd.Series, y: list[Tuple[pd.Series, str]], title: str, ylabel: str, xlabel: str, vlinesx: list[Tuple[pd.Series, str, str]], ymin: int, ymax: int) -> None:
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
    lines = list()
    labels = list()
    plt.figure(figsize=(16,8))
    for line, label in y:
        line, = plt.plot(x, line, label = label)
        lines.append(line)
        labels.append(label)
    for x, color, label in vlinesx:
        if not x.empty:
            line = plt.vlines(x = x, ymin = ymin, ymax = ymax, color = color)
            lines.append(line)
            labels.append(label)
    plt.legend(lines, labels)
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

def month_year_iter(start_month, start_year, end_month, end_year):
    """
    Year month iterator

    Args:
        start_month ([int]): starting month
        start_year ([int]): starting year
        end_month ([int]): ending month
        end_year ([int]): ending year

    Yields:
        Tuple[int, int]: year and month
    """
    ym_start= 12 * start_year + start_month - 1
    ym_end= 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod( ym, 12 )
        yield y, m + 1

def z_score_user_activity_amount_month_interval(x: pd.Series, y: pd.Series, vlinesx: Tuple[pd.Series, str], month_interval: int) -> Tuple[bool, pd.DataFrame]:
    """
    Computes the z-score on the user activity, before and after twelve months, the user has received the last serious warnings date, 
    stored in the vlinesx tuple

    Args:
        x (pd.Series): x (date)
        y (pd.Series): y (edit count)
        vlinesx (Tuple[pd.Series, str]): last warning, and line color

    Returns:
        Tuple[bool, pd.DataFrame]: (the zscore can be computed, pandas dataframe storing the z-score of the user's activity)
    """
    # compute the z-score in the 24 month interval
    # https://en.wikipedia.org/wiki/Standard_score
    
    if not vlinesx[0]:
        return False, None
    
    start_date = monthdelta(parse(vlinesx[0]), -month_interval)
    end_date = monthdelta(parse(vlinesx[0]), +month_interval)
    mean = 0
    mean_values = list()
    dates = list()
    month_counter = 0

    # compute the mean over the months
    for year, month in month_year_iter(start_date.month, start_date.year, end_date.month + 1, end_date.year):
        try:
            value = y['activities count'].loc[y['date'] == datetime(year, month, 1)].item()
        except ValueError:
            value = 0
        mean += value
        mean_values.append(value)
        dates.append(datetime(year, month, 1))
        month_counter += 1
    
    mean /= month_counter

    # compute the standard deviation
    std = 0
    for month_value in mean_values:
        std += ( month_value - mean)**2
    
    std /= month_counter
    std = math.sqrt(std)

    if not std:
        std = 1

    # applicare el - mean / std a tutti i valori
    mean_values = pd.Series(mean_values).apply(lambda x: (x - mean) / std)
    dates = pd.Series(dates)
    return True, pd.DataFrame({'date': dates, 'activities z-score': mean_values})