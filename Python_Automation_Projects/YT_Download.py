#!/usr/bin/env python3
"""
YouTube Video Downloader
━━━━━━━━━━━━━━━━━━━━━━━
Downloads a YouTube video to your local system in best quality.

Requirements:
    pip install yt-dlp

Usage:
    python yt_downloader.py
    python yt_downloader.py --url "https://youtu.be/VIDEO_ID"
    python yt_downloader.py --url URL --quality 720
    python yt_downloader.py --url URL --output "C:/Videos"
    python yt_downloader.py --url URL --audio-only
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# ── Dependency check ──────────────────────────────────────────────────────────

def check_dependencies():
    try:
        import yt_dlp
    except ImportError:
        print("\n❌  Missing package: yt-dlp")
        print("    Run: pip install yt-dlp\n")
        sys.exit(1)

check_dependencies()

import yt_dlp

# ── Colors ────────────────────────────────────────────────────────────────────

C = {
    "reset":"\033[0m","bold":"\033[1m","dim":"\033[2m",
    "red":"\033[91m","green":"\033[92m","yellow":"\033[93m",
    "cyan":"\033[96m","white":"\033[97m","blue":"\033[94m",
}

def c(text, *cols):
    return "".join(C.get(x,"") for x in cols) + str(text) + C["reset"]

def banner():
    print(c("""
