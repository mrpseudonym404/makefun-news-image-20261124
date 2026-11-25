#!/usr/bin/env python3
"""Build the news-image entry for 24 November 2026.

Renders 'The World in One Day - Tuesday 24 November 2026' as a 1024x1024
newspaper-style summary: one hero story (Nvidia / Jensen Huang), a 2x2 grid
of four cards, a BY THE NUMBERS strip, and four ALSO TODAY items.

Deterministic: PIL only, no network, no randomness. Output is written next
to this script as entry-20261124.png, or to the path given as argv[1].
The hero photograph (hero-20261124.png) must sit next to this script.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
CREAM = (247, 241, 222)      # page background
CARD = (255, 253, 245)       # card / strip background
INK = (20, 20, 20)           # near-black
BLACK = (17, 17, 17)         # masthead / dark boxes
RED = (179, 39, 30)          # accent red
GOLD = (217, 168, 33)        # date gold
BLUE = (31, 78, 121)         # POLITICS tag
PURPLE = (108, 52, 131)      # WORLD tag
GREEN = (30, 132, 73)        # positive numbers
GREY = (85, 85, 85)          # secondary text
LIGHT_GREY = (200, 196, 182) # hairlines
BODY_GREY = (51, 51, 51)

# ---- fonts --------------------------------------------------------------
FONT_DIRS = [
    Path.home() / ".fonts",
    Path.home() / "workspace" / "tools" / "fonts",
    Path("/usr/share/fonts/truetype/dejavu"),
]


def find_font(names):
    for d in FONT_DIRS:
        for n in names:
            p = d / n
            if p.exists():
                return str(p)
    return None


ANTON = find_font(["Anton-Regular.ttf"]) or find_font(["DejaVuSans-Bold.ttf"])
BEBAS = find_font(["BebasNeue-Regular.ttf"]) or ANTON
SANS = find_font(["DejaVuSans.ttf"])
SANS_BOLD = find_font(["DejaVuSans-Bold.ttf"]) or SANS


def font(path, size):
    return ImageFont.truetype(path, size)


# ---- text helpers -------------------------------------------------------
def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def fit_one_line(draw, text, fnt_path, size, max_w, min_size=13):
    """Shrink the font until the text fits on one line; returns the font."""
    s = size
    while s > min_size:
        f = font(fnt_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(fnt_path, min_size)


# ---- sections -----------------------------------------------------------
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 104], fill=BLACK)
    title = font(ANTON, 56)
    draw.text((W // 2, 12), "THE WORLD IN ONE DAY", font=title,
              fill=(255, 255, 255), anchor="ma")
    date = font(ANTON, 24)
    draw.text((W // 2, 72), "TUESDAY, 24 NOVEMBER 2026", font=date,
              fill=GOLD, anchor="ma")
    draw.rectangle([0, 104, W, 108], fill=RED)


def draw_kicker(draw):
    f = font(SANS_BOLD, 18)
    draw.text((W // 2, 118),
              "NINE STORIES THAT DEFINED THE DAY \u2022 MARKETS \u2022 WAR "
              "\u2022 INDONESIA \u2022 JUSTICE",
              font=f, fill=GREY, anchor="ma")


def hero_photo():
    """Crop the portrait hero photo to the wide hero band, with a scrim."""
    im = Image.open(HERE / "hero-20261124.png").convert("RGB")
    sw, sh = im.size
    target_w, target_h = 616, 200
    crop_h = int(sw * target_h / target_w)
    y0 = 115  # band centred on the face: hair top ~130, chin ~280
    y0 = max(0, min(y0, sh - crop_h))
    im = im.crop((0, y0, sw, y0 + crop_h)).resize(
        (target_w, target_h), Image.LANCZOS)
    # dark scrim over the bottom third so the white headline reads
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    scrim_top = int(target_h * 0.42)
    for yy in range(scrim_top, target_h):
        alpha = int(200 * (yy - scrim_top) / (target_h - scrim_top))
        od.line([(0, yy), (target_w, yy)], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def draw_hero(draw, img):
    photo = hero_photo()
    img.paste(photo, (24, 152))
    head = font(ANTON, 60)
    draw.text((36, 272), "HUANG IS BACK", font=head, fill=(255, 255, 255))

    # WHAT HAPPENS NEXT box
    draw.rectangle([652, 152, 1000, 352], fill=BLACK)
    title = font(ANTON, 28)
    draw.text((668, 162), "WHAT HAPPENS", font=title, fill=GOLD)
    draw.text((668, 194), "NEXT", font=title, fill=GOLD)
    bullets = [
        "Board reversed itself \u2014 judgment under scrutiny",
        "Rally must hold after leadership vacuum",
        "NVDA nears $4T cap",
    ]
    bf = font(SANS, 16)
    y = 236
    for b in bullets:
        lines = wrap_text(draw, b, bf, 312)
        for i, line in enumerate(lines):
            prefix = "\u2022  " if i == 0 else "     "
            draw.text((668, y), prefix + line, font=bf,
                      fill=(255, 255, 255))
            y += 21
        y += 4

    # hero body, two lines
    body = font(SANS, 20)
    text = ("Nvidia's board unanimously reinstates Jensen Huang as CEO \u2014 "
            "11 days after he resigned, and 6 days after saying it would "
            "not. NVDA soars 31%, its best day since 2003, adding $952B "
            "in value.")
    lines = wrap_text(draw, text, body, 976)
    draw_lines(draw, 24, 364, lines[:2], body, INK, 26)


def draw_sparkline(draw):
    draw.rectangle([24, 426, 1000, 428], fill=RED)
    draw.rectangle([24, 428, 1000, 486], fill=CARD, outline=LIGHT_GREY)
    lab = font(SANS_BOLD, 15)
    draw.text((36, 446), "NVDA", font=lab, fill=INK)
    sub = font(SANS, 13)
    draw.text((92, 448), "\u2014 2 WEEKS", font=sub, fill=GREY)

    # two-week path: slow slide, then the +31% jump on Monday
    pts = [(180, 450), (280, 454), (380, 458), (480, 462), (560, 466),
           (640, 470), (720, 474), (790, 478), (860, 462), (975, 442)]
    draw.line(pts, fill=INK, width=2)
    for (x, y) in pts:
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=INK)
    draw.ellipse([975 - 4, 442 - 4, 975 + 4, 442 + 4], fill=GREEN)
    neg = font(SANS_BOLD, 15)
    draw.text((742, 434), "\u221233%", font=neg, fill=RED)
    pos = font(SANS_BOLD, 15)
    draw.text((820, 432), "+31% MON", font=pos, fill=GREEN)


def draw_card(draw, x, y, w, h, accent, tag, headline, body_text):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LIGHT_GREY)
    draw.rectangle([x, y, x + w, y + 4], fill=accent)
    tf = font(BEBAS, 21)
    draw.text((x + 16, y + 12), tag, font=tf, fill=accent)
    hf = font(SANS_BOLD, 25)
    lines = wrap_text(draw, headline, hf, w - 32)
    draw_lines(draw, x + 16, y + 38, lines[:2], hf, INK, 29)
    bf = font(SANS, 17)
    blines = wrap_text(draw, body_text, bf, w - 32)
    draw_lines(draw, x + 16, y + 100, blines[:2], bf, BODY_GREY, 21)


def draw_cards(draw):
    cw, ch = 486, 158
    draw_card(draw, 24, 500, cw, ch, RED, "WAR",
              "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
              "Seven sea drones sank Merkury off Benghazi \u2014 the ~40th "
              "warship lost since 2022.")
    draw_card(draw, 514, 500, cw, ch, RED, "INDONESIA",
              "26 BODY BAGS AFTER CANDY-FACTORY FIRE",
              "Cikande blaze killed at least 26; 28 missing, DNA tests "
              "under way. Police probe negligence.")
    draw_card(draw, 24, 666, cw, ch, BLUE, "POLITICS",
              "PRABOWO NAMES TWO FOR VICE PRESIDENT",
              "Amran Sulaiman, Sugiono to replace Gibran; MPR's 732 vote "
              "11 Dec, serves to 2029.")
    draw_card(draw, 514, 666, cw, ch, PURPLE, "WORLD",
              "14 NATIONS BACK GENOCIDE RULING ON MYANMAR",
              "The ICJ's first genocide verdict in 80 years is binding. "
              "Britain sanctioned 5 generals.")


def draw_numbers(draw):
    y0, h = 836, 62
    draw.rectangle([24, y0, 1000, y0 + h], fill=CARD, outline=LIGHT_GREY)
    draw.rectangle([24, y0, 1000, y0 + 3], fill=RED)
    cols = [
        ("+6.51%", GREEN, "NASDAQ'S BEST DAY", "SINCE APRIL 2025"),
        ("167,113", INK, "CPNS 2026", "FORMATIONS"),
        ("61M", RED, "TONS OF RUBBLE", "IN GAZA"),
        ("$2,500", INK, "FINE PER GROK", "VIOLATION"),
    ]
    col_w = 244
    nf = font(ANTON, 24)
    lf = font(SANS_BOLD, 12)
    for i, (num, color, l1, l2) in enumerate(cols):
        x = 24 + i * col_w
        if i:
            draw.line([(x, y0 + 10), (x, y0 + h - 10)], fill=LIGHT_GREY)
        draw.text((x + 16, y0 + 6), num, font=nf, fill=color)
        draw.text((x + 16, y0 + 34), l1, font=lf, fill=GREY)
        draw.text((x + 16, y0 + 48), l2, font=lf, fill=GREY)


def draw_also_today(draw):
    hf = font(ANTON, 23)
    draw.text((24, 902), "ALSO TODAY", font=hf, fill=INK)
    items = [
        ("MARKETS", "MSCI firm on Indonesia review; rupiah Rp18,227 "
         "(\u22120.15%), IHSG +0.49% to 5,241.59."),
        ("TECH", "Virginia & Oregon sue SpaceX over Grok's >20,000 images "
         "of children \u2192 first state suits."),
        ("GAZA", "Oxfam: >99% of Gaza contaminated by war debris \u2192 "
         "water ~18 litres per person a day."),
        ("VENEZUELA", "US designates Cartel de los Soles a terrorist "
         "group \u2192 freezes; Maduro denies it exists."),
    ]
    y = 928
    for label, text in items:
        lf = font(SANS_BOLD, 16)
        lw = draw.textlength(label + " \u2014 ", font=lf)
        full = label + " \u2014 " + text
        bf = fit_one_line(draw, full, SANS, 16, 976)
        draw.text((24, y), label + " \u2014 ", font=lf, fill=RED)
        draw.text((24 + lw, y), text, font=bf, fill=BODY_GREY)
        y += 19


def draw_footer(draw):
    f = font(SANS, 12)
    draw.text((W // 2, 1008),
              "As of 19:45 WIB \u2022 What to watch: Nvidia rally holds? "
              "\u2022 Sources: Reuters \u2022 AP \u2022 Bloomberg \u2022 "
              "Photo: Eidesvik / Wikimedia CC BY-SA",
              font=f, fill=GREY, anchor="ma")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "entry-20261124.png"
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_kicker(draw)
    draw_hero(draw, img)
    draw_sparkline(draw)
    draw_cards(draw)
    draw_numbers(draw)
    draw_also_today(draw)
    draw_footer(draw)
    img.save(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
