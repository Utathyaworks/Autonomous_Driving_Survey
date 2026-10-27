"""Builds PAPERS.md from the survey's BibTeX files (the source of truth for the reference list)."""
import re, os, collections
root = os.path.join(os.path.dirname(__file__), "..")
files = [("references.bib", "General and cross-cutting"), ("refs-spa.bib", "Sense"),
         ("refs-plan.bib", "Plan"), ("refs-act.bib", "Act")]


def clean(v):
    v = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", v)
    v = re.sub(r"[{}\\]", "", v)
    return re.sub(r"\s+", " ", v).strip()


def parse(txt):
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", txt):
        kind, key = m.group(1).lower(), m.group(2)
        if kind in ("comment", "string", "preamble"):
            continue
        i = m.end(); depth = 1; j = i
        while j < len(txt) and depth:
            depth += (txt[j] == "{") - (txt[j] == "}"); j += 1
        body = txt[i:j - 1]; f = {}
        for fm in re.finditer(r'(\w+)\s*=\s*(\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}|"([^"]*)"|(\w+))', body):
            f[fm.group(1).lower()] = clean(fm.group(3) or fm.group(4) or fm.group(5) or "")
        out.append((key, kind, f))
    return out


seen = {}; sections = collections.OrderedDict()
for fn, label in files:
    p = os.path.join(root, "data", fn)
    if not os.path.exists(p):
        continue
    rows = []
    for key, kind, f in parse(open(p, encoding="utf-8", errors="replace").read()):
        if key in seen:
            continue
        seen[key] = 1
        a = f.get("author", ""); au = [x.strip() for x in a.split(" and ")] if a else []
        short = (au[0].split(",")[0] + (" et al." if len(au) > 1 else "")) if au else "n/a"
        venue = f.get("journal") or f.get("booktitle") or f.get("publisher") or f.get("howpublished") or f.get("institution") or ""
        link = ("https://doi.org/" + f["doi"]) if f.get("doi") else f.get("url", "")
        rows.append((f.get("year", ""), short, f.get("title", ""), venue, link, key))
    sections[label] = sorted(rows, key=lambda r: (r[0], r[1]))
total = sum(len(v) for v in sections.values())
L = ["# Papers cited in the survey", "",
     f"{total} unique entries, generated from the BibTeX files by `scripts/make_paper_list.py`. Sorted by year within each group.", ""]
for label, rows in sections.items():
    L += [f"## {label} ({len(rows)})", "", "| Year | First author | Title | Venue | Link |", "|---|---|---|---|---|"]
    for y, a, t, v, l, k in rows:
        L.append(f"| {y} | {a} | {t.replace('|', '/')} | {v.replace('|', '/')} | " + (f"[link]({l})" if l else "") + " |")
    L.append("")
open(os.path.join(root, "PAPERS.md"), "w", encoding="utf-8").write("\n".join(L))
import json
os.makedirs(os.path.join(root, "docs"), exist_ok=True)
js = [{"g": label, "y": int(y) if y.isdigit() else None, "a": a, "t": t, "v": v, "l": l, "k": k}
      for label, rows in sections.items() for y, a, t, v, l, k in rows]
json.dump(js, open(os.path.join(root, "docs", "papers.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(total, {k: len(v) for k, v in sections.items()})
