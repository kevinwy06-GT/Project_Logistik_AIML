"""
goods.py

Represents one item waiting to be transported.
"""

from dataclasses import dataclass


@dataclass
class Goods:
    item_id: str
    item_name: str
    destination_city: str
    weight_kg: float
    volume_m3: float
    dimension_type: str
    days_waiting: int
    status: str

    @property
    def dimension_multiplier(self) -> float:
        """
        Returns multiplier based on package size.
        """

        mapping = {
            "S": 1.0,
            "M": 1.2,
            "L": 1.5
        }

        return mapping[self.dimension_type]