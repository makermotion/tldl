import yt_dlp


def download_audio_from_youtube(url: str, output_dir: str = "downloads") -> str:
    """Downloads audio from a YouTube video and converts it to MP3 format.

    Args:
        url (str): The YouTube video URL to download from.
        output_dir (str, optional): Directory where the audio file will be saved.
            Defaults to "downloads".

    Returns:
        str: The full path to the downloaded MP3 file.

    Raises:
        yt_dlp.utils.DownloadError: If the video cannot be downloaded or URL is invalid.
        OSError: If the output directory cannot be accessed or created.

    Example:
        >>> file_path = download_audio_from_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        >>> print(file_path)
        'downloads/Rick Astley - Never Gonna Give You Up.mp3'
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")
        return file_path


if __name__ == "__main__":
    url = "https://music.youtube.com/watch?v=8N7mdkrXgbc"
    file_path = download_audio_from_youtube(url)
    print(file_path)
