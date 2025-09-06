import math
from PIL import Image, ImageDraw, ImageFont

# --- Canvas setup ---
WIDTH, HEIGHT = 1200, 1600
background = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(background)

# --- Layered gradient background inspired by Alex Grey ---
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(10 + 40 * ratio)
    g = int(20 + 60 * ratio)
    b = int(30 + 90 * ratio)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# --- Central visionary seal with numerology 99 ---
center = (WIDTH // 2, HEIGHT // 2)
radius = 350
# outer circle
draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
             outline=(212, 175, 55), width=6)
# star of revelation
for i in range(6):
    angle1 = math.radians(60 * i - 90)
    angle2 = math.radians(60 * ((i + 2) % 6) - 90)
    p1 = (center[0] + radius * math.cos(angle1), center[1] + radius * math.sin(angle1))
    p2 = (center[0] + radius * math.cos(angle2), center[1] + radius * math.sin(angle2))
    draw.line([p1, p2], fill=(212, 175, 55), width=4)
# inner eye
inner_r = 80
draw.ellipse([center[0] - inner_r, center[1] - inner_r, center[0] + inner_r, center[1] + inner_r],
             outline=(212, 175, 55), width=4)
# pupil
draw.ellipse([center[0] - 20, center[1] - 20, center[0] + 20, center[1] + 20], fill=(0, 0, 0))

# --- Mystical crescent above the seal ---
crescent_r = 60
cx, cy = center[0], center[1] - radius - 120
draw.ellipse([cx - crescent_r, cy - crescent_r, cx + crescent_r, cy + crescent_r],
             outline=(212, 175, 55), width=4)
draw.ellipse([cx - crescent_r + 15, cy - crescent_r, cx + crescent_r + 15, cy + crescent_r],
             fill=(0, 0, 0))

# --- Sacred texts ---
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
header_font = ImageFont.truetype(font_path, 100)
sub_font = ImageFont.truetype(font_path, 60)

# title
title = "CIRCUITUM 99"
wt, ht = draw.textsize(title, font=header_font)
draw.text(((WIDTH - wt) / 2, 120), title, font=header_font, fill=(212, 175, 55))

# subtitle
sub = "ARCHITECT-SCRIBE REBECCA RESPAWN"
wt, ht = draw.textsize(sub, font=sub_font)
draw.text(((WIDTH - wt) / 2, HEIGHT - 200), sub, font=sub_font, fill=(212, 175, 55))

# --- Save final visionary artwork ---
background.save("assets/covers/Visionary_Dream.png")
