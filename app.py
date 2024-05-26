import itertools

import streamlit as st
import torch

from download_podcast import PodcastDownloader
from summarizer import summarize
from tts_modules import do_tts

if "flow_state" not in st.session_state:
    st.session_state.flow_state = None

if "prev_name" not in st.session_state:
    st.session_state.prev_name = None

if "device" not in st.session_state:
    st.session_state.device = "cuda" if torch.cuda.is_available() else "cpu"


@st.experimental_dialog("Settings")
def settings():
    """Settings for the app."""
    st.session_state.device = st.selectbox("Select device", ["cpu", "cuda"],
                                           key="sb_device")


def clean_podcast_name(podcast_name):
    return podcast_name.replace(" ", "_").strip().lower()


def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    from: https://gist.github.com/treuille/2ce0acb6697f205e44e3e0f576e810b7

    Args:
        label: The label of the pagination selectbox.
        items: The items to display in the paginator.
        items_per_page: The number of items to display per page.
        on_sidebar: Whether to display the paginator on the sidebar.

    Returns:
        An iterator over the items in the current page.
    """

    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(label,
                                     range(n_pages),
                                     format_func=page_format_func)

    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return itertools.islice(enumerate(items), min_index, max_index)


podcast_downloader = PodcastDownloader()
st.title("TL;DL: Too Long; Didn't Listen")

podcast_name = st.text_input(
    'Enter the podcast name to search in Google Podcasts:')
with st.sidebar:
    if st.button("Settings", key="settings", use_container_width=True):
        settings()

if podcast_name and st.session_state.prev_name != podcast_name:
    st.session_state.prev_name = podcast_name
    st.session_state.episode_names = podcast_downloader.get_episode_names(
        podcast_name)
    st.session_state.episode_urls = podcast_downloader.get_episode_download_links(
        podcast_name)
    st.session_state.flow_state = "paginate"

if st.session_state.flow_state == "paginate":
    for i, podcast in paginator("Select page:",
                                st.session_state.episode_names,
                                on_sidebar=False):
        with st.expander(f"{podcast}"):
            podcast = clean_podcast_name(podcast)
            lang = st.selectbox("Select language", ["", "English", "Turkish"],
                                key=f"sb_lang_{i}")
            is_button_disabled = True if lang == "" else False
            if st.button("Download and Summarize",
                         disabled=is_button_disabled,
                         key=f"bt_{i}"):
                with st.spinner(
                        "Downloading, transcribing and summarizing the podcast..."
                ):
                    mp3_name = podcast_downloader.download_podcast(
                        st.session_state.episode_urls[i])
                    summary_text = summarize(mp3_name, podcast, lang,
                                             st.session_state.device)
                with st.spinner("Generating audio summary..."):
                    tts_summary_path = do_tts(summary_text, podcast, lang,
                                              st.session_state.device)
                st.audio(tts_summary_path, format='audio/wav')
