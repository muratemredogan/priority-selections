import re

# Tıbbi durumlar ve yaralanmaların şiddet puanları
SEVERITY_SCORES = {
    # Kritik Durumlar (9-10 puan)
    'göçük altında': 10,
    'ezilme sendromu': 10,
    'iç kanama': 10,
    'kafatası travması': 10,
    'omurga yaralanması': 10,
    'açık kırık': 9,
    'solunum durması': 10,
    'kalp durması': 10,
    'şok': 9,
    'çoklu organ travması': 10,
    
    # Ciddi Durumlar (7-8 puan)
    'kapalı kırık': 8,
    'hipotermik': 8,
    'dehidratasyon': 7,
    'ciddi yanık': 8,
    'göğüs travması': 8,
    'karın travması': 8,
    'böbrek yetmezliği': 8,
    'sepsis': 7,
    'ağır enfeksiyon': 7,
    'akciğer hasarı': 8,
    
    # Orta Şiddetli Durumlar (4-6 puan)
    'orta derece yanık': 5,
    'kas yaralanması': 4,
    'eklem çıkığı': 5,
    'kesik': 4,
    'orta derece enfeksiyon': 4,
    'sıvı kaybı': 5,
    'hipotermi riski': 5,
    'anksiyete atağı': 4,
    'yüksek ateş': 4,
    'solunum sıkıntısı': 6,
    
    # Hafif Durumlar (2-3 puan)
    'hafif yaralanma': 3,
    'yüzeysel kesik': 2,
    'sıyrık': 2,
    'hafif yanık': 2,
    'burkulmalar': 3,
    'kas ağrısı': 2,
    'baş ağrısı': 2,
    'hafif enfeksiyon': 2,
    'yorgunluk': 2,
    'uykusuzluk': 2,
    
    # Stabil Durumlar (1 puan)
    'stabil': 1,
    'ayakta tedavi': 1,
    'gözlem altında': 1,
    'kontrol altında': 1,
    'genel durum iyi': 1,
    'vital bulgular normal': 1,
    'taburcu edilebilir': 1,
    'takip gerektiren': 1,
    'kronik durum stabil': 1,
    'psikolojik destek': 1
}

def analyze_message(message):
    """
    Verilen mesajı analiz eder ve toplam şiddet puanını hesaplar.
    
    Args:
        message (str): Analiz edilecek acil durum mesajı
        
    Returns:
        tuple: (toplam puan, analiz detayları listesi)
    """
    total_score = 0
    analysis_details = []
    
    # Her anahtar kelime için kontrol
    for condition, score in SEVERITY_SCORES.items():
        # Sayı ve durumu eşleştiren regex pattern - Türkçe karakterler için güncellendi
        pattern = rf'(\d+)\s+(?:vaka(?:sı|ları)?\s+)?{condition}(?:si|ları|leri|\s+vaka(?:sı|ları))?'
        matches = re.finditer(pattern, message.lower())
        
        for match in matches:
            count = int(match.group(1))
            condition_score = count * score
            total_score += condition_score
            analysis_details.append(f"{count} {condition}: {condition_score} puan")
    
    return total_score, analysis_details

def compare_cases(*cases):
    """
    Birden fazla vakayı karşılaştırır ve en acil olanı belirler.
    
    Args:
        *cases: (mesaj, puan) tuple'larından oluşan değişken sayıda argüman
        
    Returns:
        str: Karşılaştırma sonucu
    """
    if not cases:
        return "Karşılaştırılacak vaka bulunamadı."
    
    max_score = max(case[1] for case in cases)
    urgent_cases = [case[0] for case in cases if case[1] == max_score]
    
    if len(urgent_cases) > 1:
        return "Vakalar eşit aciliyette."
    else:
        return f"En acil vaka (Puan: {max_score}):\n{urgent_cases[0]}"

def analyze_emergency_case(message):
    """
    Acil durum vakasını analiz eder ve sonuçları yazdırır.
    
    Args:
        message (str): Analiz edilecek acil durum mesajı
    """
    print("Orijinal Mesaj:", message)
    score, details = analyze_message(message)
    print("\nAnaliz Detayları:")
    for detail in details:
        print("-", detail)
    print("\nToplam Şiddet Puanı:", score)
    return score

def calculate_aid_distribution(cases_with_scores, total_aid_packages=1000):
    """
    Bölgelere puanlarına göre orantılı yardım malzemesi dağıtımı yapar.
    
    Args:
        cases_with_scores: (mesaj, puan) tuple'larından oluşan liste
        total_aid_packages: Toplam yardım paketi sayısı
    
    Returns:
        list: Her bölge için ayrılan yardım paketi sayısı
    """
    total_score = sum(score for _, score in cases_with_scores)
    distributions = []
    
    for case, score in cases_with_scores:
        # Her bölgenin puanına göre orantılı dağıtım
        aid_count = int((score / total_score) * total_aid_packages)
        distributions.append((case, score, aid_count))
    
    return distributions

def print_aid_distribution(distributions):
    """
    Yardım malzemesi dağıtım sonuçlarını yazdırır.
    """
    print("\n=== YARDIM MALZEMESİ DAĞITIM PLANI ===")
    print("\nToplam paket sayısı: 1000")
    print("\nBölgelere göre dağılım (Öncelik sırasına göre):")
    
    # Puana göre sırala (yüksekten düşüğe)
    sorted_dist = sorted(distributions, key=lambda x: x[1], reverse=True)
    
    for i, (case, score, aid_count) in enumerate(sorted_dist, 1):
        print(f"\n{i}. Öncelikli Bölge")
        print(f"Aciliyet Puanı: {score}")
        print(f"Ayrılan Yardım Paketi: {aid_count}")
        print(f"Bölge Durumu: {case}")
        print("-" * 50)

# Test örnekleri
if __name__ == "__main__":
    print("\n=== VAKA ANALİZLERİ ===")
    
    case1 = "3 göçük altında, 5 ezilme sendromu, 10 kapalı kırık, 15 stabil"
    case2 = "2 kafatası travması, 4 iç kanama, 3 solunum durması, 8 ciddi yanık"
    case3 = "5 omurga yaralanması, 3 göğüs travması, 6 dehidratasyon, 12 sıvı kaybı"
    case4 = "20 hafif yaralanma, 15 sıyrık, 8 kas yaralanması, 2 açık kırık"
    
    print("\n--- Bölge 1 ---")
    score1 = analyze_emergency_case(case1)
    
    print("\n--- Bölge 2 ---")
    score2 = analyze_emergency_case(case2)
    
    print("\n--- Bölge 3 ---")
    score3 = analyze_emergency_case(case3)
    
    print("\n--- Bölge 4 ---")
    score4 = analyze_emergency_case(case4)
    
    print("\n=== KARŞILAŞTIRMA SONUCU ===")
    print(compare_cases((case1, score1), (case2, score2), (case3, score3), (case4, score4)))
    
    # Yardım malzemesi dağıtımı
    cases_with_scores = [(case1, score1), (case2, score2), (case3, score3), (case4, score4)]
    distributions = calculate_aid_distribution(cases_with_scores)
    print_aid_distribution(distributions) 