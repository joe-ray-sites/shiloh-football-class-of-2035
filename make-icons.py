#!/usr/bin/env python3
"""
Generate favicons and home-screen icons from assets/sc-logo.png.

    python3 make-icons.py

Re-run this any time the logo changes — it overwrites every generated icon.

Why the icons get a white plate rather than keeping transparency:
  • iOS ignores alpha on home-screen icons and composites them onto BLACK.
    The logo's navy fill is nearly black, so a transparent icon would turn
    into an unreadable dark blob on the home screen.
  • Browser tabs in dark mode have the same problem at 16px.
iOS and Android apply their own rounded/squircle mask, so these are saved as
full-bleed squares with the logo inset — no pre-rounded corners.
"""

from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required.  Install it with:  python3 -m pip install Pillow")

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "sc-logo.png"
OUT = ROOT / "assets" / "icons"
WHITE = (255, 255, 255, 255)

# size, filename, how much of the tile the logo fills
JOBS = [
    (16,  "favicon-16.png",        0.92),
    (32,  "favicon-32.png",        0.92),
    (180, "apple-touch-icon.png",  0.78),   # iOS home screen
    (192, "icon-192.png",          0.78),   # Android / manifest
    (512, "icon-512.png",          0.78),
    (512, "icon-maskable-512.png", 0.58),   # Android adaptive: keep inside the safe circle
]


def render(logo, size, fill):
    """Square white tile with the logo centred and contained."""
    tile = Image.new("RGBA", (size, size), WHITE)
    box = round(size * fill)
    art = logo.copy()
    art.thumbnail((box, box), Image.LANCZOS)
    tile.alpha_composite(art, ((size - art.width) // 2, (size - art.height) // 2))
    return tile


def main():
    if not SRC.exists():
        sys.exit(f"Missing {SRC.relative_to(ROOT)}")

    logo = Image.open(SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())          # trim transparent margin first
    OUT.mkdir(parents=True, exist_ok=True)

    for size, name, fill in JOBS:
        img = render(logo, size, fill)
        img.convert("RGB").save(OUT / name, "PNG", optimize=True)
        print(f"  {name:24} {size}x{size}")

    # Multi-resolution .ico for older browsers and pinned tabs
    ico = render(logo, 64, 0.92)
    ico.convert("RGB").save(ROOT / "favicon.ico", "ICO",
                            sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  {'favicon.ico':24} 16/32/48")
    print(f"\nDone — {len(JOBS) + 1} files written.")


if __name__ == "__main__":
    main()
