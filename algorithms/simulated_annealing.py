"""
simulated_annealing.py

Route optimization using Simulated Annealing.

This algorithm receives the best chromosome from the
Genetic Algorithm and improves the visiting order
for each truck.
"""

import copy
import math
import random

from config import (
    INITIAL_TEMPERATURE,
    COOLING_RATE,
    MIN_TEMPERATURE,
    MAX_SA_ITERATIONS,
    WAREHOUSE_CITY,
)


class SimulatedAnnealing:

    def __init__(self, routes):

        self.routes = routes

    # =====================================================
    # PUBLIC
    # =====================================================

    def optimize(self, route):

        """
        route example:

        [
            "Malang",
            "Jember",
            "Batu"
        ]
        """

        if len(route) <= 2:
            return route

        current_route = copy.deepcopy(route)

        best_route = copy.deepcopy(route)

        current_cost = self.route_distance(current_route)

        best_cost = current_cost

        temperature = INITIAL_TEMPERATURE

        while (
            temperature > MIN_TEMPERATURE
        ):

            for _ in range(MAX_SA_ITERATIONS):

                candidate = self.neighbor(current_route)

                candidate_cost = self.route_distance(candidate)

                delta = candidate_cost - current_cost

                if delta < 0:

                    current_route = candidate
                    current_cost = candidate_cost

                    if current_cost < best_cost:

                        best_route = copy.deepcopy(current_route)

                        best_cost = current_cost

                else:

                    probability = math.exp(
                        -delta / temperature
                    )

                    if random.random() < probability:

                        current_route = candidate

                        current_cost = candidate_cost

            temperature *= COOLING_RATE

        return best_route

    # =====================================================
    # PRIVATE
    # =====================================================

    def neighbor(self, route):

        """
        Creates a neighboring solution
        by swapping two cities.
        """

        candidate = copy.deepcopy(route)

        i, j = random.sample(
            range(len(candidate)),
            2
        )

        candidate[i], candidate[j] = (
            candidate[j],
            candidate[i]
        )

        return candidate

    def route_distance(self, route):

        """
        Calculates total travel distance.
        """

        total = 0

        current = WAREHOUSE_CITY

        for city in route:

            total += self.routes[
                current
            ][
                city
            ]["distance"]

            current = city

        total += self.routes[
            current
        ][
            WAREHOUSE_CITY
        ]["distance"]

        return total