# Audio Transcription CLI - FasterWhisper

A self-contained Python CLI tool for transcribing audio files to text using FasterWhisper, a faster implementation of OpenAI's Whisper model.

## Features

- **Faster transcription**: Uses FasterWhisper (2-5x faster than standard Whisper with minimal accuracy loss)
- **GPU optimized**: Automatically uses GPU acceleration when available
- **Local transcription**: Uses Whisper model entirely offline (after initial model download)
- **Auto language detection**: Automatically detects the language, or specify manually
- **Flexible output**: Print to stdout or save to file
- **Supports multiple audio formats**: MP3, WAV, M4A, FLAC, OGG, Opus, AAC

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages Python and the virtual environment automatically
- FFMPEG — required by Whisper for audio processing
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`

## Installation

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone or download this repository.

3. Symlink the `transcribe` wrapper into a directory on your `$PATH`. **Symlink — do not copy**, because the wrapper resolves its own location to find `transcribe.py`.
   ```bash
   ln -s /path/to/repo/transcribe ~/.local/bin/transcribe
   ```

That's it. On first run, `uv` will automatically create a virtual environment and install dependencies.

> **No manual `pip install` or venv activation needed.**

4. (Optional) Set your HuggingFace token to avoid rate limit warnings on model downloads:
   ```bash
   cp .env.example .env
   # Edit .env and add your token from https://huggingface.co/settings/tokens
   ```

## Usage

```bash
transcribe audio.mp3
transcribe audio.wav --model tiny
transcribe audio.m4a --model large --output transcript.txt
transcribe audio.mp3 --language es
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-m`, `--model` | `small` | Model size: tiny, base, small, medium, large |
| `-l`, `--language` | auto-detect | Language code, e.g. `en`, `es`, `fr` |
| `-o`, `--output` | stdout | Output file path |

### Running the script directly

```bash
uv run transcribe.py audio.mp3
```

## Model Sizes

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~40MB | ⚡⚡⚡ | ⭐ |
| base | ~140MB | ⚡⚡ | ⭐⭐ |
| small | ~466MB | ⚡ | ⭐⭐⭐ |
| medium | ~1.5GB | 🐢 | ⭐⭐⭐⭐ |
| large | ~2.9GB | 🐢🐢 | ⭐⭐⭐⭐⭐ |

The first run downloads the model to `~/.cache/huggingface/` (not stored in this repo).

## Supported Audio Formats

MP3, WAV, M4A, FLAC, OGG, Opus, AAC

## Troubleshooting

**`uv: command not found`**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**`FFMPEG not found`**
- Install ffmpeg using the instructions in the Requirements section above.

**Unsupported audio format**
- Convert with ffmpeg: `ffmpeg -i input.m4b -acodec libmp3lame -ab 192k output.mp3`
