from sys import argv
import pandas as pd
from plotter.utils import (
    get_file_path, 
    plot_bar_chart, 
    plot_line_chart_with_vertical_lines, 
    plot_line_chart, 
    user_data_extraction, 
    create_folder_if_not_exists,
    z_score_user_activity_amount_month_interval,
    plot_bar_chart_stacked,
    plot_multiple_bar_plot,
    TEMPORAL_BLOCKS
)

def plot_warnings_stats(file_path: str, month_interval: int) -> None:
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
    df = df.loc[df['last_serious_warning_name'].notna()]
    
    # stopped editing after the last serious warning
    print('Dataset retrieved')
    
    # temporal and infinite blocks column
    df['temporal_block'] = df['last_serious_warning_name'].apply(lambda x: x in TEMPORAL_BLOCKS)
    df['infinite_block'] = df['banned']
    
    # #############################################
    # DECREASE IN ACTIVITY
    # #############################################

    # decrease activity
    df['Decrease activity'] = df['average_edit_count_after_last_serious_warning_date'] < df['average_edit_count_before_last_serious_warning_date']
    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    # decrease activity (considering also blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True].shape[0]
    not_stopped = df.loc[df['Decrease activity'] == False].shape[0]
    stopped_total = not_stopped + stopped if not_stopped + stopped else 1
    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (including blocks and bans)', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    # decrease activity (without blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['temporal_block'] == False]
    stopped = stopped.loc[stopped['infinite_block'] == False].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['temporal_block'] == False]
    not_stopped = not_stopped.loc[not_stopped['infinite_block'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1
    
    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (without blocks and bans)', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # DECREASE IN ACTIVITY MEN AND WOMEN
    # #############################################


    # #############################################
    # DECREASE IN ACTIVITY              MEN ONLY
    # #############################################

    # decrease activity (considering also blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['sex'] == True].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == True].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (including blocks and bans)\nMen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    # decrease activity (without blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['sex'] == True]
    stopped = stopped.loc[stopped['temporal_block'] == False]
    stopped = stopped.loc[stopped['infinite_block'] == False].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == True]
    not_stopped = not_stopped.loc[not_stopped['temporal_block'] == False]
    not_stopped = not_stopped.loc[not_stopped['infinite_block'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (without blocks and bans)\nMen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # DECREASE IN ACTIVITY              WOMEN ONLY
    # #############################################

    # decrease activity (considering also blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['sex'] == False].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (including blocks and bans)\nWomen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    # decrease activity (without blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['sex'] == False]
    stopped = stopped.loc[stopped['temporal_block'] == False]
    stopped = stopped.loc[stopped['infinite_block'] == False].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == False]
    not_stopped = not_stopped.loc[not_stopped['temporal_block'] == False]
    not_stopped = not_stopped.loc[not_stopped['infinite_block'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Decrease in activity, in the following 12 months, after the last serious warning (without blocks and bans)\nWomen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # DECREASE IN ACTIVITY STACKED
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    no_blocks_ban = df.loc[df['temporal_block'] == False]
    no_blocks_ban = no_blocks_ban.loc[no_blocks_ban['infinite_block'] == False]
    no_blocks_ban = no_blocks_ban[no_blocks_ban['sex'].notna()]

    total = no_blocks_ban.shape[0]

    male_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == True]
    male_stopped = male_stopped.loc[male_stopped['sex'] == True].shape[0]

    male_not_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == False]
    male_not_stopped = male_not_stopped.loc[male_not_stopped['sex'] == True].shape[0]

    female_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == True]
    female_stopped = female_stopped.loc[female_stopped['sex'] == False].shape[0]

    female_not_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == False]
    female_not_stopped = female_not_stopped.loc[female_not_stopped['sex'] == False].shape[0]

    plot_bar_chart_stacked(
        title='Decrease in activity, in the following 12 months, after the last serious warning (without blocks and bans, grouped by sex)', 
        y = [
                [
                    (male_stopped/total) * 100, 
                    (male_not_stopped/total) * 100
                ],
                [
                    (female_stopped/total) * 100, 
                    (female_not_stopped/total) * 100
                ],
        ], 
        x = ['Has decreased the activity', 'Has not decreased the activity'],
        xlabel = '',
        ylabel = 'Percentage of users',
        legend = ['Men', 'Women'],
        legend_pos = 'center right',
        percentage = True,
        text = 'Considered users: {}\n'.format(total)
    )

    # #############################################
    # DECREASE IN ACTIVITY              COMPARISON
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    no_blocks_ban = df.loc[df['temporal_block'] == False]
    no_blocks_ban = no_blocks_ban.loc[no_blocks_ban['infinite_block'] == False]
    no_blocks_ban = no_blocks_ban[no_blocks_ban['sex'].notna()]

    male_total = no_blocks_ban.loc[no_blocks_ban['sex'] == True].shape[0]
    female_total = no_blocks_ban.loc[no_blocks_ban['sex'] == False].shape[0]

    male_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == True]
    male_stopped = male_stopped.loc[male_stopped['sex'] == True].shape[0]

    male_not_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == False]
    male_not_stopped = male_not_stopped.loc[male_not_stopped['sex'] == True].shape[0]

    female_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == True]
    female_stopped = female_stopped.loc[female_stopped['sex'] == False].shape[0]

    female_not_stopped = no_blocks_ban.loc[no_blocks_ban['Decrease activity'] == False]
    female_not_stopped = female_not_stopped.loc[female_not_stopped['sex'] == False].shape[0]

    # decrease activity (without blocks and bans)
    stopped = df.loc[df['Decrease activity'] == True]
    stopped = stopped.loc[stopped['temporal_block'] == False]
    stopped = stopped.loc[stopped['infinite_block'] == False].shape[0]

    not_stopped = df.loc[df['Decrease activity'] == False]
    not_stopped = not_stopped.loc[not_stopped['temporal_block'] == False]
    not_stopped = not_stopped.loc[not_stopped['infinite_block'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_multiple_bar_plot(
        title='Decrease in activity, in the following 12 months, after the last serious warning\n(without blocks and bans, grouped by sex)', 
        x_labels = ['Has decreased the activity', 'Has not decreased the activity'], 
        y_values = [
            ('total', [(stopped/stopped_total) * 100, (not_stopped/stopped_total) * 100]), 
            ('men', [(male_stopped/male_total) * 100, (male_not_stopped/male_total) * 100]), 
            ('women', [(female_stopped/female_total) * 100, (female_not_stopped/female_total) * 100])
        ], 
        total_width=.8, 
        single_width=.9,  
        text = 'Considered users: \nall {} men {}, women {}\n'.format(stopped_total, male_total, female_total)
    )

    # #############################################
    # BANNED USERS AMOUNT
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    stopped = df.loc[df['banned'] == True].shape[0]

    not_stopped = df.loc[df['banned'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Banned users', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Banned users', 'Not banned'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # BANNED USERS AMOUNT                   MEN
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    stopped = df.loc[df['banned'] == True]
    stopped = stopped.loc[stopped['sex'] == True].shape[0]

    not_stopped = df.loc[df['banned'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == True].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Banned users\nMen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Banned users', 'Not banned'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # BANNED USERS AMOUNT                   WOMEN
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    stopped = df.loc[df['banned'] == True]
    stopped = stopped.loc[stopped['sex'] == False].shape[0]

    not_stopped = df.loc[df['banned'] == False]
    not_stopped = not_stopped.loc[not_stopped['sex'] == False].shape[0]

    stopped_total = not_stopped + stopped if not_stopped + stopped else 1

    plot_bar_chart(
        title='Banned users\nWomen only', 
        y = [
            (stopped/stopped_total) * 100, 
            (not_stopped/stopped_total) * 100
        ], 
        x = ['Banned users', 'Not banned'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # #############################################
    # BANNED USERS AMOUNT       GROUPED BY CATEGORY
    # #############################################

    print('Plotting chart n {}...'.format(chart_counter))
    chart_counter += 1

    banned = df.loc[df['banned'] == True]
    banned = no_blocks_ban[no_blocks_ban['sex'].notna()]

    total = banned.shape[0]

    male_banned = banned.loc[banned['sex'] == True].shape[0]

    female_banned = banned.loc[banned['sex'] == False].shape[0]

    plot_bar_chart(
        title='Banned users, grouped by sex', 
        y = [
            (male_banned/total) * 100, 
            (female_banned/total) * 100
        ], 
        x = ['Men banned', 'Women banned'],
        xlabel = '',
        ylabel = 'Percentage of users',
        percentage = True,
        text = 'Considered users: {}\n'.format(stopped_total)
    )

    # bad users analysis (5 users)
    for _, user in df.nlargest(5, 'count_serious_templates_transcluded').iterrows():
        
        user = user[[
            'name', 
            'transcluded_user_warnings', 
            'last_edit_month', 
            'last_edit_year', 
            'edit_history', 
            'warnings_history', 
            'last_serious_warning_date', 
            'last_serious_warning_name', 
            'last_normal_warning', 
            'last_not_serious_warning', 
            'count_serious_templates_transcluded'
        ]]

        # no more users with serious templates
        if user['count_serious_templates_transcluded'] == 0:
            break

        print('Pass')

        # user data
        user_data = user_data_extraction(user)

        # plot only the warnings received
        print('Plotting chart n {}...'.format(chart_counter))
        chart_counter += 1
        plot_line_chart(
            x = user_data['date'],
            y = [
                (user_data['serious warnings'], 'high-severity warning received'),
                (user_data['warnings'], 'medium-severity warning received'),
                (user_data['not serious warnings'], 'low-severity warning received')
            ],
            title = 'User analysis: warnings received',
            ylabel = 'number of user warnings received ',
            xlabel = 'date',
            text = 'Warnings transcluded: (S:{}, W:{}, NS:{}) Warnings received: (S:{}, W:{}, NS:{})'.format(
                user_data['serious warnings'].sum(),
                user_data['warnings'].sum(),
                user_data['not serious warnings'].sum(),
                user_data['serious warnings subst'].sum(),
                user_data['warnings subst'].sum(),
                user_data['not serious warnings subst'].sum()
            )
        )

        # plot user activity with serious warning treshold
        print('Plotting chart n {}...'.format(chart_counter))
        plot_line_chart_with_vertical_lines(
            x = user_data['date'],
            y = [
                (user_data['activities count'], 'activity level')
            ],
            title = 'User activity versus warnings, blocks, and bans received',
            ylabel = 'user activity',
            xlabel = 'date',
            vlinesx = [
                (user_data.query('serious_line == serious_line')[['serious_line']]['serious_line'], 'red', 'high-severity warning received'),
                (user_data.query('infinite_block == infinite_block')[['infinite_block']]['infinite_block'], 'black', 'infinite ban received'),
                (user_data.query('temporal_block == temporal_block')[['temporal_block']]['temporal_block'], 'purple', 'temporary block received'),
                (user_data.query('warning_line == warning_line')[['warning_line']]['warning_line'], 'yellow', 'medium-severity warning received'),
                (user_data.query('not_serious_line == not_serious_line')[['not_serious_line']]['not_serious_line'], 'green', 'low-severity warning received')
            ], 
            ymin = 0, 
            ymax = user_data['activities count'].max(),
            text = 'Warnings transcluded: (S:{}, W:{}, NS:{}) Warnings received: (S:{}, W:{}, NS:{})'.format(
                user_data['serious warnings'].sum(),
                user_data['warnings'].sum(),
                user_data['not serious warnings'].sum(),
                user_data['serious warnings subst'].sum(),
                user_data['warnings subst'].sum(),
                user_data['not serious warnings subst'].sum()
            )
        )

        print('Plotting chart n {}...'.format(chart_counter))
        chart_counter += 1
        # last serious warnings date
        last_serious_date = user['last_serious_warning_date']
        # compute the z-score
        exists, zscore_data = z_score_user_activity_amount_month_interval(
            x = user_data['date'],
            y = user_data,
            vlinesx = (last_serious_date, 'red'),
            month_interval=month_interval
        )
        min_date = zscore_data['date'].min()
        max_date = zscore_data['date'].max()
        if exists:
            ymin = zscore_data['activities z-score'].min()
            ymax = zscore_data['activities z-score'].max()
            if ymin == ymax:
                ymax += 1
            plot_line_chart_with_vertical_lines(
                x = zscore_data['date'],
                y = [
                    (zscore_data['activities z-score'], 'activities z-score')
                ],
                title = 'z-score computed on user\'s activity (from 12 month before the last warning to the 12 month after having received it)',
                ylabel = 'user activity z-score',
                xlabel = 'date',
                vlinesx = [
                    (user_data.loc[(pd.isnull(user_data['serious_line']) == False) & (user_data['date'] > min_date) & (user_data['date'] < max_date), ['serious_line']]['serious_line'], 'red', 'high-severity warning received'),
                    (user_data.loc[(pd.isnull(user_data['infinite_block']) == False) & (user_data['date'] > min_date) & (user_data['date'] < max_date), ['infinite_block']]['infinite_block'], 'black', 'infinite ban received'),
                    (user_data.loc[(pd.isnull(user_data['temporal_block']) == False) & (user_data['date'] > min_date) & (user_data['date'] < max_date), ['temporal_block']]['temporal_block'], 'purple', 'temporary block received'),
                    (user_data.loc[(pd.isnull(user_data['warning_line']) == False) & (user_data['date'] > min_date) & (user_data['date'] < max_date), ['warning_line']]['warning_line'], 'yellow', 'medium-severity warning received'),
                    (user_data.loc[(pd.isnull(user_data['not_serious_line']) == False) & (user_data['date'] > min_date) & (user_data['date'] < max_date), ['not_serious_line']]['not_serious_line'], 'green', 'low-severity warning received')
                ], 
                ymin = ymin,
                ymax = ymax,
                text = 'Warnings transcluded: (S:{}, W:{}, NS:{}) Warnings received: (S:{}, W:{}, NS:{})'.format(
                    user_data['serious warnings'].sum(),
                    user_data['warnings'].sum(),
                    user_data['not serious warnings'].sum(),
                    user_data['serious warnings subst'].sum(),
                    user_data['warnings subst'].sum(),
                    user_data['not serious warnings subst'].sum()
                )
            )
    # finished 
    print('Finished')

if __name__ == '__main__':
    lang = argv[1]
    month_interval = 12
    if len(argv) > 2:
        month_interval = int(argv[2])
    path = get_file_path(lang)
    create_folder_if_not_exists(lang)
    plot_warnings_stats(path, month_interval)