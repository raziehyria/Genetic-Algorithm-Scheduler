from config import Config
from schedule import Schedule
from operator import methodcaller


class Population:
    def __init__(self, size):
        self._size = size
        self._data = Config.getInstance().get_data()
        self._schedules = []
        for _ in range(self._size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules

    #  multisorting technique reference, scroll down to "Sort Stability and Complex Sorts"
    #  https://docs.python.org/3.9/howto/sorting.html#sort-stability-and-complex-sorts

    def sort_schedules(self):

        # We want to sort with minimum major and minor conflicts (i.e., higher fitness score).
        # First sort by minor conflicts, then sort by major conflicts
        # -- that way in case of a tie in major conflicts, less number of minor conflicts is prioritized.

        for schedule in self._schedules:
            schedule.set_fitness()
        self._schedules.sort(key=methodcaller('get_numberofMinorConflicts'))  # sort on secondary key
        self._schedules.sort(key=methodcaller('get_fitness'), reverse=True)  # now sort on primary key, descending

    def __str__(self):
        tempstr = ""
        for i, schedule in enumerate(self.get_schedules()):
            tempstr += ("No. {}, Fitness: {}, Major Conflicts: {}, Minor Conflicts: {}\n".format(i, schedule.get_fitness(),
                                                                                     schedule.get_numberofMajorConflicts(),
                                                                                     schedule.get_numberofMinorConflicts()))
        return tempstr
