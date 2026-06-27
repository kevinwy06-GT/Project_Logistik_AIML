"""
chromosome.py

Represents one chromosome used by the Genetic Algorithm.
"""

from dataclasses import dataclass, field


@dataclass
class Chromosome:

    truck_assignment: list

    priorities: list

    fitness: float = field(default=0.0)

    def copy(self):
        """
        Returns a deep copy of this chromosome.
        """

        return Chromosome(
            truck_assignment=self.truck_assignment.copy(),
            priorities=self.priorities.copy(),
            fitness=self.fitness
        )

    @property
    def genes(self):
        """
        Returns the complete chromosome.
        """

        return self.truck_assignment + self.priorities