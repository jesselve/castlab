#!/usr/bin/env python3
"""Tests for compress_cast.py."""

import json
import tempfile
from pathlib import Path

from compress_cast import compress_events, default_output, main, parse_args


class TestParseArgs:
    def test_input_file(self):
        args = parse_args(["demo.cast"])
        assert args.input == "demo.cast"
        assert args.output is None
        assert args.max_gap == 1.0

    def test_input_with_output(self):
        args = parse_args(["demo.cast", "-o", "out.cast"])
        assert args.input == "demo.cast"
        assert args.output == "out.cast"

    def test_custom_max_gap(self):
        args = parse_args(["demo.cast", "--max-gap", "2.5"])
        assert args.max_gap == 2.5

    def test_stdin_requires_output(self):
        import pytest
        with pytest.raises(SystemExit):
            parse_args([])

    def test_stdin_with_output(self):
        args = parse_args(["-o", "out.cast"])
        assert args.input is None
        assert args.output == "out.cast"


class TestCompressEvents:
    def test_no_gaps(self):
        events = [[0.0, "o", "a"], [0.5, "o", "b"], [1.0, "o", "c"]]
        result = compress_events(events, max_gap=1.0)
        assert result == events

    def test_single_large_gap(self):
        events = [[0.0, "o", "a"], [5.0, "o", "b"], [5.5, "o", "c"]]
        result = compress_events(events, max_gap=1.0)
        assert result[0][0] == 0.0
        assert result[1][0] == 1.0
        assert result[2][0] == 1.5

    def test_multiple_gaps(self):
        events = [[0.0, "o", "a"], [3.0, "o", "b"], [6.0, "o", "c"]]
        result = compress_events(events, max_gap=1.0)
        assert result[0][0] == 0.0
        assert result[1][0] == 1.0
        assert result[2][0] == 2.0

    def test_custom_max_gap(self):
        events = [[0.0, "o", "a"], [5.0, "o", "b"]]
        result = compress_events(events, max_gap=3.0)
        assert result[1][0] == 3.0

    def test_preserves_event_data(self):
        events = [[0.0, "o", "hello"], [10.0, "i", "world"]]
        result = compress_events(events, max_gap=1.0)
        assert result[0][1:] == ["o", "hello"]
        assert result[1][1:] == ["i", "world"]


class TestDefaultOutput:
    def test_basic(self):
        assert default_output("demo.cast") == "demo_compressed.cast"

    def test_with_path(self):
        result = default_output("path/to/demo.cast")
        assert result == str(Path("path/to/demo_compressed.cast"))


class TestMainIntegration:
    def test_file_roundtrip(self, tmp_path):
        header = {"version": 2, "width": 80, "height": 24}
        events = [[0.0, "o", "a"], [5.0, "o", "b"], [5.5, "o", "c"]]
        input_file = tmp_path / "test.cast"
        output_file = tmp_path / "out.cast"

        with open(input_file, "w") as f:
            f.write(json.dumps(header) + "\n")
            for e in events:
                f.write(json.dumps(e) + "\n")

        main([str(input_file), "-o", str(output_file), "--max-gap", "1.0"])

        with open(output_file) as f:
            lines = f.readlines()

        assert json.loads(lines[0]) == header
        result_events = [json.loads(l) for l in lines[1:]]
        assert result_events[1][0] == 1.0
