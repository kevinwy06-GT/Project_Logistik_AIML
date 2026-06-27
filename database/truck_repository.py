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