# TikTok Scraper

[![ci](https://github.com/quantumproxies/tiktok-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/tiktok-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape TikTok from Python or the command line: public profile stats (followers, following, total likes, video count, bio) and per-video metrics (views, likes, comments, shares, saves, duration, sound, hashtags), for up to 50 accounts or videos per run, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/tiktok-scraper
tiktok-scraper login
tiktok-scraper videos https://www.tiktok.com/@nasa/video/7668779420412284191 -o videos.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `tiktok-scraper profiles` | handles or profile URLs | Followers, likes, videos, bio, 16 fields per row ([fields and price](https://quanticdata.io/collectors/tiktok-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper)) | up to 50 |
| `tiktok-scraper videos` | video URLs or ids | Views, likes, comments, shares, saves, 39 fields per row ([fields and price](https://quanticdata.io/collectors/tiktok-video-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper)) | up to 50 |

## Sample output

A real row from `tiktok-scraper profiles nasa @natgeo --max-results 2` (2026-10-22):

```json
{
  "url": "https://www.tiktok.com/@nasa",
  "likes": 11300000,
  "posts": 58,
  "user_id": "7664638705177150477",
  "category": null,
  "platform": "tiktok",
  "username": "nasa",
  "verified": true,
  "biography": "Making the seemingly impossible, possible.",
  "followers": 2100000,
  "following": 23,
  "full_name": "NASA",
  "is_private": false,
  "is_business": false,
  "profile_pic": "https://p19-common-sign.tiktokcdn-us.com/tos-useast5-avt-0068-tx/e5143212a59c09a008bf50f487d54d1f~tplv-tiktokx-cropcenter:1080:1080.jpeg?dr=9640&refresh_token=ff01af68&x-expires=1792882800&x-signature=A5CNRQtyy3jRBwB7SquTBbN85IA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=useast5",
  "external_url": "science.nasa.gov/feature/artemis-ii-preliminary-lunar-science-report"
}
```

## Python

```python
from quanticdata_tiktok_scraper import TikTokScraper

tiktok = TikTokScraper()  # saved login, or QUANTICDATA_API_KEY

for p in tiktok.profiles(["nasa", "natgeo"]):
    print(p["username"], p["followers"], p["likes"], p["posts"])

videos = tiktok.videos(["https://www.tiktok.com/@nasa/video/7668779420412284191"])
for v in videos:
    print(v["video_id"], v["views"], v["likes"], v["comments"], v["shares"], v["saves"])
videos.to_csv("videos.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Video metrics over time**: Check the views, likes, comments, shares and saves of a list of videos every few hours and keep the history in one CSV, to see how a launch or a campaign post performs. See [`examples/video_metrics.py`](examples/video_metrics.py).
- **Creator tracking**: Snapshot followers, total likes and video count of a list of accounts every day, with the change since the last check. See [`examples/profile_tracker.py`](examples/profile_tracker.py).
- **Engagement report**: Rank a set of videos by engagement rate (likes, comments, shares and saves over views) with their sound, duration and hashtags, for content research. See [`examples/engagement_report.py`](examples/engagement_report.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `tiktok-scraper run <id> -o out.csv` collects it later.

### `tiktok-scraper profiles`

Public TikTok profile stats — followers, likes, videos, bio.

```
tiktok-scraper profiles USERNAMES [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `USERNAMES` | string[] |  | Handles (with or without @) or profile URLs. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many profiles to deliver at most (1–50). You pay only for delivered profiles. |

### `tiktok-scraper videos`

Per-video TikTok metrics — views, likes, comments, shares, saves.

```
tiktok-scraper videos VIDEOS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `VIDEOS` | string[] |  | Video URLs (https://www.tiktok.com/@user/video/123…) or numeric ids. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many videos to deliver at most (1–50). You pay only for delivered videos. |

## Output fields

<details><summary><code>tiktok-scraper profiles</code>: 16 fields</summary>

| Field | Type | Description |
|---|---|---|
| `platform` | string | instagram or tiktok. |
| `username` | string | Handle. |
| `user_id` | string or null | Platform-side account id. |
| `full_name` | string or null | Display name. |
| `biography` | string or null | Bio text. |
| `verified` | boolean | Verified badge. |
| `is_private` | boolean | Private account. |
| `is_business` | boolean | Business/creator account. |
| `category` | string or null | Account category when set. |
| `external_url` | string or null | Link in bio. |
| `followers` | integer or null | Follower count. |
| `following` | integer or null | Following count. |
| `posts` | integer or null | Posts (Instagram) or videos (TikTok). |
| `likes` | integer or null | Total likes — TikTok only, null on Instagram. |
| `profile_pic` | string or null | Profile picture URL. |
| `url` | string | Profile URL. |

</details>

<details><summary><code>tiktok-scraper videos</code>: 39 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based delivery order. |
| `video_id` | string | TikTok video id. |
| `url` | string | Video URL. |
| `description` | string or null | Caption. |
| `created_at` | string or null | Publish time (ISO 8601). |
| `author` | string or null | Author handle. |
| `author_name` | string or null | Author display name. |
| `author_id` | string or null | Author id. |
| `author_verified` | boolean | Author verified badge. |
| `author_followers` | integer or null | Author follower count. |
| `views` | integer or null | Play count. |
| `likes` | integer or null | Like count. |
| `comments` | integer or null | Comment count. |
| `shares` | integer or null | Share count. |
| `saves` | integer or null | Save/collect count. |
| `duration_seconds` | integer or null | Duration in seconds. |
| `music` | string or null | Music title. |
| `music_author` | string or null | Music author. |
| `hashtags` | string[] | Hashtags in the caption. |
| `cover` | string or null | Cover image URL. |
| `mentions` | string[] | Accounts mentioned in the caption. |
| `reposts` | integer or null | Repost count. |
| `author_following` | integer or null | Accounts the author follows. |
| `author_likes` | integer or null | Total likes on the author's videos. |
| `author_videos` | integer or null | Videos published by the author. |
| `author_signature` | string or null | Author bio. |
| `music_id` | string or null | TikTok sound id. |
| `music_original` | boolean or null | True when the sound is the author's original. |
| `location_created` | string or null | Country the video was posted from. |
| `language` | string or null | Caption language. |
| `width` | integer or null | Video width (px). |
| `height` | integer or null | Video height (px). |
| `is_ad` | boolean | Marked as an ad. |
| `ai_generated` | boolean | Labelled AI-generated by TikTok. |
| `duet_enabled` | boolean or null | Duets allowed. |
| `stitch_enabled` | boolean or null | Stitches allowed. |
| `is_photo_post` | boolean | Photo carousel rather than a video. |
| `subtitle_languages` | string[] | Subtitle languages available. |
| `related_searches` | string[] | Searches TikTok suggests next to the video. |

</details>

## Sign-in and API keys

- `tiktok-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `tiktok-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `tiktok-scraper login --api-key`.
- `tiktok-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/tiktok_profile/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"usernames": ["nasa", "@natgeo"], "max_results": 2}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this TikTok scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send handles or video URLs and get rows back; the requests run on QuanticData's side. You do not need a TikTok account either.

**What does it read?**

Public profiles and public videos only: the counts, captions and details that any visitor of the page sees. You are responsible for how you use the data and for respecting TikTok's terms.

**How many profiles or videos can one run return?**

Up to 50 profiles or 50 videos per run; ask for fewer with --max-results and you pay only for what is delivered. Videos take a full URL or the numeric video id.

**Can I export to CSV or Excel?**

Add -o videos.csv (or .json, .jsonl). List fields such as hashtags and mentions are joined with semicolons in one cell, so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/video_metrics.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Instagram Scraper](https://github.com/quantumproxies/instagram-scraper): Instagram scraper for Python and the command line.
- [YouTube Scraper](https://github.com/quantumproxies/youtube-scraper): YouTube scraper for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=tiktok-scraper).
