from cs.config import Config
from cs.geneticalgorithm import GeneticAlgorithm
from cs.population import Population

config = Config()

population = Population(config.get_POPULATION_SIZE())
genAlgo = GeneticAlgorithm(config)
# population.get_schedules().sort(key=lambda  x: x.get_fitness(), reverse=True)
# print(population)
generationCount = 1

while True:
    fitness = population.get_schedules()[0].get_fitness()
    if fitness >= 0.5:
        break
    genAlgo.evlove(population)
    # population = population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    generationCount += 1
    print(fitness)
print(generationCount)
