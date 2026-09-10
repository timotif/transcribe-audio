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

4. (Optional) Configure environment variables — copy the example file and edit it:
   ```bash
   cp .env.example .env
   ```

   | Variable | Default | Purpose |
   |----------|---------|---------|
   | `HF_TOKEN` | unset | Your Hugging Face token ([get one here](https://huggingface.co/settings/tokens)). Avoids rate-limit warnings/throttling on model downloads. |
   | `HF_XET_HIGH_PERFORMANCE` | `1` (set automatically by `transcribe.py`) | Enables extra parallelism in Hugging Face's Xet transfer client for faster model downloads. Set to `0` in `.env` to disable, e.g. on a constrained connection. |

   `.env` is loaded automatically from the repo directory on every run; both variables are optional.

## Usage

```bash
transcribe audio.mp3
transcribe audio.wav --model tiny
transcribe audio.m4a --model turbo --output transcript.txt
transcribe audio.mp3 --language es
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-m`, `--model` | `small` | Model name — see [Models](#models). Run `transcribe --help` for the full list. |
| `-l`, `--language` | auto-detect | Language code, e.g. `en`, `es`, `fr` |
| `-o`, `--output` | stdout | Output file path |

### Running the script directly

```bash
uv run transcribe.py audio.mp3
```

## Models

The `--model` flag accepts any model name FasterWhisper can resolve. The
common ones:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~40MB | ⚡⚡⚡ | ⭐ |
| base | ~140MB | ⚡⚡ | ⭐⭐ |
| small | ~466MB | ⚡ | ⭐⭐⭐ |
| medium | ~1.5GB | 🐢 | ⭐⭐⭐⭐ |
| large | ~3.1GB | 🐢🐢 | ⭐⭐⭐⭐⭐ |
| turbo | ~1.6GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |

`turbo` is usually the best trade-off for long files: near-`large` accuracy at
a fraction of the size and time.

Also available: version-pinned `large-v1`/`large-v2`/`large-v3`
(`large` is an alias for `large-v3`), English-only `.en` variants
(`tiny.en`, `base.en`, `small.en`, `medium.en`), and the smaller distilled
`distil-*` models. Run `transcribe --help` for the authoritative list — it is
read from FasterWhisper itself, so it stays correct as upstream adds models.

The first run for a given model size downloads it to `~/.cache/huggingface/` (not stored in this repo) — larger models can take a while. `transcribe` tells you up front whether the model is already cached locally or needs to be downloaded, so a slow first run for `medium`/`large` isn't mistaken for the tool hanging.

## Supported Audio Formats

MP3, WAV, M4A, FLAC, OGG, Opus, AAC

## Troubleshooting

**`uv: command not found`**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**`FFMPEG not found`**
- Install ffmpeg using the instructions in the Requirements section above.

**Unsupported audio format**
- Convert with ffmpeg: `ffmpeg -i input.m4b -acodec libmp3lame -ab 192k output.mp3`
