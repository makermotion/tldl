# tl;dl - Too Long; Didn't Listen

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31012/)

tl;dl is an AI-powered podcast summarization tool that converts Google Podcasts episodes into concise summaries. It downloads podcast episodes, transcribes them, generates summaries, and can even create audio versions of the summaries.

## Features

- 🎙️ Download podcasts from YouTube Music Podcasts
- 📝 Transcribe audio to text using OpenAI's Whisper
- 🤖 Generate summaries using local LLM through Ollama
- 🗣️ Convert summaries back to speech using TTS
- 🌐 User-friendly web interface with Streamlit

## Architecture

The project uses the following key technologies:

- [Streamlit](https://github.com/streamlit/streamlit) - Web interface
- [Whisper](https://github.com/openai/whisper) - Speech-to-text transcription
- [Ollama](https://ollama.com/) - Local LLM for summarization
- [TTS](https://github.com/coqui-ai/TTS) - Text-to-speech synthesis

## Prerequisites

1. Python 3.10.12 or higher
2. [Ollama](https://ollama.com/) installed and running locally
3. At least 8GB RAM recommended
4. GPU recommended but not required

## Installation

1. Clone the repository:

```bash
git clone https://github.com/makermotion/tldl.git
cd tldl
```

2. Create and activate virtual environment:

```bash
python3.10 -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

3. Install the package:

```bash
pip install .
```

4. Start Ollama server with the required model:

```bash
ollama run <model> 
```

## Usage

1. Start the web interface:

```bash
streamlit run src/app.py
```

2. Open your browser and navigate to `http://localhost:8501`
3. Search a podcast by its name like you do in YouTube music.

## Known Limitations

- Processing time depends on episode length and system capabilities.

## Contributing

Contributions are welcome! Here are some ways you can help:

- Submit bug fixes or improvements via pull requests
- Help with documentation
- Suggest new features

Current development priorities:

- Command-line interface implementation
- Docker containerization
- Improved podcast source compatibility
- Performance optimizations

If you encounter any issues or have questions:

- Create an [issue](https://github.com/makermotion/tldl/issues)
- Check existing issues for solutions

## License

Released under the MIT License. See [LICENSE](./LICENSE) for details.
