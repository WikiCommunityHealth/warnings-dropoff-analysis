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
    # devo computare gli i blocchi sui warnings ricevuti, putroppo. Vediamo di farlo domani. 
    # Poi, rivedere la parte del decremento di attività e anche lì dividerlo per tipo di warnings
    # infinite warnings date
    infinite_warnings_dates = set()
    last_year = max([int(user['last_edit_year']), parse(user['last_serious_warning_date']).year])
    temporal_blocks_dates = set()
    
    for el in user['transcluded_user_warnings']:
        if el['name'] in INFINITE_BLOCKS:
            infinite_warnings_dates.add((parse(el['date']).year, parse(el['date']).month))
        if el['name'] in TEMPORAL_BLOCKS:
            temporal_blocks_dates.add((parse(el['date']).year, parse(el['date']).month))

    for year in data:
        if int(year) > last_year + 1:
            break
        year = str(year)
        for month in data[year]:
            if not year in warning_data or not month in warning_data[year]:
                warnings_value = {
                    'serious_transcluded': 0,
                    'warning_transcluded': 0, 
                    'not_serious_transcluded': 0,
                    'serious_substituted': 0,
                    'warning_substituted': 0,
                    'not_serious_substituted': 0,
                    'temporal_block': 0,
                    'infinite_block': 0
                }
            else:   
                warnings_value = {
                    'serious_transcluded': warning_data[year][month]['serious_transcluded'],
                    'warning_transcluded': warning_data[year][month]['warning_transcluded'], 
                    'not_serious_transcluded': warning_data[year][month]['not_serious_transcluded'],
                    'serious_substituted': warning_data[year][month]['serious_substituted'],
                    'warning_substituted': warning_data[year][month]['warning_substituted'],
                    'not_serious_substituted': warning_data[year][month]['not_serious_substituted'],
                }
            is_temporal_block = (int(year), int(month)) in temporal_blocks_dates
            is_infinite_block = (int(year), int(month)) in infinite_warnings_dates
            user_data.append({
                'date': datetime(int(year), int(month), 1), 
                'activities count': data[year][month], 
                'serious warnings': warnings_value['serious_transcluded'],
                'warnings': warnings_value['warning_transcluded'],
                'not serious warnings': warnings_value['not_serious_transcluded'],
                'serious warnings subst': warnings_value['serious_substituted'],
                'warnings subst': warnings_value['warning_substituted'],
                'not serious warnings subst': warnings_value['not_serious_substituted'],
                'serious_line': datetime(int(year), int(month), 1) if warnings_value['serious_transcluded'] and not is_infinite_block and not is_temporal_block else None,
                'temporal_block': datetime(int(year), int(month), 1) if is_temporal_block and not is_infinite_block else None,
                'infinite_block': datetime(int(year), int(month), 1) if is_infinite_block else None,
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

def addlabels(x: list[Any], y: list[int], percentage: bool):
    for i in range(len(x)):
        if type(y[i]) == float:
            text = '{:.2f}'.format(y[i])
        else:
            text = str(y[i])
        if percentage:
            text = ''.join([text, '%'])
        plt.text(i, y[i] + 0.3, text, ha = 'center')

def plot_bar_chart(title: str, y: list[int], x: list[Any], ylabel: str, xlabel: str, percentage: bool = False, text: str = None) -> None:
    """
    Plots a basic bar chart in a figure
    Args:
        title (str): title
        y (list[int]): y
        x (list[Any]): x
    """
    plt.figure(figsize=(16,8))
    plt.title(title)
    plt.bar(x, y)
    addlabels(x, y, percentage)
    if text:
        plt.text(0.83, 0.95, text, transform=plt.gca().transAxes)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

def plot_bar_chart_stacked(title: str, y: list[int], x: list[list[Any]], ylabel: str, xlabel: str, percentage: bool = False, legend: list[str] = None, text: str = None, legend_pos: str = None) -> None:
    """
    Plots a basic bar chart in a figure
    Args:
        title (str): title
        y (list[int]): y
        x (list[Any]): x
    """
    plt.figure(figsize=(16,8))
    plt.title(title)
    for el in y:
        plt.bar(x, el)
    y_add_labels = [0, 0]
    for el in y:
        y_add_labels[0] += el[0]
        y_add_labels[1] += el[1]
    addlabels(x, y_add_labels, percentage)
    if legend:
        if legend_pos:
            plt.legend(legend, loc=legend_pos)
        else:
            plt.legend(legend)
    if text:
        plt.text(0.83, 0.85, text, transform=plt.gca().transAxes)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

def plot_multiple_bar_plot(title:str, x_labels: list[str], y_values: list[Tuple[str, list]], colors:list[str] =None, total_width:float=0.8, single_width:int=1, legend:bool =True, text:str = None) -> None:
    """
    Plots a multiple bar chart for the same value of x
    Args:
        title (str): title of the plot
        x_labels (list[str]): list of x values
        y_values (list[Tuple[str, list]]): pair of label, y values
        colors (list): list of colors 
        total_width (float): width of the bars
        single_width (int): width of a bar, 
        legend (bool): whether the legend should be present or not
        text (str): text to display
    """

    fig, ax = plt.subplots(figsize=(16, 8))
    plt.title(title)
    
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(y_values)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(y_values):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
            for rect in bar:
                h = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1*h, '{:.2f}%'.format(h),
                        ha='center', va='bottom')
        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, [y[0] for y in y_values])

    if text:
        plt.text(0.80, 0.80, text, transform=plt.gca().transAxes)

    plt.xticks(range(len(x_labels)), x_labels)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

