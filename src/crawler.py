import logging
import time
from collections import deque
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.parser import HTMLParser
from src.utils import (
    is_internal_url,
    normalize_url,
    wait_between_requests,
)


class WebCrawler:
    """Recursive website crawler with safety controls."""

    def __init__(
        self,
        seed_urls: list[str],
        max_depth: int = 1,
        max_pages: int = 10,
        request_delay: float = 1.0,
        request_timeout: int = 15,
        max_retries: int = 3,
        respect_robots: bool = True,
    ):
        self.seed_urls = [
            url.rstrip("/")
            for url in seed_urls
            if url
        ]

        self.max_depth = max_depth
        self.max_pages = max_pages
        self.request_delay = request_delay
        self.request_timeout = request_timeout
        self.max_retries = max_retries
        self.respect_robots = respect_robots

        self.logger = logging.getLogger(__name__)

        self.parser = HTMLParser()

        self.session = self._create_session()

        self.visited_urls: set[str] = set()
        self.failed_urls: list[str] = []
        self.pages: list[dict] = []

        self.start_time = 0.0
        self.end_time = 0.0

        self.robots_cache: dict[
            str,
            RobotFileParser
        ] = {}

    def _create_session(self) -> requests.Session:
        """Create an HTTP session with retry support."""

        session = requests.Session()

        retry_strategy = Retry(
            total=self.max_retries,
            connect=self.max_retries,
            read=self.max_retries,
            status=self.max_retries,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=[
                "HEAD",
                "GET",
            ],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        session.mount(
            "http://",
            adapter,
        )

        session.mount(
            "https://",
            adapter,
        )

        session.headers.update(
            {
                "User-Agent": (
                    "AlgoryxWebCrawler/1.0 "
                    "(Educational Project)"
                )
            }
        )

        return session

    def _get_robots_parser(
        self,
        url: str,
    ) -> RobotFileParser | None:
        """Load and cache robots.txt for a domain."""

        parsed_url = urlparse(url)

        robots_url = (
            f"{parsed_url.scheme}://"
            f"{parsed_url.netloc}/robots.txt"
        )

        if robots_url in self.robots_cache:
            return self.robots_cache[robots_url]

        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            parser.read()

            self.robots_cache[
                robots_url
            ] = parser

            return parser

        except Exception as error:
            self.logger.warning(
                "Could not read robots.txt: %s",
                error,
            )

            return None

    def _is_allowed_by_robots(
        self,
        url: str,
    ) -> bool:
        """Check whether robots.txt allows crawling a URL."""

        if not self.respect_robots:
            return True

        parser = self._get_robots_parser(url)

        if parser is None:
            return True

        return parser.can_fetch(
            "AlgoryxWebCrawler",
            url,
        )

    def _fetch_page(
        self,
        url: str,
    ) -> str | None:
        """Download a webpage with timeout and error handling."""

        try:
            self.logger.info(
                "Downloading: %s",
                url,
            )

            response = self.session.get(
                url,
                timeout=self.request_timeout,
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            if "text/html" not in content_type:
                self.logger.warning(
                    "Skipping non-HTML resource: %s",
                    url,
                )

                return None

            return response.text

        except requests.RequestException as error:
            self.logger.error(
                "Request failed for %s: %s",
                url,
                error,
            )

            return None

    def crawl(self) -> list[dict]:
        """Start recursive crawling from the seed URLs."""

        self.start_time = time.perf_counter()

        queue = deque(
            (
                url,
                0,
            )
            for url in self.seed_urls
        )

        while queue and len(
            self.visited_urls
        ) < self.max_pages:

            current_url, depth = queue.popleft()

            normalized_url = normalize_url(
                current_url,
                current_url,
            )

            if not normalized_url:
                continue

            if normalized_url in self.visited_urls:
                continue

            if depth > self.max_depth:
                continue

            if not self._is_allowed_by_robots(
                normalized_url
            ):
                self.logger.warning(
                    "Blocked by robots.txt: %s",
                    normalized_url,
                )

                self.visited_urls.add(
                    normalized_url
                )

                continue

            self.visited_urls.add(
                normalized_url
            )

            html = self._fetch_page(
                normalized_url
            )

            if html is None:
                self.failed_urls.append(
                    normalized_url
                )

                wait_between_requests(
                    self.request_delay
                )

                continue

            try:
                page_data = self.parser.parse(
                    normalized_url,
                    html,
                )

                self.pages.append(
                    page_data
                )

                self.logger.info(
                    "Parsed successfully: %s",
                    normalized_url,
                )

                if depth < self.max_depth:

                    for link in page_data[
                        "links"
                    ]:

                        absolute_url = normalize_url(
                            normalized_url,
                            link,
                        )

                        if not absolute_url:
                            continue

                        if not is_internal_url(
                            normalized_url,
                            absolute_url,
                        ):
                            continue

                        if absolute_url in self.visited_urls:
                            continue

                        if len(
                            self.visited_urls
                        ) + len(queue) >= self.max_pages:
                            break

                        queue.append(
                            (
                                absolute_url,
                                depth + 1,
                            )
                        )

            except Exception as error:

                self.logger.exception(
                    "Parsing failed for %s: %s",
                    normalized_url,
                    error,
                )

                self.failed_urls.append(
                    normalized_url
                )

            wait_between_requests(
                self.request_delay
            )

        self.end_time = time.perf_counter()

        self.logger.info(
            "Crawling completed."
        )

        return self.pages

    def search_keyword(
        self,
        keyword: str,
    ) -> list[dict]:
        """Search collected page content for a keyword."""

        if not keyword:
            return self.pages

        search_term = keyword.lower()

        matches = []

        for page in self.pages:

            searchable_content = " ".join(
                [
                    page.get("title", ""),
                    " ".join(
                        page.get(
                            "headings",
                            [],
                        )
                    ),
                    " ".join(
                        page.get(
                            "paragraphs",
                            [],
                        )
                    ),
                ]
            ).lower()

            if search_term in searchable_content:
                matches.append(page)

        return matches

    def get_statistics(self) -> dict:
        """Return crawl statistics."""

        execution_time = 0.0

        if self.end_time:
            execution_time = (
                self.end_time
                - self.start_time
            )

        return {
            "pages_visited": len(
                self.visited_urls
            ),
            "pages_extracted": len(
                self.pages
            ),
            "failures": len(
                self.failed_urls
            ),
            "execution_time_seconds": round(
                execution_time,
                2,
            ),
        }

    def close(self):
        """Close the HTTP session."""

        self.session.close()