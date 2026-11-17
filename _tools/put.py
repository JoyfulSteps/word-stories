"""Write several stories from stdin.  Blocks start with a line '=== W14-1 ==='."""
import re, sys
from pathlib import Path
sys.stdin.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
parts = re.split(r"^=== (\S+) ===\s*$", src, flags=re.M)
for i in range(1, len(parts), 2):
    (ROOT / "text" / f"{parts[i]}.md").write_text(parts[i + 1].strip() + "\n", encoding="utf-8")
    print("wrote", parts[i])
