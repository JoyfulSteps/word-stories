"""Remove ** from words that are not new in that story.  python _tools/unbold.py W12-1 [W12-2 ...]"""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(__file__).resolve().parent.parent
import importlib.util
spec = importlib.util.spec_from_file_location("b", ROOT / "_tools" / "build.py")
src = (ROOT / "_tools" / "build.py").read_text(encoding="utf-8")
ns = {"__file__": str(ROOT / "_tools" / "build.py")}
exec(src.split("words = list(")[0], ns)   # only the helpers
forms = ns["forms"]
rows = list(csv.DictReader(open(ROOT / "words.tsv", encoding="utf-8"), delimiter="\t"))
for sid in sys.argv[1:]:
    new = set()
    for r in rows:
        if r["story"] == sid and r["status"] == "new":
            new |= forms(r["word"])
    p = ROOT / "text" / f"{sid}.md"
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r"\*\*(.+?)\*\*", lambda m: m.group(0) if m.group(1).lower() in new else m.group(1), s)
    p.write_text(s2, encoding="utf-8")
    print(sid, "unbolded", s.count("**") // 2 - s2.count("**") // 2)
