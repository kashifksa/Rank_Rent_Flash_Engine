"""
=============================================================
  YOUTUBE TRANSCRIPT SCRAPER
  Rank & Rent Pipeline — Research Tool
=============================================================

What this does:
  1. Reads YouTube video URLs from youtube_urls.txt (one per line)
  2. Automatically fetches the transcript/captions for each video
  3. Cleans the text (removes timestamps, filler words)
  4. Saves everything to youtube_data.txt for review
  5. You copy relevant parts into data.txt

Usage:
  python youtube_scraper.py
  python youtube_scraper.py --urls my_videos.txt --out youtube_data.txt

How to add URLs:
  Create a file called youtube_urls.txt in the same folder.
  Paste one YouTube URL per line. Example:

    https://www.youtube.com/watch?v=abc123
    https://youtu.be/xyz789
    https://www.youtube.com/watch?v=def456

No API key needed. Completely free.
=============================================================
"""

import sys
import os
import re
import time
import argparse
import textwrap
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("ERROR: youtube-transcript-api not installed.")
    print("Run: pip install youtube-transcript-api")
    sys.exit(1)

# Single shared API instance (v1.x uses instance methods)
_yt_api = YouTubeTranscriptApi()

# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def extract_video_id(url):
    """
    Extract the YouTube video ID from any YouTube URL format.
    Supports:
      https://www.youtube.com/watch?v=VIDEO_ID
      https://youtu.be/VIDEO_ID
      https://www.youtube.com/embed/VIDEO_ID
    """
    url = url.strip()

    # youtu.be short links
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0].strip()

    # Standard youtube.com/watch?v= links
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            return qs.get("v", [None])[0]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[1].split("?")[0]

    return None


def clean_transcript(raw_segments):
    """
    Convert raw transcript segments into clean readable text.
    Removes duplicate lines, filler words, and merges into paragraphs.
    """
    texts = []
    seen  = set()

    for seg in raw_segments:
        text = seg.get("text", "").strip()

        # Skip music/sound effect markers
        if re.match(r"^\[.*\]$", text):
            continue

        # Deduplicate repeated lines (common in auto-captions)
        if text.lower() in seen:
            continue
        seen.add(text.lower())

        texts.append(text)

    # Join into a single clean paragraph block
    full_text = " ".join(texts)

    # Clean up extra spaces
    full_text = re.sub(r"\s+", " ", full_text).strip()

    return full_text


def load_urls(filepath):
    """Load and validate YouTube URLs from a text file."""
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found.")
        print(f"Create a file called {filepath} and paste YouTube URLs into it (one per line).")
        sys.exit(1)

    urls = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue
            urls.append(line)

    return urls


# ─────────────────────────────────────────────────────────────
#  CORE SCRAPER
# ─────────────────────────────────────────────────────────────

def fetch_transcript(video_id):
    """
    Fetch transcript for a video ID using youtube-transcript-api v1.x.
    Tries English first, then falls back to any available language.
    Returns (transcript_text, language_used) or (None, error_message).
    """
    try:
        # ── Try English directly first (fastest path) ──
        try:
            fetched = _yt_api.fetch(video_id, languages=["en", "en-US", "en-GB"])
            raw_segments = [{"text": s.text} for s in fetched]
            return clean_transcript(raw_segments), "English"
        except Exception:
            pass

        # ── List all available transcripts and pick the best ──
        transcript_list = _yt_api.list(video_id)
        available = list(transcript_list)

        if not available:
            return None, "No transcripts available for this video"

        # Pick first available transcript
        best = available[0]
        lang = best.language

        fetched      = _yt_api.fetch(video_id, languages=[best.language_code])
        raw_segments = [{"text": s.text} for s in fetched]
        clean_text   = clean_transcript(raw_segments)
        return clean_text, f"{lang} (auto)"

    except Exception as e:
        err = str(e)
        if "disabled" in err.lower():
            return None, "Transcripts disabled by video owner"
        if "Could not retrieve" in err or "no element" in err.lower():
            return None, "No transcript available for this video"
        return None, f"Error: {err}"


# ─────────────────────────────────────────────────────────────
#  OUTPUT WRITER
# ─────────────────────────────────────────────────────────────

