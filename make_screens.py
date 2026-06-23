"""Skaluje Apka1-4 do jednolitych zrzutów 1080x1920 dla Google Play."""
from PIL import Image
import glob, os

CW, CH = 1080, 1920
BG = (7, 13, 26)  # #070d1a

files = sorted(glob.glob("Apka*.jpg"))
for i, f in enumerate(files, 1):
    src = Image.open(f).convert("RGB")
    # dopasuj szerokość do 1000 px (margines), zachowaj proporcje
    target_w = 1000
    ratio = target_w / src.width
    new_h = int(src.height * ratio)
    if new_h > CH - 80:
        new_h = CH - 80
        ratio = new_h / src.height
        target_w = int(src.width * ratio)
    src = src.resize((target_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (CW, CH), BG)
    x = (CW - target_w) // 2
    y = (CH - new_h) // 2
    canvas.paste(src, (x, y))
    out = f"screen{i}.png"
    canvas.save(out, "PNG")
    print("zapisano", out, f"{CW}x{CH}")
print("Gotowe:", len(files), "zrzutów")
