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
            self._FILE_PATH = input("Please provide the full path to the input excel file:\n")
            self._POPULATION_SIZE = 23
            self._NUM_OF_ELITE_SCHEDULES = 2
            self._MUTATION_RATE = 0.002  #originally at 0.1
            self._TOURNAMENT_SELECTION_SIZE = 7
            self._MAX_ITERATION = 2000
            self._data = Data(self._FILE_PATH)
            Config.__singletonConfig = self

    def get_POPULATION_SIZE(self):
        return self._POPULATION_SIZE

    def get_NUM_OF_ELITE_SCHEDULES(self):
        return self._NUM_OF_ELITE_SCHEDULES

    def get_MUTATION_RATE(self):
        return self._MUTATION_RATE

    def get_TOURNAMENT_SELECTION_SIZE(self):
        return self._TOURNAMENT_SELECTION_SIZE

    def get_MAX_ITERATION(self):
        return self._MAX_ITERATION

    def get_data(self):
        return self._data
