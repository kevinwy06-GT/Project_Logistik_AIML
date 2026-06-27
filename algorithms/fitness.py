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

                total_profit += truck_result["profit"]

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

            if current_city != item.destination_city:

                distance += self.routes[current_city][item.destination_city]["distance"]

                toll += self.routes[current_city][item.destination_city]["toll"]

            current_city = item.destination_city

            total_weight += item.weight_kg
            total_volume += item.volume_m3


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
    
        return {

            "profit": profit,

            "revenue": revenue,

            "distance": distance,

            "toll": toll,

            "operating_cost": operating_cost,

            "weight": total_weight,

            "volume": total_volume

        }
    

    # =====================================================
    # PUBLIC SUMMARY
    # =====================================================

    def build_summary(self, chromosome):
        """
        Build a detailed summary of the optimization result.
        This does NOT change the fitness calculation.
        """

        summary = {
            "total_distance": 0.0,
            "total_operating_cost": 0.0,
            "total_toll_cost": 0.0,
            "total_revenue": 0.0,
            "net_profit": 0.0,
            "truck_utilization": {},
            "truck_distance": {},
            "truck_profit": {},
            "truck_weight": {},
            "truck_volume": {},
        }

        truck_loads = self._group_goods_by_truck(chromosome)

        for truck_index, item_indices in truck_loads.items():

            if truck_index >= len(self.trucks):
                continue

            truck = self.trucks[truck_index]

            total_weight = 0
            total_volume = 0

            for idx in item_indices:

                item = self.goods[idx]

                total_weight += item.weight_kg
                total_volume += item.volume_m3

            utilization = (
                total_weight / truck.max_weight_kg
                if truck.max_weight_kg > 0
                else 0
            )

            summary["truck_utilization"][truck.truck_id] = round(
                utilization * 100,
                2,
            )

            summary["truck_weight"][truck.truck_id] = total_weight

            summary["truck_volume"][truck.truck_id] = total_volume

        return summary
