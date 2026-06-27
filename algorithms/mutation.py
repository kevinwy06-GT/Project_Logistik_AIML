"""
mutation.py

Mutation operators for the Genetic Algorithm.
"""

import random

from config import MUTATION_RATE


class Mutation:

    @staticmethod
    def mutate(chromosome, truck_count):
        """
        Applies mutation to a chromosome.
        """

        goods_count = len(chromosome.truck_assignment)

        warehouse_id = truck_count

        # -----------------------------------------
        # Truck Assignment Mutation
        # -----------------------------------------

        if random.random() < MUTATION_RATE:

            index = random.randint(
                0,
                goods_count - 1
            )

            chromosome.truck_assignment[index] = random.randint(
                0,
                warehouse_id
            )

        # -----------------------------------------
        # Priority Swap Mutation
        # -----------------------------------------

        if random.random() < MUTATION_RATE:

            i1, i2 = random.sample(
                range(goods_count),
                2
            )

            chromosome.priorities[i1], chromosome.priorities[i2] = (
                chromosome.priorities[i2],
                chromosome.priorities[i1]
            )

        return chromosome