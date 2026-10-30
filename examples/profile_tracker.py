"""Track TikTok followers, total likes and video count of a list of accounts.

    python profile_tracker.py nasa natgeo nba --out profile_history.csv

Appends one row per account with a UTC timestamp and prints the change in
followers and likes since the previous check, so a daily cron job turns the
file into a growth history.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_tiktok_scraper import TikTokScraper

FIELDS = ["checked_at", "username", "full_name", "followers", "following", "likes", "posts", "verified"]


def previous(path: str) -> dict:
    """Latest followers and likes of each account in an existing history file."""
    last = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                last[row["username"]] = row
    return last


def delta(now, before) -> str:
    if now is None or not before:
        return "n/a"
    return f"{now - int(before):+,}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("handles", nargs="+", help="handles (with or without @) or profile URLs")
    parser.add_argument("--out", default="profile_history.csv")
    args = parser.parse_args()

    last = previous(args.out)
    tiktok = TikTokScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for i in range(0, len(args.handles), 50):  # up to 50 accounts per run
            for p in tiktok.profiles(args.handles[i:i + 50], max_results=50):
                writer.writerow({"checked_at": checked_at, **p})
                before = last.get(p["username"], {})
                print(f"{p['username']}: followers {delta(p.get('followers'), before.get('followers'))}, "
                      f"likes {delta(p.get('likes'), before.get('likes'))}")
    print(f"history in {args.out}")


if __name__ == "__main__":
    main()
