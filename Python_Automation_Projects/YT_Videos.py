#!/usr/bin/env python3
"""
Local Video → Viral Shorts Extractor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loads a video from your PC, uses Groq AI to detect the BEST moments,
then cuts and exports them as vertical 9:16 short clips with ffmpeg.

Requirements:
    pip install groq
    ffmpeg must be installed:
        Windows : https://ffmpeg.org/download.html  (add to PATH)
        Mac     : brew install ffmpeg
        Linux   : sudo apt install ffmpeg

FREE Groq API key: https://console.groq.com

Usage:
    python local_shorts_extractor.py
    python local_shorts_extractor.py --video "C:/Videos/myvideo.mp4" --shorts 5
    python local_shorts_extractor.py --video myvideo.mp4 --api-key gsk_xxx
    python local_shorts_extractor.py --video myvideo.mp4 --no-crop
    python local_shorts_extractor.py --video myvideo.mp4 --lang hindi
"""

import os
import re
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ── Dependency check ──────────────────────────────────────────────────────────

def check_dependencies():
    try:
        import groq
    except ImportError:
        print("\n❌  Missing package: groq")
        print("    Run: pip install groq\n")
        sys.exit(1)

    if not shutil.which("ffmpeg"):
        print("\n❌  ffmpeg not found in PATH.")
        print("    Windows : https://ffmpeg.org/download.html  → add C:\\ffmpeg\\bin to PATH")
        print("    Mac     : brew install ffmpeg")
        print("    Linux   : sudo apt install ffmpeg\n")
        sys.exit(1)

    if not shutil.which("ffprobe"):
        print("\n❌  ffprobe not found. It comes with ffmpeg — reinstall ffmpeg.\n")
        sys.exit(1)

check_dependencies()

import groq as groq_sdk

# ── Colors ────────────────────────────────────────────────────────────────────

C = {
    "reset":"\033[0m","bold":"\033[1m","dim":"\033[2m",
    "red":"\033[91m","green":"\033[92m","yellow":"\033[93m",
    "cyan":"\033[96m","white":"\033[97m",
}

def c(text, *cols):
    return "".join(C.get(x,"") for x in cols) + str(text) + C["reset"]

def banner():
    print(c("""
╔══════════════════════════════════════════════════════════╗
║   Local Video → Viral Shorts Extractor  ✂️  🎬           ║
║   Groq AI detects best moments • ffmpeg cuts clips       ║
╚══════════════════════════════════════════════════════════╝
""", "cyan", "bold"))

def step(msg):  print(c(f"\n▶  {msg}", "bold", "white"))
def ok(msg):    print(c(f"   ✅  {msg}", "green"))
def warn(msg):  print(c(f"   ⚠️   {msg}", "yellow"))
def info(msg):  print(c(f"   ℹ️   {msg}", "dim"))
def err(msg):   print(c(f"   ❌  {msg}", "red"))

# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt_time(seconds: float) -> str:
    s = int(seconds)
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def fmt_duration(seconds: int) -> str:
    if not seconds: return "Unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

def safe_name(text: str, maxlen: int = 40) -> str:
    text = re.sub(r"[^\w\s-]", "", str(text)).strip()
    return re.sub(r"\s+", "_", text)[:maxlen]

def viral_bar(score: int, width: int = 18) -> str:
    filled = round(score / 100 * width)
    bar    = "█" * filled + "░" * (width - filled)
    color  = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    return c(bar, color) + f"  {c(str(score)+'%', 'bold', color)}"

def progress_bar(done, total, width=28):
    filled = int(width * done / max(total, 1))
    bar    = "█" * filled + "░" * (width - filled)
    pct    = int(100 * done / max(total, 1))
    return f"[{bar}] {pct}%  ({done}/{total})"

# ── Video info via ffprobe ────────────────────────────────────────────────────

