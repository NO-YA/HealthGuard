import os
import numpy as np
import cv2

BASE_DIR = "ml/datasets"
TASKS = ["diabetes", "anemia", "deficiency"]
SPLITS = ["train", "val"]
CLASSES = ["positive", "negative"]

IMG_SIZE = (224, 224)
IMAGES_PER_CLASS = 10


def generate_image():
    return np.random.randint(0, 255, (*IMG_SIZE, 3), dtype=np.uint8)


for task in TASKS:
    for split in SPLITS:
        for cls in CLASSES:
            dir_path = os.path.join(BASE_DIR, task, split, cls)
            os.makedirs(dir_path, exist_ok=True)

            for i in range(IMAGES_PER_CLASS):
                img = generate_image()
                img_path = os.path.join(dir_path, f"{cls}_{i}.jpg")
                cv2.imwrite(img_path, img)

print("✅ Dataset factice généré")
