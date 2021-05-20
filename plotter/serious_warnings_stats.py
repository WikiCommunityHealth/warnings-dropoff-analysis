from sys import argv
import pandas as pd
from plotter.utils import (
    get_file_path, 
    plot_bar_chart, 
    plot_line_chart_with_vertical_lines, 
    plot_line_chart, 
    user_data_extraction, 
    create_folder_if_not_exists,
    z_score_user_activity_amount_6_month_interval
)

def plot_warnings_stats(file_path: str) -> None:
    """
    Plots some graphs about the users who have recieved at least a serious warning

    Args:
        file_path (str): file path
    """
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
    stopped = df.loc[df['average_edit_count_after_last_serious_warning_date'] == 0].shape[0]
    not_stopped = df.loc[df['average_edit_count_after_last_serious_warning_date'] > 0].shape[0]
    stopped_total = not_stopped + stopped if not_stopped + stopped else 1
    plot_bar_chart(
        title='Stop eding after last serious warning', 
        y=[
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ],
        x=['Has stopped editing', 'Has continued editing'],
        xlabel = '', 
        ylabel = 'Percentage of users'
    )
    # decrease activity
    df['Decrease activity'] = df['average_edit_count_after_last_serious_warning_date'] < df['average_edit_count_before_last_serious_warning_date']
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1
    stopped = df.loc[df['Decrease activity'] == True].shape[0]
    not_stopped = df.loc[df['Decrease activity'] == False].shape[0]
    stopped_total = not_stopped + stopped if not_stopped + stopped else 1
    plot_bar_chart(
        title='Decrease in activity after the last serious warning', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '', 
        ylabel = 'Percentage of users'
    )
    # bad users analysis (5 users)
    for _, user in df.nlargest(5, 'count_serious_templates_transcluded').iterrows():
        
        user = user[['name', 'last_edit_month', 'last_edit_year', 'edit_history', 'warnings_history', 'last_serious_warning', 'last_normal_warning', 'last_not_serious_warning', 'count_serious_templates_transcluded']]

        # no more users with serious templates
        if user['count_serious_templates_transcluded'] == 0:
            break

        print('User: {}'.format(user['name']))
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
            title = 'User analysis: warnings received compared to the user\'s activity\n{}'.format(user['name']),
            ylabel = 'number of user warnings received / activity in the community',
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
            title = 'User analysis: warnings received\n{}'.format(user['name']),
            ylabel = 'number of user warnings received ',
            xlabel = 'date',
        )

        # plot user activity with serious warning treshold
        print('Plotting chart n {}...'.format(chart_counter))
        plot_line_chart_with_vertical_lines(
            x = user_data['date'],
            y = [
                (user_data['activities count'], 'activities count')
            ],
            title = 'User analysis: user activity with serious warnings date\n{}'.format(user['name']),
            ylabel = 'user activity',
            xlabel = 'date',
            vlinesx = [
                (user_data.query('serious_line == serious_line')[['serious_line']]['serious_line'], 'red'),
                (user_data.query('warning_line == warning_line')[['warning_line']]['warning_line'], 'orange'),
                (user_data.query('not_serious_line == not_serious_line')[['not_serious_line']]['not_serious_line'], 'green')
            ], 
            ymin = 0, 
            ymax = user_data['activities count'].max()
        )

        print('Plotting chart n {}...'.format(chart_counter))
        chart_counter += 1
        # last serious warnings date
        if 'date' in user['last_serious_warning']:
            last_serious_date = user['last_serious_warning']['date']
        else:
            last_serious_date = None
        # compute the z-score
        exists, zscore_data = z_score_user_activity_amount_6_month_interval(
            x = user_data['date'],
            y = user_data,
            vlinesx = (last_serious_date, 'red')
        )
        min_date = zscore_data['date'].min()
        if exists:
            plot_line_chart_with_vertical_lines(
                x = zscore_data['date'],
                y = [
                    (zscore_data['activities z-score'], 'activities z-score')
                ],
                title = 'Z score computed on user\'s activity (from six month before the last warning to the six month after having received it)\n{}'.format(user['name']),
                ylabel = 'user activity z-score',
                xlabel = 'date',
                vlinesx = [
                    (user_data.loc[(pd.isnull(user_data['serious_line']) == False) & (user_data['date'] > min_date), ['serious_line']]['serious_line'], 'red'),
                    (user_data.loc[(pd.isnull(user_data['warning_line']) == False) & (user_data['date'] > min_date), ['warning_line']]['warning_line'], 'orange'),
                    (user_data.loc[(pd.isnull(user_data['not_serious_line']) == False) & (user_data['date'] > min_date), ['not_serious_line']]['not_serious_line'], 'green')
                ], 
                ymin = zscore_data['activities z-score'].min(), 
                ymax = zscore_data['activities z-score'].max()
            )
    # finished 
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    create_folder_if_not_exists(lang)
    plot_warnings_stats(path)