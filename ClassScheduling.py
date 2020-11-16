import signal
import sys
from datetime import datetime

from config import Config
from display.display import DisplayMgr
from geneticalgorithm import GeneticAlgorithm
from population import Population


#  added the try-catch block because I was getting exception error from the Config class

def my_custom_handler(signum, stack_frame):
    print('CTRL+C was pressed.  Writing the best schedule so far and will exit the process...')
    display_manager.writeSchedule(best_schedule)
    sys.exit(0)


signal.signal(signal.SIGINT, my_custom_handler)

try:
    config = Config()
except Exception:
    config = Config.getInstance()

start_time = datetime.now()

display_manager = DisplayMgr()
population = Population(config.get_POPULATION_SIZE())
genAlgo = GeneticAlgorithm(config)

population.sort_schedules()

generationCount = 0
no_change_count = 0
prev_fitness = 0

while no_change_count < config.get_MAX_ITERATION():
    best_schedule = population.get_schedules()[0]
    best_schedule_fitness = best_schedule.get_fitness()
    if best_schedule_fitness >= 0.5:
        break
    population = genAlgo.evolve(population)
    generationCount += 1
    if prev_fitness == best_schedule_fitness:
        no_change_count += 1
    else:
        no_change_count = 0
        prev_fitness = best_schedule_fitness

    time_since_start = datetime.now() - start_time
    # adding string formatting for pretty print: https://mkaz.blog/code/python-string-format-cookbook/
    print(
        "Generation #: {: >4d} - # MajorConflict: {: >3d} - # MinorConflict: {: >3d} - No Change Count {: >4d} - Running for: {}".format(
            generationCount,
            best_schedule.get_numberofMajorConflicts(),
            best_schedule.get_numberofMinorConflicts(),
            no_change_count, time_since_start))

display_manager.writeSchedule(best_schedule)
end_time = datetime.now()

print('Total time = {}'.format(end_time - start_time))
