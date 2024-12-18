import pandas as pd
import numpy as np

# Veriyi yükleme
categories = [
    {"Kategori": "Bilinçsiz ve Kalp Durması", "Puan": 30},
    {"Kategori": "Ağır İç Kanama", "Puan": 29},
    {"Kategori": "Açık Kafa Travması", "Puan": 28},
    {"Kategori": "Nefes Darlığı (Akut)", "Puan": 27},
    {"Kategori": "Omurilik Yaralanması", "Puan": 26},
    {"Kategori": "Ağır Yanıklar (3. Derece)", "Puan": 25},
    {"Kategori": "Ampute Uzuv", "Puan": 24},
    {"Kategori": "Göğüs Delici Yaralanma", "Puan": 23},
    {"Kategori": "Karın Delici Yaralanma", "Puan": 22},
    {"Kategori": "Ağır Kemik Kırıkları", "Puan": 21},
    {"Kategori": "Travmatik Şok", "Puan": 20},
    {"Kategori": "Bilinç Bulanıklığı", "Puan": 19},
    {"Kategori": "Kan Kaybı (Orta Derece)", "Puan": 18},
    {"Kategori": "Ağır Solunum Problemi", "Puan": 17},
    {"Kategori": "Orta Derece Yanıklar", "Puan": 16},
    {"Kategori": "Kol veya Bacak Kırığı", "Puan": 15},
    {"Kategori": "Kas Zedelenmesi", "Puan": 14},
    {"Kategori": "Yüzeyel Kesikler", "Puan": 13},
    {"Kategori": "Bilinçsiz, Kalp Atışı Var", "Puan": 12},
    {"Kategori": "Burun Kanaması", "Puan": 11},
    {"Kategori": "Kafa Travması (Hafif)", "Puan": 10},
    {"Kategori": "Nefes Darlığı (Hafif)", "Puan": 9},
    {"Kategori": "Doku Zedelenmesi", "Puan": 8},
    {"Kategori": "Orta Derece Kanama", "Puan": 7},
    {"Kategori": "Aşırı Yorgunluk", "Puan": 6},
    {"Kategori": "Hafif Yanıklar", "Puan": 5},
    {"Kategori": "Morarma", "Puan": 4},
    {"Kategori": "Kas Çekmesi", "Puan": 3},
    {"Kategori": "Hafif Sıyrıklar", "Puan": 2},
    {"Kategori": "Psikolojik Şok", "Puan": 1},
]

df_categories = pd.DataFrame(categories)

# Ağırlıkları belirleme
def categorize(score):
    if score >= 21:
        return "Ağır Yaralı (3 Puan)"
    elif 11 <= score <= 20:
        return "Orta Yaralı (2 Puan)"
    else:
        return "Hafif Yaralı (1 Puan)"

df_categories["Kategori Grubu"] = df_categories["Puan"].apply(categorize)

# İki farklı bölgedeki yaralı sayılarının rastgele simülasyonu
np.random.seed(42)  # Rastgelelik için sabit bir seed
x_bolgesi = {
    kategori: np.random.randint(0, 10) for kategori in df_categories["Kategori"]
}
y_bolgesi = {
    kategori: np.random.randint(0, 10) for kategori in df_categories["Kategori"]
}

# İhtiyaç duyulan ekipmanları belirleyen bir fonksiyon
def ekipman_gereksinimi(kategori, sayi):
    if "Ağır Yaralı" in kategori:
        return sayi * 2  # Ağır yaralılar için daha fazla ekipman
    elif "Orta Yaralı" in kategori:
        return sayi * 1  # Orta yaralılar için standart ekipman
    else:
        return max(sayi // 2, 1)  # Hafif yaralılar için daha az ekipman

# Geri bildirim oluşturma
def geri_bildirim(yarali_verisi, kategori_gruplari):
    geri_bildirim_listesi = []
    for kategori, sayi in yarali_verisi.items():
        grup = kategori_gruplari.loc[kategori_gruplari["Kategori"] == kategori, "Kategori Grubu"].values[0]
        ekipman = ekipman_gereksinimi(grup, sayi)
        geri_bildirim_listesi.append({
            "Bölge": "X Bölgesi" if yarali_verisi == x_bolgesi else "Y Bölgesi",
            "Kategori": kategori,
            "Yaralı Sayısı": sayi,
            "Kategori Grubu": grup,
            "Gerekli Ekipman": ekipman
        })
    return geri_bildirim_listesi

# Kategori gruplarını hazırlama
kategori_gruplari = df_categories[["Kategori", "Kategori Grubu"]]

# Geri bildirimleri toplama ve birleştirme
x_geri_bildirim = geri_bildirim(x_bolgesi, kategori_gruplari)
y_geri_bildirim = geri_bildirim(y_bolgesi, kategori_gruplari)

# Verileri birleştirme
tum_geri_bildirim = pd.DataFrame(x_geri_bildirim + y_geri_bildirim)

# DataFrame'i ekrana yazdırma
print(tum_geri_bildirim)

