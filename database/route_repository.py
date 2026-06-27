from sqlalchemy import text

from database.connection import get_session


class RouteRepository:

    def get_route_matrix(self):

        session = get_session()

        try:

            query = text("""
                SELECT *
                FROM route_matrix
            """)

            result = session.execute(query)

            routes = {}

            for row in result.mappings():

                origin = row["origin_city"]
                destination = row["destination_city"]

                if origin not in routes:
                    routes[origin] = {}

                routes[origin][destination] = {
                    "distance": float(row["distance_km"]),
                    "toll": float(row["toll_fee"])
                }

            return routes

        finally:
            session.close()