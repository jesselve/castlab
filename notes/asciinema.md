# asciinema

Terminal session recorder for Linux and macOS.

## Install

```bash
# macOS
brew install asciinema

# Ubuntu/Debian
sudo apt install asciinema

# pip (any platform)
pip install asciinema
```

## Record

```bash
# Basic recording
asciinema rec demo.cast

# With idle time limit (caps pauses to 1 second)
asciinema rec --idle-time-limit 1 demo.cast

# With a title
asciinema rec --title "My Demo" demo.cast

# Combine flags
asciinema rec --idle-time-limit 1 --title "My Demo" demo.cast
```

Type `exit` or press Ctrl-D to stop recording.

## Playback

```bash
# Play locally in terminal
asciinema play demo.cast

# Play at 2x speed
asciinema play -s 2 demo.cast
```

## Useful Flags

| Flag | Purpose |
|------|---------|
| `--idle-time-limit N` | Cap pauses to N seconds during recording |
| `--title "text"` | Set recording title (stored in .cast header) |
| `-s N` | Playback speed multiplier |
| `--overwrite` | Overwrite output file if it exists |

## Tips

- Always use `--idle-time-limit` unless you want to compress later with `compress_cast.py`
- Cast files are plain JSON — you can inspect and hand-edit them
- The header (first line) contains metadata; remaining lines are `[timestamp, type, data]` events
