"""
selection.py

Selection operators for the Genetic Algorithm.
"""

import random


class Selection:

    @staticmethod
    def roulette(population):
        """
        Roulette Wheel Selection.

        Returns one Chromosome.
        """

        scores = [
            chromosome.fitness
            for chromosome in population
        ]

        minimum = min(scores)

        shifted_scores = [
            score - minimum + 1
            for score in scores
        ]

        selected = random.choices(
            population.chromosomes,
            weights=shifted_scores,
            k=1
        )[0]

        return selected.copy()