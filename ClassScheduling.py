from datetime import datetime
from config import Config
from display.display import DisplayMgr
from geneticalgorithm import GeneticAlgorithm
from population import Population


class ClassScheduling:

    def start(self, cs_app):
        # getting all widgets from app class that are used here to update gui
        execution_stats_text = cs_app.execution_stats_text

        #  added the try-catch block because I was getting exception error from the Config class

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
            # check if stop button pressed
            if cs_app.stop_scheduling:
                break

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
            if cs_app.show_stats():     # if checkbox toggled then we show them
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
        execution_stats_text.see("end")
        execution_stats_text.update()
