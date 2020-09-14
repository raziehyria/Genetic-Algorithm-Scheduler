from cs.config import Config
from cs.geneticalgorithm import GeneticAlgorithm
from cs.population import Population

config = Config()

population = Population(config.get_POPULATION_SIZE())
genAlgo = GeneticAlgorithm(config)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
# print(population)
generationCount = 1

while True:
    best_schedule = population.get_schedules()[0]
    best_schedule_fitness = best_schedule.get_fitness()
    if best_schedule_fitness >= 0.5:
        print(best_schedule)
        break
    genAlgo.evolve(population)
    # population = population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    generationCount += 1
    print(best_schedule_fitness)
print(generationCount)
