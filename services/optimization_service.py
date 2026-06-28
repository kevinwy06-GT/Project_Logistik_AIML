"""
optimization_service.py

Coordinates the complete optimization workflow.

Flow:
Database
    ↓
Genetic Algorithm
    ↓
Simulated Annealing
    ↓
Optimization Result
"""

from database.goods_repository import GoodsRepository
from database.truck_repository import TruckRepository
from database.route_repository import RouteRepository

from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealing


class OptimizationService:

    def __init__(self):

        self.goods_repository = GoodsRepository()
        self.truck_repository = TruckRepository()
        self.route_repository = RouteRepository()

    def optimize(
        self,
        population_size,
        generations,
        mutation_rate,
        cooling_rate,
    ):

        # =====================================================
        # Load data
        # =====================================================

        goods = self.goods_repository.get_all_goods()

        trucks = self.truck_repository.get_all_trucks()

        routes = self.route_repository.get_route_matrix()

        # =====================================================
        # Run Genetic Algorithm
        # =====================================================

        ga = GeneticAlgorithm(
            goods=goods,
            trucks=trucks,
            routes=routes,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
        )

        result = ga.run()

        result.cooling_rate = cooling_rate

        # =====================================================
        # Run Simulated Annealing
        # =====================================================

        sa = SimulatedAnnealing(
            routes=routes,
            cooling_rate=cooling_rate,
        )

        optimized_routes = {}

        total_before_distance = 0.0
        total_after_distance = 0.0

        for truck_name, assigned_goods in result.truck_assignments.items():

            cities = []
            seen = set()

            for item in assigned_goods:

                if item.destination_city not in seen:

                    seen.add(item.destination_city)
                    cities.append(item.destination_city)

            analysis = sa.analyze(cities)

            optimized_routes[truck_name] = analysis["optimized_route"]

            total_before_distance += analysis["before_distance"]
            total_after_distance += analysis["after_distance"]

        # =====================================================
        # Store SA Results
        # =====================================================

        result.routes = optimized_routes

        result.before_sa_distance = total_before_distance
        result.after_sa_distance = total_after_distance
        result.distance_saved = (
            total_before_distance
            - total_after_distance
        )

        return result
