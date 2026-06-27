"""
fitness.py

Fitness evaluation for the Genetic Algorithm.

The objective is to maximize daily company profit.
"""

from config import (
    WAREHOUSE_CITY,
    BASE_REVENUE_PER_KG_KM
)


class FitnessCalculator:

    def __init__(self, goods, trucks, routes):

        self.goods = goods
        self.trucks = trucks
        self.routes = routes

    # =====================================================
    # PUBLIC
    # =====================================================

    def calculate(self, chromosome):

        total_profit = 0

        truck_loads = self._group_goods_by_truck(chromosome)

        for truck_index, item_indices in truck_loads.items():

            if len(item_indices) == 0:
                continue

            if truck_index >= len(self.trucks):
                total_profit += self._warehouse_penalty(item_indices)
            else:
                total_profit += self._truck_profit(
                    truck_index,
                    item_indices,
                    chromosome
                )

        chromosome.fitness = total_profit

        return total_profit

    # =====================================================
    # PRIVATE
    # =====================================================

    def _group_goods_by_truck(self, chromosome):

        grouped = {}

        for truck_id in range(len(self.trucks) + 1):
            grouped[truck_id] = []

        for index, truck_id in enumerate(chromosome.truck_assignment):
            grouped[truck_id].append(index)

        return grouped

    # -----------------------------------------------------

    def _warehouse_penalty(self, item_indices):

        penalty = 0

        for index in item_indices:

            item = self.goods[index]

            penalty -= (item.days_waiting + 1) * 25000

        return penalty

    # -----------------------------------------------------

    def _truck_profit(
        self,
        truck_index,
        item_indices,
        chromosome
    ):

        truck = self.trucks[truck_index]

        ordered_indices = sorted(
            item_indices,
            key=lambda idx: chromosome.priorities[idx]
        )

        total_weight = 0
        total_volume = 0

        revenue = 0
        distance = 0
        toll = 0

        current_city = WAREHOUSE_CITY

        for idx in ordered_indices:

            item = self.goods[idx]

            origin_distance = self.routes[
                WAREHOUSE_CITY
            ][
                item.destination_city
            ]["distance"]

            revenue += (
                item.weight_kg
                * origin_distance
                * item.dimension_multiplier
                * BASE_REVENUE_PER_KG_KM
            )

            # distance += self.routes[
            #     current_city
            # ][
            #     item.destination_city
            # ]["distance"]

            # toll += self.routes[
            #     current_city
            # ][
            #     item.destination_city
            # ]["toll"]

            # current_city = item.destination_city

            # If already in the destination city,
            # there is no travel cost.

            if current_city != item.destination_city:

                distance += self.routes[current_city][item.destination_city]["distance"]

                toll += self.routes[current_city][item.destination_city]["toll"]

            current_city = item.destination_city

            # ---------

            total_weight += item.weight_kg
            total_volume += item.volume_m3

        # distance += self.routes[
        #     current_city
        # ][
        #     WAREHOUSE_CITY
        # ]["distance"]

        # toll += self.routes[
        #     current_city
        # ][
        #     WAREHOUSE_CITY
        # ]["toll"]

        if current_city != WAREHOUSE_CITY:

            distance += self.routes[current_city][WAREHOUSE_CITY]["distance"]

            toll += self.routes[current_city][WAREHOUSE_CITY]["toll"]

        # ------------

        operating_cost = (
            distance
            * truck.operating_cost_per_km
        )

        total_cost = operating_cost + toll

        profit = revenue - total_cost

        if (
            total_weight > truck.max_weight_kg
            or
            total_volume > truck.max_volume_m3
        ):
            profit *= 0.1

        return profit