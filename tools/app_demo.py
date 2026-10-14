"""Explainer Reel for caffeboulevard.com features (customer page), 1080x1920, ~24 s.
Scenes: QR on table -> home screen -> Thirr Kamarieren -> Kërko Faturën -> Porosit nga Menu -> Skano Biletën -> outro.
python3 tools/app_demo.py out.mp4 tmpdir
"""
import os, sys, math, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
W, H, FPS = 1080, 1920, 30
BG = (14, 11, 8); CREAM = (246, 238, 226); GOLD = (232, 199, 109); MUTED = (185, 168, 145)
DARKBTN = (32, 25, 19); OK = (88, 190, 120)

def lora(s, w=500):
    f = ImageFont.truetype(os.path.join(T, "Lora-Variable.ttf"), s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pop(s, w="Regular"): return ImageFont.truetype(os.path.join(T, f"Poppins-{w}.ttf"), s)
def check(d, cx, cy, r, fill, w=7):
    d.line([(cx - r * .55, cy), (cx - r * .15, cy + r * .45), (cx + r * .6, cy - r * .45)], fill=fill, width=w, joint="curve")

def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def ctext(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f); d.text((cx - (bb[2] - bb[0]) // 2 - bb[0], y), s, font=f, fill=fill)

# phone geometry
PX, PY, PW, PH = 190, 330, 700, 1340
SX, SY, SW, SH = PX + 26, PY + 26, PW - 52, PH - 52

def background():
    bg = Image.open(os.path.join(ROOT, "media", "base", "terrace.jpg")).convert("RGB")
    s = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    x, y = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(30))
    return Image.blend(bg, Image.new("RGB", (W, H), BG), 0.72)

def button(d, box, label, style="dark", icon=None):
    x0, y0, x1, y1 = box
    if style == "gold":
        d.rounded_rectangle(box, 22, fill=GOLD); col = (30, 22, 14)
    else:
        d.rounded_rectangle(box, 22, fill=DARKBTN, outline=(120, 96, 52), width=2); col = CREAM
    f = pop(28, "Medium")
    tw = d.textlength(label, font=f); ix = (x0 + x1) / 2 - tw / 2
    if icon:
        d.ellipse([ix - 46, (y0 + y1) / 2 - 16, ix - 14, (y0 + y1) / 2 + 16], fill=GOLD if style != "gold" else (30, 22, 14))
        d.text((ix - 38, (y0 + y1) / 2 - 18), icon, font=pop(22, "Medium"), fill=(30, 22, 14) if style != "gold" else GOLD)
    d.text((ix, (y0 + y1) / 2 - 20), label, font=f, fill=col)

BTN = {}
def home_screen():
    sc = Image.new("RGB", (SW, SH), (20, 16, 12)); d = ImageDraw.Draw(sc)
    d.rounded_rectangle([40, 40, SW - 40, 330], 26, fill=(28, 22, 16), outline=GOLD, width=2)
    d.ellipse([SW / 2 - 70, 70, SW / 2 + 70, 210], outline=GOLD, width=4)
    ctext(d, SW / 2, 82, "B", lora(100, 600), GOLD)
    ctext(d, SW / 2, 228, "Boulevard Caffe", lora(46), CREAM)
    ctext(d, SW / 2, 284, "Café Elbasan · Eat · Drink · Connect", pop(20), MUTED)
    d.line([(40, 360), (SW - 40, 360)], fill=GOLD, width=3)
    ctext(d, SW / 2, 382, "Mirë se erdhët! Si mund t'ju ndihmojmë?", pop(24), CREAM)
    y = 450; hh = 104; g = 22; L, R = 40, SW - 40; mid = SW / 2
    BTN["waiter"] = (L, y, mid - 8, y + hh); BTN["bill"] = (mid + 8, y, R, y + hh)
    button(d, BTN["waiter"], "Thirr Kamarieren", "dark", "!"); button(d, BTN["bill"], "Kërko Faturën", "gold", "€")
    y += hh + g; BTN["menu"] = (L, y, R, y + hh); button(d, BTN["menu"], "Porosit nga Menu", "dark", "+")
    y += hh + g; BTN["staff"] = (L, y, mid - 8, y + hh); BTN["offers"] = (mid + 8, y, R, y + hh)
    button(d, BTN["staff"], "Pyet Stafin", "dark", "?"); button(d, BTN["offers"], "Shiko Ofertat", "gold", "%")
    y += hh + g; BTN["scan"] = (L, y, R, y + hh); button(d, BTN["scan"], "Skano Biletën", "dark", "#")
    y += hh + g; button(d, (L, y, R, y + hh), "Na vlerëso në Google", "gold", "*")
    return sc

MENU = [("Kafe ekspres", 70), ("Kapuçino", 170), ("Çokollatë", 170), ("Briosh", 60),
        ("Heineken shishe", 250), ("Pizza Margarita", 500)]
def menu_screen(added):
    sc = Image.new("RGB", (SW, SH), (20, 16, 12)); d = ImageDraw.Draw(sc)
    d.rectangle([0, 0, SW, 150], fill=(28, 22, 16))
    ctext(d, SW / 2, 40, "Menuja", lora(54), CREAM); ctext(d, SW / 2, 108, "Tavolina 7", pop(22), GOLD)
    y = 190
    for i, (n, p) in enumerate(MENU):
        d.rounded_rectangle([34, y, SW - 34, y + 128], 20, fill=DARKBTN)
        d.text((64, y + 24), n, font=lora(38), fill=CREAM)
        d.text((64, y + 76), f"{p} lekë", font=pop(24), fill=GOLD)
        on = i in added
        d.ellipse([SW - 130, y + 30, SW - 64, y + 96], fill=OK if on else GOLD)
        if on: check(d, SW - 97, y + 63, 22, (20, 16, 12))
        else: ctext(d, SW - 97, y + 34, "+", pop(40, "Medium"), (20, 16, 12))
        BTN[f"m{i}"] = (SW - 130, y + 30, SW - 64, y + 96); y += 146
    total = sum(MENU[i][1] for i in added)
    if added:
        d.rounded_rectangle([34, SH - 150, SW - 34, SH - 44], 24, fill=GOLD)
        ctext(d, SW / 2, SH - 128, f"Dërgo porosinë · {total} lekë", pop(32, "Medium"), (30, 22, 14))
    return sc

def toast(sc, title, sub, a):
    if a <= 0: return sc
    sc = sc.copy(); ov = Image.new("RGBA", sc.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    y = int(60 - 40 * (1 - ease(a)))
    d.rounded_rectangle([34, y, SW - 34, y + 150], 24, fill=(36, 30, 22, int(250 * a)), outline=(*OK, int(255 * a)), width=3)
    d.ellipse([60, y + 45, 120, y + 105], fill=(*OK, int(255 * a)))
    check(d, 90, y + 75, 20, (20, 16, 12, int(255 * a)), 6)
    d.text((146, y + 30), title, font=pop(32, "Medium"), fill=(*CREAM, int(255 * a)))
    d.text((146, y + 82), sub, font=pop(22), fill=(*MUTED, int(255 * a)))
    return Image.alpha_composite(sc.convert("RGBA"), ov).convert("RGB")

def tap(sc, box, t):
    """press highlight + ripple, t in 0..1"""
    if t <= 0 or t >= 1: return sc
    sc = sc.copy().convert("RGBA"); ov = Image.new("RGBA", sc.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    r = 30 + 160 * t
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 240, 200, int(200 * (1 - t))), width=6)
    d.rounded_rectangle(box, 22, fill=(255, 240, 200, int(70 * (1 - t))))
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 255, 255, int(150 * (1 - t))))
    return Image.alpha_composite(sc, ov).convert("RGB")