╔══════════════════════════════════════════════════════╗
║        YouTube Video Downloader  📥                  ║
║        Saves video directly to your PC               ║
╚══════════════════════════════════════════════════════╝
""", "cyan", "bold"))

def ok(msg):   print(c(f"   ✅  {msg}", "green"))
def warn(msg): print(c(f"   ⚠️   {msg}", "yellow"))
def info(msg): print(c(f"   ℹ️   {msg}", "dim"))
def err(msg):  print(c(f"   ❌  {msg}", "red"))
def step(msg): print(c(f"\n▶  {msg}", "bold", "white"))

# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt_size(bytes_val):
    if not bytes_val: return "Unknown size"
    mb = bytes_val / 1_000_000
    return f"{mb:.1f} MB" if mb < 1000 else f"{mb/1000:.2f} GB"

def fmt_duration(seconds):
    if not seconds: return "Unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

QUALITIES = {
    "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "1080": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
    "720":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
    "480":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
    "360":  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best",
    "audio":"bestaudio[ext=m4a]/bestaudio",
}

# ── Fetch video info ──────────────────────────────────────────────────────────

def get_video_info(url: str) -> dict:
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# ── Download ──────────────────────────────────────────────────────────────────

def download_video(url: str, output_dir: Path, quality: str, audio_only: bool):
    fmt = QUALITIES["audio"] if audio_only else QUALITIES.get(quality, QUALITIES["best"])
    ext = "mp3" if audio_only else "mp4"

    # Output template: saves as "Title [VideoID].mp4" inside output_dir
    outtmpl = str(output_dir / f"%(title)s [%(id)s].{ext}")

    last_status = {}

    def progress_hook(d):
        if d["status"] == "downloading":
            pct      = d.get("_percent_str", "?%").strip()
            speed    = d.get("_speed_str",   "?").strip()
            eta      = d.get("_eta_str",     "?").strip()
            total    = fmt_size(d.get("total_bytes") or d.get("total_bytes_estimate"))
            downloaded = fmt_size(d.get("downloaded_bytes", 0))
            print(f"\r   {c('⟳','cyan')}  {c(pct,'bold','cyan')}  "
                  f"{downloaded} / {total}  "
                  f"{c(speed,'white')}  ETA {eta}        ",
                  end="", flush=True)
            last_status["filename"] = d.get("filename","")

        elif d["status"] == "finished":
            print()
            last_status["filename"] = d.get("filename","")

    ydl_opts = {
        "format":                fmt,
        "outtmpl":               outtmpl,
        "merge_output_format":   ext,
        "progress_hooks":        [progress_hook],
        "quiet":                 True,
        "no_warnings":           True,
        "postprocessors": [
            {
                "key":            "FFmpegVideoConvertor",
                "preferedformat": ext,
            }
        ] if not audio_only else [
            {
                "key":            "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return last_status.get("filename", "")

# ── Quality picker ────────────────────────────────────────────────────────────

def pick_quality() -> str:
    print(c("\n  Select video quality:", "bold"))
    options = [
        ("1", "best",  "Best available quality (recommended)"),
        ("2", "1080",  "1080p Full HD"),
        ("3", "720",   "720p HD"),
        ("4", "480",   "480p"),
        ("5", "360",   "360p (smallest file)"),
        ("6", "audio", "Audio only (MP3)"),
    ]
    for num, key, label in options:
        print(f"   {c(num, 'cyan')}.  {label}")

    while True:
        try:
            choice = input(c("\n  Enter number [default 1]: ", "dim")).strip() or "1"
            idx    = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][1]
        except (ValueError, EOFError):
            pass
        print(c("  ⚠️  Invalid choice, try again.", "yellow"))

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Video Downloader — saves video to your local PC"
    )
    parser.add_argument("--url",        help="YouTube video URL")
    parser.add_argument("--quality",    default="", help="Quality: best/1080/720/480/360/audio")
    parser.add_argument("--output",     default="", help="Output folder path")
    parser.add_argument("--audio-only", action="store_true", help="Download audio only (MP3)")
    args = parser.parse_args()

    banner()

    # Check ffmpeg
    if not shutil.which("ffmpeg"):
        warn("ffmpeg not found — video+audio merging may fail.")
        warn("Install: https://ffmpeg.org/download.html\n")

    # ── URL ───────────────────────────────────────────────────────────────────
    url = args.url
    if not url:
        print(c("📎  Paste your YouTube video URL:", "bold"))
        url = input(c("  → ", "cyan")).strip()
    if not url:
        err("No URL provided."); sys.exit(1)

    # ── Output folder ─────────────────────────────────────────────────────────
    output_str = args.output
    if not output_str:
        print(c("\n📁  Where to save the video?", "bold"))
        print(c("    (Press Enter to save in current folder)", "dim"))
        output_str = input(c("  → ", "cyan")).strip().strip('"').strip("'")

    output_dir = Path(output_str) if output_str else Path.cwd() / "downloads"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Fetch video info ──────────────────────────────────────────────────────
    step("Fetching video info...")
    try:
        info_data = get_video_info(url)
    except Exception as e:
        err(f"Could not fetch video info: {e}")
        sys.exit(1)

    title    = info_data.get("title",    "Unknown")
    channel  = info_data.get("uploader", "Unknown")
    duration = info_data.get("duration", 0)
    views    = info_data.get("view_count", 0)

    print(f"\n   {c('Title:',   'cyan')}    {title}")
    print(f"   {c('Channel:', 'cyan')}  {channel}")
    print(f"   {c('Duration:','cyan')} {fmt_duration(duration)}")
    print(f"   {c('Views:',   'cyan')}    {views:,}")

    # ── Quality ───────────────────────────────────────────────────────────────
    audio_only = args.audio_only
    if args.quality:
        quality = args.quality.lower()
    elif audio_only:
        quality = "audio"
    else:
        quality = pick_quality()
        if quality == "audio":
            audio_only = True

    # ── Download ──────────────────────────────────────────────────────────────
    step(f"Downloading {'audio' if audio_only else quality + 'p' if quality != 'best' else 'best quality'} video...")
    info(f"Saving to: {output_dir.resolve()}")
    print()

    try:
        saved_file = download_video(url, output_dir, quality, audio_only)
    except yt_dlp.utils.DownloadError as e:
        err(f"Download failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        warn("Download cancelled by user.")
        sys.exit(0)
    except Exception as e:
        err(f"Unexpected error: {e}")
        sys.exit(1)

    # ── Find saved file ───────────────────────────────────────────────────────
    ext   = "mp3" if audio_only else "mp4"
    files = sorted(output_dir.glob(f"*.{ext}"), key=lambda f: f.stat().st_mtime, reverse=True)
    saved = Path(saved_file) if saved_file and Path(saved_file).exists() else \
            (files[0] if files else None)

    # ── Result ────────────────────────────────────────────────────────────────
    print(c(f"\n{'═'*54}", "cyan"))
    print(c("  ✅  Download Complete!", "bold", "green"))
    print(c(f"{'═'*54}", "cyan"))

    if saved and saved.exists():
        size = saved.stat().st_size / 1_000_000
        print(f"  {c('File:', 'cyan')}   {c(saved.name, 'white', 'bold')}")
        print(f"  {c('Size:', 'cyan')}   {size:.1f} MB")
        print(f"  {c('Saved:', 'cyan')}  {c(str(saved.resolve()), 'white')}")
    else:
        print(f"  {c('Folder:', 'cyan')} {c(str(output_dir.resolve()), 'white')}")

    print(c("\n  🎬  Video saved! You can now use it with local_shorts_extractor.py\n", "bold", "green"))

if __name__ == "__main__":
    main()