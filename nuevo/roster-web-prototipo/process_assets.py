# -*- coding: utf-8 -*-
import base64, io, json, os
from PIL import Image, ImageOps

FOTOS = "/Users/tomascardozo/main/big/fotos"
OUT = os.path.dirname(__file__)

PEOPLE = [
    ("pia_scarnato", "Pía Scarnato", "Pia Scarnato/_DSC6098.jpg", ["Humor", "Lifestyle"], "1.1 M", "2.1 M"),
    ("dulce_pink", "Dulce Pink", "Dulce Pink f/572711958_18534878179053734_5588458490720228584_n.jpg", ["Humor", "Lifestyle"], "1 M", "2.5 M"),
    ("giuli_bellicoso", "Giuli Bellicoso", "Giuli Bellicoso - w/WhatsApp Image 2026-04-28 at 11.32.45 AM.jpeg", ["Humor", "Sketch"], "252 K", "748 K"),
    ("maca_castro", "Maca Castro", "Maca Castro f/maca 1.jpg", ["Humor", "Lifestyle"], "70 K", "521 K"),
    ("ammichis", "Ammichis", "Ammichis f/499810533_17975244713849340_7725534501626320821_n.jpg", ["Humor", "Lifestyle"], "13.5 K", "186 K"),
    ("giuli_lourdes", "Giuli Lourdes", "giuli Lourdes- w/IMG_0539.JPG.jpeg", ["Humor", "Lifestyle"], "316 K", "872 K"),
    ("mely_francano", "Mely Francano", "Mely Francano f/mely 1.jpg", ["Humor", "Sketch"], "154 K", "434 K"),
    ("martu_morales", "Martu Morales", "Martu Morales f/martu 2.jpg", ["Trend", "Lifestyle"], "2.3 M", "7.2 M"),
    ("tiago_bergallo", "Tiago Bergallo", "Tiago Bergallo f/thiago 1.jpg", ["Humor", "Trends"], "141 K", "616 K"),
]

def to_data_uri(path, max_dim=900, quality=76):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    w, h = img.size
    scale = max_dim / max(w, h)
    if scale < 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}", len(buf.getvalue())

data = {}
total = 0
for pid, name, relpath, tags, ig, tt in PEOPLE:
    full = os.path.join(FOTOS, relpath)
    uri, size = to_data_uri(full)
    total += size
    data[pid] = dict(name=name, photo=uri, tags=tags, ig=ig, tt=tt)
    print(f"{pid}: {size/1024:.0f}KB")

print(f"TOTAL photos: {total/1024:.0f}KB")

with open(os.path.join(OUT, "people.json"), "w") as f:
    json.dump(data, f)

# fonts
fonts = {}
for w in ["Regular", "Medium", "Bold", "Black"]:
    p = os.path.join(OUT, f"Inter-{w}.woff2")
    with open(p, "rb") as f:
        b = f.read()
    fonts[w] = base64.b64encode(b).decode()
    print(f"font {w}: {len(b)/1024:.0f}KB")

with open(os.path.join(OUT, "fonts.json"), "w") as f:
    json.dump(fonts, f)
