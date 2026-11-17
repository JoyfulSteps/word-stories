"""Check every story covers its words, then build stories.html (one self-contained page).

Story source: text/<story>.md . First line '# Title'. New words in **bold**. '> ' = letter/quote.
Run from D:/English/stories:  python _tools/build.py
"""
import csv, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"

IRREG = {
    "tear": ["tore", "torn"], "die": ["died", "dying"], "shake": ["shook", "shaken"], "bleed": ["bled"],
    "hang": ["hung"], "sweep": ["swept"], "breathe": ["breathing"], "wear": ["wore"], "lie": ["lay"],
    "children": ["children"], "mister": ["mr"], "fly": ["flew", "flies"], "ring": ["rang", "rung"],
    "sink": ["sank", "sunk"], "lead": ["led"], "feel": ["felt"], "lose": ["lost"], "hold": ["held"],
    "hurt": ["hurt"], "marry": ["married"], "bear": ["born"], "grandchild": ["grandchildren"], "fall": ["fell"],
}


_IRR = """be was were been being am is are|go went gone goes|come came|take took taken|give gave given|do did does done|
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

stories, problems = [], 0
for path in sorted(TEXT.glob("*.md")):
    sid = path.stem
    raw = path.read_text(encoding="utf-8")
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
    problems += bool(miss or not_bold or extra_bold)
    stories.append({
        "id": sid, "title": title, "body": body, "words": n_words,
        "new": [{"w": r["word"], "p": r["pos"], "vi": r["vi"]} for r in new],
    })

done_words = sum(len(by_story.get(s["id"], [])) for s in stories)
print(f"\n{len(stories)} stories, cover {done_words}/{len(words)} cards. Problems: {problems}")

tpl = (ROOT / "_tools" / "reader.html").read_text(encoding="utf-8")
out = tpl.replace("/*DATA*/null", json.dumps(stories, ensure_ascii=False))
(ROOT / "stories.html").write_text(out, encoding="utf-8")
(ROOT / "index.html").write_text(out, encoding="utf-8")   # GitHub Pages opens index.html
print("wrote stories.html + index.html")
sys.exit(1 if problems else 0)
