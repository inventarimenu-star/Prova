"""10:00 'last hour of the breakfast offer' Story for Boulevard Caffe.

python3 tools/lastcall.py YYYY-MM-DD rows.json [--until 10:00]
rows.json: [["Çokollatë e nxehtë", 150, 170], ["Tost mëngjesi", 150, null], ...]  (label, price now, old price or null)
Writes media/daily/oferta-ora-fundit-YYYY-MM-DD.jpg (1080x1920).
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
W, H = 1080, 1920
CREAM, GOLD, MUTED = (246, 238, 226), (226, 192, 128), (200, 185, 165)

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

def render(date, rows, until="10:00", qr=False):
    p = Image.open(os.path.join(ROOT, "media", "base", "latte-flatlay.jpg")).convert("RGB")
    s = max(W / p.width, H / p.height)
    p = p.resize((int(p.width * s) + 1, int(p.height * s) + 1))
    x, y = (p.width - W) // 2, (p.height - H) // 2
    im = p.crop((x, y, x + W, y + H))
    shade = Image.new("L", (1, H))
    for yy in range(H):
        shade.putpixel((0, yy), 232 if yy < 1380 else max(0, int(232 * (1 - (yy - 1380) / 300))))
    im = Image.composite(Image.new("RGB", (W, H), (22, 15, 10)), im, shade.resize((W, H)))
    d = ImageDraw.Draw(im)
    center(d, 250, "BOULEVARD CAFFE · ELBASAN", pop(30, "Medium"), GOLD)
    center(d, 320, "Ora e fundit", lora(100), CREAM)
    center(d, 450, f"e ofertës së mëngjesit · deri në {until}", pop(40, "Medium"), GOLD)
    y = 580
    for label, now, old in rows[:6]:
        d.text((130, y), label, font=lora(56), fill=CREAM)
        pf = lora(62, 650); nb = d.textbbox((0, 0), str(now), font=pf)
        d.text((950 - (nb[2] - nb[0]), y), str(now), font=pf, fill=GOLD)
        if old:
            of = pop(32); ob = d.textbbox((0, 0), str(old), font=of)
            ox = 950 - (nb[2] - nb[0]) - 22 - (ob[2] - ob[0])
            d.text((ox, y + 20), str(old), font=of, fill=MUTED)
            d.line([(ox, y + 40), (ox + ob[2] - ob[0], y + 40)], fill=MUTED, width=3)
        d.line([(130, y + 102), (950, y + 102)], fill=(120, 100, 70), width=2)
        y += 122
    center(d, y + 30, "lekë · Ju presim deri në " + until, pop(36), CREAM)
    center(d, y + 90, "Last hour of the breakfast offer", pop(28), MUTED)
    out = os.path.join(ROOT, "media", "daily", f"oferta-ora-fundit-{date}.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if qr: qr_line(im)
    im.save(out, quality=90)
    return out

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("date"); a.add_argument("rows"); a.add_argument("--until", default="10:00"); a.add_argument("--qr", action="store_true")
    a = a.parse_args()
    print(render(a.date, json.load(open(a.rows)), a.until, qr=a.qr))
