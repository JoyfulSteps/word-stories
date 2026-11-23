"""Word tools for build.py: the dictionary's headwords, which story words map to which headword, which words are
still unknown to the reader, and the "My day" story format.

The reader page looks a tapped word up in the dictionary's own data.js (typing-app/exports/dictionary/site/data.js,
on the web /english-words-dictionary/data.js). build.py only adds a small index: token -> headwords, for every
token in the stories whose headword is not simply the token itself (stood -> stand, leaves -> leave/leaf).
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_JS = ROOT.parent / "typing-app" / "exports" / "dictionary" / "site" / "data.js"

# Number words and the like are not dictionary cards; a story may use them freely.
FREE = set("""a an i one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen
seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred hundreds thousand thousands
million millions billion first second third fourth fifth sixth seventh eighth ninth tenth a.m p.m ok okay""".split())

TOKEN = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")

# Forms that are almost always another word, not the form the table gives ("a bit" is not the past of bite).
NOT_FORMS = {"bit"}


def load_heads():
    """Lower-case headwords of the dictionary (cards + word-family words). Empty set if the file is missing."""
    if not DICT_JS.exists():
        print(f"!! dictionary data not found: {DICT_JS} (tap-to-look-up index will be empty)")
        return set()
    s = DICT_JS.read_text(encoding="utf-8")
    data = json.loads(s[s.index("=") + 1:].strip().rstrip(";"))
    return {e["w"].lower() for e in data["e"]}


class Lexicon:
    def __init__(self, heads, unknown, forms, irreg_all):
        self.heads = heads
        self.unknown = unknown                      # lower-case words with status "new" in words.tsv
        self.by_form = {}                           # inflected form -> headwords it can come from
        for h in heads:
            if " " in h:
                continue
            for f in forms(h):
                if f != h:
                    self.by_form.setdefault(f, set()).add(h)
        self.irr = {}                               # irregular form -> base (found -> find)
        for base, fs in irreg_all.items():
            for f in fs:
                self.irr.setdefault(f, set()).add(base)
        self._cache = {}

    def candidates(self, tok):
        """Headwords a token may stand for, best first. [] if none."""
        tok = tok.lower()
        if tok in self._cache:
            return self._cache[tok]
        if tok in NOT_FORMS and tok not in self.heads:
            out = []
        elif tok in self.heads:
            more = sorted(b for b in self.irr.get(tok, ()) if b in self.heads and b != tok)
            out = [tok] + more
        else:
            cs = [h for h in self.by_form.get(tok, ()) if h in self.heads]
            if len(cs) > 1:                         # "used" comes from use, not from us
                cs = [h for h in cs if len(h) > 2] or cs
            out = sorted(cs, key=lambda h: (len(tok) - len(h), h))[:3]
        self._cache[tok] = out
        return out

    def is_unknown(self, tok):
        """True when every headword the token may stand for is still unknown (found -> find is known, so no)."""
        cs = self.candidates(tok)
        return bool(cs) and all(c in self.unknown for c in cs)


def tokens_of(text):
    """English tokens as written (case kept). Vietnamese words with tone marks are not tokens."""
    return [m.group(0) for m in TOKEN.finditer(text) if not _touches_non_ascii(text, m)]


def _touches_non_ascii(text, m):
    a, b = m.start(), m.end()
    return (a > 0 and text[a - 1].isalpha() and not text[a - 1].isascii()) or \
           (b < len(text) and text[b].isalpha() and not text[b].isascii())


def is_name(text, m):
    """A capital letter in the middle of a sentence: a name (Bit, Rose), not a word to learn. "I" is not a name."""
    w = m.group(0)
    if not w[0].isupper() or w == "I" or w.startswith("I'"):
        return False
    before = text[:m.start()].rstrip(" \t\"'“‘(")
    return bool(before) and before[-1] not in ".!?:\n"


def bold_unknown(text, lex):
    """Wrap every unknown word in **…** (used for "My day" stories, which have no word list of their own)."""
    def sub(m):
        if _touches_non_ascii(text, m) or is_name(text, m):
            return m.group(0)
        return "**" + m.group(0) + "**" if lex.is_unknown(m.group(0)) else m.group(0)
    return TOKEN.sub(sub, text)


def parse_day(raw):
    """A "My day" story file:

        # Title
        English paragraph…
        = Vietnamese translation of that paragraph (optional, may be several lines)

        ## Say it yourself
        - Useful sentence. = Câu tiếng Việt.
        ! Your turn: a small task. = Việc nhỏ.

        ## Extra words
        honk | v | bấm còi

    Returns title, [[english, vietnamese], …], say [[en, vi], …], task [en, vi] or None, extra [{w, p, vi}, …].
    """
    lines = raw.strip().splitlines()
    title = lines[0].lstrip("# ").strip()
    section, paras, say, task, extra = "story", [], [], None, []
    block_en, block_vi = [], []

    def flush():
        if block_en:
            paras.append(["\n".join(block_en), "\n".join(block_vi)])
        block_en.clear(); block_vi.clear()

    for line in lines[1:] + [""]:
        s = line.strip()
        if s.startswith("## "):
            flush()
            name = s[3:].strip().lower()
            section = "say" if name.startswith("say") else "extra" if name.startswith("extra") else name
            continue
        if section == "story":
            if not s:
                flush()
            elif s.startswith("="):
                block_vi.append(s[1:].strip())
            else:
                block_en.append(line.rstrip())
        elif section == "say" and s:
            kind, body = s[0], s[1:].strip()
            en, _, vi = body.partition(" = ")
            if kind == "-":
                say.append([en.strip(), vi.strip()])
            elif kind == "!":
                task = [en.strip(), vi.strip()]
        elif section == "extra" and s:
            parts = [x.strip() for x in s.split("|")]
            if len(parts) >= 3:
                extra.append({"w": parts[0], "p": parts[1], "vi": parts[2]})
    flush()
    return title, paras, say, task, extra
