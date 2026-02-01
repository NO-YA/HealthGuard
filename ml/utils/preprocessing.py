import cv2
import numpy as np
from typing import Tuple


IMG_SIZE: Tuple[int, int] = (224, 224)


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Charge et prépare une image pour un modèle TensorFlow Lite.

    Étapes :
    - lecture image
    - resize
    - normalisation
    - ajout dimension batch

    Retour :
    - numpy array de shape (1, 224, 224, 3)
    """

    # Lecture image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de lire l'image : {image_path}")

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize
    image = cv2.resize(image, IMG_SIZE)

    # Normalisation [0, 1]
    image = image.astype("float32") / 255.0

    # Ajout dimension batch
    image = np.expand_dims(image, axis=0)

    return image
