import csv
import json
from pathlib import Path


class DataExporter:
    """Export crawled webpage data to JSON and CSV."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def export_json(
        self,
        pages: list[dict],
        filename: str = "crawl_results.json",
    ) -> Path:
        """Export complete crawl data to JSON."""

        output_file = self.output_dir / filename

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                pages,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_file

    def export_csv(
        self,
        pages: list[dict],
        filename: str = "crawl_results.csv",
    ) -> Path:
        """Export crawl data to CSV."""

        output_file = self.output_dir / filename

        fieldnames = [
            "url",
            "title",
            "headings",
            "paragraphs",
            "links",
            "images",
            "metadata",
        ]

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for page in pages:
                writer.writerow(
                    {
                        "url": page.get(
                            "url",
                            "",
                        ),
                        "title": page.get(
                            "title",
                            "",
                        ),
                        "headings": self._list_to_text(
                            page.get(
                                "headings",
                                [],
                            )
                        ),
                        "paragraphs": self._list_to_text(
                            page.get(
                                "paragraphs",
                                [],
                            )
                        ),
                        "links": self._list_to_text(
                            page.get(
                                "links",
                                [],
                            )
                        ),
                        "images": self._images_to_text(
                            page.get(
                                "images",
                                [],
                            )
                        ),
                        "metadata": json.dumps(
                            page.get(
                                "metadata",
                                {},
                            ),
                            ensure_ascii=False,
                        ),
                    }
                )

        return output_file

    @staticmethod
    def _list_to_text(
        values: list,
    ) -> str:
        """Convert a list into readable CSV text."""

        return " | ".join(
            str(value)
            for value in values
        )

    @staticmethod
    def _images_to_text(
        images: list[dict],
    ) -> str:
        """Convert image information into readable text."""

        image_values = []

        for image in images:
            source = image.get(
                "src",
                "",
            )

            alt = image.get(
                "alt",
                "",
            )

            if alt:
                image_values.append(
                    f"{source} ({alt})"
                )
            else:
                image_values.append(source)

        return " | ".join(image_values)