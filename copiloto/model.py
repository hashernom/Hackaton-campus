"""Modelo de somnolencia basado en Hugging Face (transformers).

Carga un clasificador de imágenes pre-entrenado (ViT fine-tuned) y clasifica
cada cuadro. Hace inferencia manual (modelo + image processor) en lugar de
`pipeline`, porque algunos repos de la comunidad no traen completo el
`preprocessor_config.json` y el pipeline falla al autodetectar el procesador.

La importación de transformers/torch es perezosa para que el resto de la app
funcione aunque no estén instalados (modo MediaPipe / EAR).
"""
import cv2
from PIL import Image

import config


class DrowsinessModel:
    def __init__(self, name=None):
        import torch  # import perezoso
        from transformers import AutoModelForImageClassification
        self._torch = torch
        self.name = name or config.MODEL_NAME

        self.model = AutoModelForImageClassification.from_pretrained(self.name)
        self.model.eval()
        self.processor = self._load_processor(self.name)
        self.id2label = self.model.config.id2label
        print(f"[model] cargado: {self.name}")
        print(f"[model] etiquetas: {self.id2label}")

    @staticmethod
    def _load_processor(name):
        from transformers import AutoImageProcessor, ViTImageProcessor
        try:
            return AutoImageProcessor.from_pretrained(name)
        except Exception:
            # Fallback robusto para repos con preprocessor_config incompleto.
            return ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")

    def _infer(self, pil_img):
        inputs = self.processor(pil_img.convert("RGB"), return_tensors="pt")
        with self._torch.no_grad():
            logits = self.model(**inputs).logits
        probs = logits.softmax(-1)[0]
        idx = int(probs.argmax())
        return self.id2label[idx], float(probs[idx])

    def predict(self, frame_bgr):
        """Devuelve (label, score) a partir de un cuadro BGR de OpenCV."""
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return self._infer(Image.fromarray(rgb))

    def predict_path(self, path):
        """Devuelve (label, score) a partir de la ruta de una imagen (validación)."""
        return self._infer(Image.open(path))

    @staticmethod
    def is_risk(label):
        """True si la etiqueta corresponde a un estado de riesgo (somnolencia)."""
        return config.label_is_risk(label)
