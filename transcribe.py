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
    import whisper
except ImportError:
    print("Error: whisper is not installed.", file=sys.stderr)
    print("Install it with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


def transcribe_audio(audio_path: str, model_name: str = "base", language: str = None, output_format: str = "text") -> str:
    """
    Transcribe an audio file using Whisper.
    
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
    
    print(f"Loading Whisper model '{model_name}'...", file=sys.stderr)
    model = whisper.load_model(model_name)
    
    print(f"Transcribing audio file: {audio_path}", file=sys.stderr)
    result = model.transcribe(str(audio_path), language=language)
    
    return result["text"]


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to text using OpenAI's Whisper model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe.py audio.mp3
  python transcribe.py audio.wav --model small --language en
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
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base). Larger models are more accurate but slower."
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
