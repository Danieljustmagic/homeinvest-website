#!/usr/bin/env python3
"""
HomeInvest Immobilier — Page d'accueil mockup
Inspiré de Scale with Ouss : typo XXL, numéros géants, cartes bordurées, photo en cercle décoré
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

# ── Dimensions ──────────────────────────────────────────────────────────────
W = 1440
H = 4200  # tall canvas; will be cropped

FONTS = "/Users/danielinvernon/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/29fc74f7-03ff-446e-8983-32a1b23e5a13/9e579411-ca43-4f0f-8103-fa52016de7b9/skills/canvas-design/canvas-fonts"

# ── Palette ──────────────────────────────────────────────────────────────────
RED        = (212, 20,  20)
RED_SOFT   = (220, 60,  60)
GRAY_DARK  = (64,  64,  64)
GRAY_MED   = (120, 120, 120)
GRAY_LIGHT = (176, 176, 176)
GRAY_PALE  = (220, 218, 215)
CREAM      = (248, 245, 240)
WHITE      = (255, 255, 255)
BLACK      = (20,  20,  20)

# ── Font helpers ─────────────────────────────────────────────────────────────
def f(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

BIG   = lambda s: f("BigShoulders-Bold.ttf",        s)  # impact / numbers
CRIB  = lambda s: f("CrimsonPro-Bold.ttf",           s)  # elegant serif titles
CRII  = lambda s: f("CrimsonPro-Italic.ttf",         s)  # serif italic
OUTB  = lambda s: f("Outfit-Bold.ttf",               s)  # UI bold
OUTR  = lambda s: f("Outfit-Regular.ttf",            s)  # UI regular
WRKB  = lambda s: f("WorkSans-Bold.ttf",             s)  # nav / labels
WRKR  = lambda s: f("WorkSans-Regular.ttf",          s)  # nav regular
BRICB = lambda s: f("BricolageGrotesque-Bold.ttf",   s)  # display bold
BRICR = lambda s: f("BricolageGrotesque-Regular.ttf",s)  # body

# ── Canvas ────────────────────────────────────────────────────────────────────
img  = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

def tlen(text, font):
    return int(draw.textlength(text, font=font))

def cx_text(text, font, y, color=GRAY_DARK):
    w = tlen(text, font)
    draw.text(((W - w) // 2, y), text, font=font, fill=color)

def label_tag(text, x, y, bg=RED, fg=WHITE):
    tw = tlen(text, WRKB(12)) + 24
    draw.rectangle([x, y, x + tw, y + 26], fill=bg)
    draw.text((x + 12, y + 6), text, font=WRKB(12), fill=fg)
    return tw

def dashed_circle(cx, cy, r, color, width=2, dash=6, gap=4):
    step = dash + gap
    total = int(2 * math.pi * r)
    for i in range(0, total, step):
        a1 = i / r
        a2 = (i + dash) / r
        x1 = cx + r * math.cos(a1)
        y1 = cy + r * math.sin(a1)
        x2 = cx + r * math.cos(a2)
        y2 = cy + r * math.sin(a2)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

def wrap_text(text, font, max_w, draw_at=None, x=0, y=0, color=GRAY_MED, line_h=22):
    words = text.split()
    lines = []
    line  = ""
    for w in words:
        test = line + w + " "
        if tlen(test, font) > max_w:
            lines.append(line.strip())
            line = w + " "
        else:
            line = test
    if line:
        lines.append(line.strip())
    if draw_at:
        for i, l in enumerate(lines):
            draw.text((x, y + i * line_h), l, font=font, fill=color)
    return lines

y = 0  # running y cursor


# ══════════════════════════════════════════════════════════
#  1. NAVBAR
# ══════════════════════════════════════════════════════════
NAV_H = 80
draw.rectangle([0, 0, W, NAV_H], fill=WHITE)
draw.line([(0, NAV_H), (W, NAV_H)], fill=GRAY_PALE, width=1)

# Logo mark (H + I)
lx, ly = 48, 18
draw.rectangle([lx,       ly+4,  lx+9,  ly+40], fill=RED)        # H left leg
draw.rectangle([lx+20,    ly+4,  lx+29, ly+40], fill=RED)        # H right leg
draw.rectangle([lx+9,     ly+19, lx+20, ly+27], fill=RED)        # H crossbar
draw.rectangle([lx+36,    ly+4,  lx+43, ly+40], fill=GRAY_LIGHT) # I bar

draw.text((lx+52, ly+6),  "HOMEINVEST", font=WRKB(16), fill=GRAY_DARK)
draw.text((lx+52, ly+27), "IMMOBILIER", font=WRKB(11), fill=RED)

# Nav links
nav_items = ["Ventes", "Locations", "Estimation", "Équipe", "Contact"]
nx = 760
for item in nav_items:
    draw.text((nx, 30), item, font=WRKR(14), fill=GRAY_DARK)
    nx += tlen(item, WRKR(14)) + 44

# CTA button
draw.rectangle([1310, 22, 1390, 56], fill=RED)
draw.text((1324, 31), "Estimer", font=WRKB(14), fill=WHITE)

y = NAV_H


# ══════════════════════════════════════════════════════════
#  2. HERO
# ══════════════════════════════════════════════════════════
HERO_H = 680

# ── Marseille – Vieux-Port illustration ──
HORIZ = y + 415   # quay / sea level
SEA_Y = y + 432   # water surface

# 1. Mediterranean sky (deep blue → warm golden horizon)
for i in range(HERO_H):
    t = i / HERO_H
    r = int(72  + 158 * (t ** 0.55))
    g = int(108 + 88  * (t ** 0.65))
    b = int(198 - 68  * t)
    draw.line([(0, y + i), (W, y + i)], fill=(r, g, b))

# 2. Sea (overdraws sky in lower portion)
for i in range(HERO_H - 415 + 1):
    t = i / max(1, HERO_H - 415)
    r = int(48 + 18 * t)
    g = int(112 + 28 * t)
    b = int(192 - 22 * t)
    draw.line([(0, HORIZ + i), (W, HORIZ + i)], fill=(r, g, b))

# 3. Distant coastline right
far_coast = [
    (600, HORIZ), (660, HORIZ-18), (730, HORIZ-28),
    (800, HORIZ-15), (870, HORIZ-22), (1200, HORIZ-8),
    (1440, HORIZ-12), (1440, HORIZ)
]
draw.polygon(far_coast, fill=(118, 98, 78))

# 4. Notre-Dame de la Garde — rocky hill
NDG_CX  = 1010
NDG_BASE = HORIZ - 148   # hill peak / church floor

hill_poly = [
    (820, HORIZ),
    (870, HORIZ-42), (920, HORIZ-80), (965, HORIZ-125),
    (NDG_CX-30, HORIZ-145), (NDG_CX, NDG_BASE),
    (NDG_CX+30, HORIZ-140),
    (1060, HORIZ-110), (1105, HORIZ-70), (1155, HORIZ-38),
    (1210, HORIZ-15), (1300, HORIZ-5), (1440, HORIZ)
]
draw.polygon(hill_poly, fill=(90, 74, 58))
hill_shadow = [
    (NDG_CX, NDG_BASE),
    (NDG_CX+30, HORIZ-140), (1060, HORIZ-110),
    (1050, HORIZ-60), (NDG_CX+15, HORIZ-80)
]
draw.polygon(hill_shadow, fill=(72, 58, 45))

# 5. Basilica Notre-Dame de la Garde
CH_W    = 110
CH_BASE = NDG_BASE
CH_TOP  = CH_BASE - 58

# Main nave
draw.rectangle([NDG_CX-CH_W//2, CH_TOP, NDG_CX+CH_W//2, CH_BASE], fill=(248, 241, 222))
# Side volumes
draw.rectangle([NDG_CX-CH_W//2-22, CH_BASE-38, NDG_CX-CH_W//2, CH_BASE], fill=(235, 226, 208))
draw.rectangle([NDG_CX+CH_W//2, CH_BASE-38, NDG_CX+CH_W//2+22, CH_BASE],  fill=(235, 226, 208))
# Nave roof
draw.polygon([(NDG_CX-CH_W//2-4, CH_TOP), (NDG_CX+CH_W//2+4, CH_TOP),
              (NDG_CX, CH_TOP-14)], fill=(210, 195, 170))
# Arched windows
for wwx in [NDG_CX-32, NDG_CX-8, NDG_CX+16]:
    draw.rectangle([wwx, CH_TOP+14, wwx+18, CH_TOP+38], fill=(125, 152, 188))
    draw.ellipse([wwx, CH_TOP+6, wwx+18, CH_TOP+20],    fill=(125, 152, 188))

# Bell tower
TW  = 24
TX  = NDG_CX - TW//2
T_TOP = CH_TOP - 118
draw.rectangle([TX, T_TOP, TX+TW, CH_TOP], fill=(252, 246, 230))
for tbl in [T_TOP+28, T_TOP+58, T_TOP+88]:
    draw.line([(TX, tbl), (TX+TW, tbl)], fill=(205, 195, 175), width=1)
for twy in [T_TOP+10, T_TOP+40, T_TOP+70]:
    draw.rectangle([TX+6, twy, TX+18, twy+17], fill=(118, 145, 182))
    draw.ellipse([TX+6, twy-7, TX+18, twy+5],  fill=(118, 145, 182))
draw.rectangle([TX-4, T_TOP-8, TX+TW+4, T_TOP], fill=(220, 205, 180))

# Golden dome
D_CX  = NDG_CX
D_BASE = T_TOP - 4
draw.ellipse([D_CX-16, D_BASE-22, D_CX+16, D_BASE+10], fill=(218, 178, 32))
draw.ellipse([D_CX-8,  D_BASE-30, D_CX+8,  D_BASE-16], fill=(228, 188, 42))

# Madonna statue
M_BASE = D_BASE - 30
draw.line([(D_CX, M_BASE-40), (D_CX, M_BASE)], fill=(225, 185, 38), width=4)
draw.line([(D_CX-10, M_BASE-28), (D_CX+10, M_BASE-28)], fill=(225, 185, 38), width=3)
draw.ellipse([D_CX-6, M_BASE-52, D_CX+6, M_BASE-40], fill=(225, 185, 38))

# 6. Quay surface
draw.rectangle([0, HORIZ, W, SEA_Y], fill=(108, 92, 74))
draw.line([(0, SEA_Y), (W, SEA_Y)], fill=(88, 74, 60), width=2)
for bol_x in range(60, 680, 85):
    draw.rectangle([bol_x, HORIZ-10, bol_x+9, HORIZ+2], fill=(78, 65, 52))
    draw.ellipse([bol_x-2, HORIZ-14, bol_x+11, HORIZ-6],  fill=(68, 56, 44))

# 7. Quay buildings — Marseille Haussmann north quay
qbuilds = [
    #  x    w    h   facade               roof
    (  0,  90, 200, (202, 170, 110),  (155, 122, 76)),
    ( 90,  74, 168, (220, 188, 124),  (170, 135, 82)),
    (164,  96, 215, (196, 156,  98),  (150, 115, 70)),
    (260,  78, 180, (230, 200, 132),  (178, 142, 86)),
    (338,  88, 202, (206, 166, 106),  (158, 124, 75)),
    (426,  76, 160, (218, 184, 120),  (168, 132, 80)),
    (502,  86, 192, (200, 162, 102),  (154, 120, 73)),
    (588,  72, 172, (225, 192, 128),  (172, 138, 84)),
    (660,  82, 148, (214, 180, 116),  (164, 128, 78)),
    (742,  68, 135, (210, 175, 112),  (160, 126, 76)),
]
for bx, bw, bh, bc, rc in qbuilds:
    bt = HORIZ - bh
    draw.rectangle([bx, bt, bx+bw, HORIZ], fill=bc)
    draw.rectangle([bx-2, bt-12, bx+bw+2, bt], fill=rc)
    for chx in range(bx+10, bx+bw-8, 28):
        draw.rectangle([chx, bt-24, chx+8, bt-12], fill=rc)
    num_fl = min(4, bh // 44)
    for fl in range(num_fl):
        wy = bt + 16 + fl * 44
        for col in range(max(1, bw // 28 - 1)):
            wx_ = bx + 8 + col * 28
            if wx_ + 18 <= bx + bw - 8:
                draw.rectangle([wx_, wy, wx_+18, wy+26], fill=(158, 180, 215))
                draw.line([(wx_+9, wy), (wx_+9, wy+26)], fill=(135, 158, 195), width=1)
                draw.rectangle([wx_-5, wy-2, wx_, wy+28],    fill=(52, 80, 132))
                draw.rectangle([wx_+18, wy-2, wx_+23, wy+28], fill=(52, 80, 132))

# 8. Sailboats in the Vieux-Port
sailboats = [
    #  cx   hull_w  sail_h  sail_col
    ( 268,  74,  98, (244, 240, 230)),
    ( 365,  60,  80, (238, 232, 218)),
    ( 455,  82, 110, (242, 238, 226)),
    ( 562,  66,  88, (240, 234, 222)),
    ( 672,  56,  74, (235, 228, 215)),
    ( 788,  78, 102, (246, 242, 232)),
    ( 908,  62,  84, (238, 233, 220)),
    (1115,  52,  70, (232, 226, 212)),
]
for bcx, bw, sh, sc in sailboats:
    deck_y = SEA_Y + 5
    hh = 20 + bw // 8
    draw.polygon([
        (bcx-bw//2, deck_y), (bcx+bw//2, deck_y),
        (bcx+bw//2-7, deck_y+hh), (bcx-bw//2+7, deck_y+hh),
    ], fill=(248, 244, 236))
    draw.line([(bcx-bw//2+5, deck_y+hh//2), (bcx+bw//2-5, deck_y+hh//2)],
              fill=RED, width=3)
    mx = bcx + 4
    draw.line([(mx, deck_y-2), (mx, deck_y-sh)], fill=(88, 70, 50), width=3)
    # Main sail
    draw.polygon([
        (mx,                    deck_y-sh+6),
        (mx,                    deck_y-4),
        (mx+int(sh*0.58),       deck_y-int(sh*0.28)),
    ], fill=sc)
    # Jib
    draw.polygon([
        (mx,                    deck_y-sh+14),
        (mx-int(sh*0.30),       deck_y-int(sh*0.45)+18),
        (mx,                    deck_y-int(sh*0.45)),
    ], fill=(sc[0]-12, sc[1]-12, sc[2]-12))
    draw.line([(bcx-bw//2+5, deck_y+hh), (bcx+bw//2-5, deck_y+hh+5)],
              fill=(50, 100, 160), width=1)

# 9. Water reflections + waves
for wx_s in range(0, 750, 52):
    for row in range(4):
        ry_ = SEA_Y + 28 + row * 12 + (wx_s % 8)
        cb  = min(255, 68 + wx_s % 20)
        draw.line([(wx_s+row*5, ry_), (wx_s+42-row*3, ry_)], fill=(45, 92, cb), width=1)
for wx_w in range(0, W, 175):
    wy_w = SEA_Y + 48 + (wx_w % 35)
    draw.arc([wx_w,    wy_w,    wx_w+75,  wy_w+14], 0, 180, fill=(68, 128, 188), width=1)
    draw.arc([wx_w+40, wy_w+9,  wx_w+110, wy_w+20], 0, 180, fill=(62, 120, 180), width=1)

# ── Dark overlay ──
ov = Image.new("RGBA", (W, HERO_H), (15, 12, 10, 175))
base_img = img.convert("RGBA")
base_img.paste(ov, (0, y), ov)
img  = base_img.convert("RGB")
draw = ImageDraw.Draw(img)

# ── Hero text ──
label_w = label_tag("AGENCE INDÉPENDANTE · MARSEILLE & ALENTOURS",
                     (W - tlen("AGENCE INDÉPENDANTE · MARSEILLE & ALENTOURS", WRKB(12)) - 24) // 2,
                     y + 110)

h1 = "VOTRE BIEN,"
h2 = "NOTRE PASSION."
cx_text(h1, BIG(95),  y + 165, WHITE)
cx_text(h2, BIG(95),  y + 260, RED)

sub = "Tout l'immobilier dans votre région · 15 ans d'expérience"
cx_text(sub, CRII(22), y + 380, (215, 205, 195))

# Thin red rule
draw.line([(W//2-60, y+420), (W//2+60, y+420)], fill=RED, width=2)

# CTA buttons
b1x, b2x = W//2 - 225, W//2 + 25
draw.rectangle([b1x, y+448, b1x+185, y+494], fill=RED)
draw.text((b1x + (185 - tlen("Voir nos biens", WRKB(16)))//2, y+460),
          "Voir nos biens", font=WRKB(16), fill=WHITE)

draw.rectangle([b2x, y+448, b2x+185, y+494], outline=WHITE, width=2)
draw.text((b2x + (185 - tlen("Estimation gratuite", WRKB(15)))//2, y+461),
          "Estimation gratuite", font=WRKB(15), fill=WHITE)

y += HERO_H


# ══════════════════════════════════════════════════════════
#  3. STATS BAR
# ══════════════════════════════════════════════════════════
STATS_H = 110
draw.rectangle([0, y, W, y+STATS_H], fill=WHITE)
draw.line([(0, y),          (W, y)],          fill=GRAY_PALE, width=1)
draw.line([(0, y+STATS_H), (W, y+STATS_H)],  fill=GRAY_PALE, width=1)

stats = [("15 ans", "d'expérience"), ("+500", "biens vendus"), ("5", "experts locaux"), ("Marseille", "13e arrondissement")]
sw = W // 4
for i, (num, lbl) in enumerate(stats):
    sx = i * sw
    if i:
        draw.line([(sx, y+22), (sx, y+STATS_H-22)], fill=GRAY_PALE, width=1)
    nw = tlen(num, BIG(38))
    draw.text((sx + sw//2 - nw//2, y+14), num, font=BIG(38), fill=RED)
    lw = tlen(lbl, OUTR(13))
    draw.text((sx + sw//2 - lw//2, y+60), lbl, font=OUTR(13), fill=GRAY_MED)

y += STATS_H


# ══════════════════════════════════════════════════════════
#  4. SERVICES
# ══════════════════════════════════════════════════════════
SERV_H = 560
NAVY   = (22, 34, 62)

# Fond crème très léger pour différencier de la stats bar blanche
draw.rectangle([0, y, W, y+SERV_H], fill=(250, 248, 245))
draw.line([(0, y+SERV_H), (W, y+SERV_H)], fill=GRAY_PALE, width=1)

# Label + titre section
_lw = tlen("NOS SERVICES", WRKB(12)) + 24
draw.rectangle([(W-_lw)//2, y+36, (W+_lw)//2, y+62], fill=RED)
draw.text(((W - tlen("NOS SERVICES", WRKB(12)))//2, y+44),
          "NOS SERVICES", font=WRKB(12), fill=WHITE)
cx_text("Ce que nous faisons pour vous avec passion", CRIB(44), y+70, NAVY)

# Mise en page cartes
CARD_W = 400
CGAP   = 40
CMRG   = (W - 3*CARD_W - 2*CGAP) // 2

svc_data = [
    ("01", "Vente & Achat",
     "Trouvez le bien idéal ou vendez au meilleur prix. Notre réseau local fait la différence.",
     ["Résidentiel", "Terrain", "Neuf"]),
    ("02", "Location",
     "Gestion locative complète. Appartements, maisons, villas. Sérénité de A à Z.",
     ["Longue durée", "Gestion locative"]),
    ("03", "Immobilier Pro",
     "Bureaux, commerces, locaux d'activité. Nous accompagnons les entrepreneurs du territoire.",
     ["Bureaux", "Commerces"]),
]

for i, (num, title, desc, tags) in enumerate(svc_data):
    cx_c   = CMRG + i * (CARD_W + CGAP)
    cy_top = y + 148
    cy_bot = y + 508

    # Ombre portée
    draw.rectangle([cx_c+5, cy_top+5, cx_c+CARD_W+5, cy_bot+5], fill=(215, 210, 204))
    # Fond carte blanc
    draw.rectangle([cx_c, cy_top, cx_c+CARD_W, cy_bot], fill=WHITE)
    # Barre rouge en haut (6px)
    draw.rectangle([cx_c, cy_top, cx_c+CARD_W, cy_top+6], fill=RED)
    # Bordure fine grise
    draw.rectangle([cx_c, cy_top, cx_c+CARD_W, cy_bot], outline=GRAY_PALE, width=1)


    # ── Illustration Marseillaise centrée ──
    ICO_H = 110
    iy_i  = cy_top + 18
    icx   = cx_c + CARD_W // 2

    if i == 0:  # Maison provençale — ocre, volets bleus, tuiles terracotta
        facade_c  = (202, 168, 108)
        roof_c    = (178, 98,  68)
        shutter_c = (72,  108, 148)
        bx1, bx2  = icx - 52, icx + 52
        by_wall_top = iy_i + 42
        by_wall_bot = iy_i + ICO_H

        # Corps façade
        draw.rectangle([bx1, by_wall_top, bx2, by_wall_bot], fill=facade_c)

        # Toit pentu
        draw.polygon([
            (bx1 - 6, by_wall_top), (bx2 + 6, by_wall_top), (icx, iy_i + 4),
        ], fill=roof_c)
        # Rangées de tuiles
        for ti in range(3):
            ty_tile = iy_i + 12 + ti * 10
            for tx_tile in range(icx - 44 + ti * 8, icx + 44 - ti * 8, 18):
                draw.arc([tx_tile, ty_tile, tx_tile + 16, ty_tile + 10], 0, 180,
                         fill=(148, 72, 48), width=2)

        # Cheminée
        draw.rectangle([bx2 - 24, iy_i + 14, bx2 - 12, iy_i + 42], fill=(160, 88, 60))

        # Fenêtres avec volets
        for wx_off in [-30, 16]:
            wx1, wx2 = icx + wx_off, icx + wx_off + 20
            wy1, wy2 = by_wall_top + 12, by_wall_top + 36
            draw.rectangle([wx1 - 10, wy1, wx1 - 1, wy2], fill=shutter_c)
            draw.rectangle([wx1, wy1, wx2, wy2], fill=(148, 178, 210))
            draw.line([(wx1, (wy1+wy2)//2), (wx2, (wy1+wy2)//2)], fill=(118, 148, 180), width=1)
            draw.line([((wx1+wx2)//2, wy1), ((wx1+wx2)//2, wy2)], fill=(118, 148, 180), width=1)
            draw.rectangle([wx2 + 1, wy1, wx2 + 10, wy2], fill=shutter_c)

        # Porte cintrée
        px1, px2 = icx - 14, icx + 14
        py1 = by_wall_top + 52
        draw.rectangle([px1, py1, px2, by_wall_bot], fill=(88, 62, 38))
        draw.pieslice([px1, py1 - 12, px2, py1 + 4], 0, 180, fill=(88, 62, 38))
        draw.ellipse([icx - 3, py1 + 24, icx + 3, py1 + 30], fill=(200, 158, 58))

        # Sol
        draw.line([(bx1 - 8, by_wall_bot), (bx2 + 8, by_wall_bot)],
                  fill=(160, 132, 88), width=3)

    elif i == 1:  # Voilier du Vieux-Port
        boat_cx = icx + 4
        deck_y  = iy_i + ICO_H - 8
        hull_w  = 88

        # Vagues
        for wx_wave in range(icx - 68, icx + 62, 28):
            draw.arc([wx_wave, deck_y + 6, wx_wave + 22, deck_y + 14], 0, 180,
                     fill=(88, 148, 200), width=2)

        # Coque
        draw.polygon([
            (boat_cx - hull_w//2, deck_y),
            (boat_cx + hull_w//2, deck_y),
            (boat_cx + hull_w//2 - 10, deck_y + 22),
            (boat_cx - hull_w//2 + 10, deck_y + 22),
        ], fill=(248, 244, 236))
        draw.line([(boat_cx - hull_w//2 + 2, deck_y + 10),
                   (boat_cx + hull_w//2 - 2, deck_y + 10)], fill=RED, width=3)

        # Cabine
        draw.rectangle([boat_cx - 20, deck_y - 22, boat_cx + 14, deck_y],
                       fill=(238, 232, 218))
        draw.rectangle([boat_cx - 14, deck_y - 18, boat_cx - 4, deck_y - 6],
                       fill=(148, 178, 210))

        # Mât
        mast_x   = boat_cx + 6
        mast_top = iy_i + 2
        draw.line([(mast_x, deck_y - 2), (mast_x, mast_top)], fill=(88, 70, 50), width=3)
        # Barre de flèche
        draw.line([(mast_x - 22, mast_top + 38), (mast_x + 18, mast_top + 38)],
                  fill=(88, 70, 50), width=2)

        # Grande voile
        sail_h = deck_y - mast_top
        draw.polygon([
            (mast_x, mast_top + 4),
            (mast_x, deck_y - 4),
            (mast_x + int(sail_h * 0.65), deck_y - int(sail_h * 0.25)),
        ], fill=(244, 240, 230))

        # Foc
        draw.polygon([
            (mast_x, mast_top + 18),
            (mast_x - int(sail_h * 0.38), deck_y - int(sail_h * 0.42) + 10),
            (mast_x, deck_y - int(sail_h * 0.42)),
        ], fill=(232, 226, 212))

    else:  # Façade Haussmannienne marseillaise
        fb_x1, fb_x2 = icx - 56, icx + 56
        fb_top = iy_i + 8
        fb_bot = iy_i + ICO_H
        fac_c  = (210, 180, 118)
        cor_c  = (148, 112, 72)
        win_c  = (138, 168, 208)
        sht_c  = (64,  98,  138)

        # Corps
        draw.rectangle([fb_x1, fb_top + 16, fb_x2, fb_bot], fill=fac_c)

        # Corniche + mansarde
        draw.rectangle([fb_x1 - 4, fb_top + 4, fb_x2 + 4, fb_top + 18], fill=cor_c)
        draw.polygon([
            (fb_x1 - 4, fb_top + 4), (fb_x2 + 4, fb_top + 4),
            (fb_x2 - 6, fb_top),     (fb_x1 + 6, fb_top),
        ], fill=(128, 96, 60))

        # Lucarnes
        for luc_x in [icx - 28, icx + 8]:
            draw.pieslice([luc_x, fb_top - 8, luc_x + 18, fb_top + 2], 0, 180, fill=(88, 62, 40))
            draw.rectangle([luc_x, fb_top - 2, luc_x + 18, fb_top + 6], fill=(88, 62, 40))

        # Grille de fenêtres 3 colonnes × 3 rangées
        for fl in range(3):
            wy_fl = fb_top + 22 + fl * 28
            for col_idx in range(3):
                wx_col = fb_x1 + 10 + col_idx * 36
                draw.rectangle([wx_col,      wy_fl, wx_col + 7,  wy_fl + 20], fill=sht_c)
                draw.rectangle([wx_col + 7,  wy_fl, wx_col + 21, wy_fl + 20], fill=win_c)
                draw.line([(wx_col + 14, wy_fl), (wx_col + 14, wy_fl + 20)],
                          fill=(108, 138, 178), width=1)
                draw.rectangle([wx_col + 21, wy_fl, wx_col + 28, wy_fl + 20], fill=sht_c)
                draw.rectangle([wx_col + 5, wy_fl + 20, wx_col + 23, wy_fl + 23], fill=cor_c)

        # Porte voûtée centrale
        px1, px2 = icx - 14, icx + 14
        py1 = fb_bot - 34
        draw.rectangle([px1, py1, px2, fb_bot], fill=(72, 50, 32))
        draw.pieslice([px1, py1 - 14, px2, py1 + 4], 0, 180, fill=(72, 50, 32))
        draw.ellipse([icx - 3, py1 + 14, icx + 3, py1 + 20], fill=(188, 148, 48))

        # Trottoir
        draw.line([(fb_x1 - 12, fb_bot), (fb_x2 + 12, fb_bot)],
                  fill=(170, 140, 90), width=3)

    # ── Titre ──
    title_y = cy_top + 142
    draw.text((cx_c + 28, title_y), title, font=BRICB(26), fill=NAVY)
    tl_w = tlen(title, BRICB(26))
    draw.rectangle([cx_c+28, title_y+34, cx_c+28+tl_w, title_y+37], fill=RED)

    # ── Description ──
    wrap_text(desc, BRICR(16), CARD_W-56,
              draw_at=True, x=cx_c+28, y=title_y+50, color=GRAY_MED, line_h=26)


y += SERV_H


# ══════════════════════════════════════════════════════════
#  5. ENGAGEMENT SOCIÉTAL
# ══════════════════════════════════════════════════════════
ENG_H = 520

# Full cream background — unified, warm, human
draw.rectangle([0, y, W, y+ENG_H], fill=(248, 244, 238))

# Subtle top border
draw.line([(0, y), (W, y)], fill=GRAY_PALE, width=1)

# ── Left column — commitment text ──
lx_e = 100

# Section label
_elw = tlen("ENGAGEMENT SOCIÉTAL", WRKB(11)) + 24
draw.rectangle([lx_e, y+52, lx_e+_elw, y+76], fill=RED)
draw.text((lx_e+12, y+59), "ENGAGEMENT SOCIÉTAL", font=WRKB(11), fill=WHITE)

# Title — big serif
draw.text((lx_e, y+100), "Chaque transaction,", font=CRIB(48), fill=GRAY_DARK)
draw.text((lx_e, y+152), "un sourire de plus.", font=CRIB(48), fill=RED)

# Red underline rule
draw.line([(lx_e, y+208), (lx_e+320, y+208)], fill=RED, width=2)

# Body text
wrap_text(
    "Chez HomeInvest, nous avons choisi de donner du sens à chaque transaction. "
    "Une partie de notre chiffre d'affaires est reversée à l'association Sourire à la Vie, "
    "qui accompagne les enfants atteints de cancer et leurs familles.",
    BRICR(15), W//2 - lx_e - 60,
    draw_at=True, x=lx_e, y=y+226, color=GRAY_MED, line_h=27
)

# Director quote
quote = "« Faire de l'immobilier autrement, c'est aussi"
quote2 = "construire un monde meilleur pour nos enfants. »"
draw.text((lx_e, y+348), quote,  font=CRII(17), fill=GRAY_DARK)
draw.text((lx_e, y+372), quote2, font=CRII(17), fill=GRAY_DARK)
draw.text((lx_e, y+400), "— Loïc Salebert, Directeur", font=WRKB(12), fill=RED)

# ── Vertical divider ──
draw.line([(W//2+30, y+60), (W//2+30, y+ENG_H-60)], fill=GRAY_PALE, width=1)

# ── Right column — logo réel Sourire à la Vie ──
rx_e         = W//2 + 90
right_center = rx_e + (W - rx_e - 80) // 2

_logo_src = Image.open(
    "/Users/danielinvernon/Claude code/HomeInvest website/Logo principal.png"
).convert("RGBA")
_logo_w = 280
_logo_h = int(_logo_w * _logo_src.height / _logo_src.width)
_logo   = _logo_src.resize((_logo_w, _logo_h), Image.LANCZOS)

_lx = right_center - _logo_w // 2
_ly = y + 48
img.paste(_logo, (_lx, _ly), _logo)
draw = ImageDraw.Draw(img)

# Texte sous le logo
_tag = "Protéger l'enfance à chaque étape du soin."
_tw  = tlen(_tag, CRII(16))
draw.text((right_center - _tw // 2, _ly + _logo_h + 18), _tag, font=CRII(16), fill=GRAY_MED)

wrap_text(
    "Association nationale accompagnant les enfants atteints de cancer : "
    "activité physique adaptée, soutien psychologique, expéditions thérapeutiques.",
    OUTR(13), W - rx_e - 80,
    draw_at=True, x=rx_e, y=_ly + _logo_h + 52, color=GRAY_MED, line_h=22
)

pill_txt = "sourirealavie.fr →"
pill_w   = tlen(pill_txt, WRKB(12)) + 32
pill_x   = right_center - pill_w // 2
draw.rounded_rectangle([pill_x, _ly + _logo_h + 108, pill_x + pill_w, _ly + _logo_h + 138],
                        radius=14, outline=RED, width=2)
draw.text((pill_x + 16, _ly + _logo_h + 117), pill_txt, font=WRKB(12), fill=RED)

commit_txt = "Partenaire engagé"
_ctw = tlen(commit_txt, WRKB(11)) + 24
draw.rectangle([W - _ctw - 80, y + ENG_H - 52, W - 80, y + ENG_H - 26], fill=RED)
draw.text((W - _ctw - 80 + 12, y + ENG_H - 46), commit_txt, font=WRKB(11), fill=WHITE)

y += ENG_H


# ══════════════════════════════════════════════════════════
#  6. BIENS À LA UNE
# ══════════════════════════════════════════════════════════
BIENS_H = 560
draw.rectangle([0, y, W, y+BIENS_H], fill=CREAM)

label_tag("SÉLECTION", 100, y+44)
draw.text((100, y+78), "Nos biens à la une", font=CRIB(44), fill=GRAY_DARK)

voir = "Voir tous les biens →"
draw.text((W-100-tlen(voir, WRKB(13)), y+90), voir, font=WRKB(13), fill=RED)

biens = [
    ("Coup de cœur", RED,        "Villa provençale",       "Allauch · 13190",           "695 000 €", "5 pièces · 180 m²"),
    ("Exclusivité",  GRAY_DARK,  "Appartement vue mer",    "Marseille 8e · 13008",       "420 000 €", "4 pièces · 95 m²"),
    ("Nouveauté",    (40,130,75),"Maison de ville",        "Plan-de-Cuques · 13380",     "385 000 €", "4 pièces · 130 m²"),
]

bw_  = 408
bgap = (W - 3*bw_ - 120) // 2
bx0  = 60

# Warm gradient palettes per card
photo_palettes = [
    ((185,155,105),(145,115,75)),
    ((120,145,175),(80,105,140)),
    ((155,170,130),(115,135,90)),
]

for i, (badge_txt, badge_col, title, location, price, details) in enumerate(biens):
    bx_ = bx0 + i*(bw_ + bgap + 30)
    by_ = y + 148

    # Shadow
    draw.rectangle([bx_+5, by_+5, bx_+bw_+5, by_+375], fill=(210, 205, 198))
    # Card white
    draw.rectangle([bx_, by_, bx_+bw_, by_+375], fill=WHITE)

    # Photo (illustrated gradient)
    ph = 210
    c1, c2 = photo_palettes[i]
    for pi in range(ph):
        t = pi/ph
        r_ = int(c1[0]*(1-t) + c2[0]*t)
        g_ = int(c1[1]*(1-t) + c2[1]*t)
        b_ = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(bx_, by_+pi), (bx_+bw_, by_+pi)], fill=(r_,g_,b_))

    # Silhouette house in photo
    hcx, hcy = bx_+bw_//2, by_+100
    hw_h = 130
    draw.rectangle([hcx-hw_h, hcy, hcx+hw_h, hcy+95], fill=(int(c2[0]*0.65),int(c2[1]*0.65),int(c2[2]*0.65)))
    draw.polygon([(hcx-hw_h-15,hcy),(hcx+hw_h+15,hcy),(hcx,hcy-55)],
                 fill=(int(c2[0]*0.5),int(c2[1]*0.45),int(c2[2]*0.5)))
    for wx_ in [hcx-70, hcx+20]:
        draw.rectangle([wx_, hcy+20, wx_+40, hcy+65], fill=(int(c1[0]*1.1),int(c1[1]*1.05),int(c1[2]*1.2)))

    # Badge pill
    bpw = tlen(badge_txt, WRKB(11)) + 24
    draw.rectangle([bx_+16, by_+16, bx_+16+bpw, by_+40], fill=badge_col)
    draw.text((bx_+28, by_+23), badge_txt, font=WRKB(11), fill=WHITE)

    # Content
    draw.text((bx_+20, by_+226), title,    font=CRIB(22),  fill=GRAY_DARK)
    draw.text((bx_+20, by_+256), location, font=OUTR(13),  fill=GRAY_MED)
    draw.line([(bx_+20, by_+284), (bx_+bw_-20, by_+284)], fill=GRAY_PALE, width=1)
    draw.text((bx_+20, by_+296), price,   font=BIG(30),   fill=RED)
    draw.text((bx_+20, by_+340), details, font=OUTR(13),  fill=GRAY_MED)

y += BIENS_H


# ══════════════════════════════════════════════════════════
#  6. À PROPOS
# ══════════════════════════════════════════════════════════
APROPS_H = 480
draw.rectangle([0, y, W, y+APROPS_H], fill=WHITE)

# ── Left: placeholder vidéo vertical (9:16, style short podcast) ──
VID_W = 185
VID_H = int(VID_W * 16 / 9)   # ≈ 329px
vcx   = 270
vx1   = vcx - VID_W // 2
vy1   = y + 44
vx2   = vx1 + VID_W
vy2   = vy1 + VID_H

# Ombre
draw.rounded_rectangle([vx1+5, vy1+5, vx2+5, vy2+5], radius=18, fill=(200, 196, 190))
# Fond sombre studio (dégradé bas→haut)
for gi in range(VID_H):
    t  = gi / VID_H
    rc = int(22 + 20 * t)
    gc = int(18 + 16 * t)
    bc = int(16 + 14 * t)
    draw.line([(vx1, vy1 + gi), (vx2, vy1 + gi)], fill=(rc, gc, bc))
# Contour arrondi (par-dessus le dégradé)
draw.rounded_rectangle([vx1, vy1, vx2, vy2], radius=18, outline=(55, 48, 42), width=2)

# Halo lumière chaude de studio (spot derrière le sujet)
for hr in range(55, 0, -1):
    alpha = int(28 * (1 - hr / 55))
    draw.ellipse([vcx - hr, vy1 + VID_H // 3 - hr // 2,
                  vcx + hr, vy1 + VID_H // 3 + hr // 2],
                 outline=(180 + alpha, 140 + alpha, 80 + alpha), width=1)

# Silhouette podcasteur — buste + tête
sil_cx  = vcx - 4
bust_y  = vy2 - 30   # bas du buste
neck_y  = vy1 + VID_H * 55 // 100
head_cy = neck_y - 32
# Épaules/buste
draw.polygon([
    (sil_cx - 62, vy2 + 2),
    (sil_cx + 62, vy2 + 2),
    (sil_cx + 44, neck_y + 12),
    (sil_cx - 44, neck_y + 12),
], fill=(38, 32, 28))
# Cou
draw.rectangle([sil_cx - 13, neck_y, sil_cx + 13, neck_y + 14], fill=(38, 32, 28))
# Tête
draw.ellipse([sil_cx - 28, head_cy - 30, sil_cx + 28, head_cy + 30], fill=(38, 32, 28))

# Micro de studio (bras articulé + capsule)
mic_arm_x = sil_cx + 55
mic_arm_y = vy1 + 22
mic_cap_y = head_cy - 16
draw.line([(vx2 - 10, mic_arm_y), (mic_arm_x, mic_arm_y)], fill=(72, 64, 55), width=3)
draw.line([(mic_arm_x, mic_arm_y), (mic_arm_x, mic_cap_y + 20)], fill=(72, 64, 55), width=3)
draw.rounded_rectangle([mic_arm_x - 11, mic_cap_y, mic_arm_x + 11, mic_cap_y + 28],
                        radius=8, fill=(88, 78, 66))
draw.ellipse([mic_arm_x - 7, mic_cap_y - 8, mic_arm_x + 7, mic_cap_y + 2],
             fill=(88, 78, 66))

# Bouton play (cercle + triangle)
play_cy = vy1 + VID_H // 2
draw.ellipse([vcx - 26, play_cy - 26, vcx + 26, play_cy + 26], fill=(255, 255, 255))
draw.ellipse([vcx - 22, play_cy - 22, vcx + 22, play_cy + 22], fill=(240, 236, 230))
draw.polygon([
    (vcx - 7, play_cy - 13),
    (vcx - 7, play_cy + 13),
    (vcx + 16, play_cy),
], fill=GRAY_DARK)

# Badge durée "0:58" (coin haut droit)
dur_txt = "0:58"
dur_w   = tlen(dur_txt, WRKB(11)) + 14
draw.rounded_rectangle([vx2 - dur_w - 8, vy1 + 10, vx2 - 8, vy1 + 28],
                        radius=5, fill=(12, 10, 8))
draw.text((vx2 - dur_w - 1, vy1 + 13), dur_txt, font=WRKB(11), fill=WHITE)

# Barre de progression rouge (35% lu)
draw.rectangle([vx1, vy2 - 4, vx1 + int(VID_W * 0.35), vy2 - 1], fill=RED)
draw.rectangle([vx1 + int(VID_W * 0.35), vy2 - 4, vx2, vy2 - 1], fill=(70, 60, 52))

# Labels sous la vidéo
vid_lbl = "Son engagement →"
vlw = tlen(vid_lbl, WRKB(12))
draw.text((vcx - vlw // 2, vy2 + 14), vid_lbl, font=WRKB(12), fill=RED)
name_sub = "Loïc Salebert · Directeur"
nsw = tlen(name_sub, OUTR(11))
draw.text((vcx - nsw // 2, vy2 + 34), name_sub, font=OUTR(11), fill=GRAY_MED)

# ── Right: text ──
rx_ = 560
draw.text((rx_, y+48),  "À PROPOS", font=WRKB(12), fill=RED)
draw.text((rx_, y+72),  "Une agence à taille",  font=CRIB(50), fill=GRAY_DARK)
draw.text((rx_, y+128), "humaine.",              font=CRIB(50), fill=GRAY_DARK)

draw.text((rx_, y+200),
          "Loïc Salebert fonde HomeInvest avec une conviction :",
          font=BRICR(16), fill=GRAY_MED)

# Highlighted phrase (red underline, Scale with Ouss style)
hl = "l'immobilier se vit avec des personnes, pas des algorithmes."
draw.text((rx_, y+230), hl, font=BRICR(16), fill=GRAY_DARK)
hl_w = tlen(hl, BRICR(16))
draw.rectangle([rx_, y+252, rx_+hl_w, y+255], fill=RED)

wrap_text(
    "Depuis 15 ans, notre équipe de 5 experts accompagne vendeurs, acheteurs et locataires sur Marseille et ses alentours.",
    BRICR(16), W - rx_ - 80,
    draw_at=True, x=rx_, y=y+272, color=GRAY_MED, line_h=26
)

# Tags (pill chips)
tags = ["Indépendant", "Ancré localement", "Expert Marseille"]
tx_ = rx_
for tag in tags:
    tw_ = tlen(tag, WRKB(12)) + 28
    draw.rounded_rectangle([tx_, y+360, tx_+tw_, y+390], radius=14, outline=GRAY_LIGHT, width=1)
    draw.text((tx_+14, y+368), tag, font=WRKB(12), fill=GRAY_DARK)
    tx_ += tw_ + 14

y += APROPS_H


# ══════════════════════════════════════════════════════════
#  7. ÉQUIPE
# ══════════════════════════════════════════════════════════
TEAM_H = 360
draw.rectangle([0, y, W, y+TEAM_H], fill=CREAM)

label_tag("L'ÉQUIPE", (W - tlen("L'ÉQUIPE", WRKB(12)) - 24)//2, y+40)
cx_text("5 experts à votre service", CRIB(40), y+72)

team = [
    ("LS", "Loïc Salebert",   "Directeur",   RED),
    ("ET", "Eric Trech",      "Consultant",  (75, 115, 160)),
    ("DI", "Danie Invernon",  "Consultant",  (85, 135, 75)),
    ("ES", "Elodie Salebert", "Consultante", (140, 80, 120)),
    ("L",  "Laurent",         "Consultant",  (160, 115, 40)),
]

tw_  = 210
tgap = (W - 5*tw_ - 4*20) // 2 - 10
tx0  = tgap

for i, (ini, name, role, color) in enumerate(team):
    tcx_ = tx0 + i*(tw_+30)
    tcy_ = y + 128

    draw.rectangle([tcx_, tcy_, tcx_+tw_, tcy_+188], fill=WHITE)

    # Avatar + silhouette profil
    av_cx, av_cy = tcx_+tw_//2, tcy_+56
    draw.ellipse([av_cx-36, av_cy-36, av_cx+36, av_cy+36], fill=color)
    # Silhouette — tête + épaules en blanc semi-transparent
    sil = tuple(min(255, int(c * 0.35 + 175)) for c in color)
    # Tête
    draw.ellipse([av_cx-12, av_cy-28, av_cx+12, av_cy-4], fill=sil)
    # Épaules (ellipse large, bas du cercle)
    draw.ellipse([av_cx-28, av_cy+2, av_cx+28, av_cy+52], fill=sil)

    # Name
    nw_ = tlen(name, OUTB(13))
    draw.text((tcx_+tw_//2-nw_//2, tcy_+106), name, font=OUTB(13), fill=GRAY_DARK)

    # Role
    rw_ = tlen(role, OUTR(12))
    draw.text((tcx_+tw_//2-rw_//2, tcy_+126), role, font=OUTR(12), fill=GRAY_MED)

    # Red dot separator
    draw.ellipse([tcx_+tw_//2-3, tcy_+150, tcx_+tw_//2+3, tcy_+157], fill=RED)

    # Phone
    ph_t = "06 XX XX XX XX"
    pw_ = tlen(ph_t, OUTR(10))
    draw.text((tcx_+tw_//2-pw_//2, tcy_+164), ph_t, font=OUTR(10), fill=GRAY_LIGHT)

y += TEAM_H


# ══════════════════════════════════════════════════════════
#  8. CTA ESTIMATION
# ══════════════════════════════════════════════════════════
CTA_H = 200
draw.rectangle([0, y, W, y+CTA_H], fill=RED)

cta1 = "ESTIMEZ VOTRE BIEN GRATUITEMENT"
cx_text(cta1, BIG(54), y+32, WHITE)

cta2 = "Réponse rapide · Sans engagement · Par un expert local"
cx_text(cta2, CRII(20), y+102, (255, 205, 205))

btn_w_ = 230
btn_x_ = (W - btn_w_) // 2
draw.rectangle([btn_x_, y+132, btn_x_+btn_w_, y+174], fill=WHITE)
btn_lbl = "Nous contacter →"
blw = tlen(btn_lbl, WRKB(16))
draw.text((btn_x_+btn_w_//2-blw//2, y+143), btn_lbl, font=WRKB(16), fill=RED)

y += CTA_H


# ══════════════════════════════════════════════════════════
#  9. FOOTER
# ══════════════════════════════════════════════════════════
FOOT_H = 230
draw.rectangle([0, y, W, y+FOOT_H], fill=GRAY_DARK)

# Logo white
flx_, fly_ = 80, y+38
draw.rectangle([flx_,    fly_+4,  flx_+9,  fly_+39], fill=WHITE)
draw.rectangle([flx_+20, fly_+4,  flx_+29, fly_+39], fill=WHITE)
draw.rectangle([flx_+9,  fly_+18, flx_+20, fly_+26], fill=WHITE)
draw.rectangle([flx_+36, fly_+4,  flx_+43, fly_+39], fill=GRAY_LIGHT)
draw.text((flx_+52, fly_+7),  "HOMEINVEST", font=WRKB(16), fill=WHITE)
draw.text((flx_+52, fly_+27), "IMMOBILIER", font=WRKB(11), fill=RED)

draw.text((flx_, fly_+58), "Votre partenaire immobilier à Marseille",
          font=CRII(15), fill=GRAY_LIGHT)

# Center
fcx = W//2 - 160
draw.text((fcx, y+38), "106 Traverse Des Fenêtres Rouges",   font=OUTR(13), fill=GRAY_LIGHT)
draw.text((fcx, y+60), "13011 Marseille",                    font=OUTR(13), fill=GRAY_LIGHT)
draw.text((fcx, y+88), "06 24 56 23 36",                     font=WRKB(17), fill=WHITE)
draw.text((fcx, y+114), "contact@homeinvest.fr",             font=OUTR(13), fill=GRAY_LIGHT)

# Right
frx = W - 310
draw.text((frx, y+38),  "Mentions légales",             font=OUTR(12), fill=GRAY_LIGHT)
draw.text((frx, y+60),  "Politique de confidentialité", font=OUTR(12), fill=GRAY_LIGHT)
draw.text((frx, y+82),  "RGPD",                         font=OUTR(12), fill=GRAY_LIGHT)
draw.text((frx, y+110), "© 2024 HomeInvest Immobilier", font=OUTR(11), fill=(100,100,100))

# Divider
draw.line([(0, y+160), (W, y+160)], fill=(85, 85, 85), width=1)

y += FOOT_H


# ══════════════════════════════════════════════════════════
#  EXPORT
# ══════════════════════════════════════════════════════════
final = img.crop((0, 0, W, y))
out   = "/Users/danielinvernon/Claude code/HomeInvest website/homeinvest_mockup_v1.png"
final.save(out, "PNG", dpi=(144, 144))
print(f"✓  Saved → {out}")
print(f"   Size : {final.size[0]} × {final.size[1]} px")
