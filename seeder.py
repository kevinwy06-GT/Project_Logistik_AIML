import pandas as pd
from sqlalchemy import create_engine, text
import random

# ==========================================
# 1. KONFIGURASI KONEKSI DATABASE
# ==========================================
# Format: mysql+pymysql://username:password@host:port/nama_database
# Jika MySQL Anda ada passwordnya, ubah root:@localhost menjadi root:passwordAnda@localhost
DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/db_logistik'
engine = create_engine(DATABASE_URI)

print("⏳ Menghubungkan ke database dan menyiapkan data...")

# ==========================================
# 2. DATA MATRIX (Jarak & Tol)
# ==========================================
dist_matrix = {
    'Surabaya': {'Surabaya': 0, 'Malang': 93, 'Kediri': 118, 'Probolinggo': 102, 'Madiun': 162, 'Blitar': 161, 'Pasuruan': 65, 'Mojokerto': 52, 'Batu': 105, 'Jember': 198, 'Banyuwangi': 305, 'Tuban': 98},
    'Malang': {'Surabaya': 93, 'Malang': 0, 'Kediri': 105, 'Probolinggo': 110, 'Madiun': 230, 'Blitar': 80, 'Pasuruan': 52, 'Mojokerto': 115, 'Batu': 18, 'Jember': 202, 'Banyuwangi': 308, 'Tuban': 195},
    'Kediri': {'Surabaya': 118, 'Malang': 105, 'Kediri': 0, 'Probolinggo': 200, 'Madiun': 88, 'Blitar': 42, 'Pasuruan': 165, 'Mojokerto': 78, 'Batu': 85, 'Jember': 260, 'Banyuwangi': 390, 'Tuban': 110},
    'Probolinggo': {'Surabaya': 102, 'Malang': 110, 'Kediri': 200, 'Probolinggo': 0, 'Madiun': 245, 'Blitar': 185, 'Pasuruan': 42, 'Mojokerto': 130, 'Batu': 120, 'Jember': 96, 'Banyuwangi': 188, 'Tuban': 210},
    'Madiun': {'Surabaya': 162, 'Malang': 230, 'Kediri': 88, 'Probolinggo': 245, 'Madiun': 0, 'Blitar': 130, 'Pasuruan': 205, 'Mojokerto': 110, 'Batu': 160, 'Jember': 335, 'Banyuwangi': 460, 'Tuban': 112},
    'Blitar': {'Surabaya': 161, 'Malang': 80, 'Kediri': 42, 'Probolinggo': 185, 'Madiun': 130, 'Blitar': 0, 'Pasuruan': 125, 'Mojokerto': 95, 'Batu': 75, 'Jember': 220, 'Banyuwangi': 315, 'Tuban': 205},
    'Pasuruan': {'Surabaya': 65, 'Malang': 52, 'Kediri': 165, 'Probolinggo': 42, 'Madiun': 205, 'Blitar': 125, 'Pasuruan': 0, 'Mojokerto': 92, 'Batu': 68, 'Jember': 138, 'Banyuwangi': 230, 'Tuban': 170},
    'Mojokerto': {'Surabaya': 52, 'Malang': 115, 'Kediri': 78, 'Probolinggo': 130, 'Madiun': 110, 'Blitar': 95, 'Pasuruan': 92, 'Mojokerto': 0, 'Batu': 62, 'Jember': 225, 'Banyuwangi': 320, 'Tuban': 95},
    'Batu': {'Surabaya': 105, 'Malang': 18, 'Kediri': 85, 'Probolinggo': 120, 'Madiun': 160, 'Blitar': 75, 'Pasuruan': 68, 'Mojokerto': 62, 'Batu': 0, 'Jember': 215, 'Banyuwangi': 310, 'Tuban': 155},
    'Jember': {'Surabaya': 198, 'Malang': 202, 'Kediri': 260, 'Probolinggo': 96, 'Madiun': 335, 'Blitar': 220, 'Pasuruan': 138, 'Mojokerto': 225, 'Batu': 215, 'Jember': 0, 'Banyuwangi': 92, 'Tuban': 305},
    'Banyuwangi': {'Surabaya': 305, 'Malang': 308, 'Kediri': 390, 'Probolinggo': 188, 'Madiun': 460, 'Blitar': 315, 'Pasuruan': 230, 'Mojokerto': 320, 'Batu': 310, 'Jember': 92, 'Banyuwangi': 0, 'Tuban': 402},
    'Tuban': {'Surabaya': 98, 'Malang': 195, 'Kediri': 110, 'Probolinggo': 210, 'Madiun': 112, 'Blitar': 205, 'Pasuruan': 170, 'Mojokerto': 95, 'Batu': 155, 'Jember': 305, 'Banyuwangi': 402, 'Tuban': 0}
}

