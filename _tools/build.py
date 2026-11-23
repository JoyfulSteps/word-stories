"""Check every story covers its words, then build stories.html (one self-contained page) and stories.json.

Story source: text/<story>.md . First line '# Title'. New words in **bold**. '> ' = letter/quote.
Run from D:/English/stories:  python _tools/build.py

Sentences are split HERE, once, and numbered 1, 2, 3… inside each story. The reader, the dictionary
(typing-app/tools/build_dictionary.py) and the grammar cards (ielts-grammar/_web/build_site.py) all use these numbers,
so a link like …/word-stories/#W02-1?s=12&w=coat opens sentence 12 of W02-1 and marks "coat".
stories.json is the export the other two sites read (schema "word-stories/1").
"""
import csv, html, json, re, sys
from pathlib import Path

from lexicon import FREE, TOKEN, Lexicon, bold_unknown, is_name, load_heads, parse_day, tokens_of

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
SITE = "https://joyfulsteps.github.io/word-stories/"

# A series is a set of stories told together. A story belongs to the first series whose pattern matches its id.
# To start a new series (e.g. daily-life stories D001, D002…): add a line here, write text/D001.md, build.
SERIES = [
    {"id": "minh", "name": "Minh's story", "pattern": r"^W\d\d-\d+$"},
    # Daily life in Hanoi, told by "I" (format: lexicon.parse_day). No word list: unknown words are bolded by build.
    {"id": "day", "name": "My day", "pattern": r"^D\d{3}$"},
]


def series_of(sid):
    for s in SERIES:
        if re.match(s["pattern"], sid):
            return s["id"]
    return "other"


def split_sentences(text):
    """Same rule the reader used before: up to . ! ? (plus closing quotes), but not after Mr. Mrs. Ms. Dr."""
    parts = re.findall(r"[^.!?]+(?:[.!?]+[\"'’)\]]*\s*|$)", text) or [text]
    out = []
    for p in parts:
        if not p:
            continue
        if out and re.search(r"\b(Mr|Mrs|Ms|Dr)\.\s*$", out[-1]):
            out[-1] += p
        else:
            out.append(p)
    return out


def paragraphs(body):
    """[[is_quote, [sentence, …]], …]. Sentences keep their own spaces and line breaks, so the page looks the same."""
    out = []
    for block in re.split(r"\n\s*\n", body):
        if not block.strip():
            continue
        quote = block.startswith(">")
        raw = re.sub(r"^> ?", "", block, flags=re.M)
        out.append([1 if quote else 0, split_sentences(raw)])
    return out

IRREG = {
    "tear": ["tore", "torn"], "die": ["died", "dying"], "shake": ["shook", "shaken"], "bleed": ["bled"],
    "hang": ["hung"], "sweep": ["swept"], "breathe": ["breathing"], "wear": ["wore"], "lie": ["lay"],
    "children": ["children"], "mister": ["mr"], "fly": ["flew", "flies"], "ring": ["rang", "rung"],
    "sink": ["sank", "sunk"], "lead": ["led"], "feel": ["felt"], "lose": ["lost"], "hold": ["held"],
    "hurt": ["hurt"], "marry": ["married"], "bear": ["born"], "grandchild": ["grandchildren"], "fall": ["fell"],
}


_IRR = """be was were been being am is are|become became|go went gone goes|come came|take took taken|give gave given|do did does done|
have had has|drink drank drunk|bring brought|meet met|make made|get got gotten|see saw seen|say said|tell told|
think thought|know knew known|find found|leave left|eat ate eaten|buy bought|sell sold|teach taught|catch caught|
fight fought|run ran|swim swam swum|sing sang sung|begin began begun|write wrote written|ride rode ridden|
drive drove driven|speak spoke spoken|break broke broken|choose chose chosen|forget forgot forgotten|
freeze froze frozen|steal stole stolen|wake woke woken|hide hid hidden|bite bit bitten|fall fell fallen|
feel felt|keep kept|sleep slept|sweep swept|weep wept|lend lent|send sent|spend spent|build built|
lose lost|hold held|stand stood|understand understood|sit sat|win won|hang hung|dig dug|stick stuck|
strike struck|sting stung|swing swung|light lit|lead led|feed fed|bleed bled|flee fled|shoot shot|
pay paid|lay laid|lie lay lain|hear heard|mean meant|draw drew drawn|grow grew grown|throw threw thrown|
blow blew blown|fly flew flown flies|show showed shown|wear wore worn|tear tore torn|bear bore born borne|
shake shook shaken|rise rose risen|arise arose arisen|seek sought|bind bound|grind ground|
deal dealt|dream dreamt dreamed|burn burnt|learn learnt|spell spelt|spill spilt|smell smelt|
child children|man men|woman women|tooth teeth|foot feet|mouse mice|person people|wife wives|knife knives|
life lives|leaf leaves|thief thieves|half halves|shelf shelves|ox oxen|goose geese|crisis crises|
analysis analyses|phenomenon phenomena|criterion criteria|medium media|datum data|stimulus stimuli|
fungus fungi|cactus cacti|nucleus nuclei|thesis theses|hypothesis hypotheses|index indices indexes|
good better best|bad worse worst|far further farther|little less least|many more most"""
IRREG_ALL = {}
for grp in _IRR.replace("\n", "").split("|"):
    ws = grp.split()
    if ws:
        IRREG_ALL.setdefault(ws[0], set()).update(ws[1:])


