"""Turn a Story image into a 10 s video Story with a slow zoom and original Italian-style music.

python3 tools/story_video.py in.jpg out.mp4 mattina|pranzo|sera [seed] [--sec 10]
No voice. Text in the image stays fully inside the frame (max zoom 4%).
"""
import argparse, os, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    a = argparse.ArgumentParser()
    a.add_argument("src"); a.add_argument("out"); a.add_argument("style")
    a.add_argument("seed", nargs="?", default="1"); a.add_argument("--sec", type=int, default=10)
    a = a.parse_args()
    n = a.sec * 30
    with tempfile.TemporaryDirectory() as t:
        wav = os.path.join(t, "m.wav")
        subprocess.run(["python3", os.path.join(ROOT, "tools", "italian_music.py"), str(a.sec), wav, a.style, a.seed],
                       check=True, stdout=subprocess.DEVNULL)
        vf = (f"scale=2160:3840,zoompan=z='1+0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d={n}:s=1080x1920:fps=30,format=yuv420p")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", a.src, "-i", wav,
                        "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-c:a", "aac", "-b:a", "160k", "-af", f"afade=t=out:st={a.sec - 1.2}:d=1.2",
                        "-shortest", "-movflags", "+faststart", a.out], check=True)
    print(a.out)

if __name__ == "__main__":
    main()
