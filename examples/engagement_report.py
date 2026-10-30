"""Rank TikTok videos by engagement rate.

    python engagement_report.py @videos.txt --out engagement.csv

Takes video URLs or ids (on the command line or as @file.txt, one per line),
computes the engagement rate of each one as (likes + comments + shares + saves)
divided by views, and writes the videos sorted by that rate, with their sound,
duration, hashtags and publish time.
"""

import argparse

from quanticdata_tiktok_scraper import TikTokScraper, write


def read_videos(values: list) -> list:
    videos = []
    for value in values:
        if value.startswith("@") and value.endswith(".txt"):
            with open(value[1:], encoding="utf-8") as fh:
                videos += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        else:
            videos.append(value)
    return videos


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("videos", nargs="+", help="video URLs, numeric ids or @file.txt")
    parser.add_argument("--out", default="engagement.csv")
    args = parser.parse_args()

    videos = read_videos(args.videos)
    tiktok = TikTokScraper()
    rows = []
    for i in range(0, len(videos), 50):  # up to 50 videos per run
        for v in tiktok.videos(videos[i:i + 50], max_results=50):
            views = v.get("views") or 0
            actions = sum(v.get(k) or 0 for k in ("likes", "comments", "shares", "saves"))
            rows.append({
                "video_id": v["video_id"],
                "author": v.get("author"),
                "created_at": v.get("created_at"),
                "views": views,
                "engagement_rate_percent": round(100 * actions / views, 2) if views else None,
                "likes": v.get("likes"),
                "comments": v.get("comments"),
                "shares": v.get("shares"),
                "saves": v.get("saves"),
                "duration_seconds": v.get("duration_seconds"),
                "music": v.get("music"),
                "music_original": v.get("music_original"),
                "hashtags": v.get("hashtags"),
                "url": v.get("url"),
            })
    rows.sort(key=lambda r: r["engagement_rate_percent"] or 0, reverse=True)

    for r in rows[:10]:
        rate = "n/a" if r["engagement_rate_percent"] is None else f"{r['engagement_rate_percent']}%"
        print(f"{rate:>7}  {r['views']:>12,} views  @{r['author']}  {r['video_id']}")
    write(rows, args.out)
    print(f"{len(rows)} videos written to {args.out}")


if __name__ == "__main__":
    main()
