from config import Config
from display import DisplayMgr
from geneticalgorithm import GeneticAlgorithm
from population import Population

config = Config()
display_manager = DisplayMgr()

population = Population(config.get_POPULATION_SIZE())
genAlgo = GeneticAlgorithm(config)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
# print(population)
generationCount = 1

while True:
    best_schedule = population.get_schedules()[0]
    best_schedule_fitness = best_schedule.get_fitness()
    if best_schedule_fitness >= 0.5:
        break
    genAlgo.evolve(population)
    # population = population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    generationCount += 1
    print(best_schedule_fitness)
display_manager.print_available_data()
display_manager.print_generation(population)
display_manager.print_schedules_as_table(best_schedule)
