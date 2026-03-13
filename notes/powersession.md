# PowerSession

Terminal session recorder for Windows (PowerShell). Produces .cast files
compatible with asciinema-player.

## Install

```powershell
# Install from PowerShell Gallery
Install-Module -Name PowerSession -Scope CurrentUser

# Or via dotnet tool
dotnet tool install --global PowerSession
```

## Record

```powershell
# Basic recording
PowerSession rec demo.cast

# With a title
PowerSession rec --title "My Demo" demo.cast
```

Type `exit` to stop recording.

## Key Differences from asciinema

| Feature | asciinema | PowerSession |
|---------|-----------|--------------|
| Platform | Linux/macOS | Windows |
| `--idle-time-limit` | Supported | Not available |
| Shell | Default shell | PowerShell |
| Output format | asciicast v2 | asciicast v2 (compatible) |

## Handling Idle Time

PowerSession does not support `--idle-time-limit`. Use `compress_cast.py` after recording:

```bash
python scripts/compress_cast.py demo.cast --max-gap 1.0
```

This is the primary reason `compress_cast.py` exists.

## Tips

- Resize your terminal to a consistent size before recording
- PowerSession output is compatible with asciinema-player — no conversion needed
- Close other terminal tabs to avoid recording noise
