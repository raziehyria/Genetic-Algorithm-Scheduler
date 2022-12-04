import json

import pandas

from meetingtime import MeetingTime


class MeetingTimeData:
    """
    This class handles creating objects for Meeting Times
    """

    def __init__(self, file_path):
        meetingTimeData = pandas.read_excel(file_path, sheet_name='Meeting Times')
        json_str = meetingTimeData.to_json()
        data = json.loads(json_str)
        self._meeting_times = []

        # dictionary to speed up the lookup
        self._format_time_slot_dict = {}

        data_keys = data.keys()
        for each_key in data_keys:
            all_the_days, duration = self._parse_days(each_key)
            for each_day in all_the_days:
                for each_time_slot in data.get(each_key).values():
                    if each_time_slot is None or "Common Break" in each_time_slot:
                        continue
                    else:
                        each_time_slot = self._format_time_slot(each_time_slot)
                        self._meeting_times.append((MeetingTime(each_day, duration, each_time_slot)))

    def _format_time_slot(self, time_slot):
        """
        Formats the time slot into XX:XX [am|pm] - XX:XX [am|pm]
        input 8:00-8:50a, i.e, 'a' or 'p' carries over from end to start time
        output 8:00 a - 8:50 a
        """
        # if previously seen, return that formatted value
        if time_slot in self._format_time_slot_dict:
            return self._format_time_slot_dict[time_slot]

        times = []
        time_slot = time_slot.lower()
        output = time_slot

        items = time_slot.split('-')

        # sometimes the hyphen is used, instead of dash
        if len(items) != 2:
            items = time_slot.split('–')
        am_or_pm = ''

        # process in reverse to carry 'a' or 'p' from end time for the start time (if absent)
        for item in items[::-1]:
            item = item.strip()
            if 'a' in item:
                t = item.split('a')[0].strip()
                am_or_pm = 'am'
            elif 'p' in item:
                t = item.split('p')[0].strip()
                am_or_pm = 'pm'
            else:
                t = item

            times.append(am_or_pm)
            times.append(t)

        # to check index out of bound error.
        if len(times) == 4:
            # update the missing 'am':  11:00 - 12:15p => 11:00 am - 12:15 pm
            start_time = int(times[3].split(':')[0])
            # if start time anywhere between 8 to 11 in the morning
            if times[2] == 'pm' and start_time in range(8, 12):
                times[2] = 'am'

            output = '{} {} - {} {}'.format(times[3], times[2], times[1], times[0])

        # update dictionary for future use
        self._format_time_slot_dict[time_slot] = output
        return output

    def _parse_days(self, days_duration_string):
        """
         input: "M or W or F, 2 hr, MW or WF or FM, 2hr'
         output : ['M', 'W', 'F', ..], 2hr
        """
        all_the_days = []
        items = days_duration_string.split(',')
        duration = items[-1].strip().lower()

        # format duration into 'xxx min' format
        if 'hr' in duration:
            num = duration.split('hr')[0].strip()
            duration = "{} min".format(int(num) * 60)
        elif 'min' in duration:
            num = duration.split('min')[0].strip()
            duration = "{} min".format(num)

        for item in items:
            if 'hr' not in item and 'min' not in item:
                days = item.split('or')
                for day in days:
                    all_the_days.append(day.strip().upper())

        return all_the_days, duration

    def get_meeting_times_objects_list(self):
        return self._meeting_times
