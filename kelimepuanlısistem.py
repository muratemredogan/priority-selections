import re

# Kelime puanları
word_scores = {
    "ağır": 10, "iç kanama": 10, "bilinci kapalı": 9, "şok": 9,
    "hayati tehlike": 10, "kritik": 9, "durumu stabil değil": 9,
    "nabız yok": 10, "kan kaybı": 10, "solunum durması": 10,
    "orta kırık": 6, "travmatik": 6, "yanık": 5, "kanama": 6,
    "kafa travması": 7, "omurga zedelenmesi": 7, "ciddi yaralanma": 6,
    "tansiyon düşmesi": 5, "bilinç kaybı": 6, "nefes darlığı": 6,
    "hafif": 2, "çizik": 1, "çatlak": 2, "kırık": 3,
    "morluk": 1, "şişlik": 1, "burkulma": 2, "sarsıntı": 2,
    "hafif yaralanma": 3, "doku zedelenmesi": 2, "baygınlık": 8,
    "iç kanama ihtimali": 8, "boğulma": 10, "göçük altında": 9,
    "tıbbi müdahale": 7, "ciddi enfeksiyon": 7, "felç": 9,
    "yüksek ateş": 6, "düşük tansiyon": 5, "kırık omurga": 8,
    "derin kesik": 8, "aşırı kanama": 9, "kan pıhtılaşması": 7,
    "organ hasarı": 9, "omuz çıkığı": 3, "kaburga kırığı": 7,
    "iç organ yaralanması": 10, "yüz travması": 6, "yanık derecesi": 5,
    "kan zehirlenmesi": 8
}

# Mesajı analiz eden fonksiyon
def analyze_message(message):
    total_score = 0
    for key, score in word_scores.items():
        # Regex ile anahtar kelime ve öncesindeki sayı eşleşmesini bul
        matches = re.findall(rf"(\d+)?\s*{key}", message)
        for match in matches:
            if len(match) > 0 and match[0].isdigit():  # Eğer sayı varsa al
                count = int(match[0])
            else:
                count = 1  # Sayı yoksa varsayılan olarak 1 al
            total_score += count * score
    return total_score

# Örnek vakalar
vaka_1 = "10 ağır yaralı, kritik 9 kişi, bilinci kapalı 15 kişi."
vaka_2 = "10 orta kırık, 3 ciddi enfeksiyon, 15 hafif yaralı."

# Skor hesaplama
manual_score_1 = analyze_message(vaka_1)
manual_score_2 = analyze_message(vaka_2)

# Sonuçları yazdırma
print(f"Vaka 1: {vaka_1}")
print(f"Toplam önem puanı: {manual_score_1}\n")

print(f"Vaka 2: {vaka_2}")
print(f"Toplam önem puanı: {manual_score_2}\n")

# Aciliyet karşılaştırması
if manual_score_1 > manual_score_2:
    print("Vaka 1 daha acil!")
elif manual_score_1 < manual_score_2:
    print("Vaka 2 daha acil!")
else:
    print("İki vaka da aynı derecede acil!")
