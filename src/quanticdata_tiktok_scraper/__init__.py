"""TikTok Scraper: TikTok scraper for Python and the command line: public profile stats (followers, likes, videos, bio) and per-video metrics (views, likes, comments, shares, saves, sound, hashtags) as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_tiktok_scraper import TikTokScraper

    scraper = TikTokScraper()   # saved login (`tiktok-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.profiles(...)   # public profile stats for one or more TikTok accounts
    run = scraper.videos(...)   # views, likes, comments, shares and saves of one or more videos
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["TikTokScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class TikTokScraper:
    """TikTok Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="tiktok-scraper/0.1.0 (+https://github.com/quantumproxies/tiktok-scraper)", timeout=timeout)

    def profiles(
        self, usernames: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public TikTok profile stats — followers, likes, videos, bio.

        Args:
            usernames: Handles (with or without @) or profile URLs.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many profiles to deliver at most (1–50). You pay only for delivered profiles.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per profile: see ``types.TiktokProfileRow``.
        """
        payload = {
            "usernames": _as_list(usernames),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("tiktok_profile", payload, wait=wait, timeout=timeout)

    def videos(
        self, videos: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Per-video TikTok metrics — views, likes, comments, shares, saves.

        Args:
            videos: Video URLs (https://www.tiktok.com/@user/video/123…) or numeric ids.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many videos to deliver at most (1–50). You pay only for delivered videos.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per video: see ``types.TiktokVideoRow``.
        """
        payload = {
            "videos": _as_list(videos),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("tiktok_video", payload, wait=wait, timeout=timeout)
