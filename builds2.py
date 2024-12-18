import pandas as pd

# 30 farklı bina kategorisi ve puanlama
building_categories = [
    {"Kategori": "Hastane", "Puan": 30},
    {"Kategori": "Alışveriş Merkezi", "Puan": 29},
    {"Kategori": "Okul", "Puan": 28},
    {"Kategori": "Polis Merkezi", "Puan": 27},
    {"Kategori": "İtfaiye Binası", "Puan": 26},
    {"Kategori": "Havalimanı", "Puan": 25},
    {"Kategori": "Üniversite Kampüsü", "Puan": 24},
    {"Kategori": "Otogar", "Puan": 23},
    {"Kategori": "Metro İstasyonu", "Puan": 22},
    {"Kategori": "Stadyum", "Puan": 21},
    {"Kategori": "Sanayi Tesisi", "Puan": 20},
    {"Kategori": "Enerji Santrali", "Puan": 19},
    {"Kategori": "Otel", "Puan": 18},
    {"Kategori": "Belediye Binası", "Puan": 17},
    {"Kategori": "Toplu Konut Bloğu", "Puan": 16},
    {"Kategori": "Apartman", "Puan": 15},
    {"Kategori": "Hükümet Binası", "Puan": 14},
    {"Kategori": "Tren İstasyonu", "Puan": 13},
    {"Kategori": "Kütüphane", "Puan": 12},
    {"Kategori": "Kültür Merkezi", "Puan": 11},
    {"Kategori": "Altyapı Deposu", "Puan": 10},
    {"Kategori": "Kilise veya Cami", "Puan": 9},
    {"Kategori": "Sosyal Tesis", "Puan": 8},
    {"Kategori": "Fabrika", "Puan": 7},
    {"Kategori": "Küçük İşletme Binası", "Puan": 6},
    {"Kategori": "Ofis Binası", "Puan": 5},
    {"Kategori": "Köy Evi", "Puan": 4},
    {"Kategori": "Depo", "Puan": 3},
    {"Kategori": "Çiftlik Binası", "Puan": 2},
    {"Kategori": "Küçük Kulübe", "Puan": 1},
]

# Veriyi DataFrame'e aktarma
df_buildings = pd.DataFrame(building_categories)

# Bina kategorilerini büyüklüğüne göre 3 gruba ayırma
def categorize_building(score):
    if score >= 21:
        return "Büyük"
    elif 11 <= score <= 20:
        return "Orta"
    else:
        return "Küçük"

# Yeni kategori sütunu ekleme
df_buildings["Büyüklük"] = df_buildings["Puan"].apply(categorize_building)

import ace_tools as tools; tools.display_dataframe_to_user("Binalar ve Büyüklükleri", df_buildings)
