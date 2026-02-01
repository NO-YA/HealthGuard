import tensorflow as tf
import os

KERAS_DIR = "ml/models/keras"
TFLITE_DIR = "ml/models/inference"

os.makedirs(TFLITE_DIR, exist_ok=True)

MODELS = {
    "diabetes": "diabetes_model.h5",
    "anemia": "anemia_model.h5",
    "deficiency": "deficiency_model.h5",
}

for name, filename in MODELS.items():
    keras_path = os.path.join(KERAS_DIR, filename)
    tflite_path = os.path.join(TFLITE_DIR, f"{name}.tflite")

    model = tf.keras.models.load_model(keras_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()

    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"✅ {name}.tflite généré")
