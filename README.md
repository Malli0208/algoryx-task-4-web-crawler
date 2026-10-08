# Intelligent Website Crawler & Data Extraction Engine

A production-oriented Python web crawler that automatically downloads webpages, extracts structured information, follows internal links recursively, respects `robots.txt`, handles network failures, and exports collected data to JSON and CSV.

This project was developed as **Task 4 – Web Crawler & Data Extraction Engine** for the **Algoryx Python Internship**.

---

## 📌 Project Overview

The Intelligent Website Crawler automates website data collection through a clean, modular, and configurable architecture.

The crawler can:

- Accept one or more seed URLs
- Download webpages using `requests`
- Parse HTML using `BeautifulSoup`
- Extract titles, headings, paragraphs, hyperlinks, images, and metadata
- Recursively follow internal links
- Avoid duplicate URLs
- Respect `robots.txt`
- Apply configurable request delays
- Retry failed HTTP requests
- Handle request timeouts
- Export results to JSON and CSV
- Search collected content using keywords
- Display crawl statistics
- Maintain application logs
- Provide a command-line interface

---

## 🎯 Objective

Build a scalable Python web crawler that automatically downloads webpages, extracts human-readable information, follows internal links, and exports structured datasets.

The project demonstrates:

- Web crawling
- HTTP networking
- HTML parsing
- Data extraction
- Recursive traversal
- Error handling
- Configuration management
- Object-oriented programming
- Structured data export
- Logging
- CLI-based execution

---

## 🏗️ Architecture

    User / CLI
         │
         ▼
    ┌───────────────┐
    │    main.py    │
    │ Application   │
    │    Entry      │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  WebCrawler   │
    │ Crawl Engine  │
    └───────┬───────┘
            │
       ┌────┴────┐
       │         │
       ▼         ▼
    HTTP      robots.txt
    Requests   Control
       │
       ▼
    ┌───────────────┐
    │  HTMLParser   │
    │ BeautifulSoup │
    └───────┬───────┘
            │
            ▼
    ┌────────────────────┐
    │ Structured Data    │
    │                    │
    │ Title              │
    │ Headings           │
    │ Paragraphs         │
    │ Links              │
    │ Images             │
    │ Metadata           │
    └──────────┬─────────┘
               │
               ▼
    ┌────────────────────┐
    │   DataExporter     │
    └──────────┬─────────┘
               │
          ┌────┴────┐
          ▼         ▼
        JSON       CSV

---

## 📂 Project Structure

    algoryx-task-4-web-crawler/
    │
    ├── src/
    │   ├── __init__.py
    │   ├── crawler.py
    │   ├── parser.py
    │   ├── exporter.py
    │   └── utils.py
    │
    ├── samples/
    │   ├── crawl_results.json
    │   └── crawl_results.csv
    │
    ├── data/
    ├── logs/
    ├── output/
    │
    ├── .env
    ├── .gitignore
    ├── main.py
    ├── README.md
    └── requirements.txt

---

## 🛠️ Technologies Used

- Python 3.11+
- Requests
- BeautifulSoup4
- python-dotenv
- urllib.robotparser
- CSV
- JSON
- Object-Oriented Programming

---

## ⚙️ Configuration

The crawler uses a `.env` file for configurable settings.

Example:

    SEED_URLS=https://books.toscrape.com/

    MAX_DEPTH=1
    MAX_PAGES=10

    REQUEST_DELAY=1
    REQUEST_TIMEOUT=15
    MAX_RETRIES=3

    RESPECT_ROBOTS=true

    KEYWORD=python

### Configuration Parameters

| Parameter | Description |
|---|---|
| `SEED_URLS` | Starting URL or URLs for crawling |
| `MAX_DEPTH` | Maximum recursive crawl depth |
| `MAX_PAGES` | Maximum number of pages to process |
| `REQUEST_DELAY` | Delay between HTTP requests |
| `REQUEST_TIMEOUT` | HTTP request timeout |
| `MAX_RETRIES` | Maximum retry attempts |
| `RESPECT_ROBOTS` | Enable or disable `robots.txt` handling |
| `KEYWORD` | Keyword used for content search |

---

## 🚀 Installation

### 1. Clone the repository

    git clone https://github.com/Malli0208/algoryx-task-4-web-crawler.git

