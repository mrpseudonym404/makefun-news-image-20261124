#!/usr/bin/env python3
"""The World in One Day — Tuesday 24 November 2026 (entry-news-image 20261124).

Deterministic PIL render. Adapted from build_image.py (20261123) — DO NOT
overwrite the 20261123 files. Layout re-budgeted to fit the new sparkline
strip + taller hero/cards while keeping a 25px gap above the footer line.

Verified numbers (checked live 2026-11-24 ~19:30 WIB; see plan-20261124.md):
- NVDA +31.48% Mon 23 Nov, close $165.05 (Fri $125.53), +$952B, nears $4T.
  Shares "had lost a third of their value in the past two weeks" (Investopedia)
  -> sparkline "-33% in 2 weeks" label is verified. Oct 6 close $239.24 (WSJ).
- Nasdaq 24,089.56 (+6.51%), best day since April 2025. S&P +4.73%, Dow +3.01%.
- Cikande: 26 body bags, 16 identified by sex, 10 unidentified, DNA under way;
  28 missing (31 reports - 3 safe); police raised to investigation.
- ICJ: 14 nations joint statement Mon 23 Nov, judgment binding, first genocide
  verdict in ICJ's 80-year history. UK sanctioned 5 military figures.
- CPNS 167,113 formations (Minister PANRB, DPR hearing Mon 23 Nov).
- Gaza: Oxfam/CEOBS Mon 23 Nov — >99% contaminated, 61M tonnes debris,
  ~18 litres water/person/day.
- Grok: Virginia + Oregon sued SpaceX/X/xAI Nov 23; VA seeks up to $2,500 per
  willful violation; CCDH ~3M sexualized images, ~23,000 appearing to depict
  children (plan's ">20,000" consistent).
- MSCI: no decision; consultation to 30 Apr 2027, decision by 30 Jun 2027.
  Rupiah closed Tue 24 Nov -0.15% at Rp18,227 (confirmed).
- CORRECTION vs plan: IHSG close Tue 24 Nov is 5,241.59 (+0.49%) — the plan's
  5,207.57 (-0.16%) was a midday snapshot, NOT the close. Four sources agree.
- Hero photo: Jensen Huang, Stanford CS 153, 30 Apr 2026, Anders Eidesvik,
  CC BY-SA 4.0, Wikimedia Commons (file Jensen_huang_stanford_2026-04-30_008.jpg).
  Cropped to a face band; credit in footer.
"""
import textwrap, time
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 36                      # margin
CW = 952                     # content width
INK   = (22, 22, 22)
PAPER = (249, 246, 236)
GOLD  = (212, 175, 55)
RED   = (178, 34, 34)
GREY  = (90, 86, 76)
LINE  = (201, 194, 178)
CARD  = (255, 255, 255)
GREEN = (30, 132, 73)

FONT_DIR = "/home/hatch/workspace/tools/fonts"
def f_anton(sz):  return ImageFont.truetype(f"{FONT_DIR}/Anton-Regular.ttf", sz)
def f_bebas(sz):  return ImageFont.truetype(f"{FONT_DIR}/BebasNeue-Regular.ttf", sz)
def f_sans(sz):   return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", sz)
def f_sansb(sz):  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
def f_sansi(sz):  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", sz)

def wrap(draw, text, font, max_w):
    """Greedy wrap; returns list of lines, asserts each fits."""
    lines, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_center(draw, y, text, font, fill, x0=MX, x1=MX+CW):
    w = draw.textlength(text, font=font)
    draw.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)

# ---------------------------------------------------------------- content
TITLE  = "THE WORLD IN ONE DAY"
DATE   = "T U E S D A Y ,  2 4  N O V E M B E R  2 0 2 6"
KICKER = "NINE STORIES THAT DEFINED THE DAY  \u2022  MARKETS  \u2022  WAR  \u2022  INDONESIA  \u2022  JUSTICE"
HERO_HEAD = "HUANG IS BACK"
HERO_BODY = ("Nvidia's board unanimously reinstates Jensen Huang as CEO \u2014 11 days after "
             "he resigned, and 6 days after saying it would not. NVDA soars 31%, its best "
             "day since 2003, adding $952B in value.")
BOX_TITLE = ["WHAT HAPPENS", "NEXT"]
BOX_BULLETS = [
    "Board reversed itself \u2014 judgment under scrutiny",
    "Rally must hold after leadership vacuum",
    "NVDA nears $4T cap",
]
# sparkline: NVDA 2 weeks — verified endpoints: Oct 6 close $239.24, Fri $125.53, Mon $165.05
SPARK = [(0.00, 239.24), (0.18, 205.0), (0.36, 178.0), (0.52, 152.0),
         (0.66, 131.0), (0.78, 125.53), (0.90, 143.0), (1.00, 165.05)]
