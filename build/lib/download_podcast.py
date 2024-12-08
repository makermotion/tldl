import io
import logging
import os
import tempfile
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import urlopen

import numpy as np
import requests
from bs4 import BeautifulSoup as soup
from tqdm import tqdm


class PodcastDownloader:
    """A class to download podcasts from Google Podcasts."""

    def __init__(self, base_url='https://podcasts.google.com'):
        """Initializes the PodcastDownloader object.

        Args:
            base_url (str): The base URL for Google Podcasts.
        """
        self.base_url = base_url

    def _prepare_url_for_google(self, podcast_name):
        """Constructs the search URL for the given podcast name.

        Args:
            podcast_name (str): The name of the podcast to search for.
        Returns:
            str: The search URL for the given podcast name.
        """
        podcast_name_safe = quote(podcast_name.encode('utf-8'))
        logging.info(f"Podcast Name SAFE: {podcast_name}")
        return f'{self.base_url}/search/{podcast_name_safe}'

    def _get_content(self, url):
        """Retrieves the HTML content from the given URL.

        Args:
            url (str): The URL to fetch the content from.
        Returns:
            BeautifulSoup: The parsed HTML content.
        """

        client = urlopen(url)
        html_content = client.read()
        client.close()
        return soup(html_content, 'html.parser')

    def _go2show(self, content):
        """Finds the full show URL from the parsed HTML content.

        Args:
            content (BeautifulSoup): The parsed HTML content.
        Returns:
            str: The full show URL.
        """

        full_show = content.find('a', {'class': 'pyK9td'}, href=True)
        full_show_url = f'{self.base_url}/{full_show["href"][2:]}'
        return full_show_url

    def get_episode_names(self, podcast_name):
        """Retrieves the episode names.

        Args:
            full_show_page_content (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.
        Returns:
            list: A list of episode names.
        """

        url = self._prepare_url_for_google(podcast_name)
        content = self._get_content(url)
        full_show_url = self._go2show(content)
        full_show_page_content = self._get_content(full_show_url)
        episode_names = full_show_page_content.findAll('div',
                                                       {'class': 'LTUrYb'})
        names = [name.text for name in episode_names]
        return names

    def get_episode_download_links(self, podcast_name):
        """Retrieves the episode download links.

        Args:
            podcast_name (str): The name of the podcast to search for.
        Returns:
            list: A list of episode download links.
        """

        url = self._prepare_url_for_google(podcast_name)
        content = self._get_content(url)
        full_show_url = self._go2show(content)
        full_show_page_content = self._get_content(full_show_url)
        episode_links = full_show_page_content.findAll('div',
                                                       {'jsname': 'fvi9Ef'})
        links = [link['jsdata'][7:] for link in episode_links]
        return links

    def _get_mp3(self, url):
        """Retrieves the MP3 file from the provided URL and converts it into
        numpy array.

        Args:
            url (str): The URL of the MP3 file.
        Returns:
            str: The path to the saved MP3 file.
            np.array: The MP3 file as a numpy array.
        """
        mp3_bytes = requests.get(url, stream=True).content
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(mp3_bytes)
            fp.close()
            return fp.name, mp3_bytes

    def download_podcast(self, episode_url):
        """Downloads the podcast episode from the provided URL.

        Args:
            episode_url (str): The URL of the podcast episode.
            dir_to_save (str): The directory to save the episode to.
        Returns:
            str: The name of the saved MP3 file.
        """
        mp3_name, _ = self._get_mp3(episode_url)
        return mp3_name
