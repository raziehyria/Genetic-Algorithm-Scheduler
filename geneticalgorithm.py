import random as rnd

from population import Population
from schedule import Schedule


class GeneticAlgorithm:

    def __init__(self, config):
        self._config = config

    def evolve(self, population):
        population = self._mutate_population(self._crossover_population(population))
        population.sort_schedules()
        return population

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(self._config.get_NUM_OF_ELITE_SCHEDULES()):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])

        i = self._config.get_NUM_OF_ELITE_SCHEDULES()

        while i < self._config.get_POPULATION_SIZE():
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1

        return crossover_pop

    def _mutate_population(self, population):
        for i in range(self._config.get_NUM_OF_ELITE_SCHEDULES(), self._config.get_POPULATION_SIZE()):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(len(crossoverSchedule.get_classes())):
            if rnd.random() >= 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]

        return crossoverSchedule

    def _mutate_schedule(self, schedule):
        newSchedule = Schedule().initialize()
        for i in range(len(schedule.get_classes())):
            if rnd.random() <= self._config.get_MUTATION_RATE():
                schedule.get_classes()[i] = newSchedule.get_classes()[i]
        return schedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)  # empty/clean schedule
        for _ in range(self._config.get_TOURNAMENT_SELECTION_SIZE()):
            tournament_pop.get_schedules().append(
                pop.get_schedules()[rnd.randrange(self._config.get_POPULATION_SIZE())])

        tournament_pop.sort_schedules()
        return tournament_pop
