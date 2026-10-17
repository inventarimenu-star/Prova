"""Match-day Story for Boulevard Caffe, with club crests next to team names (owner's decision, 17 Oct 2026).

python3 tools/matchday.py YYYY-MM-DD matches.json [--offer "Heineken 200 lekë"] [--qr] [--no-logos] [--style stadium|classic]
Default style "stadium" (owner's chosen design, background media/base/stadium.jpg).
Crests come from tools/logos (see tools/logos.py); a team without a crest is shown with its name only.
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

def fit(d, txt, size, maxw, w="Medium"):
    while size > 24:
        f = pop(size, w)
        if d.textlength(txt, font=f) <= maxw: return f
        size -= 2
    return pop(size, w)

def crest(name, size):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("logos", os.path.join(T, "logos.py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        p = m.find(name)
        if not p: return None
        im = Image.open(p).convert("RGBA"); s = size / max(im.size)
        return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    except Exception:
        return None

def row_content(im, d, y, t, home, away, comp, logos):
    d.text((125, y + 26), t, font=pop(42, "Medium"), fill=GOLD)
    lh, la = (crest(home, 52), crest(away, 52)) if logos else (None, None)
    avail = W - 90 - 300 - 30 - (60 if lh else 0) - (60 if la else 0)
    txt = f"{home} – {away}"; f = fit(d, txt, 40, avail); x = 300
    if lh: im.paste(lh, (x + (52 - lh.width) // 2, y + 12 + (52 - lh.height) // 2), lh); x += 60
    d.text((x, y + 14), txt, font=f, fill=CREAM); x += int(d.textlength(txt, font=f)) + 8
    if la: im.paste(la, (x + (52 - la.width) // 2, y + 12 + (52 - la.height) // 2), la)
    d.text((300, y + 64), comp, font=pop(24), fill=MUTED)

def render_stadium(date, matches, offer=None, qr=False, logos=True):
    """Owner's chosen design (17 Oct 2026): night stadium + ball, dark rows with gold border."""
    im = Image.open(os.path.join(ROOT, "media", "base", "stadium.jpg")).convert("RGB").resize((W, H))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
    n = len(matches[:7]); rh, gap = 104, 120
    y0 = 600 + max(0, (7 - n) * gap // 3)
    for i in range(n):
        y = y0 + i * gap
        o.rounded_rectangle([90, y, W - 90, y + rh], 20, fill=(24, 20, 14, 238), outline=(226, 192, 128, 255), width=2)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    center(d, 248, "BOULEVARD CAFFE · ELBASAN", pop(32, "Medium"), GOLD)
    center(d, 330, "Sonte ndeshjet", lora(104, 600), (255, 255, 255))
    center(d, 478, "të gjitha live te ne", pop(42, "Medium"), GOLD)
    for i, (t, home, away, comp) in enumerate(matches[:7]):
        row_content(im, d, y0 + i * gap, t, home, away, comp, logos)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    lines = ([(1490, offer, pop(44, "Medium"), GOLD)] if offer else []) + [
        (1556, "Rezervo tavolinën: 067 401 0030", pop(36, "Medium"), CREAM),
        (1606, "Tonight's matches live at Boulevard Caffe", pop(28, "Medium"), CREAM)]
    for yy, t, f, _ in lines:
        bb = sd.textbbox((0, 0), t, font=f); sd.text(((W - (bb[2] - bb[0])) // 2 - bb[0] + 2, yy + 3), t, font=f, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    im = Image.alpha_composite(im.convert("RGBA"), sh).convert("RGB"); d = ImageDraw.Draw(im)
    for yy, t, f, col in lines: center(d, yy, t, f, col)
    # pill always drawn in the same place (covers the old artwork under it)
    t = "Skano QR-në në faturë: mund të jesh fitues" if qr else "Boulevard Caffe · Bulevardi Qemal Stafa"
    f = pop(36, "Medium")
    d.rounded_rectangle([135, 1662, 945, 1742], 40, fill=(226, 192, 128))
    tw = d.textlength(t, font=f); d.text((540 - tw / 2, 1679), t, font=f, fill=(30, 22, 14))
    out = os.path.join(ROOT, "media", "daily", f"ndeshjet-{date}.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, quality=90)
    return out

def render(date, matches, offer=None, qr=False, logos=True):
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
        lh, la = (crest(home, 52), crest(away, 52)) if logos else (None, None)
        if lh or la:
            # [crest] Home – Away [crest]
            avail = W - 90 - 300 - 30 - (60 if lh else 0) - (60 if la else 0)
            f = fit(d, f"{home} – {away}", 40, avail)
            x = 300
            if lh: im.paste(lh, (x + (52 - lh.width) // 2, y + 12 + (52 - lh.height) // 2), lh); x += 60
            txt = f"{home} – {away}"; d.text((x, y + 14), txt, font=f, fill=CREAM); x += int(d.textlength(txt, font=f)) + 8
            if la: im.paste(la, (x + (52 - la.width) // 2, y + 12 + (52 - la.height) // 2), la)
        else:
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
    if qr: qr_line(im, y=max(1590, y + 115))   # always below the footer lines
    im.save(out, quality=90)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("date"); p.add_argument("matches"); p.add_argument("--offer"); p.add_argument("--qr", action="store_true"); p.add_argument("--no-logos", action="store_true")
    p.add_argument("--style", choices=["stadium", "classic"], default="stadium")
    a = p.parse_args()
    fn = render_stadium if a.style == "stadium" else render
    print(fn(a.date, json.load(open(a.matches)), a.offer, qr=a.qr, logos=not a.no_logos))
