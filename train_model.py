import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Load Data ──────────────────────────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv("Crop_recommendation.csv")

print(f"Dataset shape: {df.shape}")
print(f"Crops: {df['label'].unique()}")
print(f"Missing values: {df.isnull().sum().sum()}")

# ── 2. Preprocess ─────────────────────────────────────────────────────────────
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Encode crop labels to integers
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Stratified 80/20 split (preserves class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Standardise features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 3. Train & Evaluate All Models ───────────────────────────────────────────
models = {
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM (RBF)":           SVC(kernel='rbf', probability=True, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
}

results = {}
print("\n" + "="*55)
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)
    acc   = accuracy_score(y_test, preds)
    results[name] = acc
    print(f"\n{name}")
    print(f"  Accuracy : {acc*100:.2f}%")
    print(f"  Report   :\n{classification_report(y_test, preds, target_names=le.classes_)}")
print("="*55)

# ── 4. Feature Importance (Random Forest) ─────────────────────────────────────
rf = models["Random Forest"]
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importance (Random Forest):")
print(importances)

# ── 5. Confusion Matrix ───────────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

best_model = models["Random Forest"]
cm = confusion_matrix(y_test, best_model.predict(X_test_scaled))
plt.figure(figsize=(16, 12))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=le.classes_,
            yticklabels=le.classes_, cmap='Blues')
plt.title("Random Forest — Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=150)
plt.close()
print("\nConfusion matrix saved → outputs/confusion_matrix.png")

# Feature importance plot
plt.figure(figsize=(8, 5))
importances.plot(kind='bar', color='steelblue')
plt.title("Feature Importance — Random Forest")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.savefig("outputs/feature_importance.png", dpi=150)
plt.close()
print("Feature importance plot saved → outputs/feature_importance.png")

# ── 6. Save Best Model, Scaler & Label Encoder ───────────────────────────────
joblib.dump(best_model, "model/crop_model.pkl")
joblib.dump(scaler,     "model/scaler.pkl")
joblib.dump(le,         "model/label_encoder.pkl")

print("\n✅ Model saved → model/crop_model.pkl")
print("✅ Scaler saved → model/scaler.pkl")
print("✅ Label encoder saved → model/label_encoder.pkl")
print("\n📋 Copy these accuracy numbers into your README:")
for name, acc in results.items():
    print(f"   {name:25s}: {acc*100:.2f}%")
