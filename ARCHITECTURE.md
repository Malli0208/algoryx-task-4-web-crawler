# Architecture Documentation

## Intelligent Website Crawler & Data Extraction Engine

### 1. Overview

The Intelligent Website Crawler is a modular Python application designed to crawl websites, extract structured information from HTML pages, follow internal links recursively, and export collected data to JSON and CSV formats.

The application follows an object-oriented and modular architecture to separate crawling, parsing, exporting, utility functions, and application configuration.

---

## 2. High-Level Architecture

    ┌─────────────────────────┐
    │       User / CLI        │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │         main.py         │
    │   Application Entry     │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │      WebCrawler         │
    │     crawler.py          │
    └────────────┬────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
    HTTP Requests      robots.txt
    Retry / Timeout     Validation
        │
        ▼
    ┌─────────────────────────┐
    │       HTMLParser        │
    │        parser.py        │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │    Structured Data      │
    │                         │
    │ Titles                  │
    │ Headings                │
    │ Paragraphs              │
    │ Links                   │
    │ Images                  │
    │ Metadata                │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │      DataExporter       │
    │       exporter.py       │
    └────────────┬────────────┘
                 │
            ┌────┴────┐
            ▼         ▼
          JSON        CSV

---

## 3. Project Components

### 3.1 `main.py`

`main.py` is the application entry point.

Responsibilities:

- Load `.env` configuration
- Parse command-line arguments
- Configure crawler settings
- Create the `WebCrawler` object
- Start the crawling process
- Export crawl results
- Display crawl statistics
- Perform keyword searches
- Handle application-level exceptions
- Close crawler resources

---

### 3.2 `src/crawler.py`

`crawler.py` contains the main crawling engine.

The primary class is:

    WebCrawler

Responsibilities:

- Manage seed URLs
- Maintain the crawl queue
- Track visited URLs
- Control crawl depth
- Control maximum pages
- Download webpages
- Handle request retries
- Handle request timeouts
- Check `robots.txt`
- Follow internal links
- Ignore external links
- Prevent duplicate crawling
- Track failed URLs
- Measure execution time
- Search collected content
- Generate crawl statistics

The crawler uses a queue-based traversal approach.

---

## 4. Crawling Flow

The crawler follows this process:

    1. Read seed URLs
            │
            ▼
    2. Normalize URLs
            │
            ▼
    3. Check visited URLs
            │
            ▼
    4. Check robots.txt
            │
            ▼
    5. Download webpage
            │
            ▼
    6. Validate HTML response
            │
            ▼
    7. Parse HTML
            │
            ▼
    8. Extract webpage information
            │
            ▼
    9. Find internal links
            │
            ▼
    10. Add new URLs to queue
            │
            ▼
    11. Continue until depth/page limit
            │
            ▼
    12. Export results
            │
            ▼
    13. Display statistics

---

## 5. Queue-Based Crawling

The crawler uses Python's `collections.deque` to maintain URLs waiting to be processed.

Each queue entry contains:

    (url, depth)

Example:

    ("https://example.com/", 0)

When an internal link is discovered, it is added with an increased depth:

    ("https://example.com/about", 1)

This allows the crawler to control recursive crawling using `MAX_DEPTH`.

---

## 6. URL Normalization

The crawler normalizes URLs before processing them.

Normalization handles:

- URL fragments
- Trailing slashes
- `/index.html`
- Default HTTP ports
- Default HTTPS ports
- Hostname casing
- Relative URLs

Example:

    https://example.com
    https://example.com/
    https://example.com/index.html

are treated as the same homepage representation.

This reduces duplicate requests and improves crawl accuracy.

---

## 7. Internal Link Detection

Only links belonging to the same domain are followed.

For example, if the seed URL is:

    https://example.com/

Then:

    https://example.com/about

is considered an internal URL.

However:

    https://another-site.com/

is considered external and is ignored.

This prevents the crawler from unintentionally expanding into unrelated websites.

---

## 8. robots.txt Handling

The crawler supports `robots.txt` compliance through Python's `urllib.robotparser`.

When enabled:

    RESPECT_ROBOTS=true

the crawler checks whether a URL is allowed before downloading it.

The crawler caches robots parsers for domains to avoid repeatedly processing the same robots file.

---

## 9. HTTP Request Management

HTTP requests are handled using the `requests` library.

The crawler configures:

- HTTP sessions
- User-Agent
- Request timeout
- Retry attempts
- Retryable HTTP status codes
- Request delays

Retryable status codes include:

    429
    500
    502
    503
    504

This improves reliability when temporary network or server errors occur.

---

## 10. HTML Parsing

HTML parsing is handled by BeautifulSoup.

The main parser class is:

    HTMLParser

The parser receives:

    URL
    HTML content

and returns structured webpage information.

---

## 11. Data Extraction

The parser extracts the following information.

### Title

Extracts the webpage `<title>`.

### Headings

Extracts:

    H1
    H2
    H3
    H4
    H5
    H6

### Paragraphs

Extracts text from `<p>` elements.

### Hyperlinks

Extracts `href` values from `<a>` elements.

