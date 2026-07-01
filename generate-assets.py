from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import zipfile


ROOT = Path(__file__).resolve().parent
EXTENSION_DIR = ROOT / "klaviyo-replace-button-extension"
ICONS_DIR = EXTENSION_DIR / "icons"
STORE_DIR = ROOT / "store-assets"
ZIP_PATH = ROOT / "klaviyo-replace-button-extension.zip"


BLUE = "#2457d6"
BLUE_DARK = "#15327f"
INK = "#162033"
MUTED = "#64748b"
GREEN = "#18a957"
PANEL = "#f7f9fc"
LINE = "#d8dee8"


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient(size, top, bottom):
    img = Image.new("RGB", size, top)
    d = ImageDraw.Draw(img)
    h = size[1]
    top_rgb = tuple(int(top[i : i + 2], 16) for i in (1, 3, 5))
    bottom_rgb = tuple(int(bottom[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        t = y / max(h - 1, 1)
        rgb = tuple(round(top_rgb[i] * (1 - t) + bottom_rgb[i] * t) for i in range(3))
        d.line([(0, y), (size[0], y)], fill=rgb)
    return img


def draw_replace_mark(draw, x, y, scale=1):
    rounded(draw, (x, y, x + 62 * scale, y + 46 * scale), 8 * scale, "#ffffff", "#c7d2fe", max(1, int(2 * scale)))
    draw.rectangle((x + 8 * scale, y + 9 * scale, x + 54 * scale, y + 34 * scale), fill="#e8f0ff")
    draw.polygon(
        [
            (x + 13 * scale, y + 34 * scale),
            (x + 28 * scale, y + 20 * scale),
            (x + 40 * scale, y + 34 * scale),
        ],
        fill="#7aa4ff",
    )
    draw.ellipse((x + 41 * scale, y + 13 * scale, x + 48 * scale, y + 20 * scale), fill="#f6c65b")

    cx, cy = x + 45 * scale, y + 36 * scale
    r = 14 * scale
    width = max(2, int(4 * scale))
    draw.arc((cx - r, cy - r, cx + r, cy + r), 20, 310, fill=GREEN, width=width)
    draw.polygon(
        [
            (cx + 12 * scale, cy - 11 * scale),
            (cx + 25 * scale, cy - 11 * scale),
            (cx + 18 * scale, cy - 1 * scale),
        ],
        fill=GREEN,
    )


def wrap_text(draw, text, text_font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=text_font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_icon(path, size):
    img = gradient((size, size), BLUE, BLUE_DARK).convert("RGBA")
    draw = ImageDraw.Draw(img)

    pad = max(4, int(size * 0.12))
    rounded(draw, (pad, pad, size - pad, size - pad), int(size * 0.18), "#ffffff", None)
    rounded(
        draw,
        (pad + size * 0.07, pad + size * 0.10, size - pad - size * 0.07, size - pad - size * 0.18),
        int(size * 0.08),
        "#eaf1ff",
        "#b9c9ff",
        max(1, int(size * 0.025)),
    )
    draw.polygon(
        [
            (size * 0.27, size * 0.61),
            (size * 0.43, size * 0.44),
            (size * 0.57, size * 0.61),
        ],
        fill="#7aa4ff",
    )
    draw.ellipse((size * 0.58, size * 0.31, size * 0.69, size * 0.42), fill="#f6c65b")

    cx, cy = size * 0.60, size * 0.66
    r = size * 0.18
    width = max(2, int(size * 0.06))
    draw.arc((cx - r, cy - r, cx + r, cy + r), 20, 315, fill=GREEN, width=width)
    draw.polygon(
        [
            (cx + size * 0.14, cy - size * 0.13),
            (cx + size * 0.27, cy - size * 0.12),
            (cx + size * 0.20, cy - size * 0.02),
        ],
        fill=GREEN,
    )
    img.save(path)


def draw_ui_mockup(draw, x, y, w, h, compact=False):
    rounded(draw, (x, y, x + w, y + h), 18, "#ffffff", "#dfe6f1", 2)
    draw.rectangle((x, y, x + w, y + 52), fill="#f2f5f9")
    draw.line((x, y + 52, x + w, y + 52), fill="#dfe6f1", width=2)
    draw.text((x + 24, y + 16), "Klaviyo editor", fill=INK, font=font(19 if not compact else 16, True))
    draw.text((x + w - 138, y + 16), "Preview", fill=INK, font=font(16 if not compact else 13))

    sidebar_w = int(w * 0.34)
    draw.line((x + sidebar_w, y + 52, x + sidebar_w, y + h), fill="#dfe6f1", width=2)
    draw.text((x + 26, y + 78), "Image", fill=INK, font=font(26 if not compact else 19, True))
    rounded(draw, (x + 26, y + 125, x + sidebar_w - 26, y + 238), 14, PANEL, LINE, 2)
    rounded(draw, (x + 42, y + 141, x + 132, y + 207), 8, "#e8f0ff", "#c7d2fe", 1)
    draw.polygon([(x + 52, y + 198), (x + 77, y + 171), (x + 110, y + 198)], fill="#7aa4ff")
    draw.text((x + 150, y + 151), "FRAME_13_SPF30", fill=INK, font=font(16 if not compact else 13, True))
    draw.text((x + 150, y + 179), "2000 x 3453", fill=MUTED, font=font(14 if not compact else 12))

    button_y = y + 256
    labels = [("Crop", 62), ("Replace", 92), ("Remix", 78)]
    bx = x + 28
    for label, bw in labels:
        fill = "#eaf2ff" if label == "Replace" else "#ffffff"
        outline = BLUE if label == "Replace" else "#cbd5e1"
        rounded(draw, (bx, button_y, bx + bw, button_y + 38), 8, fill, outline, 2)
        draw.text((bx + 14, button_y + 10), label, fill=BLUE if label == "Replace" else INK, font=font(14, label == "Replace"))
        bx += bw + 10

    canvas_x = x + sidebar_w + 40
    canvas_y = y + 95
    canvas_w = w - sidebar_w - 80
    canvas_h = h - 145
    rounded(draw, (canvas_x, canvas_y, canvas_x + canvas_w, canvas_y + canvas_h), 10, "#f9fbff", "#e2e8f0", 2)
    rounded(draw, (canvas_x + 34, canvas_y + 48, canvas_x + canvas_w - 34, canvas_y + canvas_h - 62), 14, "#102319", None)
    draw.ellipse((canvas_x + canvas_w - 120, canvas_y + 85, canvas_x + canvas_w - 50, canvas_y + 155), fill="#d7ded3")
    draw.rectangle((canvas_x + canvas_w - 96, canvas_y + 130, canvas_x + canvas_w - 72, canvas_y + 245), fill="#f7f2e8")
    draw.text((canvas_x + canvas_w - 102, canvas_y + 206), "IMG", fill="#62432f", font=font(18, True))
    callout_x = canvas_x + 46
    callout_y = canvas_y + canvas_h - 116
    rounded(draw, (callout_x, callout_y, callout_x + 238, callout_y + 48), 12, "#ffffff", "#b8cdfd", 2)
    draw.text((callout_x + 18, callout_y + 12), "Replace restored", fill=BLUE_DARK, font=font(23 if not compact else 18, True))


def draw_tile(path, size, title_size, subtitle_size):
    img = gradient(size, "#eef5ff", "#dbeafe")
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.ellipse((w * 0.70, -h * 0.25, w * 1.08, h * 0.55), fill="#c8dcff")
    draw.ellipse((-w * 0.12, h * 0.62, w * 0.22, h * 1.20), fill="#d7fae5")
    mark_scale = max(0.9, w / 1000)
    mark_x = int(w * 0.08)
    mark_y = int(h * 0.22)
    draw_replace_mark(draw, mark_x, mark_y, mark_scale)

    text_x = int(w * (0.25 if w < 700 else 0.20))
    text_y = int(h * 0.24)
    max_width = int(w * 0.68)
    title_font = font(title_size, True)
    subtitle_font = font(subtitle_size)
    title_lines = ["Klaviyo Replace", "Button Restorer"]
    for index, line in enumerate(title_lines):
        draw.text((text_x, text_y + index * int(title_size * 1.15)), line, fill=INK, font=title_font)

    subtitle = "Restore the one-click image Replace button."
    subtitle_y = text_y + int(title_size * 2.55)
    for index, line in enumerate(wrap_text(draw, subtitle, subtitle_font, max_width)):
        draw.text((text_x, subtitle_y + index * int(subtitle_size * 1.45)), line, fill=MUTED, font=subtitle_font)
    img.save(path)


def rebuild_zip():
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(EXTENSION_DIR.rglob("*")):
            if file.is_file():
                zf.write(file, file.relative_to(EXTENSION_DIR).as_posix())


def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    STORE_DIR.mkdir(parents=True, exist_ok=True)

    for size in (16, 32, 48, 128):
        draw_icon(ICONS_DIR / f"icon-{size}.png", size)
    draw_icon(STORE_DIR / "store-icon-128.png", 128)

    screenshot = Image.new("RGB", (1280, 800), "#eef2f7")
    draw = ImageDraw.Draw(screenshot)
    draw_ui_mockup(draw, 64, 62, 1152, 676)
    screenshot.save(STORE_DIR / "screenshot-1280x800.png")

    small_screenshot = Image.new("RGB", (640, 400), "#eef2f7")
    draw = ImageDraw.Draw(small_screenshot)
    draw_ui_mockup(draw, 32, 30, 576, 338, compact=True)
    small_screenshot.save(STORE_DIR / "screenshot-640x400.png")

    draw_tile(STORE_DIR / "small-promo-tile-440x280.png", (440, 280), 38, 18)
    draw_tile(STORE_DIR / "marquee-promo-tile-1400x560.png", (1400, 560), 74, 30)
    rebuild_zip()


if __name__ == "__main__":
    main()
