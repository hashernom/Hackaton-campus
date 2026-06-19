"""Registro de viaje: conductor + contactos de emergencia.

Persistencia simple en copiloto/trip.json. Es el punto de entrada de la
propuesta de valor: el conductor que viaja solo deja a quién avisar.

Uso CLI:
  python copiloto/trip.py --driver "Juan Perez" --contact "Mama:123456789"
  python copiloto/trip.py --show
"""
import argparse
import json
import time

import config


def start_trip(driver, contacts):
    """contacts: lista de dicts {"name": str, "chat_id": str}."""
    trip = {"driver": driver, "contacts": contacts, "started": time.time()}
    with open(config.TRIP_FILE, "w", encoding="utf-8") as f:
        json.dump(trip, f, indent=2, ensure_ascii=False)
    return trip


def load_trip():
    """Carga el viaje actual o devuelve un viaje por defecto usando el .env."""
    if config.TRIP_FILE.exists():
        with open(config.TRIP_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {
        "driver": "Conductor",
        "contacts": [{"name": "Contacto", "chat_id": config.DEFAULT_CHAT_ID}],
        "started": time.time(),
    }


def primary_contact(trip):
    contacts = trip.get("contacts") or []
    return contacts[0] if contacts else {"name": "Contacto", "chat_id": config.DEFAULT_CHAT_ID}


def _parse_contact(s):
    # formato "Nombre:chat_id"
    name, _, chat_id = s.partition(":")
    return {"name": name.strip(), "chat_id": chat_id.strip()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Registrar un viaje de COPILOTO")
    ap.add_argument("--driver", help="Nombre del conductor")
    ap.add_argument("--contact", action="append", default=[],
                    help='Contacto en formato "Nombre:chat_id" (repetible)')
    ap.add_argument("--show", action="store_true", help="Mostrar el viaje actual")
    args = ap.parse_args()

    if args.show:
        print(json.dumps(load_trip(), indent=2, ensure_ascii=False))
    elif args.driver:
        contacts = [_parse_contact(c) for c in args.contact] or \
                   [{"name": "Contacto", "chat_id": config.DEFAULT_CHAT_ID}]
        t = start_trip(args.driver, contacts)
        print("Viaje registrado:")
        print(json.dumps(t, indent=2, ensure_ascii=False))
    else:
        ap.print_help()
