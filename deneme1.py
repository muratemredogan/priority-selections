import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Veri oluşturma

def generate_data():
    """Rastgele acil durum verileri oluşturur."""
    data = {
        "location_type": np.random.choice(["hospital", "city_center", "outskirts", "school", "park"], size=1000),
        "damage_level": np.random.choice(["severe", "moderate", "crowded"], size=1000),
        "urgency": np.zeros(1000)
    }
    df = pd.DataFrame(data)

    # Puanlandırma sistemi (Ödül ve ceza sistemi)
    location_points = {
        "hospital": 40,
        "city_center": 50,
        "outskirts": 20,
        "school": 40,
        "park": 1
    }

    damage_points = {
        "severe": 10,
        "moderate": 5,
        "crowded": 30
    }

    df["urgency"] = df["location_type"].map(location_points) + df["damage_level"].map(damage_points)

    # Durumları sınıflandırma
    df["response_level"] = np.where(df["urgency"] > 70, "high", np.where(df["urgency"] > 30, "medium", "low"))
    return df

# Veri Hazırlığı
data = generate_data()
X = data[["location_type", "damage_level"]]
y = data["response_level"]

# Kategorik verileri dönüştürme
X = pd.get_dummies(X, columns=["location_type", "damage_level"], drop_first=True)

# Veri bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model oluşturma ve eğitim
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Tahmin ve değerlendirme
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Model Doğruluğu: {accuracy:.2f}")
print("Sınıflandırma Raporu:")
print(report)

# Örnek tahmin
def predict_urgency(location_type, damage_level):
    """Yeni bir veri için aciliyet tahmini yapar."""
    input_data = pd.DataFrame({
        "location_type": [location_type],
        "damage_level": [damage_level]
    })
    input_data = pd.get_dummies(input_data, columns=["location_type", "damage_level"], drop_first=True)
    input_data = input_data.reindex(columns=X.columns, fill_value=0)
    prediction = model.predict(input_data)[0]
    return prediction

# Örnek Kullanım
example_prediction = predict_urgency("hospital", "severe")
print(f"Tahmin Edilen Müdahale Seviyesi: {example_prediction}")
