"""Clasificación de anomalías de carretera (VLM zero-shot) + estimación de demora.

- classify_anomaly(image_path, driver_input) -> {type, description, confidence,
  justifies_delay}  usando un modelo CLIP zero-shot ya entrenado (sin entrenar nada).
- estimate_delay(name_or_type) -> minutos, por mapeo configurable (config.DELAY_ESTIMATES).

El import de transformers/torch es perezoso y el modelo se carga una sola vez. Si no
están disponibles, classify_anomaly degrada con gracia (type=None) y el orquestador
manda la incidencia a revisión humana.
"""
import difflib
import unicodedata

import config

_pipe = None  # pipeline zero-shot cacheado


def _strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normalize_to_type(text):
    """Normaliza texto libre (p. ej. 'vía cerrada') a un tipo de la taxonomía."""
    if not text:
        return None
    t = _strip_accents(str(text).lower().strip()).replace(" ", "_")

    # match directo contra las claves
    if t in config.TAXONOMY:
        return t
    # ¿alguna clave contenida en el texto, o viceversa?
    for key in config.TAXONOMY:
        if key in t or t in key:
            return key
    # match difuso contra claves y etiquetas legibles
    candidates = {}
    for key, label in config.TAXONOMY_LABELS.items():
        candidates[key] = key
        candidates[_strip_accents(label.lower())] = key
    best = difflib.get_close_matches(_strip_accents(str(text).lower()),
                                     list(candidates.keys()), n=1, cutoff=0.6)
    return candidates[best[0]] if best else None


def estimate_delay(name_or_type):
    """Devuelve el estimado de demora (minutos) para un nombre/tipo de anomalía."""
    typ = name_or_type if name_or_type in config.DELAY_ESTIMATES else normalize_to_type(name_or_type)
    return int(config.DELAY_ESTIMATES.get(typ, 0)) if typ else 0


def _get_pipe():
    """Carga (una vez) el pipeline zero-shot de transformers."""
    global _pipe
    if _pipe is None:
        from transformers import pipeline  # import perezoso
        _pipe = pipeline("zero-shot-image-classification", model=config.INCIDENT_MODEL)
        print(f"[incidents] modelo zero-shot cargado: {config.INCIDENT_MODEL}")
    return _pipe


def is_ready():
    """True si el modelo ya está cargado en memoria."""
    return _pipe is not None


def warmup():
    """Pre-carga el modelo (para llamar en un hilo al arrancar el servidor)."""
    if not config.INCIDENT_USE_MODEL:
        return
    try:
        print("[incidents] pre-cargando modelo de imagen (warm-up)…")
        _get_pipe()
        print("[incidents] modelo listo.")
    except Exception as e:
        print(f"[incidents] warm-up falló ({e}); se usará el nombre del conductor.")


def classify_anomaly(image_path, driver_input=None):
    """Clasifica la foto contra la taxonomía. Devuelve dict con tipo/confianza.

    Si hay driver_input que mapea a un tipo, se usa para fijar/corregir el tipo
    (el conductor sabe qué pasó); el modelo aporta la confianza visual.
    """
    hint_type = normalize_to_type(driver_input) if driver_input else None

    # Etiquetas legibles -> mejores resultados zero-shot. Mapa label->key.
    label_to_key = {config.TAXONOMY_LABELS[k]: k for k in config.TAXONOMY}
    candidate_labels = list(label_to_key.keys())

    pred_type, confidence = None, 0.0
    # Usar el modelo si está activado y hay imagen. Si todavía está cargando
    # (warm-up) y el conductor escribió el nombre, vamos instantáneo con el nombre;
    # si no hay nombre y no está listo, lo cargamos (bloquea solo esa vez).
    use_model = config.INCIDENT_USE_MODEL and image_path is not None
    if use_model and (is_ready() or not hint_type):
        try:
            pipe = _get_pipe()
            from PIL import Image
            img = Image.open(image_path).convert("RGB")
            results = pipe(img, candidate_labels=candidate_labels)
            top = results[0]
            pred_type = label_to_key.get(top["label"], "sin_anomalia")
            confidence = float(top["score"])
        except Exception as e:
            print(f"[incidents] modelo no disponible ({e}); uso el dato del conductor.")

    # El conductor corrige el tipo si lo escribió; si no, manda el modelo.
    final_type = hint_type or pred_type
    if final_type is None:
        return {"type": None, "description": None, "confidence": 0.0,
                "justifies_delay": False}

    description = config.TAXONOMY_LABELS.get(final_type, final_type)
    justifies = final_type != "sin_anomalia"
    return {
        "type": final_type,
        "description": description,
        "confidence": round(confidence, 4),
        "justifies_delay": justifies,
    }


if __name__ == "__main__":
    # Smoke test del mapeo de demora (sin necesidad de modelo).
    for name in ["via cerrada", "vía cerrada", "Accidente", "ponchadura", "xyz"]:
        print(f"{name!r:20} -> tipo={normalize_to_type(name)}  demora={estimate_delay(name)}min")