def save_results(results, niche, output_path):
    """Write all transcripts to a clean, organized output file."""

    successful = [r for r in results if r["transcript"]]
    failed     = [r for r in results if not r["transcript"]]

    lines = []

    # ── HEADER ──
    lines += [
        "=" * 70,
        "  YOUTUBE TRANSCRIPT DATA",
        f"  Niche    : {niche}",
        f"  Scraped  : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"  Videos   : {len(results)} total | {len(successful)} transcribed | {len(failed)} failed",
        "=" * 70,
        "",
        "HOW TO USE:",
        "  Review each transcript below.",
        "  Copy relevant customer language, pain points, and insights",
        "  into the matching sections of your data.txt file.",
        "",
    ]

    # ── SUCCESSFUL TRANSCRIPTS ──
    if successful:
        lines += [
            "=" * 70,
            f"  TRANSCRIPTS ({len(successful)} videos)",
            "=" * 70,
        ]

        for i, result in enumerate(successful, 1):
            word_count = len(result["transcript"].split())
            lines += [
                "",
                f"VIDEO {i}",
                f"  URL      : {result['url']}",
                f"  Video ID : {result['video_id']}",
                f"  Language : {result['language']}",
                f"  Words    : {word_count:,}",
                "",
                "  TRANSCRIPT:",
                "  " + "-" * 60,
            ]

            # Break transcript into readable paragraphs (~100 words each)
            words      = result["transcript"].split()
            chunk_size = 100
            chunks     = [
                " ".join(words[i: i + chunk_size])
                for i in range(0, len(words), chunk_size)
            ]
            for chunk in chunks:
                lines.append(f"  {chunk}")
                lines.append("")

    # ── FAILED VIDEOS ──
    if failed:
        lines += [
            "",
            "=" * 70,
            f"  FAILED / SKIPPED ({len(failed)} videos)",
            "=" * 70,
        ]
        for result in failed:
            lines += [
                f"  URL    : {result['url']}",
                f"  Reason : {result['error']}",
                "",
            ]

    # ── FOOTER ──
    lines += [
        "=" * 70,
        f"  END — {len(successful)} transcripts saved to {output_path}",
        "=" * 70,
    ]

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return len(successful), len(failed)


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Transcript Scraper for Rank & Rent research pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Steps:
          1. Create youtube_urls.txt and paste your YouTube URLs (one per line)
          2. Run: python youtube_scraper.py --niche "Sprinkler Repair"
          3. Review youtube_data.txt
          4. Copy relevant content into data.txt

        Example youtube_urls.txt:
          https://www.youtube.com/watch?v=abc123
          https://youtu.be/xyz789
          # This is a comment and will be skipped
        """)
    )

    parser.add_argument("--niche", default="Unknown Niche", help='Your niche e.g. "Sprinkler Repair"')
    default_out = "raw_research/youtube_transcript.txt" if os.path.exists("raw_research") else "youtube_data.txt"
    default_urls = "raw_research/youtube_urls.txt" if os.path.exists("raw_research/youtube_urls.txt") else "youtube_urls.txt"
    parser.add_argument("--urls",  default=default_urls, help=f"File with YouTube URLs (default: {default_urls})")
    parser.add_argument("--out",   default=default_out, help=f"Output file (default: {default_out})")

    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  YOUTUBE TRANSCRIPT SCRAPER")
    print(f"  Niche : {args.niche}")
    print(f"  Input : {args.urls}")
    print(f"  Output: {args.out}")
    print("=" * 60)

    # ── Step 1: Load URLs ──
    print(f"\n[Step 1] Loading URLs from {args.urls}...")
    urls = load_urls(args.urls)
    print(f"  Found {len(urls)} URL(s) to process")

    if not urls:
        print("\nNo URLs found. Add YouTube URLs to the file and try again.")
        sys.exit(0)

    # ── Step 2: Fetch transcripts ──
    print(f"\n[Step 2] Fetching transcripts...")
    results = []

    for i, url in enumerate(urls, 1):
        print(f"\n  [{i}/{len(urls)}] {url}")

        video_id = extract_video_id(url)
        if not video_id:
            print(f"    ERROR: Could not extract video ID from URL")
            results.append({
                "url":        url,
                "video_id":   None,
                "transcript": None,
                "language":   None,
                "error":      "Invalid YouTube URL format",
            })
            continue

        print(f"    Video ID : {video_id}")
        transcript, lang_or_error = fetch_transcript(video_id)

        if transcript:
            word_count = len(transcript.split())
            print(f"    Status   : OK — {word_count:,} words ({lang_or_error})")
            results.append({
                "url":        url,
                "video_id":   video_id,
                "transcript": transcript,
                "language":   lang_or_error,
                "error":      None,
            })
        else:
            print(f"    Status   : FAILED — {lang_or_error}")
            results.append({
                "url":        url,
                "video_id":   video_id,
                "transcript": None,
                "language":   None,
                "error":      lang_or_error,
            })

        # Small delay between requests to be respectful
        if i < len(urls):
            time.sleep(1)

    # ── Step 3: Save output ──
    print(f"\n[Step 3] Saving results to {args.out}...")
    successful, failed = save_results(results, args.niche, args.out)

    print()
    print("=" * 60)
    print(f"  DONE!")
    print(f"  {successful} transcripts saved  |  {failed} failed")
    print(f"  Open {args.out} and copy relevant")
    print(f"  content into your data.txt file.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
