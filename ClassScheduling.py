import requests
from datetime import datetime
from threading import Thread

from config import Config
from display.display import DisplayMgr
from geneticalgorithm import GeneticAlgorithm
from population import Population
from threading import Timer


class ClassScheduling:

    def __init__(self):
        #  added the try-catch block because I was getting exception error from the Config class
        try:
            self.config = Config()
        except Exception:
            self.config = Config.getInstance()


    def stop(self):
        requests.get('http://localhost:5000/stop')

    def start(self):
        # getting all widgets from app class that are used here to update gui
        start_time = datetime.now()
        self.progress_percent = 0

        self.display_manager = DisplayMgr()
        population = Population(self.config.get_POPULATION_SIZE())
        genAlgo = GeneticAlgorithm(self.config)

        population.sort_schedules()

        generationCount = 0
        no_change_count = 0
        prev_fitness = 0

        highest_no_change_count = 0

        is_running = True
        while no_change_count < self.config.get_MAX_ITERATION() and is_running is True:
            if no_change_count > highest_no_change_count:
                highest_no_change_count = no_change_count

            self.progress_percent = round((highest_no_change_count / self.config.get_MAX_ITERATION()) * 100)

            # Checks the `is_running` value in flask's app.py
            # The website user sets `is_running` to false with the frontend stop button
            r = requests.get('http://localhost:5000/is_running_status', headers=headers)
            is_running = r.json().get('is_running')

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

            # If the looping is done
            if no_change_count >= self.config.get_MAX_ITERATION():
                self.progress_percent = 0


            time_since_start = datetime.now() - start_time
            # adding string formatting for pretty print: https://mkaz.blog/code/python-string-format-cookbook/

        self.display_manager.writeSchedule(self.best_schedule)
        end_time = datetime.now()

        closing_remarks = "\nTotal execution time = {}.".format(end_time - start_time)
        closing_remarks += "\nResults generated, look for the 'schedule.xlsx' file in your specified \noutput directory.\n"
        closing_remarks += "\nPlease close this window to quit. Thanks!"
