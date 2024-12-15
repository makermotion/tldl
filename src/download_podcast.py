from ytmusicapi import YTMusic
import yt_dlp
import os
from typing import List, Optional


class PodcastDownloader:
    def __init__(self, output_dir: str = "downloads"):
        """Initialize PodcastDownloader.

        Args:
            output_dir (str): Directory for downloaded podcasts
        """
        self.ytmusic = YTMusic()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Configure yt-dlp options
        self.ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
        }

    def get_episode_names(self, podcast_name: str) -> List[str]:
        """Get list of episode names for a podcast.

        Args:
            podcast_name (str): Name of the podcast to search

        Returns:
            List[str]: List of episode names
        """
        try:
            # Search for the podcast
            results = self.ytmusic.search(podcast_name, filter="podcasts", limit=1)
            if not results:
                return []

            # Get podcast details
            podcast = self.ytmusic.get_podcast(results[0]["browseId"])
            if not podcast or "episodes" not in podcast:
                return []

            # Extract episode names
            return [episode["title"] for episode in podcast["episodes"]]

        except Exception as e:
            print(f"Error getting episode names: {e}")
            return []

    def get_episode_download_links(self, podcast_name: str) -> List[str]:
        """Get download links for podcast episodes.

        Args:
            podcast_name (str): Name of the podcast to search

        Returns:
            List[str]: List of episode download links (video IDs)
        """
        try:
            # Search for the podcast
            results = self.ytmusic.search(podcast_name, filter="podcasts", limit=1)
            if not results:
                return []

            # Get podcast details
            podcast = self.ytmusic.get_podcast(results[0]["browseId"])
            if not podcast or "episodes" not in podcast:
                return []

            # Extract video IDs
            return [episode["videoId"] for episode in podcast["episodes"]]

        except Exception as e:
            print(f"Error getting download links: {e}")
            return []

    def download_podcast(self, video_id: str) -> Optional[str]:
        """Download podcast episode.

        Args:
            video_id (str): YouTube video ID

        Returns:
            Optional[str]: Path to downloaded MP3 file
        """
        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Return the MP3 filename
                mp3_path = os.path.splitext(filename)[0] + ".mp3"
                return mp3_path
        except Exception as e:
            print(f"Download error: {e}")
            return None
