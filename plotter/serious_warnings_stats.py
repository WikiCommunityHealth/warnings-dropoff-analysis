from sys import argv
import pandas as pd
from plotter.utils import get_file_path, plot_bar_chart, plot_line_chart_with_vertical_lines, plot_line_chart, user_data_extraction, create_folder_if_not_exists

def plot_warnings_stats(file_path: str) -> None:
    print(file_path)
    chart_counter = 1
    print('Retrieving the dataframe...')
    df = pd.read_json(file_path, compression='gzip', lines=True)
    # received at least a serious warning
    df = df.loc[df['last_serious_warning'] != {}]
    # stopped editing after the last serious warning
    print('Dataset retrieved')
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_bar_chart(
        title='Stopped eding after last serious warning', 
        y=[
            df.loc[df['average_edit_count_after_last_serious_warning_date'] == 0].shape[0], 
            df.loc[df['average_edit_count_after_last_serious_warning_date'] > 0].shape[0]], 
        x=['Has stopped editing', 'Has continued editing']
    )
    # decrease activity
    df['Decrease activity'] = df['average_edit_count_after_last_serious_warning_date'] < df['average_edit_count_before_last_serious_warning_date']
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_bar_chart(
        title='Activity decrease after the last serious warning', 
        y=[
            df.loc[df['Decrease activity'] == True].shape[0], 
            df.loc[df['Decrease activity'] == False].shape[0]], 
        x=['Has decreased the activity', 'Has not decreased the activity']
    )
    # bad user analysis
    try:
        user = df[
                ['name', 'last_edit_month', 'last_edit_year', 'edit_history', 'warnings_history']
            ].loc[
                df['count_serious_templates_transcluded'] == df['count_serious_templates_transcluded'].max()
            ].iloc[0]
    except:
        print('There aren\'t user with transcluded templates')
        exit(0)
    print(user['name'])
    # user data
    user_data = user_data_extraction(user)
    # plot the user activity and warnings received
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_line_chart(
        x = user_data['date'],
        y = [
            (user_data['activities count'], 'activities count'),
            (user_data['serious warnings'], 'serious'),
            (user_data['warnings'], 'warning'),
            (user_data['not serious warnings'], 'not serious')
        ],
        title = 'User analysis: warnings received compared to the activity',
        ylabel = 'number of user warnings recived / activity in the community',
        xlabel = 'date',
    )
    # plot only the warnings received
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    plot_line_chart(
        x = user_data['date'],
        y = [
            (user_data['serious warnings'], 'serious'),
            (user_data['warnings'], 'warning'),
            (user_data['not serious warnings'], 'not serious')
        ],
        title = 'User analysis: warnings received',
        ylabel = 'number of user warnings recived ',
        xlabel = 'date',
    )
    # plot user activity with serious warning treshold
    print('Plotting chart n {}...'.format(chart_counter))
    plot_line_chart_with_vertical_lines(
        x = user_data['date'],
        y = [
            (user_data['activities count'], 'activities count')
        ],
        title = 'User analysis: user activity with serious warning date',
        ylabel = 'user activity',
        xlabel = 'date',
        vlinesx = [
            (user_data.query('serious_line == serious_line')[['serious_line']]['serious_line'], 'red'),
            (user_data.query('warning_line == warning_line')[['warning_line']]['warning_line'], 'yellow'),
            (user_data.query('not_serious_line == not_serious_line')[['not_serious_line']]['not_serious_line'], 'green')
        ], 
        ymin = 0, 
        ymax = user_data['activities count'].max()
    )
    # finished 
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    create_folder_if_not_exists(lang)
    plot_warnings_stats(path)