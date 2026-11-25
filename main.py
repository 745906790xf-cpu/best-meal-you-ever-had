"""The Best Meal You Ever Had entry for make.fun.

Writes one sentence to /output/entry.txt: the best meal the entrant
ever had -- grandmother's clay-pot rice, eaten at eight years old
while rain drummed on the tin roof. The sandbox runs this program
twice and both runs must write the same bytes, so the sentence is a
fixed string with no randomness, clock, or network access. The
sentence is built to the judge's brief: a named dish, a place, a
texture, a smell and one specific moment, in one clean sentence that
reads aloud well, ending on a turn that stays with the reader.
"""

import argparse
import os

MAX_CHARS = 200
ENTRY_PATH = "/output/entry.txt"

LINE = (
    "My grandmother\u2019s clay-pot rice, crust crackling under my spoon "
    "as rain drummed the tin roof and soy and scallion steamed around "
    "us \u2014 I was eight, and I still measure every good meal against "
    "that one."
)


def check_line(line: str) -> str:
    """Return the line unchanged, guarding the gate's limits.

    The gate accepts UTF-8 text of 1 to 200 characters that is not
    only white space, so fail loudly here rather than write an entry
    the judge never sees.
    """
    if not line or len(line) > MAX_CHARS:
        raise ValueError(
            f"length rule failed: entry is {len(line)} characters, limit is {MAX_CHARS}"
        )
    if not line.strip():
        raise ValueError("entry must not be only white space")
    if line.strip() != line or "\n" in line or "\r" in line:
        raise ValueError(
            "single-line rule failed: entry has surrounding whitespace or a line break"
        )
    if "  " in line:
        raise ValueError(
            "spacing rule failed: entry contains a double space, which reads "
            "as a typo when the judge reads it aloud"
        )
    if line[-1] not in ".!?":
        raise ValueError(
            "ending rule failed: entry does not end with terminal punctuation, "
            "so it does not read as one finished sentence"
        )
    if any(ord(ch) < 32 for ch in line):
        raise ValueError(
            "control-character rule failed: entry contains a control character"
        )
    return line


def write_entry(path: str = ENTRY_PATH) -> None:
    """Write the line as UTF-8 with no trailing newline, then verify it.

    Read back what was written and compare bytes, so a partial write
    is caught here instead of in the sandbox.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    text = check_line(LINE)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("read-back verification failed: written bytes differ")
    if len(written.encode("utf-8")) != len(text.encode("utf-8")):
        raise ValueError("read-back verification failed: byte length differs")
    print(f"wrote {len(text)} characters, {len(text.split())} words to {path}")


def main(argv=None) -> int:
    """Write the sentence, to /output/entry.txt unless --out says otherwise.

    The --out flag exists for local testing only: the sandbox runs the
    program with no arguments, so it always writes the default path.
    """
    parser = argparse.ArgumentParser(
        description="Write the best-meal sentence."
    )
    parser.add_argument(
        "--out",
        default=ENTRY_PATH,
        help="where to write the sentence (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    write_entry(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
