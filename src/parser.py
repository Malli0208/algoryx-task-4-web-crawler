from bs4 import BeautifulSoup


class HTMLParser:
    """Parse HTML pages and extract structured information."""

    def parse(self, url: str, html: str) -> dict:
        """Extract useful information from an HTML document."""

        soup = BeautifulSoup(html, "html.parser")

        title = self._extract_title(soup)
        headings = self._extract_headings(soup)
        paragraphs = self._extract_paragraphs(soup)
        links = self._extract_links(soup)
        images = self._extract_images(soup)
        metadata = self._extract_metadata(soup)

        return {
            "url": url,
            "title": title,
            "headings": headings,
            "paragraphs": paragraphs,
            "links": links,
            "images": images,
            "metadata": metadata,
        }

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        """Extract the page title."""

        if soup.title:
            return soup.title.get_text(
                strip=True
            )

        return ""

    @staticmethod
    def _extract_headings(
        soup: BeautifulSoup,
    ) -> list[str]:
        """Extract H1-H6 headings."""

        headings = []

        for heading in soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6"]
        ):
            text = heading.get_text(
                " ",
                strip=True
            )

            if text:
                headings.append(text)

        return headings

    @staticmethod
    def _extract_paragraphs(
        soup: BeautifulSoup,
    ) -> list[str]:
        """Extract meaningful paragraph text."""

        paragraphs = []

        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(
                " ",
                strip=True
            )

            if text:
                paragraphs.append(text)

        return paragraphs

    @staticmethod
    def _extract_links(
        soup: BeautifulSoup,
    ) -> list[str]:
        """Extract hyperlink targets."""

        links = []

        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href")

            if href:
                links.append(href)

        return list(dict.fromkeys(links))

    @staticmethod
    def _extract_images(
        soup: BeautifulSoup,
    ) -> list[dict[str, str]]:
        """Extract image sources and alternative text."""

        images = []

        for image in soup.find_all("img"):
            source = image.get("src")

            if source:
                images.append(
                    {
                        "src": source,
                        "alt": image.get(
                            "alt",
                            ""
                        ),
                    }
                )

        return images

    @staticmethod
    def _extract_metadata(
        soup: BeautifulSoup,
    ) -> dict:
        """Extract common HTML metadata."""

        metadata = {}

        for meta in soup.find_all("meta"):
            name = (
                meta.get("name")
                or meta.get("property")
            )

            content = meta.get("content")

            if name and content:
                metadata[name] = content

        return metadata