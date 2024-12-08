# Description: Text to speech using the TTS model.
import argparse
import os
import typing
from pathlib import Path

import torch
from TTS.api import TTS

parser = argparse.ArgumentParser(description='TTS')
parser.add_argument("-o", "--output", type=str)
parser.add_argument("-s", "--speaker", type=str)
parser.add_argument("-t", "--text-file", type=str)
parser.add_argument("-l", "--lang", type=str)
parser.add_argument("-i", "--speaker_id", type=str)
parser.add_argument("-vc", "--voice_clone", type=bool, default=False)
args = parser.parse_args()

root_path = Path(__file__).absolute().parent
os.makedirs(root_path / "summary_audio", exist_ok=True)

lang_mapping = {"English": "en", "Turkish": "tr"}


def select_model(language: str) -> str:
    """Select the model based on the language. first element is the model path
    and the second element is the flag for the multi lingual model.

    Args:
        language (str): The language.
    Returns:
        str: The model path.
    """

    dict_model = {
        "en": ("tts_models/multilingual/multi-dataset/your_tts", True),
        "tr": ("tts_models/tr/common-voice/glow-tts", False)
    }
    return dict_model[language][0], dict_model[language][1]


def get_text_from_file(text_file: str) -> str:
    """Get the text from the text file.

    Args:
        text_file (str): Path to the text file.
    Returns:
        str: The text from the text file.
    """
    with open(text_file) as f:
        text = f.read()
    text = text.replace("\n", " ").strip().lower()
    return text


def do_tts_voice_clone(text_file: str, speaker_wav_path: str,
                       output_wav_path: str, language: str, device: str):
    """Text to speech using the TTS model.

    Args:
        text_file (str): Path to the text file.
        speaker_wav_path (str): Path to the speaker wav file.
        output_wav_path (str): Path to the output wav file.
        language (str): The language.
        device (str): The device [cpu or gpu].
    """
    language = lang_mapping[language]
    selected_model, is_multilingual = select_model(language)
    text = get_text_from_file(text_file)
    tts = TTS(selected_model).to(device)
    tts.tts_with_vc_to_file(text,
                            speaker_wav=speaker_wav_path,
                            file_path=output_wav_path,
                            language=language if is_multilingual else None)


def do_tts(text_file: str, podcast_name: str, language: str, device: str):
    """Text to speech using the TTS model.

    Args:
        text_file (str): Path to the text file.
        podcast_name (str): The name of the podcast.
        language (str): The language.
        device (str): The device [cpu or gpu].
    """
    language = lang_mapping[language]
    selected_model, is_multilingual = select_model(language)
    text = get_text_from_file(text_file)
    tts = TTS(selected_model).to(device)
    path = f"{root_path}/summary_audio/{podcast_name}.wav"
    tts.tts_to_file(
        text,
        file_path=path,
        speaker=None if language == "tr" else "female-en-5",
        language=language if is_multilingual else None,
    )
    return path
