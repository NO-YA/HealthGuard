import os
import numpy as np
from PIL import Image
from backend.app.ml_service import MLService

# Dossier à tester (change selon besoin)
TEST_DIR = "dataset/anemia"  # ou "dataset/normal"

ml_service = MLService(model_path="ml/anemia/model.tflite")

results = []
for fname in os.listdir(TEST_DIR):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    path = os.path.join(TEST_DIR, fname)
    with open(path, "rb") as f:
        try:
            res = ml_service.analyze_bytes(f.read())
            print(f"{fname}: {res['diagnosis']['condition']} (conf={res['diagnosis']['confidence']}, raw={res['diagnosis']['raw_output']})")
            results.append((fname, res['diagnosis']['condition'], res['diagnosis']['confidence']))
        except Exception as e:
            print(f"{fname}: Erreur - {e}")

# Statistiques
n_total = len(results)
n_anemia = sum(1 for r in results if r[1] == "anemia")
n_normal = sum(1 for r in results if r[1] == "normal")
print(f"\nTotal images: {n_total}")
print(f"Prédit 'anemia': {n_anemia}")
print(f"Prédit 'normal': {n_normal}")