def scanner_screen(a, win):
    sc = Image.new("RGB", (SW, SH), (10, 9, 8)); d = ImageDraw.Draw(sc)
    ctext(d, SW / 2, 60, "Skano Biletën", lora(50), CREAM)
    ctext(d, SW / 2, 130, "Drejto kamerën te QR kodi", pop(24), MUTED)
    ctext(d, SW / 2, 166, "në fund të biletës", pop(24), MUTED)
    bx0, by0, bx1, by1 = 110, 260, SW - 110, 260 + SW - 220
    # receipt + QR
    d.rectangle([bx0 + 40, by0 + 30, bx1 - 40, by1 + 120], fill=(238, 232, 220))
    q = 13; cell = (bx1 - bx0 - 160) // q; qx, qy = bx0 + 80, by0 + 80
    import random; rnd = random.Random(3)
    for i in range(q):
        for j in range(q):
            corner = (i < 4 and j < 4) or (i < 4 and j > q - 5) or (i > q - 5 and j < 4)
            on = (corner and not (i in (1, 2) and j in (1, 2) or i in (1, 2) and j in (q - 3, q - 2) or i in (q - 3, q - 2) and j in (1, 2))) if corner else rnd.random() < 0.5
            if on: d.rectangle([qx + j * cell, qy + i * cell, qx + (j + 1) * cell - 1, qy + (i + 1) * cell - 1], fill=(20, 16, 12))
    for (x, y, dx, dy) in [(bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)]:
        d.line([(x, y), (x + 70 * dx, y)], fill=GOLD, width=8); d.line([(x, y), (x, y + 70 * dy)], fill=GOLD, width=8)
    ly = by0 + (by1 - by0) * (0.5 + 0.45 * math.sin(a * math.pi * 2))
    d.line([(bx0 + 20, ly), (bx1 - 20, ly)], fill=(255, 90, 70), width=5)
    if win > 0:
        sc = sc.convert("RGBA"); ov = Image.new("RGBA", sc.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(ov)
        k = ease(win)
        d2.rectangle([0, 0, SW, SH], fill=(14, 11, 8, int(225 * k)))
        y0 = 420
        d2.ellipse([SW / 2 - 110, y0, SW / 2 + 110, y0 + 220], fill=(*GOLD, int(255 * k)))
        d2.rounded_rectangle([SW / 2 - 62, y0 + 70, SW / 2 + 62, y0 + 150], 12, outline=(30, 22, 14, int(255 * k)), width=7)
        d2.line([(SW / 2 + 20, y0 + 74), (SW / 2 + 20, y0 + 146)], fill=(30, 22, 14, int(255 * k)), width=4)
        ctext(d2, SW / 2, y0 + 280, "Mund të jesh fitues!", lora(54), (*CREAM, int(255 * k)))
        ctext(d2, SW / 2, y0 + 370, "Çdo faturë ka një biletë QR.", pop(26), (*MUTED, int(255 * k)))
        ctext(d2, SW / 2, y0 + 414, "Fituesit nuk e paguajnë faturën.", pop(26), (*MUTED, int(255 * k)))
        sc = Image.alpha_composite(sc, ov).convert("RGB")
    return sc

def phone(bgimg, screen, caption=None, cap_a=1.0, scale=1.0):
    im = bgimg.copy(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX, PY, PX + PW, PY + PH], 80, fill=(8, 7, 6), outline=(90, 78, 60), width=4)
    mask = Image.new("L", (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, SW, SH], 58, fill=255)
    im.paste(screen, (SX, SY), mask)
    d.rounded_rectangle([W / 2 - 90, PY + 40, W / 2 + 90, PY + 76], 18, fill=(8, 7, 6))
    if caption:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = int(255 * cap_a); dy = int(20 * (1 - cap_a))
        ctext(od, W / 2, 120 + dy, caption[0], lora(66), (*CREAM, a))
        ctext(od, W / 2, 218 + dy, caption[1], pop(32), (*GOLD, a))
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    return im

def title_card(bgimg, l1, l2, l3, a):
    im = bgimg.copy(); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); A = int(255 * a)
    ctext(d, W / 2, 640, "BOULEVARD CAFFE · ELBASAN", pop(32, "Medium"), (*GOLD, A))
    ctext(d, W / 2, 740, l1, lora(92), (*CREAM, A))
    ctext(d, W / 2, 860, l2, lora(92), (*CREAM, A))
    ctext(d, W / 2, 1010, l3, pop(38), (*MUTED, A))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def main(out, tmp):
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    bg = background(); home = home_screen()
    cnt = [0]
    def hold(fn, secs):
        n = int(secs * FPS)
        for i in range(n):
            fn(i / max(1, n - 1)).save(f"{tmp}/{cnt[0]:05d}.jpg", quality=92); cnt[0] += 1
    # 1 intro 2.5s
    hold(lambda t: title_card(bg, "Tavolina jote,", "në telefon", "Skano QR-në në tavolinë · caffeboulevard.com", min(1, t * 4)), 2.5)
    # 2 home 1.5s
    cap = ("Pa pritur kamarierin", "Gjithçka nga tavolina")
    hold(lambda t: phone(bg, home, cap, min(1, t * 3)), 1.5)
    # 3 waiter 3s
    c = ("Thirr Kamarierin", "Me një prekje")
    hold(lambda t: phone(bg, toast(tap(home, BTN["waiter"], t / 0.35), "Thirrja u dërgua!", "Kamarieri vjen së shpejti.", (t - 0.3) / 0.2), c, min(1, t * 4)), 3.0)
    # 4 bill 3s
    c = ("Kërko Faturën", "Pa e kërkuar me dorë")
    hold(lambda t: phone(bg, toast(tap(home, BTN["bill"], t / 0.35), "Kërkesa u dërgua!", "Fatura po përgatitet.", (t - 0.3) / 0.2), c, min(1, t * 4)), 3.0)
    # 5 menu 6s
    c = ("Porosit nga Menu", "Çmimet e sakta, direkt te banaku")
    def menu_frame(t):
        if t < 0.12: return phone(bg, tap(home, BTN["menu"], t / 0.12), c, min(1, t * 8))
        added = [i for i, at in ((1, .35), (3, .55), (4, .72)) if t >= at]
        sc = menu_screen(added)
        for i, at in ((1, .25), (3, .45), (4, .62)):
            if at <= t < at + .1: sc = tap(sc, BTN[f"m{i}"], (t - at) / .1)
        if t > .82: sc = toast(sc, "Porosia u dërgua!", "Po përgatitet në banak.", (t - .82) / .1)
        return phone(bg, sc, c)
    hold(menu_frame, 6.0)
    # 6 scan 4.5s
    c = ("Skano Biletën", "QR-ja në faturë")
    def scan_frame(t):
        if t < 0.12: return phone(bg, tap(home, BTN["scan"], t / 0.12), c, min(1, t * 8))
        return phone(bg, scanner_screen(t * 2, (t - 0.55) / 0.2), c)
    hold(scan_frame, 4.5)
    # 7 outro 3.5s
    hold(lambda t: title_card(bg, "Provoje sot", "te Boulevard", "caffeboulevard.com · Bulevardi Qemal Stafa", min(1, t * 4)), 3.5)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "slow", "-movflags", "+faststart", out], check=True)
    print("ok", cnt[0] / FPS)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
