#!/usr/bin/env python3
"""
Audio transcription CLI using OpenAI's Whisper model.
Transcribes audio files to text using a local Whisper model.
"""

import argparse
import sys
import os
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("Error: faster-whisper is not installed.", file=sys.stderr)
    print("Install it with: uv sync  (or run via the 'transcribe' wrapper)", file=sys.stderr)
    sys.exit(1)

# Load .env from the script's directory if present
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _, _val = _line.partition("=")
            os.environ.setdefault(_key.strip(), _val.strip())

if not os.environ.get("HF_TOKEN"):
    print("Warning: HF_TOKEN not set. Create a .env file in the script directory with HF_TOKEN=your_token to avoid rate limits.", file=sys.stderr)

# huggingface_hub downloads model files over the Xet protocol by default
# (via the hf_xet package) when it's installed, which is already faster than
# plain HTTP. HF_XET_HIGH_PERFORMANCE opts into additional parallelism on
# top of that, unless the user has already set a preference explicitly.
os.environ.setdefault("HF_XET_HIGH_PERFORMANCE", "1")


# CTranslate2 repack of the model used by faster-whisper, per model name.
_FASTER_WHISPER_REPO_PREFIX = "Systran/faster-whisper-"


def _model_is_cached(model_name: str) -> bool:
    """
    Best-effort check for whether a FasterWhisper model is already fully
    downloaded to the local Hugging Face cache. Returns False (i.e. "assume
    a download is needed") if the cache can't be inspected for any reason.
    """
    try:
        from huggingface_hub import scan_cache_dir
    except ImportError:
        return False

    repo_id = _FASTER_WHISPER_REPO_PREFIX + model_name
    try:
        cache_info = scan_cache_dir()
    except Exception:
        return False

    for repo in cache_info.repos:
        if repo.repo_id != repo_id:
            continue
        for revision in repo.revisions:
            file_names = {f.file_name for f in revision.files}
            # model.bin is the large weights file; its presence in a
            # revision snapshot means the download completed (partial /
            # in-progress downloads live in blobs/*.incomplete and never
            # get linked into a revision's file list).
            if "model.bin" in file_names:
                return True
    return False


def transcribe_audio(audio_path: str, model_name: str = "small", language: str = None, output_format: str = "text") -> str:
    """
    Transcribe an audio file using FasterWhisper.
    
    Args:
        audio_path: Path to the audio file
        model_name: Whisper model size (tiny, base, small, medium, large)
        language: Language code (e.g., 'en', 'es'). Auto-detect if None.
        output_format: Output format ('text', 'json', 'vtt', 'srt', 'tsv')
    
    Returns:
        Transcribed text
    """
    audio_file = Path(audio_path)
    
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    supported_formats = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".opus", ".aac"}
    if audio_file.suffix.lower() not in supported_formats:
        raise ValueError(f"Unsupported audio format: {audio_file.suffix}. Supported: {supported_formats}")
    
    if _model_is_cached(model_name):
        print(f"Loading FasterWhisper model '{model_name}' (cached locally)...", file=sys.stderr)
    else:
        print(
            f"Model '{model_name}' not found in local cache — downloading from Hugging Face "
            "(this can take a while for larger models; progress will be shown below)...",
            file=sys.stderr,
        )
    model = WhisperModel(model_name)
    
    print(f"Transcribing audio file: {audio_path}", file=sys.stderr)
    segments, info = model.transcribe(str(audio_path), language=language)
    
    # Extract text from segments
    text = "".join([segment.text for segment in segments])
    
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to text using FasterWhisper (faster implementation of OpenAI's Whisper model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe.py audio.mp3
  python transcribe.py audio.wav --model tiny
  python transcribe.py audio.mp3 --output output.txt
  python transcribe.py audio.m4a --model large --language es
        """
    )
    
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to transcribe"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: small). Larger models are more accurate but slower."
    )
    
    parser.add_argument(
        "-l", "--language",
        help="Language code (e.g., 'en', 'es', 'fr'). Auto-detects if not specified."
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path. If not specified, prints to stdout."
    )
    
    args = parser.parse_args()
    
    try:
        text = transcribe_audio(
            audio_path=args.audio_file,
            model_name=args.model,
            language=args.language
        )
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Transcription saved to: {output_path}", file=sys.stderr)
        else:
            print(text)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
