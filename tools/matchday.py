"""Match-day Story for Boulevard Caffe (team names only, no club logos or league marks).

python3 tools/matchday.py YYYY-MM-DD matches.json [--offer "Heineken 200 lekë"]
matches.json: [["18:45", "LASK", "Liverpool", "Champions League"], ...]  (local Tirane time, max 7)
Writes media/daily/ndeshjet-YYYY-MM-DD.jpg (1080x1920).
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
W, H = 1080, 1920
CREAM, GOLD, MUTED, GREEN = (246, 238, 226), (226, 192, 128), (200, 185, 165), (120, 200, 140)

def lora(s, w=500):
    f = ImageFont.truetype(os.path.join(T, "Lora-Variable.ttf"), s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pop(s, w="Regular"): return ImageFont.truetype(os.path.join(T, f"Poppins-{w}.ttf"), s)

def center(d, y, txt, f, fill):
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), txt, font=f, fill=fill)

def fit(d, txt, size, maxw, w="Medium"):
    while size > 24:
        f = pop(size, w)
        if d.textlength(txt, font=f) <= maxw: return f
        size -= 2
    return pop(size, w)

def render(date, matches, offer=None):
    bg = Image.open(os.path.join(ROOT, "media", "base", "heineken.jpg")).convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    x, y = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(26))  # baked-in headline becomes unreadable
    im = Image.blend(bg, Image.new("RGB", (W, H), (14, 12, 9)), 0.62)
    d = ImageDraw.Draw(im)
    center(d, 250, "BOULEVARD CAFFE · ELBASAN", pop(30, "Medium"), GOLD)
    center(d, 330, "Sonte ndeshjet", lora(96), CREAM)
    center(d, 460, "të gjitha live te ne", pop(40), MUTED)
    y = 590
    for t, home, away, comp in matches[:7]:
        d.rounded_rectangle([90, y, W - 90, y + 104], 20, fill=(30, 24, 18), outline=(226, 192, 128), width=2)
        d.text((125, y + 26), t, font=pop(42, "Medium"), fill=GOLD)
        d.text((300, y + 14), f"{home} – {away}", font=fit(d, f"{home} – {away}", 40, W - 90 - 300 - 30), fill=CREAM)
        d.text((300, y + 64), comp, font=pop(24), fill=MUTED)
        y += 124
    y += 20
    if offer:
        center(d, y, offer, pop(46, "Medium"), GOLD); y += 70
    center(d, y, "Rezervo tavolinën: 067 401 0030", pop(34), CREAM)
    center(d, y + 60, "Tonight's matches live at Boulevard Caffe", pop(28), MUTED)
    out = os.path.join(ROOT, "media", "daily", f"ndeshjet-{date}.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, quality=90)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("date"); p.add_argument("matches"); p.add_argument("--offer")
    a = p.parse_args()
    print(render(a.date, json.load(open(a.matches)), a.offer))
