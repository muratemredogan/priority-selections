import numpy as np
import random

# Q-table boyutlarını belirlemek için sabitler
NUM_STATES = 30  # Yaralı ve bina puanları
NUM_ACTIONS = 10  # 10 farklı ekip türü

# Q-table başlangıcı
q_table = np.random.rand(NUM_STATES, NUM_ACTIONS) * 100

# Örnek: Eylemler (Ekiplerin index numarası)
actions = [
    "Ambulans", "İtfaiye", "AFAD", "STK1", "STK2",
    "Polis", "Jandarma", "K9 Kurtarma", "Dağcı Kurtarma", "Gönüllü Sağlıkçılar"
]

alpha = 0.7  # Öğrenme oranı
gamma = 0.8  # Geleceğe yönelik ödül ağırlığı
epsilon = 0.1  # Keşif oranı
episodes = 1000  # Eğitim tekrar sayısı

def get_reward(state, action):
    """
    Duruma (yaralı/bina puanı) ve eyleme (ekip seçimi) bağlı ödül hesaplama
    """
    if state > 25 and action == 0:  # Ambulans yüksek puanlı yaralılar için
        return 100
    elif state > 20 and action in [1, 2]:  # İtfaiye veya AFAD binalar için
        return 90
    elif state > 15:
        return 70
    else:
        return 10  # Diğer durumlar için düşük ödül

for episode in range(episodes):
    state = random.randint(0, NUM_STATES - 1)  # Rastgele başlangıç durumu
    
    done = False
    while not done:
        # Epsilon-greedy yöntemi ile aksiyon seçimi
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, NUM_ACTIONS - 1)  # Rastgele keşif
        else:
            action = np.argmax(q_table[state])  # En iyi bilinen aksiyon
        
        # Ödül hesaplama
        reward = get_reward(state, action)
        
        # Q-Table güncelleme
        next_state = random.randint(0, NUM_STATES - 1)  # Yeni rastgele durum
        q_table[state, action] = q_table[state, action] + alpha * (
            reward + gamma * np.max(q_table[next_state]) - q_table[state, action]
        )
        
        state = next_state
        
        if reward > 90:  # Örneğin yüksek ödül aldığında döngü bitsin
            done = True

def assign_team(state):
    action = np.argmax(q_table[state])
    return actions[action]

# Test için örnek durumlar (yaralı veya bina puanları)
test_states = [28, 23, 15, 7, 3, 1]

# Test sonuçlarını kaydetme
test_results = [{"Durum (Puan)": state, "Atanan Ekip": assign_team(state)} for state in test_states]

# Sonuçları DataFrame olarak gösterme
df_test_results = pd.DataFrame(test_results)

tools.display_dataframe_to_user("Q-Learning Test Sonuçları", df_test_results)
