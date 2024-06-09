from NViXTTS.tts.configs.xtts_config import XttsConfig
from NViXTTS.tts.models.xtts import Xtts
import os

with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r", encoding="utf-8") as f:
    version = f.read().strip()

__version__ = version
