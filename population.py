from .config import Config
from .schedule import Schedule


class Population:
    def __init__(self, size):
        self._size = size
        self._data = Config.getInstance().get_data()
        self._schedules = []
        for _ in range(self._size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules
