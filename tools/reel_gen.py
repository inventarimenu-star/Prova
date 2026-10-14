import os, sys, json, math, random, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

cfg = json.load(open(sys.argv[1]))
W, H, FPS = 1080, 1920, 30
GF = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "")
GOLD, CREAM, MUTED = tuple(cfg.get("gold", [226, 192, 128])), (246, 238, 226), (200, 185, 165)
TMP = cfg["tmp"]

src = Image.open(cfg["src"]).convert("RGB")
if "crop" in cfg: src = src.crop(tuple(cfg["crop"]))
s = W / src.width
img = src.resize((W, int(src.height * s)), Image.LANCZOS)
if img.height >= H:
    top = (img.height - H) // 2
    base = img.crop((0, top, W, top + H))
else:  # extend with blurred fill
    bg = src.resize((int(src.width * H / src.height * 1.0) + 1, H)).resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = img.resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    base = bg.copy(); base.paste(img, (0, (H - img.height) // 2))
cardbg = Image.blend(base.filter(ImageFilter.GaussianBlur(28)), Image.new("RGB", (W, H), (18, 14, 10)), 0.6)

def lora(sz, w=500):
    f = ImageFont.truetype(GF + "Lora-Variable.ttf", sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pop(sz, w="Regular"): return ImageFont.truetype(GF + f"Poppins-{w}.ttf" if w in ("Regular","Medium") else "Poppins-Medium.ttf", sz)
def center(d, y, t, f, fill, a=255, cx=510):
    bb = d.textbbox((0, 0), t, font=f); d.text((cx - (bb[2]-bb[0])//2 - bb[0], y), t, font=f, fill=fill + (a,))
def ease(t): return t*t*(3-2*t)
def zoom(im, z, ay):
    w, h = W/z, H/z; x0 = (W-w)/2; y0 = ay - (ay/H)*h
    return im.crop((int(x0), int(y0), int(x0+w), int(y0+h))).resize((W, H), Image.LANCZOS)

shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
T1, T2, T3 = 6.0, 4.5, 1.5
AY = cfg.get("anchor_y", 1300)
for i in range(int((T1+T2+T3)*FPS)):
    t = i / FPS
    if t < T1:
        fr = zoom(base, 1 + 0.10*ease(t/T1), AY).convert("RGBA")
        if t > 1.2:
            a = int(255*min(1, (t-1.2)/0.4)); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
            sub = cfg["subtitle"]; f = pop(34, "Medium"); bb = d.textbbox((0, 0), sub, font=f); hw = (bb[2]-bb[0])//2 + 40
            d.rounded_rectangle([510-hw, 1335, 510+hw, 1405], 35, fill=(18, 14, 10, int(a*0.7)))
            center(d, 1347, sub, f, CREAM, a); fr = Image.alpha_composite(fr, ov)
        fr = fr.convert("RGB")
    elif t < T1+T2:
        u = t - T1
        fr = Image.blend(zoom(base, 1.10, AY), cardbg, ease(min(1, u/0.5))).convert("RGBA")
        ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        a0 = int(255*min(1, max(0, (u-0.3)/0.4)))
        center(d, 380, cfg["card_title"], lora(80), CREAM, a0)
        center(d, 490, cfg["card_sub"], pop(44, "Medium"), GOLD, a0)
        rows = cfg["rows"]; gap = 150 if len(rows) <= 3 else 120
        for k, r in enumerate(rows):
            a = int(255*min(1, max(0, (u-0.6-k*0.25)/0.35))); y = 650 + k*gap + int(30*(1-a/255))
            d.text((150, y), r[0], font=lora(58), fill=CREAM + (a,))
            if len(r) > 2 and r[2]:
                d.text((150, y+68), r[2], font=pop(30), fill=MUTED + (a,))
            pf = lora(64, 650); bb = d.textbbox((0, 0), r[1], font=pf)
            d.text((870-(bb[2]-bb[0]), y), r[1], font=pf, fill=GOLD + (a,))
            if len(r) > 3 and r[3]:
                of = pop(32); ob = d.textbbox((0, 0), r[3], font=of); ox = 870-(bb[2]-bb[0])-24-(ob[2]-ob[0])
                d.text((ox, y+22), r[3], font=of, fill=MUTED + (a,))
                d.line([(ox, y+42), (ox+(ob[2]-ob[0]), y+42)], fill=MUTED + (a,), width=3)
            d.line([(150, y+gap-22), (870, y+gap-22)], fill=GOLD + (int(a*0.3),), width=2)
        a2 = int(255*min(1, max(0, (u-2.0)/0.4)))
        center(d, 1270, cfg["foot1"], pop(36), CREAM, a2); center(d, 1330, cfg["foot2"], pop(32), GOLD, a2)
        fr = Image.alpha_composite(fr, ov).convert("RGB")
    else:
        fr = Image.blend(cardbg, base, ease(min(1, (t-T1-T2)/T3/0.7)))
    fr.save(f"{TMP}/{i:05d}.jpg", quality=92)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{TMP}/%05d.jpg", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", cfg["out"]], check=True)
print("ok")
