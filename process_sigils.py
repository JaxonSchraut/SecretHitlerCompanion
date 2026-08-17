"""
Turns the extracted (opaque, grayscale-on-white) sigil PNGs into proper
tinted + transparent badge icons: any non-white ink becomes a flat tint
color, the white background becomes fully transparent, with a short
anti-aliased ramp at the boundary so edges stay smooth at small sizes.

The two source canvases are NOT the same shape (fascist: 537x482, ~11%
wider than tall; liberal: 495x497, ~square) and aren't cropped tight to the
badge either — rendering them straight at a fixed CSS box therefore visibly
squishes the (already-round) badge art. So after tinting, this also crops
each to its actual content bounding box and pastes it centered onto a
perfectly square canvas, then resizes both to the SAME final pixel size —
guaranteeing both sigils are genuinely round and genuinely the same size,
regardless of what the source canvases looked like.

Re-run this if liberalSigil.png / fascistSigil.png are re-extracted or
replaced — it regenerates the *-tinted.png files secret-role-dealer.html
actually references (see sigilSvg() in the <script>).

Requires Pillow: pip install --user --break-system-packages pillow
"""
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_SIZE = 400   # both outputs end up exactly this size, square

JOBS = [
    (os.path.join(HERE, "liberalSigil.png"),
     os.path.join(HERE, "liberalSigil-tinted.png"),
     (47, 111, 143)),   # --liberal: #2f6f8f
    (os.path.join(HERE, "fascistSigil.png"),
     os.path.join(HERE, "fascistSigil-tinted.png"),
     (226, 59, 46)),    # --vermilion: #e23b2e
]

WHITE_CUTOFF = 248   # brightness at/above this -> fully transparent
INK_CUTOFF = 200     # brightness at/below this -> fully opaque tint

for src_path, dst_path, tint in JOBS:
    im = Image.open(src_path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            brightness = (r + g + b) / 3
            if brightness >= WHITE_CUTOFF:
                alpha = 0
            elif brightness <= INK_CUTOFF:
                alpha = 255
            else:
                t = (WHITE_CUTOFF - brightness) / (WHITE_CUTOFF - INK_CUTOFF)
                alpha = round(255 * t)
            px[x, y] = (tint[0], tint[1], tint[2], alpha)

    bbox = im.getbbox()
    content = im.crop(bbox)
    side = max(content.width, content.height)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(content, ((side - content.width) // 2, (side - content.height) // 2), content)
    square = square.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
    square.save(dst_path)
    print(f"wrote {dst_path} (content {content.size} -> square {side}x{side} -> {TARGET_SIZE}x{TARGET_SIZE})")
