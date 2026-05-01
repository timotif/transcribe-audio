# Audio Transcription CLI - FasterWhisper

A self-contained Python CLI tool for transcribing audio files to text using FasterWhisper, a faster implementation of OpenAI's Whisper model.

## Features

- **Faster transcription**: Uses FasterWhisper (2-5x faster than standard Whisper with minimal accuracy loss)
- **GPU optimized**: Automatically uses GPU acceleration when available
- **Local transcription**: Uses Whisper model entirely offline (after initial model download)
  - Smaller models are faster but less accurate
  - Larger models are more accurate but require more resources
- **Auto language detection**: Automatically detects the language, or specify manually
- **Flexible output**: Print to stdout or save to file
- **Supports multiple audio formats**: MP3, WAV, M4A, FLAC, OGG, Opus, AAC
- **Error handling**: Validates inputs and provides clear error messages

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

This will install `faster-whisper` - a much faster implementation of OpenAI's Whisper model.

### Use from anywhere (optional)

Symlink the `transcribe` wrapper into a directory on your `$PATH`. **Symlink — do not copy**, because the wrapper resolves its own location to find `transcribe.py`.

```bash
ln -s /path/to/repo/transcribe ~/.local/bin/transcribe
```

After that you can run `transcribe audio.mp3` from any directory.

## Features Overview

- **Multiple model sizes**: Choose from tiny, base, small, medium, or large models

## Usage

### Using the bash wrapper (after adding to PATH)
```bash
transcribe audio.mp3
transcribe audio.wav --model tiny
transcribe audio.m4a --model large --output transcript.txt
```

### Using the Python script directly
```bash
python transcribe.py --help
```

## Model Sizes

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~40MB | ⚡⚡⚡ | ⭐ |
| base | ~140MB | ⚡⚡ | ⭐⭐ |
| small | ~466MB | ⚡ | ⭐⭐⭐ |
| medium | ~1.5GB | 🐢 | ⭐⭐⭐⭐ |
| large | ~2.9GB | 🐢🐢 | ⭐⭐⭐⭐⭐ |

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- Opus (.opus)
- AAC (.aac)

## Requirements

- Python 3.9+
- FFMPEG (required by Whisper for audio processing)
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
  - **Windows**: Download from https://ffmpeg.org/download.html or use `choco install ffmpeg`

## Examples

Transcribe a podcast episode with the 'small' model:
```bash
python transcribe.py podcast.mp3 --model small --output podcast_transcript.txt
```

Transcribe a Spanish audio file and auto-detect language:
```bash
python transcribe.py spanish_audio.wav --model base
```

Transcribe and print to console:
```bash
python transcribe.py meeting.m4a --model medium
```

## Notes

- FasterWhisper is **2-5x faster** than standard Whisper with comparable accuracy
- The first run will download the Whisper model (~40MB-2.9GB depending on model size)
- Transcription speed depends on audio length and model size
- GPU acceleration is automatically used if available (NVIDIA CUDA, AMD ROCm, Apple Metal)
- For best results with poor audio quality, use larger models (medium/large)

## Troubleshooting

**ImportError: No module named 'whisper'**
- Run: `pip install -r requirements.txt`

**FileNotFoundError for audio file**
- Ensure the audio file path is correct and the file exists

**Unsupported audio format error**
- Convert your audio to a supported format (MP3, WAV, M4A, FLAC, OGG, Opus, AAC)
- Use ffmpeg: `ffmpeg -i input.m4b -acodec libmp3lame -ab 192k output.mp3`

**FFMPEG not found**
- Install FFMPEG using the instructions in the Requirements section

## License

This is a wrapper around FasterWhisper. See https://github.com/SYSTRAN/faster-whisper for more information.
