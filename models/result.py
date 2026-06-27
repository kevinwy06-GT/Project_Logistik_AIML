"""
result.py

Stores the complete optimization result that will be displayed
by the Streamlit dashboard.
"""

from dataclasses import dataclass, field


@dataclass
class OptimizationResult:

    # ===============================
    # Genetic Algorithm
    # ===============================

    best_chromosome: object = None

    fitness_history: list = field(default_factory=list)

    generations: int = 0

    # ===============================
    # Allocation
    # ===============================

    truck_assignments: dict = field(default_factory=dict)

    rejected_goods: list = field(default_factory=list)

    # ===============================
    # Routing
    # ===============================

    routes: dict = field(default_factory=dict)

    # ===============================
    # Financial Summary
    # ===============================

    total_revenue: float = 0

    total_operating_cost: float = 0

    total_toll: float = 0

    net_profit: float = 0

    # ===============================
    # Statistics
    # ===============================

    total_distance: float = 0

    truck_utilization: dict = field(default_factory=dict)