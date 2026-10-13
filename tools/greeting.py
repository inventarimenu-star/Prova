"""Render the daily morning Instagram Story for Boulevard Caffe.

Usage: python3 tools/greeting.py YYYY-MM-DD [--offer "Ekspres 60 lekë deri në 11:00"]
Writes media/daily/greeting-YYYY-MM-DD.jpg (1080x1920).
"""
import argparse, datetime, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
W, H = 1080, 1920
CREAM, GOLD, MUTED = (246, 238, 226), (226, 192, 128), (205, 190, 170)

# Monday=0 ... Sunday=6
LINES = [
    ("Mirëmëngjes!", "Java nis me një kafe të mirë.", "Good morning! Start the week with a good coffee."),
    ("Mirëmëngjes, Elbasan!", "Kafeja e parë po të pret.", "Good morning! Your first coffee is waiting."),
    ("Mirëmëngjes!", "Mesi i javës, filxhani plot.", "Midweek, full cup."),
    ("Mirëmëngjes!", "Edhe pak dhe vjen fundjava.", "Almost the weekend. Coffee first."),
    ("Gëzuar të premten!", "Fillojeni me një kapuçino.", "Happy Friday! Start with a cappuccino."),
    ("Mirëmëngjes!", "Fundjava fillon te ne.", "The weekend starts here."),
    ("E diel e qetë", "dhe një kafe e ngrohtë.", "Slow Sunday, warm coffee."),
]

def lora(s, w=500):
    f = ImageFont.truetype(os.path.join(T, "Lora-Variable.ttf"), s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pop(s, w="Regular"): return ImageFont.truetype(os.path.join(T, f"Poppins-{w}.ttf"), s)

def center(d, y, txt, f, fill):
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), txt, font=f, fill=fill)
    return y + (bb[3] - bb[1])

def render(date, offer=None):
    wd = date.weekday()
    photo = Image.open(os.path.join(ROOT, "media", "base", "espresso.jpg")).convert("RGB")
    s = H / photo.height
    photo = photo.resize((int(photo.width * s), H), Image.LANCZOS)
    x = (photo.width - W) // 2 + [-60, 0, 60, -30, 30, -90, 90][wd]
    x = max(0, min(photo.width - W, x))
    im = photo.crop((x, 0, x + W, H))
    # soft dark gradient on the top half for legible text
    grad = Image.new("L", (1, H))
    for y in range(H):
        grad.putpixel((0, y), 225 if y < 820 else int(max(0, 225 * (1 - (y - 820) / 420))))
    shade = Image.new("RGB", (W, H), (20, 13, 9))
    im = Image.composite(shade, im, grad.resize((W, H)))
    d = ImageDraw.Draw(im)
    h1, h2, en = LINES[wd]
    center(d, 250, "BOULEVARD CAFFE · ELBASAN", pop(30, "Medium"), GOLD)
    y = center(d, 360, h1, lora(96 if len(h1) < 16 else 80), CREAM)
    y = center(d, y + 40, h2, lora(56, 450), CREAM)
    d.line([(W // 2 - 70, y + 50), (W // 2 + 70, y + 50)], fill=GOLD, width=3)
    y = center(d, y + 90, "Ju presim te Boulevard Caffe", pop(42, "Medium"), GOLD)
    if offer:
        y = center(d, y + 30, offer, pop(40, "Medium"), CREAM)
    center(d, y + 40, en, pop(30), MUTED)
    out = os.path.join(ROOT, "media", "daily", f"greeting-{date.isoformat()}.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, quality=90)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("date"); p.add_argument("--offer", default=None)
    a = p.parse_args()
    print(render(datetime.date.fromisoformat(a.date), a.offer))
