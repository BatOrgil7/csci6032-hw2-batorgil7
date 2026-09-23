import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.text_stats import text_stats


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "text_stats.py"
SAMPLE = ROOT / "sample.txt"


class TextStatsTests(unittest.TestCase):
    def test_text_stats_counts_unicode_and_whitespace(self):
        self.assertEqual(
            text_stats("Café\n日本語 words\n"),
            {"lines": 2, "words": 3, "characters": 15},
        )

    def test_text_stats_empty_text(self):
        self.assertEqual(
            text_stats(""),
            {"lines": 0, "words": 0, "characters": 0},
        )

    def test_text_stats_reports_top_words_case_insensitively(self):
        self.assertEqual(
            text_stats("Beta alpha BETA gamma alpha delta", top=3),
            {
                "lines": 1,
                "words": 6,
                "characters": 33,
                "top": [
                    {"word": "alpha", "count": 2},
                    {"word": "beta", "count": 2},
                    {"word": "delta", "count": 1},
                ],
            },
        )

    def test_cli_reads_sample_file_and_prints_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SAMPLE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 5, "words": 40, "characters": 227},
        )

    def test_cli_reads_utf8_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "unicode.txt"
            path.write_text("naïve café\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 1, "words": 2, "characters": 11},
        )

    def test_cli_reports_top_words(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("Apple banana apple CHERRY banana", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--top", "2"],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertEqual(
            json.loads(result.stdout),
            {
                "lines": 1,
                "words": 5,
                "characters": 32,
                "top": [
                    {"word": "apple", "count": 2},
                    {"word": "banana", "count": 2},
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
