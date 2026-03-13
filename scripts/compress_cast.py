#!/usr/bin/env python3
"""Compress idle time gaps in asciinema .cast files.

asciinema supports --idle-time-limit at record time, but PowerSession
(Windows) does not.  This script fills that gap for any .cast file
where long pauses need trimming after the fact.
"""

import argparse
import json
import sys
from pathlib import Path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Compress idle time gaps in .cast files."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input .cast file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "-o", "--output",
        help=(
            "Output file. Defaults to <input>_compressed.cast. "
            "Required when reading from stdin."
        ),
    )
    parser.add_argument(
        "--max-gap",
        type=float,
        default=1.0,
        help="Maximum allowed gap in seconds (default: 1.0)",
    )
    args = parser.parse_args(argv)

    if args.input is None and args.output is None:
        parser.error("--output is required when reading from stdin")

    return args


def compress_events(events, max_gap):
    """Compress gaps larger than *max_gap* seconds between events."""
    offset = 0.0
    prev_time = 0.0
    compressed = []
    for event in events:
        t = event[0]
        gap = t - prev_time
        if gap > max_gap:
            offset += gap - max_gap
        compressed.append([round(t - offset, 6), event[1], event[2]])
        prev_time = t
    return compressed


def default_output(input_path):
    p = Path(input_path)
    return str(p.with_stem(p.stem + "_compressed"))


def main(argv=None):
    args = parse_args(argv)

    if args.input:
        with open(args.input) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    header = json.loads(lines[0])
    events = [json.loads(line) for line in lines[1:] if line.strip()]

    compressed = compress_events(events, args.max_gap)

    output_path = args.output or default_output(args.input)

    with open(output_path, "w") as f:
        f.write(json.dumps(header) + "\n")
        for e in compressed:
            f.write(json.dumps(e) + "\n")

    print(f"Compressed {len(events)} events → {output_path}")


if __name__ == "__main__":
    main()
