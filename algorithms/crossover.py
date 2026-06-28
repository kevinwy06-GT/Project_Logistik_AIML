"""
crossover.py

Crossover operators for the Genetic Algorithm.
"""

import random

from models.chromosome import Chromosome


class Crossover:

    @staticmethod
    def crossover(parent1, parent2):
        """
        Performs crossover between two chromosomes.

        Returns:
            child1, child2
        """

        goods_count = len(parent1.truck_assignment)

        # ----------------------------------------------------
        # Choose two crossover points
        # ----------------------------------------------------

        point1 = random.randint(1, goods_count - 2)
        point2 = random.randint(point1 + 1, goods_count - 1)

        # ====================================================
        # PART A
        # Truck Assignment
        # Two Point Crossover
        # ====================================================

        child1_assignment = (
            parent1.truck_assignment[:point1]
            + parent2.truck_assignment[point1:point2]
            + parent1.truck_assignment[point2:]
        )

        child2_assignment = (
            parent2.truck_assignment[:point1]
            + parent1.truck_assignment[point1:point2]
            + parent2.truck_assignment[point2:]
        )

        # ====================================================
        # PART B
        # Priority
        # Ordered Crossover (OX)
        # ====================================================

        child1_priority = Crossover.__ordered_crossover(
            parent1.priorities,
            parent2.priorities,
            point1,
            point2
        )

        child2_priority = Crossover.__ordered_crossover(
            parent2.priorities,
            parent1.priorities,
            point1,
            point2
        )

        child1 = Chromosome(
            truck_assignment=child1_assignment,
            priorities=child1_priority
        )

        child2 = Chromosome(
            truck_assignment=child2_assignment,
            priorities=child2_priority
        )

        return child1, child2

    # @staticmethod
    # def __ordered_crossover(parent_main,
    #                         parent_donor,
    #                         start,
    #                         end):
    #     """
    #     Ordered Crossover (OX).

    #     Used only for priority permutation.
    #     """

    #     size = len(parent_main)

    #     child = [None] * size

    #     # Copy middle segment
    #     child[start:end] = parent_main[start:end]

    #     current_position = end

    #     for gene in parent_donor:

    #         if gene not in child:

    #             if current_position >= size:
    #                 current_position = 0

    #             while child[current_position] is not None:

    #                 current_position += 1

    #                 if current_position >= size:
    #                     current_position = 0

    #             child[current_position] = gene

    #     return child
    
    @staticmethod
    def __ordered_crossover(parent_main, parent_donor, start, end):
        size = len(parent_main)
        child = [None] * size

        child[start:end] = parent_main[start:end]
        
        used_genes = set(parent_main[start:end])

        current_position = 0

        for gene in parent_donor:
            if gene not in used_genes:
                
                while current_position < size and child[current_position] is not None:
                    current_position += 1
                
                if current_position < size:
                    child[current_position] = gene
                    used_genes.add(gene)

        return child

