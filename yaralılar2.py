import pandas as pd

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

# Listeyi 3 gruba ayırma
grouped_categories = df_categories.groupby("Kategori Grubu").apply(lambda x: x.head(10)).reset_index(drop=True)

import ace_tools as tools; tools.display_dataframe_to_user("Yaralı Grupları", grouped_categories)
