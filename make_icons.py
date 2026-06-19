"""Generator ikon PWA dla Dziennika Malucha. Tworzy icon-192, icon-512, icon-512-maskable."""
from PIL import Image, ImageDraw, ImageFont
import math

BG1 = (74, 158, 255)    # accent
BG2 = (181, 123, 255)   # purple
DARK = (7, 13, 26)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diagonal_gradient(size, c1, c2):
    img = Image.new("RGB", (size, size), c1)
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            px[x, y] = lerp(c1, c2, t)
    return img


def draw_bottle(draw, cx, cy, scale, color=(255, 255, 255)):
    # prosta butelka: smoczek + nakrętka + korpus
    w = int(70 * scale)
    h = int(120 * scale)
    left = cx - w // 2
    top = cy - h // 2
    # korpus
    body_top = top + int(h * 0.28)
    draw.rounded_rectangle([left, body_top, left + w, top + h],
                           radius=int(w * 0.32), fill=color)
    # nakrętka
    cap_w = int(w * 0.6)
    cap_l = cx - cap_w // 2
    cap_t = top + int(h * 0.16)
    draw.rounded_rectangle([cap_l, cap_t, cap_l + cap_w, body_top + int(h*0.02)],
                           radius=int(w * 0.12), fill=color)
    # smoczek
    tw = int(w * 0.26)
    draw.rounded_rectangle([cx - tw // 2, top, cx + tw // 2, cap_t + 2],
                           radius=tw // 2, fill=color)
    # podziałka (kreski w kolorze tła)
    line_c = BG1
    for i in range(3):
        ly = body_top + int(h * 0.16) + i * int(h * 0.16)
        draw.line([left + int(w*0.18), ly, left + int(w*0.40), ly],
                  fill=line_c, width=max(2, int(4 * scale)))


def make_icon(size, maskable=False):
    img = diagonal_gradient(size, BG1, BG2).convert("RGBA")
    draw = ImageDraw.Draw(img)
    # bezpieczny obszar dla maskable (logo mniejsze, wyśrodkowane)
    scale = size / 130.0
    if maskable:
        scale *= 0.62
    else:
        scale *= 0.78
    draw_bottle(draw, size // 2, int(size * 0.50), scale)
    return img.convert("RGB")


for name, size, mask in [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-512-maskable.png", 512, True),
]:
    make_icon(size, mask).save(name, "PNG")
    print("zapisano", name)
