"""Validación del clasificador de anomalías + cola de revisión humana con FiftyOne.

Aquí FiftyOne es protagonista (no solo soporte):
  1) Evaluar el modelo zero-shot sobre fotos etiquetadas (accuracy + matriz).
  2) Curar/descubrir tipos nuevos con Brain (similitud / visualización UMAP).
  3) Servir la COLA DE REVISIÓN HUMANA: cargar de Postgres las incidencias
     'needs_review' y revisarlas en la App.

Modos:
  # Evaluar el modelo sobre un dataset por carpetas de clase
  python copiloto/validate_incidents_fiftyone.py --data ruta/al/dataset

  # Cola de revisión: cargar las incidencias pendientes desde la base de datos
  python copiloto/validate_incidents_fiftyone.py --review

  # Confirmar/corregir una incidencia tras revisarla
  python copiloto/validate_incidents_fiftyone.py --confirm 12 --as via_cerrada --by despacho
"""
import argparse

import config


def _eval_mode(data_dir, no_app):
    """Evalúa el modelo zero-shot sobre un dataset etiquetado por carpetas."""
    import fiftyone as fo
    import fiftyone.zoo as foz
    import fiftyone.brain as fob

    dataset = fo.Dataset.from_dir(
        dataset_dir=data_dir,
        dataset_type=fo.types.ImageClassificationDirectoryTree,
        name=None,
    )
    print(f"[validate] {len(dataset)} imágenes cargadas")

    # Modelo zero-shot del Model Zoo con nuestra taxonomía como clases candidatas.
    classes = config.TAXONOMY
    model = foz.load_zoo_model("clip-vit-base32-torch", classes=classes)
    dataset.apply_model(model, label_field="pred")

    # Evaluar contra ground_truth (el nombre de carpeta = etiqueta real).
    results = dataset.evaluate_classifications(
        "pred", gt_field="ground_truth", eval_key="eval"
    )
    print("\n===== REPORTE DE EVALUACIÓN =====")
    results.print_report()

    # Curación con Brain: descubrir agrupaciones / tipos nuevos.
    try:
        fob.compute_similarity(dataset, model="clip-vit-base32-torch", brain_key="sim")
        fob.compute_visualization(dataset, brain_key="viz")
        print("[validate] Brain: índice de similitud + visualización UMAP listos.")
    except Exception as e:
        print(f"[validate] Brain omitido ({e}).")

    if not no_app:
        session = fo.launch_app(dataset)
        print("[validate] App abierta. Filtra eval=False para ver los fallos.")
        session.wait()


def _review_mode(no_app):
    """Carga las incidencias 'needs_review' desde Postgres en la App para revisar."""
    import os
    import fiftyone as fo
    import db

    pending = db.list_incidents(status="needs_review", limit=500)
    pending = [p for p in pending if p.get("image_path") and os.path.exists(p["image_path"])]
    if not pending:
        print("[review] No hay incidencias 'needs_review' con imagen. Nada que revisar.")
        return

    dataset = fo.Dataset(name=None)
    for p in pending:
        sample = fo.Sample(filepath=p["image_path"])
        sample["incident_id"] = p["id"]
        sample["pred"] = fo.Classification(
            label=p.get("type") or "sin_clasificar",
            confidence=p.get("confidence") or 0.0,
        )
        sample["estimated_delay_min"] = p.get("estimated_delay_min")
        dataset.add_sample(sample)

    print(f"[review] {len(dataset)} incidencias pendientes cargadas.")
    print("[review] Revisa en la App; confirma con:")
    print("         --confirm <incident_id> --as <tipo> --by <nombre>")
    if not no_app:
        session = fo.launch_app(dataset)
        session.wait()


def _confirm(incident_id, new_type, reviewed_by):
    """Marca una incidencia como confirmada (y corrige el tipo si se indica)."""
    import db
    inc = db.get_incident(incident_id)
    if not inc:
        print(f"[confirm] incidencia {incident_id} no encontrada.")
        return
    # Si se corrige el tipo, recalcular la demora con el mapeo.
    if new_type:
        import incidents as inc_mod
        delay = inc_mod.estimate_delay(new_type)
        # Reutilizamos add/set: actualizamos estado; el tipo/demora se ajustan vía SQL directo.
        import json
        conn = db._connect()
        try:
            ph = db._placeholder()
            cur = conn.cursor()
            cur.execute(
                f"UPDATE incidents SET type={ph}, estimated_delay_min={ph}, "
                f"status={ph}, reviewed_by={ph} WHERE id={ph}",
                (new_type, delay, "confirmed", reviewed_by, incident_id),
            )
            conn.commit()
        finally:
            conn.close()
        print(f"[confirm] incidencia {incident_id} -> {new_type} ({delay} min), confirmada.")
    else:
        db.set_status(incident_id, "confirmed", reviewed_by)
        print(f"[confirm] incidencia {incident_id} confirmada.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="Directorio con subcarpetas por clase (modo evaluación)")
    ap.add_argument("--review", action="store_true", help="Cola de revisión desde la base de datos")
    ap.add_argument("--confirm", type=int, help="ID de incidencia a confirmar")
    ap.add_argument("--as", dest="new_type", help="Corregir el tipo al confirmar")
    ap.add_argument("--by", dest="reviewed_by", default="revisor", help="Quién revisa")
    ap.add_argument("--no-app", action="store_true", help="No abrir la App de FiftyOne")
    args = ap.parse_args()

    if args.confirm is not None:
        _confirm(args.confirm, args.new_type, args.reviewed_by)
    elif args.review:
        _review_mode(args.no_app)
    elif args.data:
        _eval_mode(args.data, args.no_app)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