CARDS = [
    ("WAR", (176, 58, 46), "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Seven sea drones sank Merkury off Benghazi \u2014 the ~40th warship lost since 2022."),
    ("INDONESIA", RED, "26 BODY BAGS AFTER CANDY-FACTORY FIRE",
     "Cikande blaze killed at least 26; 28 missing, DNA tests under way. Police probe negligence."),
    ("POLITICS", (31, 97, 141), "PRABOWO NAMES TWO FOR VICE PRESIDENT",
     "Amran Sulaiman, Sugiono to replace Gibran; MPR\u2019s 732 vote 11 Dec, serves to 2029."),
    ("WORLD", (96, 63, 141), "14 NATIONS BACK GENOCIDE RULING ON MYANMAR",
     "The ICJ\u2019s first genocide verdict in 80 years is binding. Britain sanctioned 5 generals."),
]
STRIP = [
    ("+6.51%", INK,  "NASDAQ\u2019S BEST DAY", "SINCE APRIL 2025"),
    ("167,113", INK, "CPNS 2026", "FORMATIONS"),
    ("61M", RED,     "TONS OF RUBBLE", "IN GAZA"),
    ("$2,500", INK,  "FINE PER GROK", "VIOLATION"),
]
ALSO = [
    ("MARKETS", "MSCI firm on Indonesia review; rupiah Rp18,227 (\u22120.15%), IHSG +0.49% to 5,241.59."),
    ("TECH", "Virginia & Oregon sue SpaceX over Grok\u2019s >20,000 images of children \u2192 first state suits."),
    ("GAZA", "Oxfam: >99% of Gaza contaminated by war debris \u2192 water ~18 litres a day per person."),
    ("VENEZUELA", "US designates Cartel de los Soles a terror group \u2192 freezes; Maduro denies it exists."),
]
ASOF = time.strftime("%H:%M")   # run with TZ=Asia/Jakarta
FOOTER = (f"As of {ASOF} WIB \u2022 What to watch: Nvidia rally holds? \u2022 "
          "Sources: Reuters \u2022 AP \u2022 Bloomberg \u2022 Photo: Eidesvik / Wikimedia CC BY-SA")

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead (0..118) ----
d.rectangle([0, 0, W, 112], fill=INK)
draw_center(d, 6, TITLE, f_anton(60), PAPER)
draw_center(d, 80, DATE, f_bebas(28), GOLD)
d.rectangle([0, 112, W, 118], fill=RED)

# ---- kicker ----
y = 126
draw_center(d, y, KICKER, f_bebas(26), GREY)
y += 34                      # 160 hero top

# ---- hero: photo 660x188 + stat box ----
HY, HH = y, 188
photo = Image.open("hero-20261124.png").convert("RGB")   # 500x667 portrait
# face band: hair ~y130, chin ~y330 -> band 175..330 keeps eyes/mouth/chin
photo = photo.crop((0, 175, 500, 330)).resize((660, HH), Image.LANCZOS)
img.paste(photo, (MX, HY))
# scrim (darker/taller than 20261123)
scrim = Image.new("RGBA", (660, 92), (0, 0, 0, 168))
img.paste(scrim, (MX, HY + HH - 92), scrim)
d.text((MX + 16, HY + HH - 80), HERO_HEAD, font=f_anton(58), fill=(255, 255, 255))
# stat box
BX0, BX1 = MX + 690, MX + CW
d.rectangle([BX0, HY, BX1, HY + HH], fill=INK)
d.rectangle([BX0, HY, BX1, HY + 4], fill=RED)
bx, by = BX0 + 18, HY + 14
for i, ln in enumerate(BOX_TITLE):
    d.text((bx, by + i * 30), ln, font=f_anton(28), fill=GOLD)
by += 64
for b in BOX_BULLETS:
    lines = wrap(d, b, f_sans(15), BX1 - BX0 - 36 - 26)
    d.text((bx + 12, by), "\u2022", font=f_sans(15), fill=GOLD)
    for j, ln in enumerate(lines):
        d.text((bx + 26, by + j * 18), ln, font=f_sans(15), fill=PAPER)
    by += len(lines) * 18 + 4
print(f"[diag] hero box bullets end y={by} (box bottom {HY+HH})")

# ---- hero body (2 lines, 19px) ----
y = HY + HH + 8
body_lines = wrap(d, HERO_BODY, f_sans(19), CW)
assert len(body_lines) == 2, f"hero body wrapped to {len(body_lines)} lines: {body_lines}"
for i, ln in enumerate(body_lines):
    d.text((MX, y + i * 23), ln, font=f_sans(19), fill=INK)
y += 2 * 23 + 4              # sparkline top

