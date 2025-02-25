import streamlit as st
from datetime import datetime
import sqlite3
import geocoder
import speech_recognition as sr
import pandas as pd
import numpy as np
from murat import EmergencyQLearning, severity_scores, equipment_priority, calculate_urgency_score
import re

# Veritabanı bağlantısı
def init_db():
    conn = sqlite3.connect('afet_veritabani.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS yarali_bilgileri
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  vaka_adresi TEXT,
                  vaka_tarihi DATE,
                  vaka_saati TEXT,
                  yarali_sayisi INTEGER,
                  bildiri_mesaji TEXT,
                  aciliyet_puani FLOAT,
                  tespit_edilen_durumlar TEXT,
                  onerilen_ekipmanlar TEXT)''')
    conn.commit()
    return conn, c

def analiz_et_ve_puan_hesapla(mesaj, konum):
    mesaj = mesaj.lower()
    detected_conditions = {}
    scores = []
    
    # Özel durum kontrolleri
    special_cases = {
        r'(\d+)\s*kişinin\s*(\w+)\s*kırık': 'kırık',
        r'(\d+)\s*kişinin\s*(\w+)\s*kırığı': 'kırık',
        r'(\d+)\s*kişi\s*(\w+)\s*kırık': 'kırık',
        r'(\d+)\s*(\w+)\s*kırığı': 'kırık',
        r'(\d+)\s*kişinin\s*(\w+)\s*yaralı': 'yaralı',
        r'(\d+)\s*kişi\s*(\w+)\s*yaralı': 'yaralı'
    }
    
    # Özel durumları kontrol et
    for pattern, condition_type in special_cases.items():
        matches = re.finditer(pattern, mesaj)
        for match in matches:
            count = int(match.group(1))
            body_part = match.group(2)
            condition = f'{body_part} {condition_type}'
            
            if condition in severity_scores:
                score = calculate_urgency_score(count, severity_scores[condition], konum)
                scores.append(score)
                detected_conditions[condition] = count
    
    # Genel durum kontrolü
    for condition, severity in severity_scores.items():
        # Farklı yazım şekilleri için pattern'lar
        patterns = [
            rf'(\d+)\s*kişi\s*{condition}',
            rf'(\d+)\s*hasta\s*{condition}',
            rf'(\d+)\s*{condition}',
            rf'(\d+)\s*kişinin\s*{condition}',
            rf'(\d+)\s*kişide\s*{condition}'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, mesaj)
            if matches:
                count = sum(int(x) for x in matches)
                score = calculate_urgency_score(count, severity, konum)
                scores.append(score)
                detected_conditions[condition] = count
                break  # Aynı durum için diğer pattern'ları kontrol etmeye gerek yok
    
    # Eğer hiçbir durum tespit edilmediyse, metin içinde geçen anahtar kelimeleri kontrol et
    if not detected_conditions:
        words = mesaj.split()
        for word in words:
            for condition in severity_scores.keys():
                if word in condition or condition in word:
                    detected_conditions[condition] = 1  # Sayı belirtilmemişse 1 varsayalım
                    score = calculate_urgency_score(1, severity_scores[condition], konum)
                    scores.append(score)
    
    if detected_conditions:
        # En yüksek öncelikli durumu bul
        max_severity_condition = max(detected_conditions.keys(), 
                                  key=lambda x: severity_scores.get(x, 0))
        
        # Ekipman önerilerini birleştir
        all_equipment = set()
        for condition in detected_conditions.keys():
            if condition in equipment_priority:
                all_equipment.update(equipment_priority[condition])
        
        # Eğer hiç ekipman önerisi bulunamazsa
        if not all_equipment:
            all_equipment = equipment_priority.get('belirsiz_durum', 
                          ['ilk yardım çantası', 'sedye', 'temel tıbbi malzemeler'])
        
        return {
            'puan': sum(scores),
            'durumlar': detected_conditions,
            'ekipmanlar': list(all_equipment)  # Tekrar eden ekipmanları temizle
        }
    
    # Hiçbir durum tespit edilemezse, basit kelime analizi yap
    emergency_keywords = ['kırık', 'yaralı', 'kanama', 'acil', 'yardım', 'kaza']
    for keyword in emergency_keywords:
        if keyword in mesaj:
            return {
                'puan': 5,  # Varsayılan düşük öncelik puanı
                'durumlar': {'belirsiz_durum': 1},
                'ekipmanlar': ['ilk yardım çantası', 'sedye', 'temel tıbbi malzemeler']
            }
    
    return None

def main():
    st.title("Afet Yönetim Sistemi")
    
    # Veritabanı bağlantısı
    conn, c = init_db()
    
    # Sidebar
    st.sidebar.header("Yeni Vaka Bildirimi")
    
    try:
        g = geocoder.ip('me')
        default_konum = f"Lat: {g.latlng[0]}, Lon: {g.latlng[1]}" if g.latlng else "Konum alınamadı"
    except:
        default_konum = "Konum alınamadı"
    
    vaka_adresi = st.sidebar.text_input("Vaka adresi", value=default_konum)
    vaka_tarihi = st.sidebar.date_input("Vaka tarihi", value=datetime.now())
    vaka_saati = st.sidebar.time_input("Vaka saati", value=datetime.now().time())
    yarali_sayisi = st.sidebar.number_input("Yaralı sayısı", min_value=0, value=1)
    
    # Ana içerik
    tab1, tab2 = st.tabs(["Vaka Bildirimi", "Vaka Listesi"])
    
    with tab1:
        st.subheader("Acil Durum Bildirimi")
        
        # Ses kaydı
        if st.button("Sesli Mesaj Al"):
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.write("Konuşmaya başlayın...")
                    audio = recognizer.listen(source)
                    bildiri_mesaji = recognizer.recognize_google(audio, language="tr-TR")
                    st.success("Ses metne dönüştürüldü!")
            except Exception as e:
                st.error(f"Ses tanıma hatası: {str(e)}")
                bildiri_mesaji = ""
        else:
            bildiri_mesaji = st.text_area("Bildiri Mesajı", height=100)
        
        if st.button("Analiz Et ve Kaydet"):
            if bildiri_mesaji:
                analiz_sonucu = analiz_et_ve_puan_hesapla(bildiri_mesaji, vaka_adresi)
                
                if analiz_sonucu:
                    # Veritabanına kaydet
                    c.execute('''INSERT INTO yarali_bilgileri 
                               (vaka_adresi, vaka_tarihi, vaka_saati, yarali_sayisi,
                                bildiri_mesaji, aciliyet_puani, tespit_edilen_durumlar,
                                onerilen_ekipmanlar)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                             (vaka_adresi, vaka_tarihi, vaka_saati.strftime("%H:%M:%S"),
                              yarali_sayisi, bildiri_mesaji, analiz_sonucu['puan'],
                              str(analiz_sonucu['durumlar']), str(analiz_sonucu['ekipmanlar'])))
                    conn.commit()
                    
                    st.success("Vaka başarıyla kaydedildi!")
                    st.info(f"Aciliyet Puanı: {analiz_sonucu['puan']}")
                    st.write("Tespit Edilen Durumlar:", analiz_sonucu['durumlar'])
                    st.write("Önerilen Ekipmanlar:", analiz_sonucu['ekipmanlar'])
                else:
                    st.warning("Acil durum tespit edilemedi.")
            else:
                st.error("Lütfen bir bildiri mesajı girin.")
    
    with tab2:
        st.subheader("Kayıtlı Vakalar")
        
        c.execute("""SELECT * FROM yarali_bilgileri ORDER BY aciliyet_puani DESC""")
        rows = c.fetchall()
        
        if rows:
            df = pd.DataFrame(rows, columns=['ID', 'Adres', 'Tarih', 'Saat', 'Yaralı Sayısı',
                                           'Mesaj', 'Aciliyet Puanı', 'Durumlar', 'Önerilen Ekipmanlar'])
            st.dataframe(df)
            
            if st.button("Seçili Vakayı Sil"):
                vaka_index = st.number_input("Silinecek vaka ID:", 1, max(df['ID']))
                c.execute("DELETE FROM yarali_bilgileri WHERE id=?", (vaka_index,))
                conn.commit()
                st.success(f"Vaka #{vaka_index} silindi.")
        else:
            st.info("Henüz kayıtlı vaka bulunmuyor.")
    
    conn.close()

if __name__ == "__main__":
    main() 