def forms(w):
    w = w.lower()
    out = {w, w + "s", w + "es", w + "ed", w + "d", w + "ing", w + "'s"}
    out |= {w + "er", w + "est", w + "r", w + "st", w + "ly"}
    if w.endswith("y"):
        out |= {w[:-1] + "ies", w[:-1] + "ied", w[:-1] + "ier", w[:-1] + "iest", w[:-1] + "ily"}
    if w.endswith("e"):
        out.add(w[:-1] + "ing")
    if re.search(r"[^aeiou][aeiou][bdgklmnprt]$", w):
        out |= {w + w[-1] + "ed", w + w[-1] + "ing"}
    if w.endswith("f"):
        out.add(w[:-1] + "ves")
    if w.endswith("fe"):
        out.add(w[:-2] + "ves")
    out |= set(IRREG.get(w, []))
    out |= IRREG_ALL.get(w, set())
    return out


def tokens(text):
    return re.findall(r"[a-z]+(?:[-'][a-z]+)*", text.lower())


def found(word, toks, text):
    w = word.lower()
    if " " in w or "-" in w:
        return w in text.lower()
    return any(f in toks for f in forms(w))


words = list(csv.DictReader(open(ROOT / "words.tsv", encoding="utf-8"), delimiter="\t"))
by_story = {}
for r in words:
    by_story.setdefault(r["story"], []).append(r)

sys.stdout.reconfigure(encoding="utf-8")
lex = Lexicon(load_heads(), {r["word"].lower() for r in words if r["status"] == "new"}, forms, IRREG_ALL)
card = {r["word"].lower(): r for r in words}
SERIES_IDS = [s["id"] for s in SERIES]


def build_day(sid, raw):
    """A "My day" story: bold its unknown words, check that every other word can be looked up."""
    title, blocks, say, task, extra = parse_day(raw)
    extra_words = {part for e in extra for part in e["w"].lower().split()}   # "banh mi" covers banh and mi
    english = "\n\n".join(en for en, _ in blocks)
    toks = tokens_of(english)
    names = {m.group(0).lower() for m in TOKEN.finditer(english) if is_name(english, m)}
    lower_seen = {t.lower() for t in toks if not t[0].isupper()}
    new, missing = [], []
    for t in toks:
        k = t.lower()
        cs = lex.candidates(k)
        if lex.is_unknown(k) and not (t[0].isupper() and k in names):
            r = card.get(cs[0])
            if r and not any(n["w"] == r["word"] for n in new):
                new.append({"w": r["word"], "p": r["pos"], "vi": r["vi"]})
        elif not cs and k not in extra_words and k not in FREE and "'" not in k and k not in missing \
                and (k in lower_seen or not t[0].isupper()):   # a word only ever written with a capital is a name
            missing.append(k)
    paras = []
    for en, vi in blocks:
        quote = en.startswith(">")
        en = re.sub(r"^> ?", "", en, flags=re.M)
        paras.append([1 if quote else 0, split_sentences(bold_unknown(en, lex)), vi])
    flag = "OK " if not missing else "!! "
    print(f"{flag}{sid}: {len(toks)} words, {len(new)} unknown words, {len(extra)} extra words"
          + (f"\n    not in the dictionary, add to '## Extra words': {missing}" if missing else ""))
    return {"id": sid, "title": title, "p": paras, "words": len(toks), "new": new,
            "say": say, "task": task, "extra": extra}, bool(missing)


