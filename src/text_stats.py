"""Count lines, words, and characters in a UTF-8 text file."""

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Dict, Optional


def non_negative_int(value: str) -> int:
    """Parse a non-negative integer for an argparse option."""
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


def text_stats(text: str, top: Optional[int] = None) -> Dict[str, object]:
    """Return line, word, and character counts for *text*."""
    stats: Dict[str, object] = {
        "lines": len(text.splitlines()),
        "words": len(text.split()),
        "characters": len(text),
    }
    if top is not None:
        counts = Counter(word.casefold() for word in text.split())
        most_frequent = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        stats["top"] = [
            {"word": word, "count": count} for word, count in most_frequent[:top]
        ]
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count lines, words, and characters in a UTF-8 text file."
    )
    parser.add_argument("file", type=Path, help="path to the UTF-8 text file")
    parser.add_argument(
        "--top",
        type=non_negative_int,
        metavar="N",
        help="include the N most frequent words, case-insensitively",
    )
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    print(json.dumps(text_stats(text, top=args.top)))


if __name__ == "__main__":
    main()