toll_matrix = {
    'Surabaya': {'Malang': 71000, 'Madiun': 185000, 'Probolinggo': 149000, 'Kediri': 125000, 'Mojokerto': 64500, 'Pasuruan': 40000},
    'Malang': {'Surabaya': 71000, 'Probolinggo': 85000},
    'Madiun': {'Surabaya': 185000, 'Kediri': 45000},
    'Probolinggo': {'Surabaya': 149000, 'Jember': 0},
    'Kediri': {'Surabaya': 125000, 'Madiun': 45000},
    'Mojokerto': {'Surabaya': 64500, 'Madiun': 120000}
}

# Flatten dictionary menjadi list untuk DataFrame
route_data = []
for origin, destinations in dist_matrix.items():
    for dest, dist in destinations.items():
        if origin == dest:
            continue # Abaikan jarak kota ke dirinya sendiri
            
        toll_fee = toll_matrix.get(origin, {}).get(dest, 0)
        route_data.append({
            'origin_city': origin,
            'destination_city': dest,
            'distance_km': dist,
            'toll_fee': toll_fee
        })

df_routes = pd.DataFrame(route_data)

# ==========================================
# 3. DATA ARMADA TRUK (Berdasarkan Konstanta)
# ==========================================
truck_data = []
for i in range(1, 5): # 4 Truk
    truck_data.append({
        'truck_id': f'TRK-0{i}',
        'license_plate': f'L {1000+i} AB',
        'max_weight_kg': 4000.00,
        'max_volume_m3': 14.00,
        'fuel_cost_per_km': 1200.00,
        'maint_cost_per_km': 1300.00
    })

df_trucks = pd.DataFrame(truck_data)

# ==========================================
# 4. DATA ANTREAN BARANG RANDOM (30 Items)
# ==========================================
CITIES = ['Malang', 'Kediri', 'Madiun', 'Jember', 'Banyuwangi', 'Probolinggo', 'Tuban', 'Blitar', 'Pasuruan', 'Mojokerto', 'Batu']
DUMMY_NAMES = ['Pupuk Urea', 'Suku Cadang', 'Beras Bulog', 'Semen Gresik', 'Minyak Goreng', 'Kardus Indomie', 'Besi Beton', 'Cat Tembok', 'Kabel Roll', 'Pipa PVC', 'Kain Tekstil', 'Keramik']

items_data = []
for i in range(1, 31):
    items_data.append({
        'item_id': f'B{i:02}',
        'item_name': random.choice(DUMMY_NAMES),
        'destination_city': random.choice(CITIES),
        'weight_kg': random.randint(50, 450),
        'volume_m3': random.randint(1, 4),
        'dimension_type': random.choice(['S', 'M', 'L']),
        'days_waiting': random.randint(0, 2),
        'status': 'Pending'
    })

df_items = pd.DataFrame(items_data)

# ==========================================
# 5. EKSEKUSI INSERT KE MYSQL
# ==========================================
try:
    with engine.begin() as conn:
        # Hapus data lama agar tidak duplikat jika script dijalankan ulang berkali-kali
        conn.execute(text("DELETE FROM route_matrix"))
        conn.execute(text("DELETE FROM truck_fleet"))
        conn.execute(text("DELETE FROM daily_goods_queue"))
        
        # Insert data baru
        df_routes.to_sql('route_matrix', con=conn, if_exists='append', index=False)
        df_trucks.to_sql('truck_fleet', con=conn, if_exists='append', index=False)
        df_items.to_sql('daily_goods_queue', con=conn, if_exists='append', index=False)
        
    print("✅ BERHASIL! Semua data master dan antrean barang telah dimasukkan ke database.")
except Exception as e:
    print(f"❌ TERJADI KESALAHAN: {e}")