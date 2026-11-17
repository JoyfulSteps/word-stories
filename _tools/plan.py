"""Build words.tsv: all 8,662 dictionary cards, known/unknown, and the story each word belongs to.
Rule: stories follow unit order; each story has at most ~30 unknown and ~70 words in total.
Run: python _tools/plan.py   (from D:/English/stories)"""
import json, math, csv
from pathlib import Path
from wordfreq import zipf_frequency

ROOT = Path(__file__).resolve().parent.parent
DATA = Path("D:/English/typing-app/exports/dictionary/site/data.js")
MAX_UNK, MAX_ALL = 30, 70

src = DATA.read_text(encoding="utf-8")
entries = json.loads(src[src.index("{"):src.rindex("}") + 1])["e"]
entries = sorted((e for e in entries if e.get("own") is not False), key=lambda e: e["order"])
unknown = set(json.loads((ROOT / "unknown-words_2026-11-17.json").read_text(encoding="utf-8"))["unknown"])

units = {}
for e in entries:
    units.setdefault(e["u"], []).append(e)

rows = []
for u, es in units.items():
    unk = [e["w"] + "|" + u in unknown for e in es]
    nu = sum(unk)
    n = max(math.ceil(nu / MAX_UNK), math.ceil(len(es) / MAX_ALL), 1)
    # contiguous chunks (keeps topics together), balanced by weight
    w = [1.0 if x else MAX_UNK / MAX_ALL for x in unk]
    total, acc, k = sum(w), 0.0, 1
    for e, x, wi in zip(es, unk, w):
        if acc >= total * k / n and k < n:
            k += 1
        acc += wi
        z = zipf_frequency(e["w"], "en")
        grp = "" if not x else ("A" if z >= 4 else "B" if z >= 3 else "C")
        rows.append([e["w"], u, e["g"], e.get("p", ""), e.get("vi", ""), "new" if x else "known",
                     f"{z:.2f}", grp, f"{u}-{k}"])

with open(ROOT / "words.tsv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f, delimiter="\t", lineterminator="\n")
    wr.writerow(["word", "unit", "page", "pos", "vi", "status", "zipf", "group", "story"])
    wr.writerows(rows)

from collections import Counter
s = Counter(r[8] for r in rows); sn = Counter(r[8] for r in rows if r[5] == "new")
print("cards", len(rows), "stories", len(s), "max new", max(sn.values()), "max all", max(s.values()))