def plot_line_chart(x: pd.Series, y: list[Tuple[pd.Series, str]], title: str, ylabel: str, xlabel: str, text: str = None) -> None:
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
    if text:
        plt.text(0.30, -0.10, text, transform=plt.gca().transAxes)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig('{}/{}.{}'.format(output_folder, title, EXT))
    plt.close()

def plot_line_chart_with_vertical_lines(x: pd.Series, y: list[Tuple[pd.Series, str]], title: str, ylabel: str, xlabel: str, vlinesx: list[Tuple[pd.Series, str, str]], ymin: int, ymax: int, text: str) -> None:
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
    if text:
        plt.text(0.30, -0.10, text, transform=plt.gca().transAxes)
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

    start_date = monthdelta(parse(vlinesx[0]), - month_interval)
    end_date = monthdelta(parse(vlinesx[0]), + month_interval)
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

TEMPORAL_BLOCKS = {
    'block-reason', 
    'aviso bloqueado', 
    'uw-epblock', 
    'uw-csblock', 
    'uw-bioblock', 
    'uw-ewpblock', 
    'uw-socialmediablock', 
    'uw-gwblock', 
    'blocco', 
    'uw-3block', 
    'uw-botblock', 
    'uw-adblock', 
    'uw-sblock', 
    'uw-vblock', 
    'tmoblock', 
    'anonblock hard', 
    'uw-nfimageblock', 
    'aviso usuario títere', 
    'uw-efblock', 
    'uw-sockblock', 
    'uw-apblock', 
    'uw-hblock', 
    'uw-npblock', 
    'uw-blocknotalk', 
    'uw-spamblacklistblock', 
    'rc', 
    'uw-ewblock', 
    'uw-disruptblock', 
    'uw-pblock', 
    'uw-cserblock', 
    'uw-aeblock', 
    'uw-pablock', 
    'uw-ucblock', 
    'uw-copyrightblock', 
    'uw-block', 
    'uw-pinfoblock', 
    'uw-dblock'
}

INFINITE_BLOCKS = {
    'bloccoinfinito', 
    'uw-botuhblock', 
    'uw-adminuhblock', 
    'uw-uhblock-double', 
    'user expelled', 
    'sockpuppet bloccato', 
    'títere', 
    'blocked impersonator', 
    'sockmasterproven', 
    'arbcomblock', 
    'uw-vaublock', 
    'uw-upeblock', 
    'uw-nothereblock', 
    'wmf-legal banned user', 
    'uw-blockindef', 
    'uw-acpblockindef', 
    'sspblock', 
    'sockblock', 
    'uw-pblockindef', 
    'uw-uhblock', 
    'banned user', 
    'uw-cabalblock', 
    'vandalo recidivo'
}