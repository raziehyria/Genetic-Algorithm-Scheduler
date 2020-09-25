class MeetingTime:
    """"""

    def __init__(self, days, duration, time):
        self._days = days
        self._duration = duration
        self._time = time

    def get_days(self): return self._days

    def get_time(self): return self._time

    def get_duration(self): return self._duration

    def get_meetingTime(self): return self._days + " " + self._time

    def __str__(self):
        return "{} {}".format(self._days, self._time)