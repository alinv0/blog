#!/usr/bin/env python3
"""
generate-audio.py — Convert a blog article's markdown to an MP3 audio file.

Uses Azure AI Speech Service for high-quality neural text-to-speech.

Usage:
    python scripts/generate-audio.py <article-folder>

Environment variables:
    AZURE_SPEECH_KEY      — Azure Speech resource key
    AZURE_SPEECH_REGION   — Azure region (e.g. westeurope)

Example:
    python scripts/generate-audio.py execution-is-cheap-judgment-isnt
"""

import os
import re
import sys
import tempfile
from pathlib import Path

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("ERROR: azure-cognitiveservices-speech not installed.", file=sys.stderr)
    print("  Run: pip install azure-cognitiveservices-speech", file=sys.stderr)
    sys.exit(1)

VOICE = "en-US-AndrewMultilingualNeural"
OUTPUT_FILENAME = "audio.mp3"
TTS_TEXT_FILENAME = "audio-text.txt"


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by --- ... ---"""
    stripped = text.lstrip()
    if not stripped.startswith("---"):
        return text
    end = stripped.find("\n---", 3)
    if end < 0:
        return text
    return stripped[end + 4:].strip()


def markdown_to_plain_text(md: str) -> str:
    """Convert markdown to readable plain text for TTS."""
    text = md
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\\$", "", text, flags=re.MULTILINE)
    text = text.replace("Nginx", "Engine X").replace("nginx", "Engine X").replace("NGINX", "Engine X")
    return text.strip()


def build_ssml(text: str) -> str:
    """Wrap text in SSML with natural pacing and pauses."""
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    paragraphs = [" ".join(p.split()) for p in escaped.split("\n\n") if p.strip()]
    body = '<break time="600ms"/>'.join(f"<p>{p}</p>" for p in paragraphs)
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xml:lang="en-US">'
        f'<voice name="{VOICE}">'
        f'<prosody rate="0.95" pitch="-2%">'
        f'{body}'
        '</prosody>'
        '</voice></speak>'
    )


MAX_CHUNK_CHARS = 4000


def _split_into_chunks(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Split text into chunks at paragraph boundaries, respecting max_chars."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para) + 2  # account for \n\n separator
        if current and current_len + para_len > max_chars:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _synthesize_chunk(speech_config, ssml: str, output_path: Path) -> None:
    """Synthesize a single SSML chunk to an MP3 file."""
    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(output_path))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Speech synthesis canceled: {cancellation.reason}"
            + (f"\n  Details: {cancellation.error_details}" if cancellation.error_details else "")
        )


def generate_audio(text: str, output_path: Path) -> None:
    """Generate MP3 audio from text using Azure AI Speech, chunking long texts."""
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        print("ERROR: AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set.", file=sys.stderr)
        sys.exit(1)

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
    )

    chunks = _split_into_chunks(text)

    if len(chunks) == 1:
        ssml = build_ssml(chunks[0])
        _synthesize_chunk(speech_config, ssml, output_path)
        return

    print(f"  Splitting into {len(chunks)} chunks for synthesis...")
    chunk_files: list[Path] = []

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            for i, chunk in enumerate(chunks):
                chunk_path = Path(tmp_dir) / f"chunk_{i:03d}.mp3"
                print(f"  Chunk {i + 1}/{len(chunks)} ({len(chunk):,} chars)...")
                ssml = build_ssml(chunk)
                _synthesize_chunk(speech_config, ssml, chunk_path)
                chunk_files.append(chunk_path)

            with open(output_path, "wb") as out:
                for cf in chunk_files:
                    out.write(cf.read_bytes())
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate-audio.py <article-folder>")
        sys.exit(1)

    folder_name = sys.argv[1]
    script_dir = Path(__file__).resolve().parent
    blog_root = script_dir.parent
    article_dir = blog_root / folder_name

    if not article_dir.is_dir():
        print(f"ERROR: Folder not found: {article_dir}", file=sys.stderr)
        sys.exit(1)

    content_file = article_dir / "content.md"
    if not content_file.is_file():
        print(f"ERROR: No content.md found in {folder_name}", file=sys.stderr)
        sys.exit(1)

    print(f"  Reading: {content_file.name}")
    raw = content_file.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    plain = markdown_to_plain_text(body)

    char_count = len(plain)
    print(f"  Text length: {char_count:,} characters")

    if char_count == 0:
        print("ERROR: No text content after stripping markdown", file=sys.stderr)
        sys.exit(1)

    tts_text_path = article_dir / TTS_TEXT_FILENAME
    tts_text_path.write_text(plain, encoding="utf-8")
    print(f"  TTS text: {tts_text_path.name}")

    output_path = article_dir / OUTPUT_FILENAME
    print(f"  Voice: {VOICE}")
    print(f"  Generating audio...")

    generate_audio(plain, output_path)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  Output: {output_path.name} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
