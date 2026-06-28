from sqlalchemy import text

from database.connection import get_session
from models.truck import Truck

class TruckRepository:

    def get_all_trucks(self):

        session = get_session()

        try:

            query = text("""
                SELECT *
                FROM truck_fleet
                ORDER BY truck_id
            """)

            result = session.execute(query)

            trucks = []

            for row in result.mappings():

                trucks.append(
                    Truck(
                        truck_id=row["truck_id"],
                        license_plate=row["license_plate"],
                        max_weight_kg=float(row["max_weight_kg"]),
                        max_volume_m3=float(row["max_volume_m3"]),
                        fuel_cost_per_km=float(row["fuel_cost_per_km"]),
                        maint_cost_per_km=float(row["maint_cost_per_km"])
                    )
                )

            return trucks

        finally:
            session.close()

    def get_truck_by_id(self, truck_id):

        session = get_session()

        try:

            query = text("""
                SELECT *
                FROM truck_fleet
                WHERE truck_id = :truck_id
            """)

            result = session.execute(
                query,
                {
                    "truck_id": truck_id
                }
            ).mappings().first()

            if result is None:
                return None

            return Truck(
                truck_id=result["truck_id"],
                license_plate=result["license_plate"],
                max_weight_kg=float(result["max_weight_kg"]),
                max_volume_m3=float(result["max_volume_m3"]),
                fuel_cost_per_km=float(result["fuel_cost_per_km"]),
                maint_cost_per_km=float(result["maint_cost_per_km"]),
            )

        finally:
            session.close()


    def update_truck(
        self,
        truck_id,
        max_weight_kg,
        max_volume_m3,
        fuel_cost_per_km,
        maint_cost_per_km,
    ):

        session = get_session()

        try:

            query = text("""
                UPDATE truck_fleet
                SET
                    max_weight_kg = :max_weight_kg,
                    max_volume_m3 = :max_volume_m3,
                    fuel_cost_per_km = :fuel_cost_per_km,
                    maint_cost_per_km = :maint_cost_per_km
                WHERE
                    truck_id = :truck_id
            """)

            session.execute(
                query,
                {
                    "truck_id": truck_id,
                    "max_weight_kg": max_weight_kg,
                    "max_volume_m3": max_volume_m3,
                    "fuel_cost_per_km": fuel_cost_per_km,
                    "maint_cost_per_km": maint_cost_per_km,
                }
            )

            session.commit()

        finally:
            session.close()