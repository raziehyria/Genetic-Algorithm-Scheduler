from meetingtime import MeetingTime
import json
import pandas
import pprint

class MeetingTimeData:
    """
    This class handles creating objects for Meeting Times
    """

    def __init__(self):
        meetingTimeData = pandas.read_excel('Course list and attributes.xlsx', sheet_name='Meeting Times')
        json_str = meetingTimeData.to_json()
        data = json.loads(json_str)
        self.meeting_times = []
        self._meeting_times = []

        data_keys = data.keys()
        for each_key in data_keys:
            all_the_days, duration = self._parse_days(each_key)
            for each_day in all_the_days:
                for each_time_slot in data.get(each_key).values():
                    if each_time_slot is None or "Common Break" in each_time_slot :
                        continue
                    else:
                        self.meeting_times.append((MeetingTime(each_day, duration, each_time_slot)))
                        self._meeting_times.append((MeetingTime(each_day, duration, each_time_slot)))

    def _parse_days(self, days_duration_string):
        """
         input: "M or W or F, 2 hr, MW or WF or FM, 2hr'
         outpuot : ['M', 'W', 'F', ..], 2hr

        """
        all_the_days = []
        items = days_duration_string.split(',')
        duration = items[-1].strip()
        for i, item in enumerate(items):
            if i % 2 == 0:
                days = item.split('or')
                for day in days:
                    all_the_days.append(day.strip())

        return all_the_days, duration

    def get_meeting_times_objects_list(self):
        return self._meeting_times
