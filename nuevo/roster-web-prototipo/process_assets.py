# -*- coding: utf-8 -*-
import base64, io, json, os, subprocess, tempfile
from PIL import Image, ImageOps

FOTOS = "/Users/tomascardozo/main/big/fotos"
OUT = os.path.dirname(__file__)

# maca_castro and ammichis excluded from every roster appearance (client request)
PEOPLE = [
    ("pia_scarnato", "Pía Scarnato", "Pia Scarnato/_DSC6098.jpg", ["Humor", "Lifestyle"], "1.1 M", "2.1 M"),
    ("dulce_pink", "Dulce Pink", "Dulce Pink f/572711958_18534878179053734_5588458490720228584_n.jpg", ["Humor", "Lifestyle"], "1 M", "2.5 M"),
    ("giuli_bellicoso", "Giuli Bellicoso", "Giuli Bellicoso - w/WhatsApp Image 2026-04-28 at 11.32.45 AM.jpeg", ["Humor", "Sketch"], "252 K", "748 K"),
    ("giuli_lourdes", "Giuli Lourdes", "giuli Lourdes- w/IMG_0539.JPG.jpeg", ["Humor", "Lifestyle"], "316 K", "872 K"),
    ("mely_francano", "Mely Francano", "Mely Francano f/mely 1.jpg", ["Humor", "Sketch"], "154 K", "434 K"),
    ("martu_morales", "Martu Morales", "Martu Morales f/martu 2.jpg", ["Trend", "Lifestyle"], "2.3 M", "7.2 M"),
    ("tiago_bergallo", "Tiago Bergallo", "Tiago Bergallo f/thiago 1.jpg", ["Humor", "Trends"], "141 K", "616 K"),
    # Mujeres (resto del grupo, sumado 2026-08-11)
    ("juli_savioli", "Juli Savioli", "Juli Savioli/_DSC6207.jpg", ["Humor", "Sketch", "Fitness"], "2.5 M", "8.9 M"),
    ("renata_blasevich", "Renata Blasevich", "Renata Blasevich -w/IMG_4897.JPG.jpeg", ["Humor", "Sketch"], "324 K", "2 M"),
    ("pauli_veltrano", "Pauli Veltrano", "Pauli /Paulina Vetrano -  PP", ["Lifestyle"], "286 K", "488 K"),
    ("agustina_cambra", "Agustina Cambra", "Agus Fc f/640377109_18389442175144335_5777850493703203233_n.jpg", ["Lifestyle"], "35.4 K", "2 M"),
    ("eve_vidal", "Eve Vidal", "Eve-w/WhatsApp Image 2026-06-30 at 1.30.47 PM.jpeg", ["Cocina", "Lifestyle"], "384 K", "360.6 K"),
    ("inez", "Inez", "Inez f/inezz.jpg", ["Humor", "Lifestyle"], "123 K", "465 K"),
    ("mumy", "Mumy", "Mumy Ratibel f/mumy.jpg", ["Humor", "Lifestyle"], "91 K", "447 K"),
    ("nanu_yael", "Nanu Yael", "Nanu Yael f/nanu 2.jpg", ["Humor", "Lifestyle"], "202 K", "1.8 M"),
    ("sabri_ludmila", "Sabri Ludmila", "Sabri Ludmila f/sabri.jpg", ["Humor", "Lifestyle"], "379 K", "764 K"),
    ("yo_soy_brisa", "Yo Soy Brisa", "Yo soy Brisa f/brisa 1.jpg", ["Lifestyle"], "762 K", "1.5 M"),
]

def to_data_uri(path, max_dim=900, quality=76):
    try:
        img = Image.open(path)
    except Exception:
        # HEIC/HEIF sources: convert via macOS `sips` first, Pillow can't read them directly
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        subprocess.run(["sips", "-s", "format", "jpeg", path, "--out", tmp.name],
                        check=True, capture_output=True)
        img = Image.open(tmp.name)
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
