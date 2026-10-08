import logging
import time
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse


BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"


def setup_logging():
    """Configure application logging."""

    LOGS_DIR.mkdir(exist_ok=True)

    log_file = LOGS_DIR / "crawler.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
    )

    return logging.getLogger(__name__)


def normalize_url(base_url: str, link: str) -> str | None:
    """Convert a link into a canonical normalized URL."""

    if not link:
        return None

    absolute_url = urljoin(base_url, link)

    clean_url, _ = urldefrag(absolute_url)

    parsed = urlparse(clean_url)

    if parsed.scheme not in {"http", "https"}:
        return None

    # Normalize the hostname.
    hostname = parsed.netloc.lower()

    # Remove the default port.
    if hostname.endswith(":80") and parsed.scheme == "http":
        hostname = hostname[:-3]

    if hostname.endswith(":443") and parsed.scheme == "https":
        hostname = hostname[:-4]

    # Normalize the path.
    path = parsed.path or "/"

    # Treat / and /index.html as the same homepage.
    if path.lower() == "/index.html":
        path = "/"

    # Remove unnecessary trailing slash.
    if path != "/":
        path = path.rstrip("/")

    normalized_url = (
        f"{parsed.scheme}://"
        f"{hostname}"
        f"{path}"
    )

    # Preserve meaningful query parameters.
    if parsed.query:
        normalized_url += f"?{parsed.query}"

    return normalized_url


def is_internal_url(base_url: str, target_url: str) -> bool:
    """Check whether a target URL belongs to the same domain."""

    base_domain = urlparse(base_url).netloc.lower()
    target_domain = urlparse(target_url).netloc.lower()

    return base_domain == target_domain


def wait_between_requests(delay: float):
    """Pause execution between HTTP requests."""

    if delay > 0:
        time.sleep(delay)