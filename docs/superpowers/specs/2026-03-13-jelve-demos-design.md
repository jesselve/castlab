# jelve-demos — Design Spec

## Overview

A GitHub repository that serves three purposes:
1. **Scripts** for post-processing `.cast` terminal recording files
2. **Notes** on using asciinema (Linux/Mac) and PowerSession (Windows)
3. **GitHub Pages site** with a gallery of live terminal demos

The audience is colleagues who want to learn how to record, process, and share terminal sessions. The repo is both a toolkit (clone it, use the scripts) and a showcase (visit the site, watch demos).

## Repository Structure

```
jelve-demos/
  scripts/
    compress_cast.py          # CLI tool to compress idle time in .cast files
  site/                       # GitHub Pages root (served from main branch /site)
    index.html                # Gallery page with cards linking to individual demos
    demos/
      <demo-name>.html        # Per-demo player page embedding asciinema-player
    casts/
      <demo-name>.cast        # Cast files served directly by the site
    assets/
      asciinema-player.min.js # Vendored from latest release
      asciinema-player.min.css
  notes/
    asciinema.md              # Install, record, useful flags, local playback
    powersession.md           # Windows equivalent, quirks, missing features
    workflow.md               # End-to-end: record → compress → publish
  README.md                   # Overview, quick start, links to site and notes
```

## Site Design

### Gallery (`site/index.html`)

- Single HTML page, minimal CSS, no framework
- Each demo rendered as a card: title, short description, link to player page
- Adding a demo = copying a card HTML block and updating title, description, and link
- No build step, no JS templating

### Player Pages (`site/demos/<demo-name>.html`)

- Embeds asciinema-player pointed at `../casts/<demo-name>.cast`
- Displays title and description
- Includes "back to gallery" link
- Sensible player defaults: fit-to-window, readable font size

### Assets (`site/assets/`)

- asciinema-player JS and CSS vendored (downloaded from release, committed to repo)
- No CDN dependency — works offline, version-controlled

## Scripts

### `scripts/compress_cast.py`

Refactored from an existing working script. Compresses idle time gaps in `.cast` files.

**CLI interface (argparse):**
```
python compress_cast.py input.cast [-o output.cast] [--max-gap 1.0]
```

- `input.cast` — required positional argument
- `-o` / `--output` — output file, defaults to `<input>_compressed.cast`
- `--max-gap` — maximum allowed gap in seconds, defaults to `1.0`
- Reads from stdin if no file argument given (pipe-friendly)

**Why this exists:** asciinema supports `--idle-time-limit` at record time, but PowerSession does not. This script fills that gap for Windows recordings and is also useful for any session where the flag wasn't used.

## Notes

Three markdown files for colleague onboarding:

- **`notes/asciinema.md`** — installation, `asciinema rec`, useful flags (`--idle-time-limit`, `--title`), local playback vs upload
- **`notes/powersession.md`** — installation, recording, differences from asciinema (no idle-time-limit), Windows-specific tips
- **`notes/workflow.md`** — end-to-end process: record → compress with `compress_cast.py` → place `.cast` in `site/casts/` → create player page → push → verify on GitHub Pages

Written for internal audience — concise, practical, no polish overhead.

## README.md

- One-paragraph overview
- Link to live GitHub Pages site (`jesselve.github.io/jelve-demos`)
- Quick start steps: record, compress, publish
- Pointers to `notes/` for guides and `scripts/` for tools

## GitHub Pages Configuration

- Source: `main` branch, `/site` directory
- URL: `jesselve.github.io/jelve-demos`
- No custom domain

## Non-Goals

- No CI/CD pipeline
- No build tools, npm, or static site generator
- No automated cast-to-site publishing workflow
- No polished external-facing documentation — internal audience only
- No additional scripts beyond `compress_cast.py` at this time

## Dependencies

- Python 3 (for `compress_cast.py`)
- A browser (for viewing the site)
- asciinema and/or PowerSession (for recording — not required to use the repo)
