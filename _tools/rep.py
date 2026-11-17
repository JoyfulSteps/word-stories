"""Patch helper: rep(story, old, new). Matches `old` with or without ** marks."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def rep(f, old, new):
    p = ROOT / "text" / f"{f}.md"
    s = p.read_text(encoding="utf-8")
    if old in s:
        s = s.replace(old, new, 1)
    else:
        plain = s.replace("**", "")
        o2 = old.replace("**", "")
        i = plain.find(o2)
        assert i >= 0, (f, old)
        # map plain index back to s index
        pos = [k for k, ch in enumerate(s) if not (s[k:k+2] == "**" or (k > 0 and s[k-1:k+1] == "**" and s[k-1:k+1] != s[k:k+2]))]
        # simpler: rebuild by walking
        j = 0; k = 0; start = end = None
        while k < len(s):
            if s.startswith("**", k):
                k += 2; continue
            if j == i: start = k
            j += 1; k += 1
            if j == i + len(o2): end = k; break
        s = s[:start] + new + s[end:]
    p.write_text(s, encoding="utf-8")
