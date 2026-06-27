"""
population.py

Represents a population of chromosomes used by the Genetic Algorithm.
"""

import random

from models.chromosome import Chromosome


class Population:

    def __init__(self):
        self.chromosomes = []

    def initialize(
        self,
        goods_count,
        truck_count,
        population_size,
    ):
        """
        Creates the initial random population.
        """

        self.chromosomes.clear()

        warehouse_id = truck_count

        from config import POPULATION_SIZE

        for _ in range(population_size):

            truck_assignment = [
                random.randint(0, warehouse_id)
                for _ in range(goods_count)
            ]

            priorities = random.sample(
                range(1, goods_count + 1),
                goods_count
            )

            chromosome = Chromosome(
                truck_assignment=truck_assignment,
                priorities=priorities
            )

            self.chromosomes.append(chromosome)

    def best(self):
        """
        Returns chromosome with highest fitness.
        """

        return max(
            self.chromosomes,
            key=lambda chromosome: chromosome.fitness
        )

    def sort(self):
        """
        Sort chromosomes by descending fitness.
        """

        self.chromosomes.sort(
            key=lambda chromosome: chromosome.fitness,
            reverse=True
        )

    def add(self, chromosome):
        self.chromosomes.append(chromosome)

    def clear(self):
        self.chromosomes.clear()

    def __len__(self):
        return len(self.chromosomes)

    def __iter__(self):
        return iter(self.chromosomes)