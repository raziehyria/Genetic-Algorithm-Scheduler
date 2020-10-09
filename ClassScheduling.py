from config import Config
from geneticalgorithm import GeneticAlgorithm
from population import Population
from display.display import DisplayMgr


config = Config()
display_manager = DisplayMgr()

population = Population(config.get_POPULATION_SIZE())
genAlgo = GeneticAlgorithm(config)

# print(population)
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
    print("Generation #: {} - #Conflict: {} - Fitness: {} - No Change Count {}".format(generationCount, best_schedule.get_numberofConflicts(), best_schedule_fitness, no_change_count))
display_manager.print_available_data(best_schedule)
display_manager.print_generation(population)
display_manager.print_schedules_as_table(best_schedule)
