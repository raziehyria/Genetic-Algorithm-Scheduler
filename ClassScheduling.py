import signal
import sys
from datetime import datetime

from config import Config
from display.display import DisplayMgr
from geneticalgorithm import GeneticAlgorithm
from population import Population


class ClassScheduling:

    #  added the try-catch block because I was getting exception error from the Config class

    def my_custom_handler(self, signum, stack_frame):
        print('CTRL+C was pressed.  Writing the best schedule so far and will exit the process...')
        self.display_manager.writeSchedule(self.best_schedule)
        sys.exit(0)

    def start(self, execution_stats_text):

        signal.signal(signal.SIGINT, self.my_custom_handler)

        try:
            config = Config()
        except Exception:
            config = Config.getInstance()

        start_time = datetime.now()

        self.display_manager = DisplayMgr()
        population = Population(config.get_POPULATION_SIZE())
        genAlgo = GeneticAlgorithm(config)

        population.sort_schedules()

        generationCount = 0
        no_change_count = 0
        prev_fitness = 0

        while no_change_count < config.get_MAX_ITERATION():
            self.best_schedule = population.get_schedules()[0]
            self.best_schedule_fitness = self.best_schedule.get_fitness()
            if self.best_schedule_fitness >= 0.5:
                break
            population = genAlgo.evolve(population)
            generationCount += 1
            if prev_fitness == self.best_schedule_fitness:
                no_change_count += 1
            else:
                no_change_count = 0
                prev_fitness = self.best_schedule_fitness

            time_since_start = datetime.now() - start_time
            # adding string formatting for pretty print: https://mkaz.blog/code/python-string-format-cookbook/
            stats = "Generation #: {: >4d} - # MajorConflict: {: >3d} - # MinorConflict: {: >3d} - No Change Count {: >4d} - Running for: {}".format(
                    generationCount,
                    self.best_schedule.get_numberofMajorConflicts(),
                    self.best_schedule.get_numberofMinorConflicts(),
                    no_change_count, time_since_start)
            execution_stats_text.insert("end", "\n" + stats)
            execution_stats_text.update()


        self.display_manager.writeSchedule(self.best_schedule)
        end_time = datetime.now()

        execution_stats_text.insert("end", "\n" + 'Total time = {}'.format(end_time - start_time))
