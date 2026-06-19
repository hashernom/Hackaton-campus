"""Notificación remota al contacto de emergencia vía Telegram.

Si no hay token/red, degrada con gracia: guarda la captura y registra en consola
(no lanza excepción, no rompe la demo en vivo).
"""
import time

import requests

import config

_last_sent = 0.0


def _safe_print(msg):
    """print() robusto: la consola de Windows (cp1252) revienta con emoji/tildes."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "replace").decode("ascii"))


def _telegram_send_photo(token, chat_id, caption, photo_path):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(photo_path, "rb") as f:
        r = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": f},
            timeout=10,
        )
    return r.ok, r.text


def notify(caption, photo_path=None, chat_id=None, token=None, respect_cooldown=True):
    """Envía la alerta al contacto. Devuelve True si se envió por Telegram."""
    global _last_sent

    if respect_cooldown and (time.time() - _last_sent) < config.NOTIFY_COOLDOWN:
        return False

    token = token or config.TELEGRAM_BOT_TOKEN
    chat_id = chat_id or config.DEFAULT_CHAT_ID

    if not token or not chat_id:
        _safe_print(f"[notifier][FALLBACK] (sin token/chat_id) {caption} :: {photo_path}")
        _last_sent = time.time()
        return False

    try:
        if photo_path:
            ok, info = _telegram_send_photo(token, chat_id, caption, photo_path)
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            r = requests.post(url, data={"chat_id": chat_id, "text": caption}, timeout=10)
            ok, info = r.ok, r.text
        if ok:
            _safe_print(f"[notifier] enviado a {chat_id}")
        else:
            _safe_print(f"[notifier][ERROR] Telegram respondió: {info}")
        _last_sent = time.time()
        return ok
    except Exception as e:
        _safe_print(f"[notifier][ERROR] no se pudo enviar: {e}")
        _last_sent = time.time()
        return False


def send_test(chat_id=None):
    """Mensaje de prueba para verificar la configuración del bot."""
    return notify("✅ COPILOTO conectado. Esta es una prueba.",
                  photo_path=None, chat_id=chat_id, respect_cooldown=False)


if __name__ == "__main__":
    print("Enviando mensaje de prueba a Telegram...")
    ok = send_test()
    print("Resultado:", "OK" if ok else "no enviado (revisa token/chat_id)")