### 2. Navigate into the project

    cd algoryx-task-4-web-crawler

### 3. Create a virtual environment

    python -m venv venv

### 4. Activate the virtual environment

#### Windows PowerShell

    .\venv\Scripts\Activate.ps1

### 5. Install dependencies

    pip install -r requirements.txt

### 6. Configure environment variables

Create a `.env` file in the project root:

    SEED_URLS=https://books.toscrape.com/

    MAX_DEPTH=1
    MAX_PAGES=10

    REQUEST_DELAY=1
    REQUEST_TIMEOUT=15
    MAX_RETRIES=3

    RESPECT_ROBOTS=true

    KEYWORD=python

---

## ▶️ Running the Crawler

Run the crawler using the `.env` configuration:

    python main.py

The application will:

1. Load configuration
2. Read seed URLs
3. Check `robots.txt`
4. Download webpages
5. Parse HTML
6. Extract structured information
7. Follow internal links
8. Prevent duplicate URLs
9. Export JSON and CSV results
10. Display crawl statistics

---

## 💻 Command-Line Usage

The crawler supports command-line arguments in addition to `.env` configuration.

### Specify a seed URL

    python main.py --url https://books.toscrape.com/

### Set crawl depth

    python main.py --depth 2

### Set maximum pages

    python main.py --pages 20

### Search for a keyword

    python main.py --keyword book

### Use multiple seed URLs

    python main.py --url https://books.toscrape.com/ https://quotes.toscrape.com/

Command-line arguments override the corresponding `.env` values.

---

## 🔎 Data Extraction

For every successfully processed webpage, the crawler extracts structured information.

### Page Title

The HTML `<title>` value is extracted.

### Headings

The crawler extracts:

    H1
    H2
    H3
    H4
    H5
    H6

### Paragraphs

Human-readable paragraph content is extracted from `<p>` elements.

### Hyperlinks

All available hyperlink targets from `<a href="">` elements are collected.

### Images

The crawler extracts:

- Image source
- Alternative text

### Metadata

Common HTML metadata is collected from `<meta>` elements, including values such as:

- Description
- Robots
- Viewport
- Open Graph properties
- Other available metadata

---

## 🔗 Internal Link Crawling

The crawler follows links belonging to the same domain as the seed URL.

External domains are ignored.

    Seed Website
         │
         ├── Internal Link A
         │       │
         │       └── Internal Link B
         │
         ├── Internal Link C
         │
         └── External Link
                 │
                 ▼
              Ignored

Crawling depth can be controlled using:

    MAX_DEPTH=1

---

## ♻️ Duplicate URL Prevention

The crawler maintains a visited URL set to prevent processing the same URL multiple times.

URLs are normalized before crawling to handle differences such as:

- URL fragments
- Trailing slashes
- `/index.html`
- Default HTTP/HTTPS ports
- Relative-link representations

For example:

    https://example.com
    https://example.com/
    https://example.com/index.html

are normalized to the same canonical homepage representation.

This prevents unnecessary duplicate requests.

---

## 🤖 robots.txt Support

The crawler checks `robots.txt` before processing URLs when:

    RESPECT_ROBOTS=true

If crawling is disallowed by the site's robots policy, the URL is skipped.

This provides responsible crawling behavior.

---

## ⏱️ Request Control

The crawler provides configurable request controls.

### Request Timeout

    REQUEST_TIMEOUT=15

Controls how long the crawler waits for a webpage response.

### Retry Attempts

    MAX_RETRIES=3

Allows temporary request failures to be retried.

### Request Delay

    REQUEST_DELAY=1

Adds a configurable delay between requests.

These controls help manage temporary network failures and reduce aggressive request rates.

---

## 📊 Crawl Statistics

After execution, the crawler displays:

- Pages visited
- Pages extracted
- Failures
- Execution time

Example:

    ============================================================
    INTELLIGENT WEBSITE CRAWLER
    ============================================================
    Pages visited   : 10
    Pages extracted : 10
    Failures        : 0
    Execution time  : 19.89 seconds
    JSON output     : output\crawl_results.json
    CSV output      : output\crawl_results.csv
    Keyword         : book
    Keyword matches : 10
    ============================================================

---

## 🔍 Keyword Search

The crawler supports keyword searching across collected webpage content.

Example:

    python main.py --keyword book

The search checks:

