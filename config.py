from componentdata import Data


class Config:
    __singletonConfig = None

    """
    Singleton Implementation take from:
    https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
    """

    @staticmethod
    def getInstance():
        if Config.__singletonConfig is None:
            Config()
        return Config.__singletonConfig

    def __init__(self):
        if Config.__singletonConfig is not None:
            raise Exception("This is a singleton class, cannot instantiate")
        else:
            self._FILE_PATH = '../uploads/Course_list_and_attributes.xlsx'
            self._POPULATION_SIZE = 23
            self._NUM_OF_ELITE_SCHEDULES = 2
            self._MUTATION_RATE = 0.002  # originally at 0.1
            self._TOURNAMENT_SELECTION_SIZE = 7
            self._MAX_ITERATION = 600
            #  self._MAX_ITERATION = 1
            #  self._data = None
            self._data = Data(self._FILE_PATH)
            Config.__singletonConfig = self

    def get_POPULATION_SIZE(self):
        return self._POPULATION_SIZE

    def set_POPULATION_SIZE(self, size):
        self._POPULATION_SIZE = size

    def get_NUM_OF_ELITE_SCHEDULES(self):
        return self._NUM_OF_ELITE_SCHEDULES

    def set_NUM_OF_ELITE_SCHEDULES(self, num):
        self._NUM_OF_ELITE_SCHEDULES = num

    def get_MUTATION_RATE(self):
        return self._MUTATION_RATE

    def set_MUTATION_RATE(self, rate):
        self._MUTATION_RATE = rate

    def get_TOURNAMENT_SELECTION_SIZE(self):
        return self._TOURNAMENT_SELECTION_SIZE

    def set_TOURNAMENT_SELECTION_SIZE(self, size):
        self._TOURNAMENT_SELECTION_SIZE = size

    def get_MAX_ITERATION(self):
        return self._MAX_ITERATION

    def set_MAX_ITERATION(self, max_iteration):
        self._MAX_ITERATION = max_iteration

    def get_data(self):
        return self._data

    def set_FILE_PATH(self, path):
        self._FILE_PATH = path
        self._data = Data(self._FILE_PATH)

    def get_FILE_PATH(self):
        return self._FILE_PATH
