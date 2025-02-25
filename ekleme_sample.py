import pandas as pd
import datetime

# Örnek veri oluştur
ornek_veriler = {
    'mesaj_id': range(1, 11),
    'konum': ['AVM Merkez', 'Gökdelen Plaza', 'Metro İstasyonu', 'İlkokul', 'Hastane'] * 2,
    'gönderen_rol': ['Doktor', 'Güvenlik', 'Vatandaş', 'Öğretmen', 'Hemşire'] * 2,
    'tarih_saat': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 10,
    'acil_durum_mesajı': [
        '2 kişi crush sendromu, 3 kişi yanık vakası',
        '1 kişi kalp durması, 2 kişi travmatik beyin',
        '5 kişi mahsur kaldı, 1 kişi göğüs travması',
        '3 kişi kafa travması, 2 kişi solunum sıkıntısı',
        '1 kişi kardiyak arrest, 4 kişi yanık',
        '2 kişi iç kanama, 1 kişi şok',
        '3 kişi multiple travma, 2 kişi açık kırık',
        '1 kişi akut solunum yetmezliği',
        '4 kişi enkaz altında',
        '2 kişi zehirlenme, 3 kişi hipotermi'
    ]
}

df = pd.DataFrame(ornek_veriler)
df.to_csv('acil_durum_mesajlari.csv', index=False) 
