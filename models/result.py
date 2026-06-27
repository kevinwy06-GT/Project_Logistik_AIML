"""
result.py

Stores the complete optimization result.
"""

from dataclasses import dataclass, field


@dataclass
class OptimizationResult:

    # ==================================================
    # Genetic Algorithm
    # ==================================================

    best_chromosome: object = None

    fitness_history: list = field(default_factory=list)

    generations: int = 0

    # ==================================================
    # Assignment
    # ==================================================

    truck_assignments: dict = field(default_factory=dict)

    rejected_goods: list = field(default_factory=list)

    routes: dict = field(default_factory=dict)

    # ==================================================
    # Financial Information
    # ==================================================

    total_revenue: float = 0.0

    total_operating_cost: float = 0.0

    total_toll_cost: float = 0.0

    total_distance: float = 0.0

    net_profit: float = 0.0

    # ==================================================
    # Truck Statistics
    # ==================================================

    truck_utilization: dict = field(default_factory=dict)

    truck_distance: dict = field(default_factory=dict)

    truck_profit: dict = field(default_factory=dict)

    truck_weight: dict = field(default_factory=dict)

    truck_volume: dict = field(default_factory=dict)

    # ==================================================
    # Simulated Annealing
    # ==================================================

    before_sa_distance: float = 0.0

    after_sa_distance: float = 0.0

    distance_saved: float = 0.0