### Images

Extracts:

- Image source
- Alternative text

### Metadata

Extracts metadata from HTML `<meta>` elements.

The resulting structure contains:

    url
    title
    headings
    paragraphs
    links
    images
    metadata

---

## 12. Data Export

Data export is handled by:

    src/exporter.py

The main class is:

    DataExporter

The exporter supports two formats.

### JSON

JSON preserves the complete nested structure of the extracted webpage data.

Output:

    output/crawl_results.json

### CSV

CSV provides a tabular representation of the crawl results.

Output:

    output/crawl_results.csv

Lists are converted into readable text fields for CSV compatibility.

---

## 13. Configuration Management

Configuration is loaded using `python-dotenv`.

The application reads settings from:

    .env

Important configuration values include:

    SEED_URLS
    MAX_DEPTH
    MAX_PAGES
    REQUEST_DELAY
    REQUEST_TIMEOUT
    MAX_RETRIES
    RESPECT_ROBOTS
    KEYWORD

Command-line arguments can override selected configuration values.

---

## 14. Logging Architecture

Logging is implemented in:

    src/utils.py

Logs are written to:

    logs/crawler.log

The logging system records:

- Application startup
- Configuration
- URL downloads
- Successful parsing
- Request failures
- robots.txt restrictions
- Crawl completion
- Resource cleanup

Logging provides visibility into crawler execution and assists debugging.

---

## 15. Error Handling

The crawler uses exception handling at multiple levels.

### Network Errors

Handled using `requests.RequestException`.

### HTTP Errors

HTTP responses are validated using:

    response.raise_for_status()

### Parsing Errors

HTML parsing is wrapped with exception handling so one problematic page does not terminate the entire crawl.

### robots.txt Errors

Failures while accessing robots information are logged and handled gracefully.

### Export Errors

The application handles failures during result generation and logs the exception.

---

## 16. Keyword Search

After crawling, collected webpage content can be searched using a keyword.

The search checks:

- Page title
- Headings
- Paragraphs

Example:

    python main.py --keyword book

Matching pages are displayed in the command-line output.

---

## 17. Statistics

The crawler records:

- Number of visited URLs
- Number of successfully extracted pages
- Number of failures
- Total execution time

Example:

    Pages visited   : 10
    Pages extracted : 10
    Failures        : 0
    Execution time  : 19.89 seconds

---

## 18. Utility Module

`src/utils.py` contains reusable functionality.

### Logging

Creates the application logger.

### URL Normalization

Converts URLs into a consistent format.

### Internal URL Validation

Determines whether a URL belongs to the same domain.

### Request Delay

Controls the delay between requests.

Keeping these operations in a utility module reduces duplication across the application.

---

## 19. Directory Responsibilities

| Directory/File | Responsibility |
|---|---|
| `src/` | Core crawler application modules |
| `samples/` | Example JSON and CSV crawl results |
| `data/` | Reserved for generated/local data |
| `logs/` | Runtime application logs |
| `output/` | Generated crawl output |
| `.env` | Local configuration |
| `.gitignore` | Prevents sensitive/generated files from Git |
| `main.py` | Application entry point |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `ARCHITECTURE.md` | Architecture documentation |

---

## 20. Design Principles

The project follows several software engineering principles.

### Separation of Concerns

Each module has a specific responsibility:

- Crawler → crawling
- Parser → extraction
- Exporter → output generation
- Utilities → shared functionality
- Main → application orchestration

### Object-Oriented Design

The core crawler, parser, and exporter are implemented using classes.

### Reusability

Common functionality is isolated into reusable methods and utility functions.

### Configuration

Runtime settings are configurable without modifying the core source code.

### Maintainability

The modular structure makes individual components easier to test, modify, and extend.

### Error Resilience

Network and parsing failures are handled without unnecessarily terminating the complete crawl.

---

## 21. Security and Responsible Crawling

The project follows responsible crawling practices by providing:

- `robots.txt` support
- Configurable request delays
- Request timeouts
- Retry limits
- Maximum page limits
- Maximum crawl depth
- Internal-link restrictions

These controls help prevent uncontrolled crawling and excessive requests.

---

## 22. Future Architecture Improvements

Future versions could introduce:

- Asynchronous crawling with `asyncio`
- SQLite storage
- Sitemap generation
- Keyword frequency analysis
- Concurrent crawling
- Unit testing
- GitHub Actions CI
- Docker containerization
- Advanced crawl scheduling
- Persistent crawl state

---

## 23. Summary

The Intelligent Website Crawler uses a modular architecture to separate crawling, parsing, exporting, configuration, and utility operations.

The overall processing pipeline is:

    Configuration
         ↓
    Seed URLs
         ↓
    WebCrawler
         ↓
    HTTP Request
         ↓
    robots.txt Check
         ↓
    HTMLParser
         ↓
    Structured Data
         ↓
    Internal Link Discovery
         ↓
    Recursive Crawling
         ↓
    DataExporter
         ↓
    JSON + CSV

This architecture provides a clean foundation for extending the crawler with asynchronous processing, databases, testing, CI/CD, and other advanced features.