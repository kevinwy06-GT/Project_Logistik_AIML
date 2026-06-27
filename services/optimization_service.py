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

        goods = self.goods_repository.get_all_goods()

        trucks = self.truck_repository.get_all_trucks()

        routes = self.route_repository.get_route_matrix()

        ga = GeneticAlgorithm(
            goods=goods,
            trucks=trucks,
            routes=routes,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
        )

        result = ga.run()

        sa = SimulatedAnnealing(
            routes=routes,
            cooling_rate=cooling_rate,
        )

        optimized_routes = {}

        for truck_name, assigned_goods in result.truck_assignments.items():

            cities = []

            seen = set()

            for item in assigned_goods:

                if item.destination_city not in seen:

                    seen.add(item.destination_city)
                    cities.append(item.destination_city)

            optimized_routes[truck_name] = sa.optimize(cities)

        result.routes = optimized_routes

        return result