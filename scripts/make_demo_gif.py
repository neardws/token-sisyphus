#!/usr/bin/env python3
"""
Generate a demo GIF for token-sisyphus showing the progress bar animation.
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# ── Config ────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 780, 300
BG      = (18, 18, 18)       # near-black
GREEN   = (80, 250, 123)     # neon green
CYAN    = (139, 233, 253)    # cyan
WHITE   = (248, 248, 242)    # off-white
GRAY    = (98, 114, 164)     # muted
YELLOW  = (241, 250, 140)    # yellow
TARGET  = 100_000

# Use a monospace font if available, else default
def get_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT_SM = get_font(14)
FONT_MD = get_font(16)
FONT_LG = get_font(18)

def draw_frame(pct, req, done=False):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)

    y = 24
    # Header
    d.text((24, y), "🪨  token-sisyphus starting...", font=FONT_MD, fill=WHITE)
    y += 34
    d.text((40, y), f"Provider : openai",    font=FONT_SM, fill=GRAY)
    y += 22
    d.text((40, y), f"Target   : {TARGET:,} tokens", font=FONT_SM, fill=GRAY)
    y += 22
    d.text((40, y), f"Model    : gpt-4o-mini",   font=FONT_SM, fill=GRAY)
    y += 22
    d.text((40, y), f"Mode     : LIVE",          font=FONT_SM, fill=GREEN)
    y += 36

    if not done:
        # Progress bar
        BAR_W = 44
        filled = int(BAR_W * pct)
        bar = "#" * filled + "-" * (BAR_W - filled)
        current = int(TARGET * pct)
        bar_line = f"  [{bar}] {pct*100:.1f}% ({current:,} / {TARGET:,} tokens)  req#{req}"
        d.text((24, y), bar_line, font=FONT_SM, fill=CYAN)
    else:
        # Done screen
        y -= 10
        d.text((24, y), "✅  Done.", font=FONT_LG, fill=GREEN)
        y += 32
        d.text((40, y), f"Total tokens burned : {TARGET:,}",  font=FONT_SM, fill=WHITE)
        y += 22
        d.text((40, y), f"Requests made       : 174",          font=FONT_SM, fill=WHITE)
        y += 22
        d.text((40, y), f"Time elapsed        : 91.3s",        font=FONT_SM, fill=WHITE)
        y += 22
        d.text((40, y), f"Avg tokens/req      : 577",          font=FONT_SM, fill=WHITE)
        y += 36
        d.text((40, y), "Your boulder has reached the top. See you tomorrow.", font=FONT_SM, fill=YELLOW)

    return img


def main():
    frames = []
    durations = []

    # Intro — hold header for 1.2s
    intro = draw_frame(0.0, 0)
    for _ in range(4):
        frames.append(intro)
        durations.append(300)

    # Progress animation — sweep 0% → 100%
    steps = 40
    for i in range(1, steps + 1):
        pct = i / steps
        req = int(pct * 174)
        frames.append(draw_frame(pct, req))
        # Faster in the middle, slower at start/end
        if i < 4 or i > steps - 3:
            durations.append(180)
        else:
            durations.append(60)

    # Done screen — hold for 3s
    done_frame = draw_frame(1.0, 174, done=True)
    for _ in range(10):
        frames.append(done_frame)
        durations.append(300)

    out = "assets/demo.gif"
    os.makedirs("assets", exist_ok=True)
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(f"Saved: {out}  ({len(frames)} frames)")


if __name__ == "__main__":
    main()
