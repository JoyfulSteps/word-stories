"""Print the words each story must use.  python _tools/words_for.py W11 [W12 ...]
*word = new (bold it), plain = known (just use it)."""
import csv, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
units = set(sys.argv[1:])
rows = list(csv.DictReader(open(ROOT / "words.tsv", encoding="utf-8"), delimiter="\t"))
cur = None
for r in rows:
    if r["unit"] not in units:
        continue
    if r["story"] != cur:
        cur = r["story"]
        done = (ROOT / "text" / f"{cur}.md").exists()
        print(f"\n## {cur}{'  (DONE)' if done else ''}")
    new = r["status"] == "new"
    print(("*" + r["word"] + "=" + r["vi"]) if new else r["word"], end="; ")
print()
