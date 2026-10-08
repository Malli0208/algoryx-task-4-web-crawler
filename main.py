import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from src.crawler import WebCrawler
from src.exporter import DataExporter
from src.utils import setup_logging


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Intelligent Website Crawler "
            "and Data Extraction Engine"
        )
    )

    parser.add_argument(
        "--url",
        nargs="+",
        help="One or more seed URLs to crawl.",
    )

    parser.add_argument(
        "--depth",
        type=int,
        help="Maximum crawl depth.",
    )

    parser.add_argument(
        "--pages",
        type=int,
        help="Maximum number of pages to crawl.",
    )

    parser.add_argument(
        "--keyword",
        help="Keyword to search in collected content.",
    )

    return parser.parse_args()


def get_boolean_env(
    name: str,
    default: bool,
) -> bool:
    """Read a boolean value from environment variables."""

    value = os.getenv(
        name,
        str(default),
    ).lower()

    return value in {
        "true",
        "1",
        "yes",
        "y",
    }


def main():
    """Run the complete web crawler application."""

    load_dotenv()

    logger = setup_logging()

    args = parse_arguments()

    seed_urls = args.url

    if not seed_urls:
        configured_urls = os.getenv(
            "SEED_URLS",
            "",
        )

        seed_urls = [
            url.strip()
            for url in configured_urls.split(",")
            if url.strip()
        ]

    if not seed_urls:
        raise ValueError(
            "No seed URL provided. "
            "Use --url or configure SEED_URLS in .env."
        )

    max_depth = (
        args.depth
        if args.depth is not None
        else int(
            os.getenv(
                "MAX_DEPTH",
                "1",
            )
        )
    )

    max_pages = (
        args.pages
        if args.pages is not None
        else int(
            os.getenv(
                "MAX_PAGES",
                "10",
            )
        )
    )

    request_delay = float(
        os.getenv(
            "REQUEST_DELAY",
            "1",
        )
    )

    request_timeout = int(
        os.getenv(
            "REQUEST_TIMEOUT",
            "15",
        )
    )

    max_retries = int(
        os.getenv(
            "MAX_RETRIES",
            "3",
        )
    )

    respect_robots = get_boolean_env(
        "RESPECT_ROBOTS",
        True,
    )

    keyword = (
        args.keyword
        if args.keyword is not None
        else os.getenv(
            "KEYWORD",
            "",
        )
    )

    logger.info(
        "Starting Intelligent Website Crawler"
    )

    logger.info(
        "Seed URLs: %s",
        seed_urls,
    )

    logger.info(
        "Maximum depth: %s",
        max_depth,
    )

    logger.info(
        "Maximum pages: %s",
        max_pages,
    )

    crawler = WebCrawler(
        seed_urls=seed_urls,
        max_depth=max_depth,
        max_pages=max_pages,
        request_delay=request_delay,
        request_timeout=request_timeout,
        max_retries=max_retries,
        respect_robots=respect_robots,
    )

    try:
        pages = crawler.crawl()

        exporter = DataExporter(
            OUTPUT_DIR
        )

        json_file = exporter.export_json(
            pages
        )

        csv_file = exporter.export_csv(
            pages
        )

        statistics = crawler.get_statistics()

        print("\n" + "=" * 60)
        print("INTELLIGENT WEBSITE CRAWLER")
        print("=" * 60)

        print(
            f"Pages visited   : "
            f"{statistics['pages_visited']}"
        )

        print(
            f"Pages extracted : "
            f"{statistics['pages_extracted']}"
        )

        print(
            f"Failures        : "
            f"{statistics['failures']}"
        )

        print(
            f"Execution time  : "
            f"{statistics['execution_time_seconds']} seconds"
        )

        print(
            f"JSON output     : {json_file}"
        )

        print(
            f"CSV output      : {csv_file}"
        )

        if keyword:
            matches = crawler.search_keyword(
                keyword
            )

            print(
                f"Keyword         : {keyword}"
            )

            print(
                f"Keyword matches : {len(matches)}"
            )

            for page in matches:
                print(
                    f"  - {page['url']}"
                )

        print("=" * 60)

        logger.info(
            "Crawler execution completed successfully."
        )

    except Exception as error:

        logger.exception(
            "Crawler execution failed: %s",
            error,
        )

        print(
            f"\nCrawler failed: {error}"
        )

    finally:

        crawler.close()

        logger.info(
            "Crawler resources closed."
        )


if __name__ == "__main__":
    main()