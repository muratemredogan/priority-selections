# Ekipler ve kişi sayıları
teams = [
    {"Ekip Adı": "Ambulans Ekipleri (Sağlıkçılar)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "İtfaiye Ekipleri (Kurtarıcılar)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "AFAD Ekipleri (Kurtarıcılar)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Sivil Toplum Kuruluşu 1 (Kurtarıcılar)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Sivil Toplum Kuruluşu 2 (Kurtarıcılar)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Polis Ekipleri (Güvenlik)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Jandarma Ekipleri (Güvenlik)", "Kişi Sayısı": 1000},
    {"Ekip Adı": "K9 Arama Kurtarma Ekipleri", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Dağcı Kurtarma Ekipleri", "Kişi Sayısı": 1000},
    {"Ekip Adı": "Gönüllü Sağlıkçılar", "Kişi Sayısı": 1000},
]

# Veriyi DataFrame'e aktarma
df_teams = pd.DataFrame(teams)

tools.display_dataframe_to_user("Kurtarma Ekipleri", df_teams)
