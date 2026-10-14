"""Offline audio for Boulevard Caffe reels: Albanian voice-over (eSpeak NG) + original royalty-free music.

python3 tools/audio.py voice "tekst" out.wav
python3 tools/audio.py music SECONDS out.wav [warm|evening]
python3 tools/audio.py mix video.mp4 music.wav [voice.wav] out.mp4
"""
import sys, ctypes, wave, subprocess
import numpy as np

SR = 44100

def voice(text, out, rate=145, pitch=55):
    import espeakng_loader
    lib = ctypes.cdll.LoadLibrary(espeakng_loader.get_library_path())
    sr = lib.espeak_Initialize(1, 0, espeakng_loader.get_data_path().encode(), 0)
    buf = bytearray()
    CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
    def cb(wav, n, ev):
        if n > 0: buf.extend(ctypes.string_at(wav, n * 2))
        return 0
    keep = CB(cb); lib.espeak_SetSynthCallback(keep)
    lib.espeak_SetVoiceByName(b"sq")
    lib.espeak_SetParameter(1, rate, 0); lib.espeak_SetParameter(3, pitch, 0)
    t = text.encode("utf-8")
    lib.espeak_Synth(t, len(t) + 1, 0, 0, 0, 1, None, None)  # 1 = UTF-8 input
    lib.espeak_Synchronize()
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(bytes(buf))

def _tone(f, dur, amp, attack=0.01, decay=1.2):
    t = np.arange(int(SR * dur)) / SR
    env = np.minimum(1, t / attack) * np.exp(-t * decay)
    s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.6 for k in (1, 2, 3, 4))  # soft electric-piano-ish
    return amp * env * s

def music(seconds, out, mood="warm"):
    bpm = 84 if mood == "warm" else 92
    beat = 60 / bpm
    n = int(SR * seconds); mix = np.zeros(n + SR * 3)
    # ii-V-I-vi in D major / A minor flavour, jazzy 7ths
    prog = [[146.83, 174.61, 220.0, 261.63], [196.0, 246.94, 293.66, 349.23],
            [146.83, 185.0, 220.0, 277.18], [123.47, 146.83, 185.0, 220.0]] if mood == "warm" else \
           [[110.0, 130.81, 164.81, 196.0], [98.0, 123.47, 146.83, 174.61],
            [87.31, 110.0, 130.81, 164.81], [82.41, 103.83, 123.47, 146.83]]
    bar = 4 * beat; i = 0; t0 = 0.0
    rng = np.random.default_rng(7)
    while t0 < seconds:
        ch = prog[i % 4]
        for f in ch:
            s = _tone(f, bar + 1, 0.06, attack=0.02, decay=0.9); a = int(t0 * SR); mix[a:a + len(s)] += s[:len(mix) - a]
        s = _tone(ch[0] / 2, bar, 0.10, decay=1.5); a = int(t0 * SR); mix[a:a + len(s)] += s[:len(mix) - a]
        for b in range(4):  # soft kick + hat
            a = int((t0 + b * beat) * SR); tt = np.arange(int(0.25 * SR)) / SR
            if b % 2 == 0:
                k = 0.18 * np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12)
                mix[a:a + len(k)] += k[:len(mix) - a]
            h = 0.02 * rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 80)
            a2 = int((t0 + b * beat + beat / 2) * SR); mix[a2:a2 + len(h)] += h[:len(mix) - a2]
        t0 += bar; i += 1
    mix = mix[:n]
    fade = int(SR * 1.2); mix[-fade:] *= np.linspace(1, 0, fade); mix[:int(SR * .3)] *= np.linspace(0, 1, int(SR * .3))
    mix = 0.8 * mix / (np.max(np.abs(mix)) + 1e-9)
    st = np.stack([mix, np.roll(mix, int(SR * 0.012))], 1)  # light stereo width
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

def mix_av(video, music_wav, voice_wav, out):
    if voice_wav:
        fc = "[1:a]volume=0.35[m];[2:a]adelay=900|900,volume=1.6[v];[m][v]amix=inputs=2:duration=first:normalize=0[a]"
        args = ["-i", video, "-i", music_wav, "-i", voice_wav]
    else:
        fc = "[1:a]volume=0.8[a]"; args = ["-i", video, "-i", music_wav]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "voice": voice(sys.argv[2], sys.argv[3])
    elif cmd == "music": music(float(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "warm")
    elif cmd == "mix": mix_av(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 5 else None, sys.argv[-1])
