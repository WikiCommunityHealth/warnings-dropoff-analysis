from .. import UserMetrics
from datetime import datetime, timedelta
from .constants import retired_template_list
from typing import Tuple, Optional
from dateutil import parser
import calendar

"""
Namespaces
"""
namespaces = [
    'n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'n10', 'n11', 'n12', 
    'n13', 'n14', 'n15', 'n100', 'n101', 'n118', 'n119', 'n710', 'n711', 'n828', 'n829', 
    'n108', 'n109', 'n446', 'n447', 'n2300', 'n2301', 'n2302', 'n2303', 'unknown'
]

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

def extract_metrics(user: dict, month_to_be_considered_retired: int) -> Tuple[Optional[UserMetrics], bool]:
    """
    Main method to extract the drop-off metrics

    Args:
        user (dict): user dictionry retrieved from the collection
        month_to_be_considered_retired (int): month threshold to consider a user in drop-off

    Returns:
        Optional[UserMetrics]: if the user is really in drop-off then it returns the metrics otherwise None
        ambiguous bollean: if the user has no edits (or the edit info is missing)
    """


    # check if the user is retired controlling the wikibreaks he has specified
    has_template, retirement_info = retired_template_extractor(user)
    # last edit date and drop-off check
    last_edit_date, in_drop_off, ambiguous = retired_edit_treshold_extractor(has_template, user, month_to_be_considered_retired)

    # user not in the target audience
    if not in_drop_off:
        return None, ambiguous

    # retire date
    if 'from_date' in retirement_info:
        retire_date = retirement_info['from_date']
    else:
        retire_date = None

    # warnings metrics
    last_warnings, warnings_count, warnings_history = retrieve_warninigs(user)
    # edits metrics
    edit_count_after_retirement, average_metrics, edit_history = retrieve_activities(has_template, retire_date, user, last_warnings, last_edit_date)

    return UserMetrics(
        name = user['username'],
        id = user['id'],
        # controllare se last edit è un campo
        retirement_declared = has_template,
        retire_date = retire_date,
        last_edit_month = last_edit_date.month,
        last_edit_year =  last_edit_date.year,
        edit_count_after_retirement = edit_count_after_retirement,
        # last elements
        last_serious_warning = last_warnings['serious'],
        last_normal_warning = last_warnings['warning'],
        last_not_serious_warning = last_warnings['not_serious'],
        # average before
        average_edit_count_before_last_serious_warning_date = average_metrics['serious']['before'],
        average_edit_count_before_last_normal_warning_date = average_metrics['warning']['before'],
        average_edit_count_before_last_not_serious_warning_date = average_metrics['not_serious']['before'],
        # average after
        average_edit_count_after_last_serious_warning_date = average_metrics['serious']['after'],
        average_edit_count_after_last_normal_warning_date = average_metrics['warning']['after'],
        average_edit_count_after_last_not_serious_warning_date = average_metrics['not_serious']['after'],
        # count
        count_serious_templates_transcluded = warnings_count['serious_transcluded'],
        count_warning_templates_transcluded = warnings_count['warning_transcluded'],
        count_not_serious_templates_transcluded = warnings_count['not_serious_transcluded'],
        count_serious_templates_substituted = warnings_count['serious_substituted'],
        count_warning_templates_substituted = warnings_count['warning_substituted'],
        count_not_serious_templates_substituted = warnings_count['not_serious_substituted'],
        # history
        edit_history = edit_history,
        warnings_history = warnings_history
    ), ambiguous

def retrieve_warninigs(user: dict) -> Tuple[dict, dict, dict]:
    """
    It extracts the metrics associated with the user warnings
    
    Args:
        user (dict): user element in the collection

    Returns:
        list[dict, dict, dict]: respectively the info about the last warnings received, 
            the total count of user warnings received, 
            history of the warnings received
    """
    last_warnings: dict = {'not_serious': dict(), 'warning':dict(), 'serious':dict()}
    counts_uw: dict = {
        'serious_transcluded': 0,
        'warning_transcluded': 0,
        'warning_substituted': 0,
        'not_serious_transcluded': 0,
        'serious_substituted': 0,
        'not_serious_substituted': 0
    }

    for uw in user['user_warnings_recieved']:
        if not last_warnings[uw['category']]:
            last_warnings[uw['category']] = dict()

        for param in uw['parameters']:
            init_date = parser.parse(param['timestamp'])
            if not 'date' in last_warnings[uw['category']] or last_warnings[uw['category']]['date'] < init_date:
                last_warnings[uw['category']]['name'] = uw['user_warning_name']
                last_warnings[uw['category']]['date'] = init_date

    for year in user['user_warnings_stats']:
        for month in user['user_warnings_stats'][year]:
            for stat in user['user_warnings_stats'][year][month]:
                counts_uw[stat] += user['user_warnings_stats'][year][month][stat]

    return last_warnings, counts_uw, user['user_warnings_stats']

