import tensorflow as tf


# Charger le meilleur modèle Keras
model = tf.keras.models.load_model('best_model.h5')

# Convertir en TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Sauvegarder le modèle TFLite
with open('ml/anemia/model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Conversion terminée !")
