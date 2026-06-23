"""Feature graphic 1024x500 dla Google Play (BabyPulse)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 500
BG1 = (74, 158, 255)
BG2 = (181, 123, 255)
WHITE = (255, 255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad(w, h, c1, c2):
    img = Image.new("RGB", (w, h), c1)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.6 + y / h * 0.4)
            px[x, y] = lerp(c1, c2, t)
    return img


def bottle(draw, cx, cy, scale, color):
    w = int(70 * scale); h = int(120 * scale)
    left = cx - w // 2; top = cy - h // 2
    body_top = top + int(h * 0.28)
    draw.rounded_rectangle([left, body_top, left + w, top + h], radius=int(w*0.32), fill=color)
    cap_w = int(w * 0.6); cap_l = cx - cap_w // 2; cap_t = top + int(h*0.16)
    draw.rounded_rectangle([cap_l, cap_t, cap_l + cap_w, body_top + int(h*0.02)], radius=int(w*0.12), fill=color)
    tw = int(w * 0.26)
    draw.rounded_rectangle([cx - tw // 2, top, cx + tw // 2, cap_t + 2], radius=tw // 2, fill=color)


def load_font(size, bold=True):
    import os
    cands = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


img = grad(W, H, BG1, BG2).convert("RGBA")
# poświata
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-150, 60, 380, 560], fill=(255, 255, 255, 22))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img)

# logo aplikacji (ikona) w zaokrąglonym kwadracie po lewej
ICON = 300
try:
    icon = Image.open("icon-512.png").convert("RGBA").resize((ICON, ICON))
    mask = Image.new("L", (ICON, ICON), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, ICON, ICON], radius=70, fill=255)
    ix, iy = 70, (H - ICON) // 2
    # delikatny cień
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([ix+6, iy+10, ix+ICON+6, iy+ICON+10], radius=78, fill=(0, 0, 0, 60))
    img = Image.alpha_composite(img, shadow)
    img.paste(icon, (ix, iy), mask)
except Exception as e:
    print("brak icon-512.png — rysuję butelkę", e)
    bottle(d, 200, 250, 1.4, WHITE)
d = ImageDraw.Draw(img)

# tekst
title_f = load_font(120, True)
sub_f = load_font(40, False)
d.text((415, 150), "BabyPulse", font=title_f, fill=(255, 255, 255, 255))
d.text((419, 290), "Karmienie · Sen · Rozwój + AI", font=sub_f, fill=(235, 240, 255, 255))
d.text((419, 345), "Feeding · Sleep · Growth + AI", font=sub_f, fill=(210, 222, 255, 230))

img.convert("RGB").save("feature-graphic.png", "PNG")
print("zapisano feature-graphic.png 1024x500")
