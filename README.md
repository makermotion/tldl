# tl;dl - Too Long; Didn't Listen

tl;dl is a podcast summarization tool for Google Podcasts. (probably buggy, since this was a side project just for myself)

It uses;

- [streamlit](https://github.com/streamlit/streamlit) for user interface
- [whisper](https://github.com/openai/whisper) for speech-to-text
- [ollama](https://ollama.com/) for summarization
- [TTS](https://github.com/coqui-ai/TTS) for text-to-speech

## Requirements

[ollama](https://ollama.com/) must be installed and served

```bash
ollama run llama3:instruct
```

## Installation

```bash
git clone https://github.com/makermotion/tldl.git
cd tldl
pip install -r requirements.txt
```

note: python version 3.10.12

## Usage

To use the podcast summarizer, you need to run the UI via:
(you need to be on the project directory)

```bash
streamlit run app.py
```

## Development

- tl;dl heavily relies on the web scraping, links for podcast soundfile links are collected from the Google Podcasts website from some specific html tags. So all podcasts may not be supported. If you want to contribute you can file an issue for not supported podcasts or you can contribute to the codebase.
- Also there may be a script for tl;dl to be used as a command line tool.
- dockerize the application

## License

This script is released under the MIT License. See the [LICENSE](./LICENSE) file in the repository for full details.
