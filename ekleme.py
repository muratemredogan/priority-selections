# Murat'ın kodunu buraya yapıştırın (severity_scores, equipment_priority vs içeren kod) 

import pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict

# Severity scores sözlüğü - Genişletilmiş versiyon
severity_scores = {
    # Kritik Durumlar (9-10 puan)
    'crush sendromu': 10,
    'ezilme sendromu': 10,
    'kardiyopulmoner arrest': 10,
    'kardiyak arrest': 10,
    'solunum durması': 10,
    'kalp durması': 10,
    'beyin kanaması': 10,
    'iç kanama': 10,
    'akut solunum yetmezliği': 10,
    'çoklu organ yetmezliği': 10,
    'ağır kafa travması': 10,
    'göçük altında': 10,
    'enkaz altında': 10,
    'masif kanama': 10,
    'nefes almıyor': 10,
    'nefes alamıyor': 10,
    'boynu kırık': 10,
    'boyun kırığı': 10,
    
    # Çok Ciddi Durumlar (8-9 puan)
    'mahsur': 8,
    'yaralı': 8,
    'susuz': 7,
    'kayıp': 8,
    'ezik': 7,
    'travmatik amputasyon': 9,
    'travmatik beyin': 9,
    'şok': 9,
    'akut böbrek yetmezliği': 9,
    'kafa travması': 8,
    'multiple travma': 8,
    'çoklu organ travması': 8,
    'kırık': 8,
    'kırığı': 8,
    'kırığı var': 8,
    
    # Ciddi Durumlar (7-8 puan)
    'yanık': 7,
    'açık kırık': 7,
    'zehirlenme': 7,
    'kimyasal yanık': 7,
    
    # Orta Şiddetli Durumlar (5-6 puan)
    'kapalı kırık': 6,
    'solunum sıkıntısı': 6,
    'bilinç bulanıklığı': 6,
    'derin kesik': 6,
    
    # Hafif-Orta Durumlar (3-4 puan)
    'basit kırık': 4,
    'yumuşak doku travması': 4,
    'eklem çıkığı': 4,
    'yüzeysel kesik': 4,
    
    # Hafif Durumlar (1-2 puan)
    'burkulmalar': 2,
    'sıyrıklar': 2,
    'kontüzyon': 2,
    'kas ağrısı': 2,
    'eklem ağrısı': 2,
    'ayağı kırık': 8,
    'ayak kırığı': 8,
    'bacağı kırık': 8,
    'bacak kırığı': 8,
    'kolu kırık': 8,
    'kol kırığı': 8
}

# Ekipman öncelik sözlüğü
equipment_priority = {
    # Kritik Durumlar için Ekipmanlar
    'crush sendromu': ['diyaliz ünitesi', 'diyaliz cihazı', 'monitör'],
    'ezilme sendromu': ['diyaliz ünitesi', 'diyaliz cihazı', 'monitör'],
    'kardiyopulmoner arrest': ['defibrilatör', 'entübasyon seti', 'acil müdahale seti'],
    'kardiyak arrest': ['defibrilatör', 'entübasyon seti', 'acil müdahale seti'],
    'solunum durması': ['entübasyon seti', 'oksijen tüpü', 'ambu cihazı'],
    'kalp durması': ['defibrilatör', 'kardiyak monitör', 'acil müdahale seti'],
    'beyin kanaması': ['beyin cerrahi seti', 'monitör', 'entübasyon seti'],
    'iç kanama': ['cerrahi set', 'kan ürünleri', 'monitör'],
    'akut solunum yetmezliği': ['ventilatör', 'oksijen tüpü', 'monitör'],
    'çoklu organ yetmezliği': ['yoğun bakım ekipmanı', 'monitör', 'ventilatör'],
    'ağır kafa travması': ['beyin cerrahi seti', 'monitör', 'entübasyon seti'],
    'göçük altında': ['kurtarma ekipmanı', 'kesme aletleri', 'ilk yardım seti'],
    'enkaz altında': ['kurtarma ekipmanı', 'kesme aletleri', 'ilk yardım seti'],
    'masif kanama': ['kan ürünleri', 'cerrahi set', 'monitör'],
    'nefes almıyor': ['entübasyon seti', 'oksijen tüpü', 'ambu cihazı'],
    'nefes alamıyor': ['entübasyon seti', 'oksijen tüpü', 'ambu cihazı'],
    'boynu kırık': ['boyunluk', 'sedye', 'stabilizasyon ekipmanı'],
    'boyun kırığı': ['boyunluk', 'sedye', 'stabilizasyon ekipmanı'],
    
    # Çok Ciddi Durumlar için Ekipmanlar
    'mahsur': ['kurtarma ekipmanı', 'ilk yardım seti', 'sedye'],
    'yaralı': ['sedye', 'ilk yardım çantası', 'pansuman seti'],
    'susuz': ['su', 'serum', 'hidrasyon seti'],
    'kayıp': ['termal kamera', 'arama ekipmanı', 'ses dinleme cihazı'],
    'ezik': ['atel', 'bandaj', 'analjezik'],
    'travmatik amputasyon': ['cerrahi set', 'kan ürünleri', 'monitör'],
    'travmatik beyin': ['beyin cerrahi seti', 'monitör', 'entübasyon seti'],
    'şok': ['defibrilatör', 'monitör', 'acil müdahale seti'],
    
    # Kırıklar için Ekipmanlar
    'kırık': ['atel', 'bandaj', 'analjezik'],
    'kırığı': ['atel', 'bandaj', 'analjezik'],
    'kırığı var': ['atel', 'bandaj', 'analjezik'],
    'ayağı kırık': ['atel', 'bandaj', 'analjezik', 'sedye'],
    'ayak kırığı': ['atel', 'bandaj', 'analjezik', 'sedye'],
    'bacağı kırık': ['atel', 'bandaj', 'analjezik', 'sedye'],
    'bacak kırığı': ['atel', 'bandaj', 'analjezik', 'sedye'],
    'kolu kırık': ['atel', 'bandaj', 'analjezik'],
    'kol kırığı': ['atel', 'bandaj', 'analjezik'],
    
    # Belirsiz durumlar için temel ekipmanlar
    'belirsiz_durum': ['ilk yardım çantası', 'sedye', 'temel tıbbi malzemeler']
}

class EmergencyQLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.episode_count = 0
        
    def get_state_features(self, conditions, location):
        """Durumları ve konum özelliklerini birleştirerek state oluştur"""
        features = []
        total_severity = 0
        max_severity = 0
        total_count = 0
        
        # Durum özellikleri
        for condition, count in conditions.items():
            severity = severity_scores.get(condition, 0)
            total_severity += severity * count
            max_severity = max(max_severity, severity)
            total_count += count
            features.extend([count, severity])
        
        # Özet özellikler
        features.extend([total_severity, max_severity, total_count])
        
        # Konum özellikleri
        location_lower = location.lower()
        location_type = 0  # Varsayılan
        if 'avm' in location_lower:
            location_type = 1
        elif 'gökdelen' in location_lower or 'plaza' in location_lower or 'rezidans' in location_lower:
            location_type = 2
        elif 'metro' in location_lower:
            location_type = 3
        elif 'okul' in location_lower or 'kreş' in location_lower or 'üniversite' in location_lower:
            location_type = 4
            
        features.append(location_type)
        return tuple(features)
    
    def get_action(self, state_features, conditions):
        """Epsilon-greedy politikası ile aksiyon seç"""
        if np.random.random() < max(0.01, self.epsilon / (1 + self.episode_count * 0.005)):
            # Keşif: Mevcut durumlarla ilgili ekipmanlar arasından seç
            possible_actions = set()
            for condition in conditions.keys():
                if condition in equipment_priority:
                    possible_actions.add(condition)
            if possible_actions:
                return np.random.choice(list(possible_actions))
            return np.random.choice(list(equipment_priority.keys()))
        
        # Sömürü: En yüksek Q-değerine sahip aksiyonu seç
        state_actions = self.q_table[state_features]
        if not state_actions:
            # Eğer durum daha önce görülmediyse, mevcut durumlarla ilgili ekipmanlardan birini seç
            possible_actions = set()
            for condition in conditions.keys():
                if condition in equipment_priority:
                    possible_actions.add(condition)
            if possible_actions:
                return np.random.choice(list(possible_actions))
            return np.random.choice(list(equipment_priority.keys()))
        
        return max(state_actions.items(), key=lambda x: x[1])[0]
    
    def update(self, state_features, action, reward, next_state_features):
        """Q-değerlerini güncelle"""
        if next_state_features in self.q_table and self.q_table[next_state_features]:
            next_max_q = max(self.q_table[next_state_features].values())
        else:
            next_max_q = 0
            
        current_q = self.q_table[state_features][action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state_features][action] = new_q
        
    def train_episode(self):
        """Bir eğitim episodunu tamamla"""
        self.episode_count += 1
        self.epsilon = max(0.01, self.epsilon * 0.995)

def calculate_urgency_score(count, severity, location):
    base_score = np.multiply(count, severity)
    location_lower = location.lower()
    location_multiplier = 1.0
    
    if 'avm' in location_lower:
        location_multiplier = 1.3
    elif 'gökdelen' in location_lower or 'plaza' in location_lower or 'rezidans' in location_lower:
        location_multiplier = 1.4
    elif 'metro' in location_lower:
        location_multiplier = 1.3
    elif 'okul' in location_lower or 'kreş' in location_lower or 'üniversite' in location_lower:
        location_multiplier = 1.2
    elif 'hastane' in location_lower:
        location_multiplier = 1.0
        
    return base_score * location_multiplier 
