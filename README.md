# castlab

A toolkit and showcase for terminal session recordings using
[asciinema](https://asciinema.org/) (Linux/macOS) and
[PowerSession](https://github.com/nicholasgasior/powersession) (Windows).

**Live demos:** [jesselve.github.io/castlab](https://jesselve.github.io/castlab/)

## Quick Start

1. **Record** a terminal session (see [notes/](notes/) for guides)
2. **Compress** idle time: `python scripts/compress_cast.py recording.cast`
3. **Publish** by adding the `.cast` file and a player page to `site/`

See [notes/workflow.md](notes/workflow.md) for the full step-by-step process.

## What's Here

| Directory | Contents |
|-----------|----------|
| `scripts/` | Post-processing tools for `.cast` files |
| `site/` | GitHub Pages gallery with embedded asciinema-player |
| `notes/` | Practical guides for asciinema, PowerSession, and the publish workflow |
