"""
truck.py

Represents one truck in the fleet.
"""

from dataclasses import dataclass


@dataclass
class Truck:
    truck_id: str
    license_plate: str
    max_weight_kg: float
    max_volume_m3: float
    fuel_cost_per_km: float
    maint_cost_per_km: float

    @property
    def operating_cost_per_km(self) -> float:
        """
        Fuel + maintenance cost.
        """

        return self.fuel_cost_per_km + self.maint_cost_per_km