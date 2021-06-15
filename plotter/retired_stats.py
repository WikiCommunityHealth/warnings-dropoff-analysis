from sys import argv
import pandas as pd
from plotter.utils import get_file_path, plot_bar_chart, create_folder_if_not_exists

def count_of_edits_bar_chart(categories: list[int], df: pd.DataFrame, field: str, title: str,  xlabel: str, ylabel: str) -> None:
    """
    Bar chart based on the user's edit count

    Args:
        categories (list[int]): categories
        df (pd.DataFrame): dataframe
        field (str): edit count field
        title (str): graph title
        xlabel (str): xlabel description
        ylabel (str): ylabel description
    """
    y = list()
    x = list()
    for i, c in enumerate(categories):
        if i == 0:
            extracted_size = df.loc[df[field] <= c].shape[0]
            x.append('{}'.format(c))
        else:
            extracted_size = df.loc[(df[field] <= c) & (df[field] > categories[i - 1])].shape[0]
            x.append('{}'.format(c))
        y.append(extracted_size)
    y.append(extracted_size)
    x.append('> {}'.format(categories[-1]))

    plot_bar_chart(
        title, 
        y=y, 
        x=x,
        xlabel=xlabel,
        ylabel=ylabel
    )

def plot_retired_stats(file_path: str) -> None:
    """
    Plots some graphs about the users who have declare the withdrawal form Wikipedia

    Args:
        file_path (str): file path
    """
    chart_counter = 1
    has_stopped_editing_treshold = 10
    print('Retrieving the dataframe...')
    df = pd.read_json(file_path, compression='gzip', lines=True)
    # retired users
    df = df.loc[df['retirement_declared'] == True]
    # stop or not after retirement
    print('Dataset retrieved')
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    total_true = df.loc[df['edit_count_after_retirement'] < has_stopped_editing_treshold].shape[0]
    total_false = df.loc[df['edit_count_after_retirement'] >= has_stopped_editing_treshold].shape[0]
    total = total_true + total_false if total_true + total_false else 1
    real_total = total_true + total_false
    plot_bar_chart(
        title='Stop editing after retirement (treshold = 10)', 
        y=[
            (total_true/total) * 100,
            (total_false/total) * 100,
        ], 
        x=['Has stopped editing', 'Has continued editing'],
        xlabel = '', 
        ylabel = 'Percentage of users',
        percentage = True,
        text = ''.join(['Total retired users: ', str(real_total)])
    )
    # other chart
    print('Plotting chart n {}...'.format(chart_counter))
    count_of_edits_bar_chart(
        categories = [0, 10, 20, 50, 100, 250, 1000, 2000, 5000],
        df = df,
        field = 'edit_count_after_retirement',
        title = 'Edit count after retirement',
        xlabel = 'Edits count', 
        ylabel = 'Number of users'
    )
    # grouped by sex
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    retired = df.loc[df['sex'].notna()]
    total = retired.shape[0]
    male_retired = retired.loc[retired['sex'] == True].shape[0]
    female_retired = retired.loc[retired['sex'] == False].shape[0]
    plot_bar_chart(
        title='Retired users, grouped by sex', 
        y = [
            (male_retired/total) * 100, 
            (female_retired/total) * 100
        ], 
        x = ['Men', 'Women'],
        xlabel = '',
        ylabel = 'Percentage of users',
        text = 'Considered users: {}\n'.format(total)
    )


if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    create_folder_if_not_exists(lang)
    plot_retired_stats(path)