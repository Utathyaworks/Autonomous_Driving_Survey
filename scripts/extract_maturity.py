"""Extracts the three maturity tables (Sense, Plan, Act) from the LaTeX sources into data/maturity.csv.
Run from the manuscript repository; the figure script reads only the CSV."""
import re, csv, os
bs = chr(92)
root = os.path.join(os.path.dirname(__file__), "..")
SRC = [("Sense", "sections/section 3.2.1 - Sense.tex", "tab:mat_sense"),
       ("Plan", "sections/section 3.2.2 - Plan.tex", "tab:mat_plan"),
       ("Act", "sections/section 3.2.3 - Act.tex", "tab:mat_act")]


def clean(s):
    s = re.sub(r"~?\\cite\{[^}]*\}", "", s)
    s = re.sub(r"\\(textbf|emph|textit)\{([^{}]*)\}", r"\2", s)
    s = s.replace("\\,", " ").replace("~", " ").replace("\\&", "&").replace("--", "-")
    s = re.sub(r"[{}$]", "", s)
    return re.sub(r"\s+", " ", s).strip()


rows = []
for stage, fn, label in SRC:
    t = open(os.path.join(root, fn), encoding="utf-8").read()
    i = t.index("\\label{" + label + "}")
    j = t.index("\\end{tabularx}", i) if "\\begin{tabularx}" in t[i:i + 900] else t.index("\\end{tabular}", i)
    body = t[i:j]
    body = body[body.index("\\toprule"):]
    for r in re.split(r"\\\\", body):
        r = re.sub(r"\\(toprule|midrule|bottomrule)", "", r).strip()
        cells = [c.strip().replace("@@AMP@@", bs + "&") for c in r.replace(bs + "&", "@@AMP@@").split("&")]
        grades = [re.fullmatch(r"M[1-4]", clean(c)) for c in cells[1:6]]
        if len(cells) >= 6 and all(grades):
            rows.append([stage, clean(cells[0])] + [clean(c) for c in cells[1:6]] + [clean(cells[6]) if len(cells) > 6 else ""])
os.makedirs(os.path.join(root, "data"), exist_ok=True)
with open(os.path.join(root, "data", "maturity.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(["stage", "family", "E1", "E2", "E3", "E4", "E5", "basis"]); w.writerows(rows)
for s in ("Sense", "Plan", "Act"):
    print(s, sum(1 for r in rows if r[0] == s))
