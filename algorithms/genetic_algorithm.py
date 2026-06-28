"""
genetic_algorithm.py

Main Genetic Algorithm engine.
"""

from config import (
    DEFAULT_ELITE_COUNT,
)

from models.population import Population
from models.result import OptimizationResult

from algorithms.selection import Selection
from algorithms.crossover import Crossover
from algorithms.mutation import Mutation
from algorithms.fitness import FitnessCalculator


class GeneticAlgorithm:

    def __init__(
        self,
        goods,
        trucks,
        routes,
        population_size,
        generations,
        mutation_rate,
    ):

        self.goods = goods
        self.trucks = trucks
        self.routes = routes

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_count = DEFAULT_ELITE_COUNT

        self.population = Population()

        self.fitness_calculator = FitnessCalculator(
            goods,
            trucks,
            routes
        )

    # ==========================================================
    # INITIALIZE
    # ==========================================================

    def initialize_population(self):

        self.population.initialize(
            goods_count=len(self.goods),
            truck_count=len(self.trucks),
            population_size=self.population_size,
        )

    # ==========================================================
    # FITNESS
    # ==========================================================

    def evaluate_population(self):

        for chromosome in self.population:
            self.fitness_calculator.calculate(chromosome)

    # ==========================================================
    # NEXT GENERATION
    # ==========================================================

    def create_next_generation(self):

        self.population.sort()

        new_population = Population()

        # ---------------------------------------
        # Elitism
        # ---------------------------------------

        for i in range(self.elite_count):
            new_population.add(
                self.population.chromosomes[i].copy()
            )

        # ---------------------------------------
        # Generate children
        # ---------------------------------------

        while len(new_population) < len(self.population):

            parent1 = Selection.roulette(self.population)
            parent2 = Selection.roulette(self.population)

            child1, child2 = Crossover.crossover(
                parent1,
                parent2
            )

            child1 = Mutation.mutate(
                child1,
                len(self.trucks),
                self.mutation_rate
            )

            child2 = Mutation.mutate(
                child2,
                len(self.trucks),
                self.mutation_rate
            )

            new_population.add(child1)

            if len(new_population) < len(self.population):
                new_population.add(child2)

        self.population = new_population

    # ==========================================================
    # RUN
    # ==========================================================

    def run(self):

        self.initialize_population()

        history = []

        for generation in range(self.generations):

            self.evaluate_population()

            best = self.population.best()

            history.append(best.fitness)

            if generation != self.generations - 1:
                self.create_next_generation()

        self.evaluate_population()

        best = self.population.best()

        result = OptimizationResult()

        result.best_chromosome = best.copy()

        result.generations = self.generations

        result.population_size = self.population_size

        result.mutation_rate = self.mutation_rate

        result.fitness_history = history

        result.truck_assignments = self._build_assignments(best)

        result.rejected_goods = self._build_rejected_goods(best)

        # =====================================================
        # Build Business Summary
        # =====================================================

        summary = self.fitness_calculator.build_summary(best)

        result.total_distance = summary["total_distance"]

        result.total_operating_cost = summary["total_operating_cost"]

        result.total_toll_cost = summary["total_toll_cost"]

        result.total_revenue = summary["total_revenue"]

        result.net_profit = summary["net_profit"]

        result.truck_utilization = summary["truck_utilization"]

        result.truck_distance = summary["truck_distance"]

        result.truck_profit = summary["truck_profit"]

        result.truck_weight = summary["truck_weight"]

        result.truck_volume = summary["truck_volume"]

        return result


    # ==========================================================
    # HELPERS
    # ==========================================================

    def _build_assignments(self, chromosome):

        assignments = {}

        for i in range(len(self.trucks)):
            assignments[f"Truck {i+1}"] = []

        for index, truck_id in enumerate(chromosome.truck_assignment):

            if truck_id >= len(self.trucks):
                continue

            assignments[f"Truck {truck_id+1}"].append(
                self.goods[index]
            )

        return assignments

    def _build_rejected_goods(self, chromosome):

        rejected = []

        for index, truck_id in enumerate(chromosome.truck_assignment):

            if truck_id >= len(self.trucks):
                rejected.append(
                    self.goods[index]
                )

        return rejected