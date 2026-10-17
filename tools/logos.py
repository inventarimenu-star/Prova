"""Find a club crest in tools/logos/<League>/<Club>.png from a short team name.

python3 tools/logos.py "Man City" "PSG" "Inter"   -> prints the file found (or NONE)
Logos come from github.com/luukhopman/football-logos (folder logos/). National teams are not included.
"""
import difflib, os, sys, unicodedata

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")

ALIASES = {
    "man city": "Manchester City", "manchester city": "Manchester City",
    "man utd": "Manchester United", "man united": "Manchester United", "manchester united": "Manchester United",
    "spurs": "Tottenham Hotspur", "tottenham": "Tottenham Hotspur", "newcastle": "Newcastle United",
    "forest": "Nottingham Forest", "brighton": "Brighton & Hove Albion", "wolves": "Wolverhampton Wanderers",
    "psg": "Paris Saint-Germain", "paris sg": "Paris Saint-Germain", "paris saint germain": "Paris Saint-Germain",
    "marseille": "Olympique Marseille", "lyon": "Olympique Lyon", "lille": "LOSC Lille", "monaco": "AS Monaco",
    "inter": "Inter Milan", "milan": "AC Milan", "ac milan": "AC Milan", "roma": "AS Roma", "lazio": "SS Lazio",
    "napoli": "SSC Napoli", "juventus": "Juventus FC", "juve": "Juventus FC", "atalanta": "Atalanta BC",
    "fiorentina": "ACF Fiorentina", "bologna": "Bologna FC 1909", "torino": "Torino FC", "como": "Como 1907",
    "barcelona": "FC Barcelona", "barca": "FC Barcelona", "atletico": "Atlético de Madrid",
    "atletico madrid": "Atlético de Madrid", "atl. madrid": "Atlético de Madrid", "betis": "Real Betis Balompié",
    "sevilla": "Sevilla FC", "villarreal": "Villarreal CF", "valencia": "Valencia CF", "bilbao": "Athletic Bilbao",
    "athletic": "Athletic Bilbao", "sociedad": "Real Sociedad",
    "bayern": "Bayern Munich", "bayern munich": "Bayern Munich", "dortmund": "Borussia Dortmund", "bvb": "Borussia Dortmund",
    "leverkusen": "Bayer 04 Leverkusen", "leipzig": "RB Leipzig", "frankfurt": "Eintracht Frankfurt", "stuttgart": "VfB Stuttgart",
    "gladbach": "Borussia Mönchengladbach",
    "benfica": "SL Benfica", "porto": "FC Porto", "sporting": "Sporting CP", "ajax": "Ajax Amsterdam", "psv": "PSV Eindhoven",
    "feyenoord": "Feyenoord Rotterdam", "celtic": "Celtic FC", "rangers": "Rangers FC", "galatasaray": "Galatasaray",
    "fenerbahce": "Fenerbahce", "besiktas": "Besiktas JK", "olympiacos": "Olympiacos Piraeus", "club brugge": "Club Brugge",
    "salzburg": "RB Salzburg", "bodo/glimt": "FK Bodø/Glimt", "bodø/glimt": "FK Bodø/Glimt", "bodo glimt": "FK Bodø/Glimt", "red bull salzburg": "RB Salzburg",
}

def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    for t in (" fc", "fc ", " cf", " afc", " sc", "ac ", " 1909", " 1907", " 1913", "."):
        s = s.replace(t, " ")
    s = s.replace("/", "")
    return " ".join(s.split())

def _index():
    out = {}
    if not os.path.isdir(ROOT): return out
    for lg in os.listdir(ROOT):
        d = os.path.join(ROOT, lg)
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if f.endswith(".png"): out[f[:-4]] = os.path.join(d, f)
    return out

_IDX = None
def find(name):
    """Return the logo path for a team name, or None if not confident."""
    global _IDX
    if _IDX is None: _IDX = _index()
    if not name: return None
    key = name.strip().lower()
    target = ALIASES.get(key)
    if target:
        for club, p in _IDX.items():
            if _norm(club) == _norm(target): return p
    n = _norm(name)
    for club, p in _IDX.items():
        if _norm(club) == n: return p
    # unique substring match ("liverpool" -> "Liverpool FC")
    hits = [p for club, p in _IDX.items() if n and (n in _norm(club).split() or _norm(club).startswith(n + " ") or n == _norm(club))]
    if len(hits) == 1: return hits[0]
    best = difflib.get_close_matches(n, [_norm(c) for c in _IDX], n=1, cutoff=0.86)
    if best:
        for club, p in _IDX.items():
            if _norm(club) == best[0]: return p
    return None

if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(f"{a!r:28} -> {find(a) or 'NONE'}")
