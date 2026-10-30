"""Track TikTok video metrics over time.

Reads video URLs or ids from videos.txt (one per line), fetches their current
views, likes, comments, shares and saves, and appends one row per video to
video_history.csv with a UTC timestamp. Run it from cron to see how a post
grows hour by hour:

    0 * * * *  cd /path/to/here && python video_metrics.py

Needs a login (`tiktok-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_tiktok_scraper import TikTokScraper

FIELDS = ["checked_at", "video_id", "author", "created_at", "views", "likes", "comments",
          "shares", "saves", "reposts", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--videos", default="videos.txt", help="file with one video URL or id per line")
    parser.add_argument("--out", default="video_history.csv")
    args = parser.parse_args()

    with open(args.videos, encoding="utf-8") as fh:
        videos = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    tiktok = TikTokScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        # The video collector takes up to 50 videos per run.
        for i in range(0, len(videos), 50):
            for video in tiktok.videos(videos[i:i + 50], max_results=50):
                writer.writerow({"checked_at": checked_at, **video})
                written += 1
    print(f"{written} videos appended to {args.out}")


if __name__ == "__main__":
    main()