def story_order(path):
    sid = path.stem
    s = series_of(sid)
    return (SERIES_IDS.index(s) if s in SERIES_IDS else len(SERIES_IDS), sid)


stories, problems = [], 0
for path in sorted(TEXT.glob("*.md"), key=story_order):
    sid = path.stem
    raw = path.read_text(encoding="utf-8")
    if series_of(sid) == "day":
        st, bad = build_day(sid, raw)
        st["series"] = "day"
        stories.append(st)
        problems += bad
        continue
    lines = raw.strip().splitlines()
    title = lines[0].lstrip("# ").strip()
    body = "\n".join(lines[1:]).strip()
    plain = body.replace("**", "")
    toks = set(tokens(plain))
    bold = {b.lower() for b in re.findall(r"\*\*(.+?)\*\*", body)}
    assigned = by_story.get(sid, [])
    new = [r for r in assigned if r["status"] == "new"]
    miss = [r["word"] for r in assigned if not found(r["word"], toks, plain)]
    not_bold = [r["word"] for r in new if not any(b in forms(r["word"]) for b in bold)]
    new_forms = set().union(*(forms(r["word"]) for r in new)) if new else set()
    extra_bold = sorted(b for b in bold if b not in new_forms)
    n_words = len(tokens(plain))
    flag = "OK " if not (miss or not_bold or extra_bold) else "!! "
    print(f"{flag}{sid}: {n_words} words, {len(assigned)} assigned ({len(new)} new)"
          + (f"\n    missing: {miss}" if miss else "")
          + (f"\n    new but not bold: {not_bold}" if not_bold else "")
          + (f"\n    bold but not new: {extra_bold}" if extra_bold else ""))
    paras = paragraphs(body)
    broken = [s for _, ss in paras for s in ss if s.count("**") % 2]
    if broken:
        print(f"!! {sid}: bold cut by a sentence end: {broken[0][:60]!r}")
        problems += 1
    problems += bool(miss or not_bold or extra_bold)
    stories.append({
        "id": sid, "series": series_of(sid), "title": title, "p": paras, "words": n_words,
        "new": [{"w": r["word"], "p": r["pos"], "vi": r["vi"]} for r in new],
    })

done_words = sum(len(by_story.get(s["id"], [])) for s in stories)
print(f"\n{len(stories)} stories, cover {done_words}/{len(words)} cards. Problems: {problems}")

# Tap-to-look-up index for the reader. lex: token -> headwords, only where that is not just the token itself
# (stood -> stand). unk: tokens that are unknown words (shown blue). seen: unknown word -> stories it is in.
lexmap, unk, seen = {}, set(), {}
for st in stories:
    text = " ".join(x for para in st["p"] for x in para[1]).replace("**", "")
    for t in sorted({x.lower() for x in tokens_of(text)}):
        cs = lex.candidates(t)
        if cs and cs != [t]:
            lexmap[t] = cs
        if lex.is_unknown(t):
            unk.add(t)
            ids = seen.setdefault(cs[0], [])
            if st["id"] not in ids:
                ids.append(st["id"])
index = {"lex": lexmap, "unk": sorted(unk), "seen": seen}
print(f"look-up index: {len(lexmap)} word forms, {len(unk)} unknown forms, {len(seen)} unknown words in the stories")

tpl = (ROOT / "_tools" / "reader.html").read_text(encoding="utf-8")
out = (tpl.replace("/*DATA*/null", json.dumps(stories, ensure_ascii=False))
          .replace("/*WORDS*/null", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
          .replace("/*SERIES*/null", json.dumps([{"id": s["id"], "name": s["name"]} for s in SERIES])))
(ROOT / "stories.html").write_text(out, encoding="utf-8")
(ROOT / "index.html").write_text(out, encoding="utf-8")   # GitHub Pages opens index.html

# Export for the dictionary and the grammar cards: one line of text per sentence, **bold** = new word in this story.
export = {
    "schema": "word-stories/1",
    "site": SITE,
    "link": "#{id}?s={s}&w={w}",
    "series": [{"id": s["id"], "name": s["name"]} for s in SERIES],
    "stories": [{
        "id": s["id"], "series": series_of(s["id"]), "title": s["title"],
        "sents": [" ".join(x.split()) for para in s["p"] for x in para[1]],   # English only, never the Vietnamese
    } for s in stories],
}
(ROOT / "stories.json").write_text(json.dumps(export, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"wrote stories.html + index.html + stories.json ({sum(len(s['sents']) for s in export['stories'])} sentences)")
sys.exit(1 if problems else 0)
