"""Original Italian-style background music (no copyrighted melodies), offline, royalty-free.

python3 tools/italian_music.py SECONDS out.wav STYLE [seed]
STYLE: mattina  - gentle mandolin waltz + guitar (breakfast, coffee)
       pranzo   - bright tarantella-ish 6/8, mandolin + accordion (lunch, pizza)
       sera     - slow romantic accordion + mandolin tremolo (evening, beer, wine)
"""
import sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(0)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def pluck(freq, dur, amp, bright=1.0):
    """plucked string: additive partials with per-partial decay + slight inharmonicity"""
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for k in range(1, 9):
        f = freq * k * (1 + 0.0004 * k * k)
        if f > SR / 2.2: break
        out += (bright ** (k - 1)) / k ** 1.1 * np.sin(2 * np.pi * f * t) * np.exp(-t * (2.2 + 1.6 * k))
    att = np.minimum(1, t / 0.003)
    return amp * att * out

def mandolin(freq, dur, amp, tremolo=False):
    """mandolin: paired detuned courses; tremolo = rapid re-plucks on long notes"""
    if not tremolo or dur < 0.3:
        return pluck(freq, dur + 0.25, amp, 0.75) + pluck(freq * 1.0025, dur + 0.25, amp * 0.8, 0.75)
    n = int(SR * (dur + 0.2)); out = np.zeros(n); step = 1 / 13.0; t0 = 0.0; i = 0
    while t0 < dur:
        a = amp * (0.75 + 0.25 * (i % 2)) * (0.9 + 0.1 * np.sin(t0 * 3))
        s = pluck(freq, 0.18, a, 0.75) + pluck(freq * 1.0025, 0.18, a * 0.8, 0.75)
        k = int(t0 * SR); m = min(len(s), n - k); out[k:k + m] += s[:m]; t0 += step; i += 1
    return out

def accordion(freq, dur, amp):
    """accordion reed: rich odd/even partials, musette detune, bellows swell + vibrato"""
    t = np.arange(int(SR * (dur + 0.05))) / SR
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5.5 * t)
    out = np.zeros_like(t)
    for det in (1.0, 1.004, 0.997):
        ph = 2 * np.pi * freq * det * np.cumsum(vib) / SR
        for k, g in ((1, 1.0), (2, 0.55), (3, 0.45), (4, 0.25), (5, 0.18), (6, 0.1)):
            out += g * np.sin(k * ph)
    env = np.minimum(1, t / 0.05) * np.minimum(1, np.maximum(0, (dur + 0.05 - t) / 0.08))
    return amp * 0.22 * env * out

def add(buf, sig, at):
    k = int(at * SR)
    if k >= len(buf): return
    m = min(len(sig), len(buf) - k); buf[k:k + m] += sig[:m]

SCALE = [0, 2, 4, 5, 7, 9, 11]
def chord_tones(root, minor=False, seventh=False):
    c = [root, root + (3 if minor else 4), root + 7]
    if seventh: c.append(root + 10)
    return c

def melody_for(chords, beats_per_bar, rng, key=60, high=72):
    """original melody: chord tones on strong beats, stepwise scale motion elsewhere"""
    notes = []  # (beat_offset, length_beats, midi)
    prev = high
    pool = sorted({key + 12 + s for s in SCALE} | {key + 24 + s for s in SCALE[:4]})
    for b, (root, minor, sev) in enumerate(chords):
        ct = [n for n in pool if (n - (root % 12)) % 12 in [(x - root) % 12 for x in chord_tones(root, minor, sev)]]
        opts = [[1, 1, 1], [2, 1], [1, 2], [0.5, 0.5, 1, 1], [3]] if beats_per_bar == 3 else \
               [[1.5, 1.5], [1, 0.5, 1, 0.5], [0.5, 0.5, 0.5, 1.5], [3]]
        rhythm = opts[int(rng.integers(len(opts)))]
        pos = 0.0
        for i, ln in enumerate(rhythm):
            if i == 0 or ln >= 1.5:
                n = min(ct, key=lambda x: abs(x - prev) + rng.random() * 2)
            else:
                idx = int(np.argmin([abs(p - prev) for p in pool])); idx = max(0, min(len(pool) - 1, idx + rng.choice([-1, 1, 1])))
                n = pool[idx]
            notes.append((b * beats_per_bar + pos, ln, n)); prev = n; pos += ln
    return notes

