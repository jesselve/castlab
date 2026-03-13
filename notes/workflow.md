# Workflow: Record → Compress → Publish

End-to-end process for creating and publishing a terminal demo.

## 1. Record

**Linux/macOS:**
```bash
asciinema rec --idle-time-limit 1 --title "My Demo" my-demo.cast
```

**Windows:**
```powershell
PowerSession rec --title "My Demo" my-demo.cast
```

## 2. Compress (if needed)

If you didn't use `--idle-time-limit`, or used PowerSession (which doesn't support it):

```bash
python scripts/compress_cast.py my-demo.cast --max-gap 1.0
```

This creates `my-demo_compressed.cast`. Review it:

```bash
asciinema play my-demo_compressed.cast
```

## 3. Add to Site

Copy the final `.cast` file into the site:

```bash
cp my-demo_compressed.cast site/casts/my-demo.cast
```

## 4. Create Player Page

Copy the example template:

```bash
cp site/demos/example.html site/demos/my-demo.html
```

Edit `my-demo.html`:
- Update the `<title>` tag
- Update the `<h1>` heading
- Update the description `<p>`
- Change the cast file path in the `AsciinemaPlayer.create()` call to `../casts/my-demo.cast`

## 5. Add Gallery Card

Edit `site/index.html`. Add a card inside the `<div class="gallery">`:

```html
<div class="card">
    <h2>My Demo</h2>
    <p>Description of what this demo shows.</p>
    <a href="demos/my-demo.html">Watch demo →</a>
</div>
```

Remove the "No demos yet" placeholder `<p>` when adding the first card.

## 6. Push and Verify

```bash
git add site/
git commit -m "feat: add my-demo recording"
git push
```

Visit `https://jesselve.github.io/castlab/` to verify.
