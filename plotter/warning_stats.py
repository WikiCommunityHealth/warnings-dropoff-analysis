from sys import argv
import pandas as pd
from plotter.utils import get_file_path, plot_pie_chart, plot_line_chart_with_vertical_lines, plot_line_chart, user_data_extraction

def plot_warnings_stats(file_path: str) -> None:
    print(file_path)
    chart_counter = 1
    print('Retrieving the dataframe...')
    df = pd.read_json(file_path, compression='gzip', lines=True)
    # recieved at least a serious warning
    df = df.loc[df['last_normal_warning'] != {}]
    # stopped editing after the last serious warning
    print('Dataset retrieved')
    # decrease activity
    df['Decrease activity'] = df['average_edit_amount_after_last_normal_warning_date'] < df['average_edit_amount_before_last_normal_warning_date']
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_pie_chart(
        title='Activity decrease after the last warning', 
        data=[
            df.loc[df['Decrease activity'] == True].shape[0], 
            df.loc[df['Decrease activity'] == False].shape[0]], 
        labels=['Has decreased the activity', 'Has not decreased the activity']
    )
    # bad user analysis
    try:
        user = df[
                ['name', 'last_edit_month', 'last_edit_year', 'edit_history', 'warnings_history']
            ].loc[
                df['amount_warning_templates_transcluded'] == df['amount_warning_templates_transcluded'].max()
            ].iloc[0]
    except:
        print('There aren\'t user with transcluded templates')
        exit(0)
    # user data
    user_data = user_data_extraction(user)
    # plot the user activity and warnings recieved
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_line_chart(
        x = user_data['date'],
        y = [
            (user_data['activities amount'], 'activities amount'),
            (user_data['serious warnings'], 'serious'),
            (user_data['warnings'], 'warning'),
            (user_data['not serious warnings'], 'not serious')
        ],
        title = 'User analysis: normal warnings recieved compared to the activity',
        ylabel = 'number of user warnings recived / activity in the community',
        xlabel = 'date',
    )
    # plot only the warnings recieved
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_line_chart(
        x = user_data['date'],
        y = [
            (user_data['serious warnings'], 'serious'),
            (user_data['warnings'], 'warning'),
            (user_data['not serious warnings'], 'not serious')
        ],
        title = 'User analysis: normal warnings recieved',
        ylabel = 'number of user warnings recived ',
        xlabel = 'date',
    )
    # plot user activity with serious warning treshold
    print('Plotting chart n {}...'.format(chart_counter))
    plot_line_chart_with_vertical_lines(
        x = user_data['date'],
        y = [
            (user_data['activities amount'], 'serious')
        ],
        title = 'User analysis: user activity with warning date',
        ylabel = 'user activity',
        xlabel = 'date',
        vlinesx = [
            (user_data.query('serious_line == serious_line')[['serious_line']]['serious_line'], 'red'),
            (user_data.query('warning_line == warning_line')[['warning_line']]['warning_line'], 'yellow'),
            (user_data.query('not_serious_line == not_serious_line')[['not_serious_line']]['not_serious_line'], 'green')
        ], 
        ymin = 0, 
        ymax = user_data['activities amount'].max()
    )
    # finished 
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    plot_warnings_stats(path)