def render(seconds, style, seed=1):
    rng = np.random.default_rng(seed)
    n = int(SR * (seconds + 2)); mix = np.zeros(n)
    if style == "pranzo":
        bpm, bpb, key = 132, 3, 62  # 6/8 feel as fast 3
        prog = [(62, False, False), (62, False, False), (69, False, True), (69, False, True),
                (67, False, False), (62, False, False), (69, False, True), (62, False, False)]
        lead, lead_amp, use_acc = "mand", 0.16, True
    elif style == "sera":
        bpm, bpb, key = 84, 3, 57
        prog = [(57, True, False), (62, True, False), (64, False, True), (57, True, False),
                (53, False, False), (62, True, False), (64, False, True), (57, True, False)]
        lead, lead_amp, use_acc = "acc", 0.14, True
    else:  # mattina
        bpm, bpb, key = 96, 3, 60
        prog = [(60, False, False), (65, False, False), (67, False, True), (60, False, False),
                (69, True, False), (65, False, False), (67, False, True), (60, False, False)]
        lead, lead_amp, use_acc = "mand", 0.15, False
    beat = 60 / bpm; bar = beat * bpb
    nbars = int(np.ceil(seconds / bar)) + 1
    chords = [prog[i % len(prog)] for i in range(nbars)]
    mel = melody_for(prog, bpb, rng, key=key) # one 8-bar theme, repeated with variation
    mel2 = melody_for(prog, bpb, np.random.default_rng(seed + 7), key=key)
    for bi, (root, minor, sev) in enumerate(chords):
        t0 = bi * bar
        ct = chord_tones(root - 12, minor, sev)
        # bass (guitar) on 1, chord plucks on 2 & 3 — waltz/oom-pah
        add(mix, pluck(midi(root - 24), bar * 0.9, 0.22, 0.6), t0)
        for b in range(1, bpb):
            for j, c in enumerate(ct[:3]):
                add(mix, pluck(midi(c), beat * 0.9, 0.06, 0.8), t0 + b * beat + j * 0.012)
        if use_acc and style == "sera":
            for c in ct[:3]: add(mix, accordion(midi(c), bar * 0.98, 0.05), t0)
        if use_acc and style == "pranzo" and bi % 2 == 1:
            for c in ct[:3]: add(mix, accordion(midi(c + 12), beat * 0.45, 0.035), t0 + beat)
    # melody: theme A, then theme B, repeat
    theme_len = len(prog) * bar
    t = 0.0; which = 0
    while t < seconds:
        for (bo, ln, note) in (mel if which % 2 == 0 else mel2):
            at = t + bo * beat; dur = ln * beat * 0.95
            if at > seconds: break
            if lead == "acc":
                add(mix, accordion(midi(note), dur, lead_amp), at)
                if ln >= 2: add(mix, mandolin(midi(note + 12), dur, 0.05, tremolo=True), at)
            else:
                add(mix, mandolin(midi(note), dur, lead_amp, tremolo=ln >= 2), at)
        t += theme_len; which += 1
    mix = mix[:int(SR * seconds)]
    # light room reverb (multi-tap) and master
    rev = np.zeros_like(mix)
    for d, g in ((0.031, .35), (0.047, .28), (0.071, .22), (0.113, .16), (0.17, .1)):
        k = int(d * SR); rev[k:] += g * mix[:-k]
    mix = mix + 0.6 * rev
    f = int(SR * 1.5); mix[-f:] *= np.linspace(1, 0, f); mix[:int(SR * .25)] *= np.linspace(0, 1, int(SR * .25))
    mix = np.tanh(1.2 * mix / (np.max(np.abs(mix)) + 1e-9)) * 0.85
    st = np.stack([mix, np.concatenate([np.zeros(int(SR * 0.009)), mix[:-int(SR * 0.009)]])], 1)
    return st

if __name__ == "__main__":
    secs, out, style = float(sys.argv[1]), sys.argv[2], sys.argv[3]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    st = render(secs, style, seed)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print(out)
