# ---------------------------------------------------------------
# Palette definitions inspired by visionary artists and movements
# ---------------------------------------------------------------
PALETTES = {
    "alex_grey": [
        "#280050",  # deep indigo
        "#460082",  # ultraviolet violet
        "#0080FF",  # electric blue
        "#00FF80",  # neon green
        "#FFC800",  # solar amber
        "#FFFFFF",  # pure light
    ],
    "hilma_af_klint": [
        "#0b1e3d",  # lapis background
        "#f1c40f",  # alchemical gold
        "#2ecc71",  # peacock green
        "#0a0a0a",  # obsidian shadow
        "#8a2be2",  # octarine shimmer
    ],
    "surrealism": [
        "#6A0DAD",  # royal purple
        "#FF6F61",  # dream coral
        "#00FFFF",  # cyan aura
        "#FFD700",  # golden vision
        "#1E90FF",  # azure spark
    ],
}


# ---------------------------------------------------------------
# Pattern drawing helpers
# ---------------------------------------------------------------
def radial(draw: ImageDraw.ImageDraw, width: int, height: int, colors: list[str]) -> None:
    """Radiating lines from the center."""
    center = (width // 2, height // 2)
    radius = min(width, height) // 2
    for i in range(360):
        angle = math.radians(i)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        draw.line([center, (x, y)], fill=colors[i % len(colors)], width=1)


def mandala(draw: ImageDraw.ImageDraw, width: int, height: int, colors: list[str]) -> None:
    """Concentric circles forming a mandala."""
    center = (width // 2, height // 2)
    max_rad