- Page titles
- Headings
- Paragraphs

Matching page URLs are displayed after the crawl.

Example:

    Keyword         : book
    Keyword matches : 10

    - https://books.toscrape.com/
    - https://books.toscrape.com/catalogue/category/books_1/index.html
    - ...

---

## 📤 Output Formats

### JSON

Complete structured crawl data is exported to:

    output/crawl_results.json

### CSV

Tabular crawl data is exported to:

    output/crawl_results.csv

### Sample Exports

Sample JSON and CSV results generated during testing are included in:

    samples/
    ├── crawl_results.json
    └── crawl_results.csv

---

## 📝 Logging

Application logs are written to:

    logs/crawler.log

The logging system records events such as:

- Application startup
- Seed URLs
- Page downloads
- Successful parsing
- Request failures
- `robots.txt` restrictions
- Crawl completion
- Resource cleanup

Logs are useful for debugging and monitoring crawler execution.

---

## 🛡️ Error Handling

The crawler includes exception handling for:

- Network failures
- HTTP errors
- Request timeouts
- Retryable server errors
- Invalid URLs
- Non-HTML resources
- HTML parsing errors
- `robots.txt` access problems
- Export errors

Errors are logged while allowing the crawler to continue processing other URLs where possible.

---

## 🧪 Testing

The crawler was tested using:

    https://books.toscrape.com/

### Successful Crawl Test

    Pages visited   : 10
    Pages extracted : 10
    Failures        : 0
    Execution time  : 19.89 seconds

### Keyword Search Test

Command:

    python main.py --keyword book

Result:

    Keyword         : book
    Keyword matches : 10

### Export Test

The crawler successfully generated:

    crawl_results.json
    crawl_results.csv

The generated files were also copied into the `samples/` directory as example outputs.

---

## 📋 Task Requirement Coverage

| Requirement | Status |
|---|---|
| Accept one or more seed URLs | ✅ |
| Webpage downloading | ✅ |
| HTML parsing | ✅ |
| Title extraction | ✅ |
| Heading extraction | ✅ |
| Paragraph extraction | ✅ |
| Hyperlink extraction | ✅ |
| Image extraction | ✅ |
| Metadata extraction | ✅ |
| Recursive internal crawling | ✅ |
| Duplicate URL prevention | ✅ |
| `robots.txt` support | ✅ |
| Configurable request delays | ✅ |
| Network retries | ✅ |
| Timeout management | ✅ |
| JSON export | ✅ |
| CSV export | ✅ |
| Crawl statistics | ✅ |
| Keyword search | ✅ |
| Logging | ✅ |
| Exception handling | ✅ |
| Object-Oriented Programming | ✅ |
| `.env` configuration | ✅ |
| Modular project structure | ✅ |
| Type hints | ✅ |
| CLI interface | ✅ Bonus |

---

## 📁 Module Responsibilities

### `main.py`

Application entry point responsible for:

- Loading configuration
- Reading CLI arguments
- Creating the crawler
- Running the crawl
- Exporting results
- Displaying statistics

### `src/crawler.py`

Core crawling engine responsible for:

- HTTP requests
- Retry handling
- Timeouts
- `robots.txt`
- Recursive crawling
- Internal-link detection
- Duplicate prevention
- Keyword search
- Crawl statistics

### `src/parser.py`

HTML extraction engine responsible for:

- Titles
- Headings
- Paragraphs
- Links
- Images
- Metadata

### `src/exporter.py`

Responsible for exporting collected data to:

- JSON
- CSV

### `src/utils.py`

Provides reusable utilities for:

- Logging
- URL normalization
- Internal URL validation
- Request delays

---

## 🔮 Future Improvements

Potential future enhancements include:

- Asynchronous crawling using `asyncio`
- SQLite database storage
- Sitemap generation
- Keyword frequency analysis
- Docker support
- Unit testing
- GitHub Actions CI/CD
- Concurrent request processing
- Advanced crawling strategies

---

## 🎓 Internship Information

**Program:** Algoryx Python Internship

**Task:** Task 4 – Web Crawler & Data Extraction Engine

**Domain:** Python / Web Crawling / Data Extraction

---

## 👨‍💻 Author

**C. Mallikarjun Reddy**

Python | Data Analytics | Automation

---

## 📄 License

This project was developed for educational and internship purposes.