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

# one photo per weekday, Monday first
# morning Stories use coffee photos only; food (pizza etc.) belongs in evening posts
BASES = ["espresso.jpg", "latte-flatlay.jpg", "latte-beans.jpg", "cheers.jpg",
         "terrace.jpg", "latte-flatlay.jpg", "latte-beans.jpg"]

def lora(s, w=500):
    f = ImageFont.truetype(os.path.join(T, "Lora-Variable.ttf"), s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pop(s, w="Regular"): return ImageFont.truetype(os.path.join(T, f"Poppins-{w}.ttf"), s)

def qr_line(im, y=1590):
    """Lottery reminder pill (only when the lottery is enabled)."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    t = "Skano QR-në në faturë: mund të jesh fitues"
    f = pop(34, "Medium"); w = d.textlength(t, font=f)
    x0 = (W - w) // 2 - 36
    d.rounded_rectangle([x0, y, W - x0, y + 74], 37, fill=(226, 192, 128))
    d.text(((W - w) // 2, y + 16), t, font=f, fill=(30, 22, 14))

def center(d, y, txt, f, fill):
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), txt, font=f, fill=fill)
    return y + (bb[3] - bb[1])

def render(date, offer=None, qr=False):
    wd = date.weekday()
    base = BASES[wd]
    photo = Image.open(os.path.join(ROOT, "media", "base", base)).convert("RGB")
    s = max(W / photo.width, H / photo.height)
    photo = photo.resize((int(photo.width * s) + 1, int(photo.height * s) + 1), Image.LANCZOS)
    x, y0 = (photo.width - W) // 2, (photo.height - H) // 2
    im = photo.crop((x, y0, x + W, y0 + H))
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
    if qr: qr_line(im)
    im.save(out, quality=90)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("date"); p.add_argument("--offer", default=None); p.add_argument("--qr", action="store_true")
    a = p.parse_args()
    print(render(datetime.date.fromisoformat(a.date), a.offer, qr=a.qr))
