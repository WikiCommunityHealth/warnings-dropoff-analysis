from sys import argv
import pandas as pd      
from plotter.utils import get_file_path, plot_bar_chart, create_folder_if_not_exists

def count_of_edits_bar_chart(categories: list[int], df: pd.DataFrame, field: str, title: str) -> None:
    # quanti hanno fatto edit dopo essersi ritirati
    categories = [0, 10, 20, 50, 100, 250, 1000, 2000, 5000]
    x = list()
    y = list()
    for i, c in enumerate(categories):
        if i == 0:
            extracted_size = df.loc[df[field] <= c].shape[0]
            y.append('{}'.format(c))
        else:
            extracted_size = df.loc[(df[field] <= c) & (df[field] > categories[i - 1])].shape[0]
            y.append('{}'.format(c))
        x.append(extracted_size)
    x.append(extracted_size)

    plot_bar_chart(
        title, 
        y=y, 
        x=x
    )

def plot_retired_stats(file_path: str) -> None:
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
    plot_bar_chart(
        title='Stopping editing after retirement', 
        y=[
            df.loc[df['edit_count_after_retirement'] < has_stopped_editing_treshold].shape[0],
            df.loc[df['edit_count_after_retirement'] >= has_stopped_editing_treshold].shape[0]
        ], 
        x=['Has stopped editing', 'Has continued editing']
    )
    # other chart
    print('Plotting chart n {}...'.format(chart_counter))
    count_of_edits_bar_chart(
        categories = [0, 10, 20, 50, 100, 250, 1000, 2000, 5000],
        df = df,
        field = 'edit_count_after_retirement',
        title = 'Edit count after retirement'
    )
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    create_folder_if_not_exists(lang)
    plot_retired_stats(path)