import os
import string
import unicodedata
from datetime import datetime
from pprint import pprint

import torch
import torchaudio
from tqdm import tqdm
from underthesea import sent_tokenize
from unidecode import unidecode

import gradio as gr
import shutil
from vinorm import TTSnorm

try:
    from NViXTTS import XttsConfig
    from NViXTTS import Xtts
except ImportError:
    print("Required libraries not found. \n Please ensure 'TTS' packages are installed.")



def get_root_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    print(f"Current Path: {current_path}")

    root_path = current_path
    return root_path


ROOT_PATH = get_root_path()
xtts_checkpoint = os.path.join(ROOT_PATH, "model", "model.pth")
xtts_config = os.path.join(ROOT_PATH, "model", "config.json")
xtts_vocab = os.path.join(ROOT_PATH, "model", "vocab.json")


def clear_gpu_cache():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_model(xtts_checkpoint, xtts_config, xtts_vocab):
    clear_gpu_cache()
    if not xtts_checkpoint or not xtts_config or not xtts_vocab:
        return "You need to run the previous steps or manually set the `XTTS checkpoint path`, `XTTS config path`, and `XTTS vocab path` fields !!"
    
    if not os.path.exists(xtts_checkpoint):
        print(f"Error: Checkpoint file not found at {xtts_checkpoint}")
        return None
    if not os.path.exists(xtts_config):
        print(f"Error: Config file not found at {xtts_config}")
        return None
    if not os.path.exists(xtts_vocab):
        print(f"Error: Vocab file not found at {xtts_vocab}")
        return None

    config = XttsConfig()
    config.load_json(xtts_config)
    XTTS_MODEL = Xtts.init_from_config(config)
    print("Loading XTTS model! ")

    use_deepspeed = torch.cuda.is_available()

    try:
        XTTS_MODEL.load_checkpoint(config,
                                   checkpoint_path=xtts_checkpoint,
                                   vocab_path=xtts_vocab,
                                   use_deepspeed=use_deepspeed)
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return None

    if torch.cuda.is_available():
        XTTS_MODEL.cuda()

    print("Model Loaded!")
    return XTTS_MODEL

vixtts_model = load_model(xtts_checkpoint, xtts_config, xtts_vocab)