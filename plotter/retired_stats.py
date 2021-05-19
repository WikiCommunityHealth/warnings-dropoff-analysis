from sys import argv
import pandas as pd      
from plotter.utils import get_file_path, plot_pie_chart, plot_bar_chart

def amount_of_edits_bar_chart(categories: list[int], df: pd.DataFrame, field: str, title: str) -> None:
    # quanti hanno fatto edit dopo essersi ritirati
    categories = [0, 10, 20, 50, 100, 250, 1000, 2000, 5000]
    x = list()
    y = list()
    for i, c in enumerate(categories):
        if i == 0:
            extracted_size = df.loc[df[field] <= c].shape[0]
            y.append('x = {}'.format(c))
        else:
            extracted_size = df.loc[(df[field] <= c) & (df[field] > categories[i - 1])].shape[0]
            y.append('{} < x <= {}'.format(categories[i-1], c))
        x.append(extracted_size)
        
    extracted_size = df.loc[df[field] > categories[-1]].shape[0]
    y.append('x > {}'.format(categories[-1]))
    x.append(extracted_size)

    plot_bar_chart(title, y=y, x=x)

def plot_retired_stats(file_path: str) -> None:
    chart_counter = 1
    print('Retrieving the dataframe...')
    df = pd.read_json(file_path, compression='gzip', lines=True)
    # retired users
    df = df.loc[df['retirement_declared'] == True]
    # stop or not after retirement
    print('Dataset retrieved')
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_pie_chart(
        title='Stopping editing after retirement', 
        data=[df.loc[df['edit_amount_after_retirement'] < 5].shape[0], df.loc[df['edit_amount_after_retirement'] >= 5].shape[0]], 
        labels=['Has stopped editing', 'Has continued editing']
    )
    # other chart
    print('Plotting chart n {}...'.format(chart_counter))
    amount_of_edits_bar_chart(
        categories = [0, 10, 20, 50, 100, 250, 1000, 2000, 5000],
        df = df,
        field = 'edit_amount_after_retirement',
        title = 'Edit amount after retirement'
    )
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    plot_retired_stats(path)