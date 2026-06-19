"""Generator zasobów Android: ikona powiadomienia (biała sylwetka) + splash screen."""
from PIL import Image, ImageDraw

BG1 = (74, 158, 255)
BG2 = (181, 123, 255)
DARK = (7, 13, 26)
WHITE = (255, 255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diagonal_gradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h), c1)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = lerp(c1, c2, t)
    return img


def bottle_path(draw, cx, cy, scale, color):
    w = int(70 * scale)
    h = int(120 * scale)
    left = cx - w // 2
    top = cy - h // 2
    body_top = top + int(h * 0.28)
    draw.rounded_rectangle([left, body_top, left + w, top + h],
                           radius=int(w * 0.32), fill=color)
    cap_w = int(w * 0.6)
    cap_l = cx - cap_w // 2
    cap_t = top + int(h * 0.16)
    draw.rounded_rectangle([cap_l, cap_t, cap_l + cap_w, body_top + int(h*0.02)],
                           radius=int(w * 0.12), fill=color)
    tw = int(w * 0.26)
    draw.rounded_rectangle([cx - tw // 2, top, cx + tw // 2, cap_t + 2],
                           radius=tw // 2, fill=color)


# ---- Ikona powiadomienia: biała sylwetka na przezroczystym tle ----
# Android pokazuje tylko alpha; kolor nadaje system (iconColor w configu).
for size in (24, 36, 48, 72, 96, 144):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bottle_path(d, size // 2, size // 2, size / 130.0 * 0.78, WHITE)
    img.save(f"notif-{size}.png", "PNG")
    print("zapisano", f"notif-{size}.png")

# Wersja domyślna używana w kodzie/configu
Image.open("notif-96.png").save("notif-icon.png")
print("zapisano notif-icon.png")

# ---- Splash screen (ekran startowy) ----
# Kwadrat 1280x1280 — Capacitor sam przeskaluje na różne ekrany.
S = 1280
splash = diagonal_gradient(S, S, BG1, BG2).convert("RGBA")
d = ImageDraw.Draw(splash)
# delikatna poświata
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([S*0.18, S*0.18, S*0.82, S*0.82], fill=(255, 255, 255, 26))
splash = Image.alpha_composite(splash, glow)
d = ImageDraw.Draw(splash)
bottle_path(d, S // 2, int(S * 0.46), S / 130.0 * 0.9, WHITE)
splash.convert("RGB").save("splash.png", "PNG")
print("zapisano splash.png")
