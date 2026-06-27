from database.goods_repository import GoodsRepository
from database.truck_repository import TruckRepository
from database.route_repository import RouteRepository

goods = GoodsRepository().get_all_goods()
trucks = TruckRepository().get_all_trucks()
routes = RouteRepository().get_route_matrix()

print("========== FIRST GOODS ==========")
print(goods[0])

print()
print(goods[0].item_name)
print(goods[0].weight_kg)
print(goods[0].destination_city)

print()

print("========== FIRST TRUCK ==========")
print(trucks[0])

print()
print(trucks[0].truck_id)
print(trucks[0].operating_cost_per_km)

print()

print(routes["Surabaya"]["Malang"])