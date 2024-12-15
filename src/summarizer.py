"""Summarize a podcast using whisper and langchain_community."""

import gc
import logging
import os
from pathlib import Path

import torch
import whisper
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

from prompt_templates import template

logging.basicConfig(level=logging.INFO)
root_path = Path(__file__).absolute().parent
os.makedirs(root_path / "transcripts", exist_ok=True)
lang_mapping = {"English": "en", "Turkish": "tr"}


def read_cache(cache_path):
    """Read a cache file.

    Args:
        cache_path (str): path to the cache file

    Returns:
        (str): content of the cache file
    """
    with open(cache_path) as cf:
        return cf.read()


def summarize(mp3_path, podcast_name, language, device, from_cache=None):
    """Summarize a podcast.

    Args:
        mp3_path (str): path to the podcast mp3 file
        podcast_name (str): name of the podcast
        language (str): language of the summary
        from_cache (str): path to the cache file

    Returns:
        summary_path (str): path to the summary file
    """
    language = lang_mapping[language]
    logging.info("Transcribing...\n")
    if from_cache is None:
        model = whisper.load_model("medium", device=device)
        logging.info("Whisper model loaded")
        transcript = model.transcribe(mp3_path, language=language)
        logging.info("Transcription done!, saving...\n")
        transcript_path = f"{root_path}/transcripts/{podcast_name}_transcript.txt"
        with open(transcript_path, "w+") as tf:
            tf.write(transcript["text"])
        del model
    else:
        transcript = read_cache(from_cache)
    torch.cuda.empty_cache()
    gc.collect()
    logging.info("Reading the full transcription successful!, Summarizing...\n")
    prompt = PromptTemplate.from_template(template)
    llm = ChatOllama(model="llama3.2", base_url="http://127.0.0.1:11434", keep_alive=0)
    chain = prompt | llm
    summary = chain.invoke({"transcript": transcript["text"], "language": language})
    summary_path = f"{root_path}/transcripts/{podcast_name}_summary.txt"
    with open(summary_path, "w+") as tf:
        tf.write(summary.content)
    logging.info("Summarization done!")
    return summary_path
