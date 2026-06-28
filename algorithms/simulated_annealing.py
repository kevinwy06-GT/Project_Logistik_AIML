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
    DEFAULT_INITIAL_TEMPERATURE,
    DEFAULT_MIN_TEMPERATURE,
    DEFAULT_MAX_SA_ITERATIONS,
    WAREHOUSE_CITY,
)


class SimulatedAnnealing:

    def __init__(
        self,
        routes,
        cooling_rate,
    ):
        self.routes = routes
        self.cooling_rate = cooling_rate

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

        temperature = DEFAULT_INITIAL_TEMPERATURE

        while (
            temperature > DEFAULT_MIN_TEMPERATURE
        ):

            for _ in range(DEFAULT_MAX_SA_ITERATIONS):

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

            temperature *= self.cooling_rate

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
    
    # =====================================================
    # ANALYSIS
    # =====================================================

    def analyze(self, route):
        """
        Runs SA and returns both the original
        and optimized route information.
        """

        before_distance = self.route_distance(route)

        optimized_route = self.optimize(route)

        after_distance = self.route_distance(
            optimized_route
        )

        return {
            "original_route": route,
            "optimized_route": optimized_route,
            "before_distance": before_distance,
            "after_distance": after_distance,
            "distance_saved": before_distance - after_distance,
        }