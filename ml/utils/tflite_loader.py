import tensorflow as tf
import numpy as np


class TFLiteModel:
    def __init__(self, model_path: str):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, input_tensor: np.ndarray) -> float:
        """
        input_tensor shape: (1, 224, 224, 3)
        return: float prediction
        """
        self.interpreter.set_tensor(
            self.input_details[0]["index"],
            input_tensor.astype("float32")
        )

        self.interpreter.invoke()

        output = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )

        return float(output[0][0])
