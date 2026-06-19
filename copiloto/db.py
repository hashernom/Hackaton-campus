"""Capa de datos de incidencias (anomalías de carretera).

Servicio de almacenamiento con Postgres para el caso empresarial. Si no hay
DATABASE_URL configurada, cae a SQLite local (copiloto/incidents.db) detrás de
la MISMA interfaz, para que la demo funcione sin Docker.

Funciones:
  init_db()                         -> crea la tabla si no existe
  add_incident(**campos)            -> inserta y devuelve el id
  list_incidents(trip_driver=None)  -> lista de dicts (más reciente primero)
  get_incident(id)                  -> dict | None
  set_status(id, status, reviewed_by=None)

Diseñado para no romper la app si la base de datos no está disponible:
las operaciones registran el error y devuelven valores vacíos.
"""
import json

import config


def _is_pg():
    return bool(config.DATABASE_URL)


def _placeholder():
    return "%s" if _is_pg() else "?"


def _connect():
    if _is_pg():
        import psycopg  # import perezoso (solo si se usa Postgres)
        return psycopg.connect(config.DATABASE_URL)
    import sqlite3
    return sqlite3.connect(str(config.SQLITE_FALLBACK))


# --- DDL específico por motor -------------------------------------------------

_DDL_PG = """
CREATE TABLE IF NOT EXISTS incidents (
    id                  SERIAL PRIMARY KEY,
    trip_driver         TEXT,
    created_at          TIMESTAMPTZ DEFAULT now(),
    location            TEXT,
    type                TEXT,
    description         TEXT,
    driver_input        TEXT,
    confidence          REAL,
    justifies_delay     BOOLEAN,
    estimated_delay_min INTEGER,
    status              TEXT,
    reviewed_by         TEXT,
    image_path          TEXT
);
"""

_DDL_SQLITE = """
CREATE TABLE IF NOT EXISTS incidents (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_driver         TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location            TEXT,
    type                TEXT,
    description         TEXT,
    driver_input        TEXT,
    confidence          REAL,
    justifies_delay     INTEGER,
    estimated_delay_min INTEGER,
    status              TEXT,
    reviewed_by         TEXT,
    image_path          TEXT
);
"""

_COLUMNS = [
    "id", "trip_driver", "created_at", "location", "type", "description",
    "driver_input", "confidence", "justifies_delay", "estimated_delay_min",
    "status", "reviewed_by", "image_path",
]


def init_db():
    """Crea la tabla si no existe. Devuelve True si tuvo éxito."""
    try:
        conn = _connect()
        try:
            cur = conn.cursor()
            cur.execute(_DDL_PG if _is_pg() else _DDL_SQLITE)
            conn.commit()
        finally:
            conn.close()
        backend = "Postgres" if _is_pg() else f"SQLite ({config.SQLITE_FALLBACK.name})"
        print(f"[db] listo ({backend})")
        return True
    except Exception as e:
        print(f"[db][ERROR] no se pudo inicializar: {e}")
        return False


def _row_to_dict(row):
    d = dict(zip(_COLUMNS, row))
    # location se guarda como JSON de texto
    if d.get("location"):
        try:
            d["location"] = json.loads(d["location"])
        except Exception:
            d["location"] = None
    d["justifies_delay"] = bool(d.get("justifies_delay"))
    d["created_at"] = str(d.get("created_at"))
    return d


def add_incident(trip_driver, type, description=None, driver_input=None,
                 confidence=0.0, justifies_delay=False, estimated_delay_min=0,
                 status="needs_review", location=None, image_path=None):
    """Inserta una incidencia y devuelve su id (o None si falla)."""
    ph = _placeholder()
    cols = ("trip_driver, location, type, description, driver_input, confidence, "
            "justifies_delay, estimated_delay_min, status, image_path")
    vals = (
        trip_driver,
        json.dumps(location) if location else None,
        type,
        description,
        driver_input,
        float(confidence),
        bool(justifies_delay),
        int(estimated_delay_min),
        status,
        image_path,
    )
    placeholders = ", ".join([ph] * len(vals))
    sql = f"INSERT INTO incidents ({cols}) VALUES ({placeholders})"
    try:
        conn = _connect()
        try:
            cur = conn.cursor()
            if _is_pg():
                cur.execute(sql + " RETURNING id", vals)
                new_id = cur.fetchone()[0]
            else:
                cur.execute(sql, vals)
                new_id = cur.lastrowid
            conn.commit()
            return new_id
        finally:
            conn.close()
    except Exception as e:
        print(f"[db][ERROR] add_incident: {e}")
        return None


def list_incidents(trip_driver=None, status=None, limit=100):
    """Devuelve incidencias (más recientes primero) como lista de dicts."""
    ph = _placeholder()
    where, params = [], []
    if trip_driver:
        where.append(f"trip_driver = {ph}")
        params.append(trip_driver)
    if status:
        where.append(f"status = {ph}")
        params.append(status)
    clause = (" WHERE " + " AND ".join(where)) if where else ""
    sql = (f"SELECT {', '.join(_COLUMNS)} FROM incidents{clause} "
           f"ORDER BY id DESC LIMIT {int(limit)}")
    try:
        conn = _connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            return [_row_to_dict(r) for r in cur.fetchall()]
        finally:
            conn.close()
    except Exception as e:
        print(f"[db][ERROR] list_incidents: {e}")
        return []


def get_incident(incident_id):
    ph = _placeholder()
    sql = f"SELECT {', '.join(_COLUMNS)} FROM incidents WHERE id = {ph}"
    try:
        conn = _connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (incident_id,))
            row = cur.fetchone()
            return _row_to_dict(row) if row else None
        finally:
            conn.close()
    except Exception as e:
        print(f"[db][ERROR] get_incident: {e}")
        return None


def set_status(incident_id, status, reviewed_by=None):
    ph = _placeholder()
    sql = f"UPDATE incidents SET status = {ph}, reviewed_by = {ph} WHERE id = {ph}"
    try:
        conn = _connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (status, reviewed_by, incident_id))
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception as e:
        print(f"[db][ERROR] set_status: {e}")
        return False


if __name__ == "__main__":
    # Smoke test: init + insert + list
    init_db()
    iid = add_incident(
        trip_driver="Demo", type="via_cerrada",
        description="prueba", confidence=0.9, justifies_delay=True,
        estimated_delay_min=120, status="auto",
    )
    print("insertado id:", iid)
    print("incidencias:", list_incidents())