def retired_template_extractor(user: dict) -> Tuple[bool, dict]:
    """
    It extracts the metrics associated with the retired template

    Args:
        user (dict): user element in the collection

    Returns:
        Tuple[bool, dict]: (if the template is present, info about the template found)
    """

    # no wikibreak found
    if not 'wikibreaks' in user:
        return False, {}
    
    has_retired_template: bool = False
    retired_template: dict = {}

    for wb in user['wikibreaks']:
        if wb['name'] in retired_template_list:
            # retirement status removed
            if wb['to_date']:
                continue
            has_retired_template = True
            retired_template['name'] = wb['name']
            retired_template['from_date'] = parser.parse(wb['from_date'])

    return has_retired_template, retired_template

def retired_edit_treshold_extractor(is_retired: bool, user: dict, month_to_be_considered_retired: int) -> Tuple[datetime, bool, bool]:
    """
    It checks if the user is in drop-off and returns some stats associated

    Args:
        is_retired (bool): if the user has declared the retirement
        user (dict): user element retrieved from the collection
        month_to_be_considered_retired (int): month of inactivity to consider the user in drop-off

    Returns:
        list[datetime, bool, bool]: date of the user's last edit, if the user is in drop-off, if the user is not ambiguous
    """

    # discard this users
    if not user['events']['per_month']:
        return None, False, True

    last_edit_date_year =  max(int(k) for k in user['events']['per_month'])
    last_edit_month = max(int(k) for k in user['events']['per_month'][str(last_edit_date_year)])
    today = datetime.utcnow()
    last_edit_date = datetime(last_edit_date_year, last_edit_month, today.day)
    drop_off = False

    if is_retired or monthdelta(today, - month_to_be_considered_retired) > last_edit_date:
        # the user is considered in drop-off
        drop_off = True
    return last_edit_date, drop_off, False

def retrieve_activities(declared_retirement: bool, retirement_date: Optional[datetime], user: dict, last_warnings: dict, last_edit: datetime) -> Tuple[int, dict, dict]:  
    """
    It retrieves the metrics associated with the user's edits

    Args:
        declared_retirement (bool): retirement declared
        retirement_date (Optional[datetime]):  retirement date if retirement specified
        user (dict): user retrieved from the collection
        last_warnings (dict): last warnings date by category
        last_edit (datetime): last edit

    Returns:
        list[int, dict, dict]: number of edits after the retirement (if specified), he metrics related to the average count of edits, and the edit history of the user
    """
    
    average_metrics: dict = {
        'serious': {
            'before': 0,
            'after': 0,
            'months_before': 0,
            'months_after': 0
        }, 'warning': {
            'before': 0,
            'after': 0,
            'months_before': 0,
            'months_after': 0
        }, 'not_serious': {
            'before': 0,
            'after': 0,
            'months_before': 0,
            'months_after': 0
        }
    }
    edit_history = dict()
    
    if declared_retirement:
        edit_count_after_retirement = 0
    else:
        edit_count_after_retirement = None
    
    first_edit_date_year =  min(int(k) for k in user['events']['per_month'])
    first_edit_month = min(int(k) for k in user['events']['per_month'][str(first_edit_date_year)])

    end_date =max([last_edit, monthdelta(datetime.utcnow(), -6)])

    for year, month in month_year_iter(first_edit_month, first_edit_date_year, end_date.month + 1, end_date.year):
        if month < 10:
            month = '0{}'.format(month)
        else:
            month = str(month)
        
        i_month = int(month)
        s_year = str(year)

        if not year in edit_history:
            edit_history[year] = dict()
            for i in range(1, 13):
                edit_history[year][i] = 0

        target = {
            'serious': 'before',
            'warning': 'before',
            'not_serious': 'before'
        }

        for key in target.keys():
            if last_warnings[key] and datetime(year, i_month, 1) > last_warnings[key]['date'].replace(tzinfo=None):
                target[key] = 'after'

        if s_year in user['events']['per_month']:
            if month in user['events']['per_month'][s_year]:
                total_activities = 0
                for namespace in user['events']['per_month'][s_year][month]:
                    if namespace in namespaces:
                        for categories in user['events']['per_month'][s_year][month][namespace]:
                            total_activities += user['events']['per_month'][s_year][month][namespace][categories]

                
                if declared_retirement and datetime(year, i_month, 1) > retirement_date.replace(tzinfo=None):
                    edit_count_after_retirement += total_activities

                edit_history[year][i_month] = total_activities

                # updating the average metrics according to the target (counting before or after) (key represents the type of warning)
                for key, value in target.items():
                    # we are counting 6 month before and afer the last warning to compute the average count
                    if last_warnings[key]:
                        is_before_6_month: bool = (value == 'before' and datetime(year, i_month, 1) >= monthdelta(last_warnings[key]['date'].replace(tzinfo=None), -6))
                        is_after_6_month: bool = (value == 'after' and datetime(year, i_month, 1) <= monthdelta(last_warnings[key]['date'].replace(tzinfo=None), +6))
                        if is_before_6_month or is_after_6_month:
                            average_metrics[key][value] += total_activities
                            average_metrics[key]['months_{}'.format(value)] += 1
        else:
            # year of inactivity
            for key, value in target.items():
                average_metrics[key]['months_{}'.format(value)] += 12

    for categories in average_metrics:
        if average_metrics[categories]['months_before']:
            average_metrics[categories]['before'] /= average_metrics[categories]['months_before']
        if average_metrics[categories]['months_after']:
            average_metrics[categories]['after'] /= average_metrics[categories]['months_after']

    return edit_count_after_retirement, average_metrics, edit_history