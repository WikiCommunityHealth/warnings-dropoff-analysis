import json
from typing import Optional, Tuple
from datetime import datetime

class UserMetrics():
    """
    Class which represent the metrics retrived for each user
    """
    def __init__(self, 
        name: str, 
        id: str, 
        last_edit_month: int, 
        last_edit_year: int,

        retirement_declared: bool, 
        retire_date: datetime,
        edit_amount_after_retirement: Optional[int],

        last_serious_warning: Optional[dict],
        last_normal_warning: Optional[dict],
        last_not_serious_warning: Optional[dict],

        average_edit_amount_before_last_serious_warning_date: Optional[float],
        average_edit_amount_before_last_normal_warning_date: Optional[float],
        average_edit_amount_before_last_not_serious_warning_date: Optional[float],
        average_edit_amount_after_last_serious_warning_date: Optional[float],
        average_edit_amount_after_last_normal_warning_date: Optional[float],
        average_edit_amount_after_last_not_serious_warning_date: Optional[float],

        amount_serious_templates_transcluded: Optional[int],
        amount_warning_templates_transcluded: Optional[int],
        amount_not_serious_templates_transcluded: Optional[int],
        amount_serious_templates_substituted: Optional[int],
        amount_warning_templates_substituted: Optional[int],
        amount_not_serious_templates_substituted: Optional[int],

        edit_history: dict,
        warnings_history: dict
        ):


        # general information
        self.name = name
        self.id = id
        self.last_edit_month = last_edit_month
        self.last_edit_year = last_edit_year

        # retirement information
        self.retirement_declared = retirement_declared
        self.retire_date = retire_date
        self.edit_amount_after_retirement = edit_amount_after_retirement

        # some metrics
        self.last_serious_warning = last_serious_warning
        self.last_normal_warning = last_normal_warning
        self.last_not_serious_warning = last_not_serious_warning

        self.average_edit_amount_before_last_serious_warning_date = average_edit_amount_before_last_serious_warning_date
        self.average_edit_amount_before_last_normal_warning_date = average_edit_amount_before_last_normal_warning_date
        self.average_edit_amount_before_last_not_serious_warning_date = average_edit_amount_before_last_not_serious_warning_date
        self.average_edit_amount_after_last_serious_warning_date = average_edit_amount_after_last_serious_warning_date
        self.average_edit_amount_after_last_normal_warning_date = average_edit_amount_after_last_normal_warning_date
        self.average_edit_amount_after_last_not_serious_warning_date = average_edit_amount_after_last_not_serious_warning_date

        self.amount_serious_templates_transcluded = amount_serious_templates_transcluded
        self.amount_warning_templates_transcluded = amount_warning_templates_transcluded
        self.amount_not_serious_templates_transcluded = amount_not_serious_templates_transcluded
        self.amount_serious_templates_substituted = amount_serious_templates_substituted
        self.amount_warning_templates_substituted = amount_warning_templates_substituted
        self.amount_not_serious_templates_substituted =amount_not_serious_templates_substituted

        self.edit_history = edit_history
        self.warnings_history = warnings_history

    @property
    def json(self):
        """
        UserMetrics object to JSON

        Returns:
            json string: json notation for the UserMetrics instance
        """
        obj = dict()
        obj['name'] = self.name
        obj['id'] = self.id
        obj['last_edit_month'] = self.last_edit_month
        obj['last_edit_year'] = self.last_edit_year

        obj['retirement_declared'] = self.retirement_declared
        obj['retire_date'] = self.retire_date
        obj['edit_amount_after_retirement'] = self.edit_amount_after_retirement

        obj['last_serious_warning'] = self.last_serious_warning
        obj['last_normal_warning'] = self.last_normal_warning
        obj['last_not_serious_warning'] = self.last_not_serious_warning

        obj['average_edit_amount_before_last_serious_warning_date'] = self.average_edit_amount_before_last_serious_warning_date
        obj['average_edit_amount_before_last_normal_warning_date'] = self.average_edit_amount_before_last_normal_warning_date
        obj['average_edit_amount_before_last_not_serious_warning_date'] = self.average_edit_amount_before_last_not_serious_warning_date
        obj['average_edit_amount_after_last_serious_warning_date'] = self.average_edit_amount_after_last_serious_warning_date
        obj['average_edit_amount_after_last_normal_warning_date'] = self.average_edit_amount_after_last_normal_warning_date
        obj['average_edit_amount_after_last_not_serious_warning_date'] = self.average_edit_amount_after_last_not_serious_warning_date

        obj['amount_serious_templates_transcluded'] = self.amount_serious_templates_transcluded
        obj['amount_warning_templates_transcluded'] = self.amount_warning_templates_transcluded
        obj['amount_not_serious_templates_transcluded'] = self.amount_not_serious_templates_transcluded
        obj['amount_serious_templates_substituted'] = self.amount_serious_templates_substituted
        obj['amount_warning_templates_substituted'] = self.amount_warning_templates_substituted
        obj['amount_not_serious_templates_substituted'] = self.amount_not_serious_templates_substituted

        obj['edit_history'] = self.edit_history
        obj['warnings_history'] = self.warnings_history

        return json.dumps(obj, default=str)