def get_video_info(video_path: Path) -> dict:
    """Get duration, width, height, fps from ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-show_format",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err(f"ffprobe failed: {result.stderr[:200]}")
        return {"duration": 0, "width": 1920, "height": 1080, "fps": 30}

    try:
        data     = json.loads(result.stdout)
        duration = float(data.get("format", {}).get("duration", 0))
        width    = 1920
        height   = 1080
        fps      = 30.0

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                width  = stream.get("width", 1920)
                height = stream.get("height", 1080)
                # Parse fps like "30/1" or "25"
                fps_raw = stream.get("r_frame_rate", "30/1")
                try:
                    if "/" in fps_raw:
                        n, d = fps_raw.split("/")
                        fps = float(n) / float(d)
                    else:
                        fps = float(fps_raw)
                except Exception:
                    fps = 30.0
                break

        return {
            "duration": int(duration),
            "width":    width,
            "height":   height,
            "fps":      round(fps, 2),
            "size_mb":  round(video_path.stat().st_size / 1_000_000, 1),
        }
    except Exception as e:
        warn(f"Could not parse video info: {e}")
        return {"duration": 0, "width": 1920, "height": 1080, "fps": 30, "size_mb": 0}

# ── Audio extraction + transcription ─────────────────────────────────────────

def extract_audio(video_path: Path, out_dir: Path) -> Path | None:
    """Extract audio from video as mp3 for transcription."""
    audio_path = out_dir / "audio_temp.mp3"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",                    # no video
        "-ar", "16000",           # 16kHz sample rate (Whisper prefers this)
        "-ac", "1",               # mono
        "-b:a", "64k",
        str(audio_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and audio_path.exists():
        return audio_path
    warn(f"Audio extraction failed: {result.stderr[-200:]}")
    return None

def _parse_segments(response) -> list[dict]:
    """
    Parse Groq Whisper response into list of {text, start, end}.
    Handles both object-style (seg.text) and dict-style (seg['text']) responses,
    which differ across groq SDK versions.
    """
    segments = []

    # Get raw segments list — could be attribute or dict key
    raw = None
    if hasattr(response, "segments"):
        raw = response.segments
    elif isinstance(response, dict):
        raw = response.get("segments", [])

    if raw:
        for seg in raw:
            try:
                if isinstance(seg, dict):
                    text  = seg.get("text", "").strip()
                    start = float(seg.get("start", 0))
                    end   = float(seg.get("end",   0))
                else:
                    text  = str(getattr(seg, "text",  "")).strip()
                    start = float(getattr(seg, "start", 0))
                    end   = float(getattr(seg, "end",   0))
                if text:
                    segments.append({"text": text, "start": start, "end": end})
            except Exception:
                continue

    # Fallback: use full text and estimate timestamps from word count
    if not segments:
        full_text = ""
        if hasattr(response, "text"):
            full_text = response.text or ""
        elif isinstance(response, dict):
            full_text = response.get("text", "")

        if full_text.strip():
            words = full_text.strip().split()
            # Estimate ~2.5 words per second (average speech)
            wps   = 2.5
            chunk = 75  # words per ~30s chunk
            for i in range(0, len(words), chunk):
                t_start = i / wps
                t_end   = (i + chunk) / wps
                segments.append({
                    "text":  " ".join(words[i:i+chunk]),
                    "start": t_start,
                    "end":   t_end,
                })

    return segments


def transcribe_with_groq(audio_path: Path, api_key: str, language: str = "en") -> list[dict]:
    """
    Transcribe audio using Groq's Whisper API.
    Returns list of {text, start, end} segments.
    """
    client = groq_sdk.Groq(api_key=api_key)

    # Groq Whisper supports files up to 25MB
    file_size_mb = audio_path.stat().st_size / 1_000_000
    info(f"Audio size: {file_size_mb:.1f} MB")

    if file_size_mb > 24:
        warn("Audio > 24MB — splitting into chunks for transcription...")
        return transcribe_in_chunks(audio_path, api_key, language)

    info("Transcribing audio with Groq Whisper...")
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file            = (audio_path.name, f, "audio/mpeg"),
            model           = "whisper-large-v3",
            response_format = "verbose_json",
            language        = language if language != "auto" else None,
            timestamp_granularities = ["segment"],
        )

    return _parse_segments(response)

def transcribe_in_chunks(audio_path: Path, api_key: str, language: str, chunk_mins: int = 10) -> list[dict]:
    """Split long audio into chunks and transcribe each."""
    client    = groq_sdk.Groq(api_key=api_key)
    chunk_dir = audio_path.parent / "chunks"
    chunk_dir.mkdir(exist_ok=True)

    chunk_secs = chunk_mins * 60
    all_segments = []
    chunk_index  = 0
    offset       = 0

    # Get total duration
    cmd = ["ffprobe","-v","quiet","-show_entries","format=duration",
           "-of","csv=p=0", str(audio_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        total_duration = float(res.stdout.strip())
    except Exception:
        total_duration = 3600  # fallback 1hr

    while offset < total_duration:
        chunk_path = chunk_dir / f"chunk_{chunk_index:03d}.mp3"
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(offset),
            "-i", str(audio_path),
            "-t", str(chunk_secs),
            "-c", "copy",
            str(chunk_path),
        ]
        subprocess.run(cmd, capture_output=True)

        if chunk_path.exists() and chunk_path.stat().st_size > 1000:
            info(f"Transcribing chunk {chunk_index+1} ({fmt_time(offset)} → {fmt_time(min(offset+chunk_secs, total_duration))})...")
            try:
                with open(chunk_path, "rb") as f:
                    response = client.audio.transcriptions.create(
                        file            = (chunk_path.name, f, "audio/mpeg"),
                        model           = "whisper-large-v3",
                        response_format = "verbose_json",
                        language        = language if language != "auto" else None,
                        timestamp_granularities = ["segment"],
                    )
                for seg in _parse_segments(response):
                    all_segments.append({
                        "text":  seg["text"],
                        "start": seg["start"] + offset,
                        "end":   seg["end"]   + offset,
                    })
            except Exception as e:
                warn(f"Chunk {chunk_index} transcription failed: {e}")

        offset      += chunk_secs
        chunk_index += 1

    # Cleanup chunks
    shutil.rmtree(chunk_dir, ignore_errors=True)
    return all_segments

# ── Groq AI moment detection ──────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a viral YouTube Shorts editor. "
    "Analyze transcripts and find the most engaging self-contained moments "
    "for 30-60 second short clips. "
    "Respond ONLY with valid JSON — no markdown, no backticks."
)

def detect_best_moments(
    segments:       list[dict],
    num_shorts:     int,
    video_duration: int,
    video_name:     str,
    api_key:        str,
) -> tuple[list[dict], str]:
    """Use Groq AI to pick the best clip timestamps."""

    # Format transcript with timestamps
    lines = []
    for seg in segments:
        m, s = divmod(int(seg["start"]), 60)
        lines.append(f"[{m:02d}:{s:02d}] {seg['text']}")
    transcript_text = "\n".join(lines)

    # Trim to fit context window
    if len(transcript_text) > 8000:
        transcript_text = transcript_text[:8000] + "\n...(truncated)"

    prompt = f"""Analyze this video transcript and identify the {num_shorts} BEST moments to extract as viral YouTube Shorts / Reels / TikToks.

Video file: "{video_name}"
Total Duration: {fmt_duration(video_duration)}

Transcript with timestamps:
{transcript_text}

Selection rules:
- Each clip: EXACTLY 20-25 seconds long (hard limit — max 25s, min 18s)
- Must be self-contained (viewer understands without prior context)
- Pick moments with: strong hooks, surprising facts, emotional peaks, actionable tips, or funny moments
- Clips must NOT overlap
- Add 1 second buffer before the interesting content
- Prefer punchy high-energy moments that work in under 25 seconds
- End on a complete sentence, not mid-word

Return ONLY this JSON (no other text):
{{
  "moments": [
    {{
      "number": 1,
      "title": "Catchy clip title (max 8 words)",
      "start_seconds": 45,
      "end_seconds": 90,
      "hook": "Why this grabs attention in 3 seconds",
      "why_viral": "One sentence why this will go viral",
      "viral_score": 88,
      "content_type": "tip|story|fact|funny|emotional|tutorial|rant|reveal"
    }}
  ],
  "video_summary": "2-sentence summary of the full video"
}}"""

    client   = groq_sdk.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature     = 0.6,
        max_tokens      = 2048,
        response_format = {"type": "json_object"},
    )

    raw  = response.choices[0].message.content.strip()
    data = json.loads(raw)

    moments = []
    for m in data.get("moments", []):
        start = max(0, int(m.get("start_seconds", 0)))
        end   = min(video_duration, int(m.get("end_seconds", start + 45)))
        if end - start < 10: continue
        if end - start > 25: end = start + 25
        if end - start < 18: end = start + 22
        m["start_seconds"] = start
        m["end_seconds"]   = end
        moments.append(m)

    return moments, data.get("video_summary", "")

# ── ffmpeg clip extraction ────────────────────────────────────────────────────

def make_watermark_vf(crop_vertical: bool) -> str:
    """
    Animated bouncing FinCode Hub watermark (DVD-screensaver style).
    Line 1: [YT] FinCode Hub  — white, bold, pulsing
    Line 2: [+] Subscribe     — yellow, pulsing
    Both bounce around the screen and never clip outside edges.
    """
    W  = 1080 if crop_vertical else 1920
    H  = 1920 if crop_vertical else 1080
    mx = W  - 380   # max x to keep text fully on screen
    my = H  - 100   # max y
    sx, sy = 85, 65 # bounce speed px/sec
    px = 2 * mx
    py = 2 * my

    # Triangular bounce wave (no commas inside — ffmpeg uses comma as filter sep)
    esc = "\\,"  # ffmpeg expression comma escape
    bx  = ("if(lt(mod(t*"+str(sx)+esc+str(px)+")"+esc+str(mx)+")"+esc
            +"mod(t*"+str(sx)+esc+str(px)+")"+esc+str(px)+"-mod(t*"+str(sx)+esc+str(px)+"))")
    by  = ("if(lt(mod(t*"+str(sy)+esc+str(py)+")"+esc+str(my)+")"+esc
            +"mod(t*"+str(sy)+esc+str(py)+")"+esc+str(py)+"-mod(t*"+str(sy)+esc+str(py)+"))")
    # Line 2 is 52px below line 1 — replicate full bounce expr + offset
    by2 = ("if(lt(mod(t*"+str(sy)+esc+str(py)+")"+esc+str(my)+")"+esc
            +"mod(t*"+str(sy)+esc+str(py)+")"+esc+str(py)+"-mod(t*"+str(sy)+esc+str(py)+"))"+"+52")

    # Smooth pulsing opacity
    op = "0.6+0.35*abs(sin(t*1.8))"

    l1 = (
        f"drawtext=text='[YT] FinCode Hub'"
        f":fontsize=42:fontcolor=white:alpha={op}"
        f":x={bx}:y={by}"
        f":shadowcolor=black:shadowx=3:shadowy=3"
        f":box=1:boxcolor=0x00000055:boxborderw=10"
    )
    l2 = (
        f"drawtext=text='[+] Subscribe'"
        f":fontsize=30:fontcolor=yellow:alpha={op}"
        f":x={bx}:y={by2}"
        f":shadowcolor=black:shadowx=2:shadowy=2"
        f":box=1:boxcolor=0x00000055:boxborderw=8"
    )
    return f"{l1},{l2}"


def extract_clip(
    source:        Path,
    start:         int,
    end:           int,
    out_path:      Path,
    crop_vertical: bool = True,
) -> bool:
    """Cut, crop to 9:16, and add animated FinCode Hub watermark."""
    duration = end - start

    # Base video filter (crop + scale)
    if crop_vertical:
        base_vf = "crop=ih*9/16:ih,scale=1080:1920,setsar=1"
    else:
        base_vf = "scale=trunc(iw/2)*2:trunc(ih/2)*2"

    # Animated watermark filter
    wm_vf = make_watermark_vf(crop_vertical)

    # Full filter: crop/scale then overlay watermark
    full_vf = f"{base_vf},{wm_vf}"

    cmd = [
        "ffmpeg", "-y",
        "-ss",      str(start),
        "-i",       str(source),
        "-t",       str(duration),
        "-vf",      full_vf,
        "-c:v",     "libx264",
        "-preset",  "fast",
        "-crf",     "23",
        "-c:a",     "aac",
        "-b:a",     "128k",
        "-movflags","+faststart",
        str(out_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# ── Report ────────────────────────────────────────────────────────────────────

def save_report(moments, video_path, out_dir, summary, video_info):
    lines = [
        "=" * 60,
        "LOCAL VIDEO → SHORTS EXTRACTION REPORT",
        f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        f"\nSource    : {video_path}",
        f"Duration  : {fmt_duration(video_info.get('duration',0))}",
        f"Resolution: {video_info.get('width','?')}x{video_info.get('height','?')}",
        f"FPS       : {video_info.get('fps','?')}",
        f"Size      : {video_info.get('size_mb','?')} MB",
        f"\nSummary   : {summary}",
        "\n" + "=" * 60,
    ]
    for m in moments:
        dur  = m['end_seconds'] - m['start_seconds']
        tags = f"{fmt_time(m['start_seconds'])} → {fmt_time(m['end_seconds'])}"
        lines += [
            f"\n--- SHORT #{m['number']}: {m['title']} ---",
            f"Timestamps : {tags}  ({dur}s)",
            f"Hook       : {m['hook']}",
            f"Why Viral  : {m['why_viral']}",
            f"Viral Score: {m['viral_score']}%",
            f"Type       : {m.get('content_type','')}",
            f"File       : short_{m['number']:02d}_{safe_name(m['title'])}.mp4",
            "-" * 60,
        ]
    path = out_dir / "extraction_report.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

# ── Main ──────────────────────────────────────────────────────────────────────

SUPPORTED_FORMATS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v"}

def main():
    parser = argparse.ArgumentParser(
        description="Local Video → Viral Shorts Extractor (Groq AI + ffmpeg)"
    )
    parser.add_argument("--video",      help="Path to your local video file")
    parser.add_argument("--shorts",     type=int, default=0, help="Number of shorts (1-10)")
    parser.add_argument("--api-key",    help="Groq API key (or set GROQ_API_KEY env var)")
    parser.add_argument("--output-dir", default="", help="Output folder (default: shorts_<videoname>)")
    parser.add_argument("--no-crop",    action="store_true", help="Keep original aspect ratio")
    parser.add_argument("--lang",       default="en", help="Audio language code (en, hi, es, auto...)")
    args = parser.parse_args()

    banner()

    # ── API Key ───────────────────────────────────────────────────────────────
    api_key = args.api_key or os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        print(c("🔑  Groq API Key needed (free at https://console.groq.com)\n", "yellow"))
        api_key = input(c("  Paste your Groq API key: ", "dim")).strip()
    if not api_key:
        err("No API key. Exiting."); sys.exit(1)

    # ── Video file ────────────────────────────────────────────────────────────
    video_path_str = args.video
    if not video_path_str:
        print(c("\n📁  Path to your video file:", "bold"))
        print(c("    (Drag and drop the file here, or type the full path)", "dim"))
        video_path_str = input(c("  → ", "cyan")).strip().strip('"').strip("'")

    video_path = Path(video_path_str)

    if not video_path.exists():
        err(f"File not found: {video_path}")
        sys.exit(1)

    if video_path.suffix.lower() not in SUPPORTED_FORMATS:
        warn(f"Unusual format: {video_path.suffix}. Supported: {', '.join(SUPPORTED_FORMATS)}")

    ok(f"Video found: {video_path.name}")

    # ── Num shorts ────────────────────────────────────────────────────────────
    num_shorts = args.shorts
    if not (1 <= num_shorts <= 10):
        try:
            raw = input(c("\n  How many shorts to extract? (1-10) [default 5]: ", "dim"))
            num_shorts = max(1, min(10, int(raw or "5")))
        except (ValueError, EOFError):
            num_shorts = 5

    crop_vertical = not args.no_crop
    language      = args.lang

    # ── Output directory ──────────────────────────────────────────────────────
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.output_dir) if args.output_dir else \
              video_path.parent / f"shorts_{safe_name(video_path.stem)}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    info(f"Output folder: {out_dir}")

    # ── Step 1: Video info ────────────────────────────────────────────────────
    step("Reading video info...")
    video_info = get_video_info(video_path)

    if not video_info["duration"]:
        err("Could not read video duration. Check the file is a valid video.")
        sys.exit(1)

    print(f"   {c('Duration:',  'cyan')}  {fmt_duration(video_info['duration'])}")
    print(f"   {c('Resolution:','cyan')}  {video_info['width']}x{video_info['height']}")
    print(f"   {c('FPS:',       'cyan')}  {video_info['fps']}")
    print(f"   {c('File size:', 'cyan')}  {video_info['size_mb']} MB")

    # ── Step 2: Extract audio ─────────────────────────────────────────────────
    step("Extracting audio from video...")
    audio_path = extract_audio(video_path, out_dir)

    if not audio_path:
        err("Audio extraction failed. Make sure the video has an audio track.")
        sys.exit(1)

    audio_mb = audio_path.stat().st_size / 1_000_000
    ok(f"Audio extracted ({audio_mb:.1f} MB)")

    # ── Step 3: Transcribe ────────────────────────────────────────────────────
    step(f"Transcribing audio with Groq Whisper (language: {language})...")
    info("This takes 10-60 seconds depending on video length...")

    try:
        segments = transcribe_with_groq(audio_path, api_key, language)
    except groq_sdk.AuthenticationError:
        err("Invalid Groq API key. Check at https://console.groq.com")
        sys.exit(1)
    except Exception as e:
        err(f"Transcription failed: {e}")
        sys.exit(1)
    finally:
        # Clean up temp audio
        if audio_path.exists():
            audio_path.unlink()

    if not segments:
        err("No transcript generated. The video may have no speech or unsupported language.")
        sys.exit(1)

    total_words = sum(len(s["text"].split()) for s in segments)
    ok(f"Transcribed {len(segments)} segments, ~{total_words} words")

    # Show sample
    if segments:
        sample = segments[0]["text"][:80]
        info(f'Sample: "{sample}..."')

    # ── Step 4: AI moment detection ───────────────────────────────────────────
    step("Asking Groq AI to detect best viral moments...")

    try:
        moments, summary = detect_best_moments(
            segments       = segments,
            num_shorts     = num_shorts,
            video_duration = video_info["duration"],
            video_name     = video_path.name,
            api_key        = api_key,
        )
    except groq_sdk.AuthenticationError:
        err("Invalid Groq API key.")
        sys.exit(1)
    except Exception as e:
        err(f"AI detection failed: {e}")
        sys.exit(1)

    if not moments:
        err("AI returned no valid moments. Try again or increase video length.")
        sys.exit(1)

    ok(f"AI detected {len(moments)} best moments!")
    if summary:
        print(c(f"\n   📋 {summary}", "dim"))

    print(c("\n   Detected moments:", "bold"))
    for m in moments:
        dur = m['end_seconds'] - m['start_seconds']
        num = m['number']
        print(f"   {c(f'#{num}', 'cyan', 'bold')}  "
              f"{fmt_time(m['start_seconds'])} → {fmt_time(m['end_seconds'])}  "
              f"({dur}s)  {viral_bar(m['viral_score'])}")
        print(f"       {c(m['title'], 'white')}  —  {c(m.get('content_type',''), 'dim')}")
        print(f"       {c(m['hook'], 'dim')}")

    # ── Step 5: Extract clips ─────────────────────────────────────────────────
    step(f"Cutting {len(moments)} clips with ffmpeg...")
    if crop_vertical:
        info("Cropping to vertical 9:16 (1080×1920) — ready for Shorts/Reels/TikTok")
    else:
        info("Keeping original aspect ratio (pass --no-crop to skip vertical crop)")

    clips_dir = out_dir / "shorts"
    clips_dir.mkdir(exist_ok=True)

    extracted = []
    for i, m in enumerate(moments, 1):
        clip_name = f"short_{m['number']:02d}_{safe_name(m['title'])}.mp4"
        clip_path = clips_dir / clip_name

        print(f"\n   {progress_bar(i-1, len(moments))}  {c(m['title'], 'dim')}")
        print(f"   Cutting {fmt_time(m['start_seconds'])} → {fmt_time(m['end_seconds'])}...")

        success = extract_clip(
            source        = video_path,
            start         = m["start_seconds"],
            end           = m["end_seconds"],
            out_path      = clip_path,
            crop_vertical = crop_vertical,
        )

        if success and clip_path.exists():
            size = clip_path.stat().st_size / 1_000_000
            ok(f"Saved → {clip_name}  ({size:.1f} MB)")
            extracted.append((m, clip_path))
        else:
            warn(f"Short #{m['number']} failed — skipping")

    print(f"\n   {progress_bar(len(moments), len(moments))}")

    # ── Step 6: Save report ───────────────────────────────────────────────────
    report = save_report(moments, video_path, out_dir, summary, video_info)
    ok(f"Report saved → {report.name}")

    # ── Final summary ─────────────────────────────────────────────────────────
    print(c(f"\n{'═'*58}", "cyan"))
    print(c(f"  🎬  Done! {len(extracted)}/{len(moments)} shorts extracted", "bold", "cyan"))
    print(c(f"{'═'*58}", "cyan"))
    print(f"  📁  Output folder : {c(str(out_dir.resolve()), 'white', 'bold')}")
    print(f"  📂  Clips folder  : {c(str(clips_dir.resolve()), 'white')}")
    print()

    for m, path in extracted:
        dur  = m['end_seconds'] - m['start_seconds']
        size = path.stat().st_size / 1_000_000
        num  = m['number']
        print(f"  {c('✓', 'green')} #{num:02d}  {c(path.name, 'white')}  "
              f"{dur}s  {size:.1f}MB  {viral_bar(m['viral_score'])}")

    print(c("\n  🚀  Upload directly to YouTube Shorts / Instagram Reels / TikTok!\n", "bold", "green"))

if __name__ == "__main__":
    main()