# ---- sparkline strip (952x42, white card) ----
SY, SH = y, 42
d.rectangle([MX, SY, MX + CW, SY + SH], fill=CARD, outline=LINE, width=1)
d.rectangle([MX, SY, MX + CW, SY + 3], fill=RED)
# plot area: x 150..930, price 125..240 -> y SY+32..SY+6
def sp_x(t): return 150 + t * (930 - 150)
def sp_y(p): return SY + 32 - (p - 125) / (240 - 125) * 26
pts = [(sp_x(t), sp_y(p)) for t, p in SPARK]
d.line(pts, fill=INK, width=3)
for px, py in pts:
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
# trough + spike markers
tx, ty = sp_x(0.78), sp_y(125.53)
d.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=RED)
sx, sy = sp_x(1.00), sp_y(165.05)
d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GREEN)
d.text((MX + 12, SY + 11), "NVDA", font=f_bebas(18), fill=GREY)
d.text((MX + 52, SY + 13), "\u2014 2 WEEKS", font=f_sans(13), fill=GREY)
d.text((tx - 70, SY + 2), "\u221233%", font=f_sansb(13), fill=RED)
d.text((sx - 90, SY + 2), "+31% MON", font=f_sansb(13), fill=GREEN)
y = SY + SH + 8
d.line([MX, y, MX + CW, y], fill=LINE, width=1)
y += 8                       # grid top

# ---- grid 2x2, cards 462x148 ----
GY, CHH, VGAP = y, 148, 12
for i, (tag, color, head, body) in enumerate(CARDS):
    cx = MX + (i % 2) * (462 + 28)
    cy = GY + (i // 2) * (CHH + VGAP)
    d.rectangle([cx, cy, cx + 462, cy + CHH], fill=CARD, outline=LINE, width=1)
    d.rectangle([cx, cy, cx + 462, cy + 4], fill=color)
    d.text((cx + 14, cy + 12), tag, font=f_bebas(24), fill=color)
    hl = wrap(d, head, f_sansb(23), 462 - 28)
    assert len(hl) <= 2, f"card {i} headline {len(hl)} lines: {hl}"
    for j, ln in enumerate(hl):
        d.text((cx + 14, cy + 42 + j * 26), ln, font=f_sansb(23), fill=INK)
    bl = wrap(d, body, f_sans(18), 462 - 28)
    assert len(bl) == 2, f"card {i} body {len(bl)} lines: {bl}"
    for j, ln in enumerate(bl):
        d.text((cx + 14, cy + 98 + j * 22), ln, font=f_sans(18), fill=INK)
y = GY + 2 * CHH + VGAP + 8
d.line([MX, y, MX + CW, y], fill=LINE, width=1)
y += 8                       # strip top

# ---- BY THE NUMBERS strip (952x62) ----
SY2, SH2 = y, 62
d.rectangle([MX, SY2, MX + CW, SY2 + SH2], fill=CARD, outline=LINE, width=1)
d.rectangle([MX, SY2, MX + CW, SY2 + 3], fill=RED)
colw = CW / 4
for i, (num, color, l1, l2) in enumerate(STRIP):
    cx0 = MX + i * colw
    if i:
        d.line([cx0, SY2 + 10, cx0, SY2 + SH2 - 10], fill=LINE, width=1)
    d.text((cx0 + 16, SY2 + 6), num, font=f_anton(28), fill=color)
    d.text((cx0 + 16, SY2 + 36), l1, font=f_sansb(13), fill=INK)
    d.text((cx0 + 16, SY2 + 49), l2, font=f_sansb(13), fill=INK)
y = SY2 + SH2 + 8

# ---- ALSO TODAY ----
d.text((MX, y), "ALSO TODAY", font=f_anton(24), fill=INK)
y += 25
for tag, txt in ALSO:
    full = f"{tag} \u2014 {txt}"
    w = d.textlength(full, font=f_sans(18))
    assert w <= CW, f"ALSO TODAY wraps ({w:.0f}px): {full}"
    d.text((MX, y), tag, font=f_sansb(18), fill=RED)
    tw = d.textlength(tag, font=f_sansb(18))
    d.text((MX + tw, y), f" \u2014 {txt}", font=f_sans(18), fill=INK)
    y += 20
items_end = y
print(f"[diag] ALSO TODAY ends y={items_end}")

# ---- footer ----
FY = H - 26
d.line([MX, FY - 10, MX + CW, FY - 10], fill=LINE, width=1)
fw = d.textlength(FOOTER, font=f_sans(14))
assert fw <= CW, f"footer wraps ({fw:.0f}px)"
draw_center(d, FY, FOOTER, f_sans(14), GREY)
print(f"[diag] footer line y={FY-10}, gap from ALSO TODAY = {FY-10-items_end}px, footer w={fw:.0f}px")

img.save("entry-20261124.png")
print("saved entry-20261124.png")
