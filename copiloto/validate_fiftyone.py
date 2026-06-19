"""Validación offline del modelo de somnolencia con FiftyOne.

Es el uso "de apoyo" de FiftyOne (no el núcleo): mide qué tan bueno es el
modelo HF y aflora dónde falla, para mostrarlo en el pitch con rigor.

Espera un directorio de imágenes organizado por clase:
    <dataset_dir>/
        drowsy/   *.jpg
        awake/    *.jpg
(los nombres de carpeta son libres; se normalizan a binario riesgo/ok).

Uso:
  python copiloto/validate_fiftyone.py --data ruta/al/dataset
  python copiloto/validate_fiftyone.py --data ruta/al/dataset --no-app
"""
import argparse

import config

RISK = "riesgo"
OK = "ok"


def to_binary(label):
    """Normaliza una etiqueta (GT o predicha) a 'riesgo'/'ok'."""
    return RISK if config.label_is_risk(label) else OK


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Directorio con subcarpetas por clase")
    ap.add_argument("--no-app", action="store_true", help="No abrir la app de FiftyOne")
    args = ap.parse_args()

    import fiftyone as fo
    from model import DrowsinessModel

    # 1) Cargar dataset (árbol de directorios = etiquetas ground truth)
    dataset = fo.Dataset.from_dir(
        dataset_dir=args.data,
        dataset_type=fo.types.ImageClassificationDirectoryTree,
        name=None,
    )
    print(f"[validate] {len(dataset)} imágenes cargadas")

    # 2) Predecir con el modelo y guardar pred + versión binaria de GT y pred
    model = DrowsinessModel()
    for sample in dataset.iter_samples(progress=True, autosave=True):
        label, score = model.predict_path(sample.filepath)
        sample["pred_raw"] = fo.Classification(label=str(label), confidence=score)
        sample["pred"] = fo.Classification(label=to_binary(label), confidence=score)
        gt = sample["ground_truth"].label if sample.has_field("ground_truth") else OK
        sample["gt_bin"] = fo.Classification(label=to_binary(gt))

    # 3) Evaluar (binario riesgo/ok)
    results = dataset.evaluate_classifications(
        "pred", gt_field="gt_bin", eval_key="eval"
    )
    print("\n===== REPORTE DE EVALUACIÓN =====")
    results.print_report()

    # Casos de fallo, ordenados por confianza (los errores "seguros" son los peores)
    mistakes = dataset.match(fo.ViewField("eval") == False).sort_by(
        "pred.confidence", reverse=True
    )
    print(f"\n[validate] {len(mistakes)} clasificaciones erróneas. "
          f"Revisa los casos de fallo en la app (noche, gafas, barba, etc.).")

    if not args.no_app:
        session = fo.launch_app(dataset)
        print("[validate] App abierta. Filtra por eval=False para ver los fallos.")
        session.wait()


if __name__ == "__main__":
    main()
