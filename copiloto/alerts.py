"""Lógica de escalado con anti-falsos-positivos + alerta por voz (TTS).

Niveles:
  0 = OK
  1 = riesgo sostenido -> alerta en cabina (voz + banner)
  2 = no se recupera    -> el orquestador dispara la notificación remota

La voz corre en un hilo aparte para no congelar el bucle de video.
"""
import os
import tempfile
import threading
import time

import config

try:
    import pyttsx3
    _HAS_TTS = True
except Exception:
    _HAS_TTS = False


def _play_mp3_windows(path):
    """Reproduce un mp3 en Windows vía MCI (ctypes), sin dependencias extra."""
    from ctypes import windll
    alias = f"cp_tts_{int(time.time() * 1000)}"
    windll.winmm.mciSendStringW(f'open "{path}" type mpegvideo alias {alias}', None, 0, 0)
    windll.winmm.mciSendStringW(f'play {alias} wait', None, 0, 0)
    windll.winmm.mciSendStringW(f'close {alias}', None, 0, 0)


def _speak_edge(text):
    """Voz neural en español con edge-tts (online). Lanza excepción si falla."""
    import asyncio
    import edge_tts

    path = os.path.join(tempfile.gettempdir(), f"cp_tts_{int(time.time() * 1000)}.mp3")

    async def _gen():
        await edge_tts.Communicate(text, config.VOICE_EDGE).save(path)

    asyncio.run(_gen())
    _play_mp3_windows(path)
    try:
        os.remove(path)
    except Exception:
        pass


def speak(text):
    """Reproduce voz en español sin bloquear el bucle de video.

    Primero intenta edge-tts (voz neural española, online). Si falla (sin
    internet), cae a pyttsx3 (voz local del sistema). Si nada hay, queda silencioso.
    """
    def _run():
        try:
            _speak_edge(text)
            return
        except Exception as e:
            print(f"[voz] edge-tts no disponible ({e}); uso voz local.")
        if _HAS_TTS:
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[voz][ERROR] {e}")

    threading.Thread(target=_run, daemon=True).start()


class Escalator:
    """Convierte una señal booleana de riesgo en un nivel estable (basado en tiempo).

    Usar tiempo de pared (no contar cuadros) hace que los umbrales en segundos
    se respeten aunque el FPS varíe.
    """

    def __init__(self, l1_secs=None, l2_secs=None):
        self.l1_secs = config.LEVEL1_SECS if l1_secs is None else l1_secs
        self.l2_secs = config.LEVEL2_SECS if l2_secs is None else l2_secs
        self.risk_start = None
        self.level = 0
        self._last_voice = 0.0
        self.alert_count = 0
        self.risk_secs = 0.0

    def update(self, is_risk):
        """Actualiza con la señal actual y devuelve el nivel (0/1/2)."""
        now = time.time()
        if is_risk:
            if self.risk_start is None:
                self.risk_start = now
            self.risk_secs = now - self.risk_start
        else:
            self.risk_start = None
            self.risk_secs = 0.0

        if self.risk_secs >= self.l2_secs:
            new_level = 2
        elif self.risk_secs >= self.l1_secs:
            new_level = 1
        else:
            new_level = 0

        # Voz mientras hay riesgo, con cooldown.
        if new_level >= 1 and (now - self._last_voice) > config.VOICE_COOLDOWN:
            speak(config.VOICE_TEXT)
            self._last_voice = now

        # Contar alertas nuevas (transición 0 -> riesgo)
        if new_level >= 1 and self.level == 0:
            self.alert_count += 1

        self.level = new_level
        return new_level
