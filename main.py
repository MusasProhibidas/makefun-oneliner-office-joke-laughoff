"""One-Line Office Joke Laugh-Off entry for make.fun.

This script is the entry for the make.fun bounty
"One-Line Office Joke Laugh-Off". It reads the single-line office joke
from ``line.txt`` (in the same directory as this script), validates that
it is exactly one non-empty line of at most 200 characters, and writes
the line (without its trailing newline) to the output path
``/output/entry.txt``, or to the path in the ``MAKEFUN_OUTPUT``
environment variable when set.

No network access. Deterministic: the same input always produces the
same output bytes.
"""

import hashlib
import os
import sys


MAX_LENGTH = 200


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, "line.txt")

    if not os.path.isfile(source_path):
        print("error: line.txt not found next to main.py", file=sys.stderr)
        return 1

    with open(source_path, "rb") as source_file:
        raw = source_file.read()

    # Remove exactly one trailing newline, if present.
    if raw.endswith(b"\n"):
        raw = raw[:-1]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("error: line.txt is not valid UTF-8", file=sys.stderr)
        return 1

    if not text:
        print("error: line.txt is empty", file=sys.stderr)
        return 1

    if "\n" in text or "\r" in text:
        print("error: line.txt must contain exactly one line", file=sys.stderr)
        return 1

    if len(text) > MAX_LENGTH:
        print(
            "error: line.txt has %d characters, exceeding the maximum of %d"
            % (len(text), MAX_LENGTH),
            file=sys.stderr,
        )
        return 1

    output_bytes = text.encode("utf-8")

    output_path = os.environ.get("MAKEFUN_OUTPUT") or "/output/entry.txt"
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "wb") as output_file:
        output_file.write(output_bytes)

    with open(output_path, "rb") as written_file:
        written_bytes = written_file.read()

    if hashlib.sha256(written_bytes).hexdigest() != hashlib.sha256(
        output_bytes
    ).hexdigest():
        print(
            "error: SHA-256 of the written output does not match the expected value",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
