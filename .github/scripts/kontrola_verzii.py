"""Po `packwiz update`: vrati spat "aktualizacie", ktore su v skutocnosti downgrade
(packwiz berie verziu podla datumu zverejnenia a Modrinth niekedy neskor zverejni
starsiu verziu), a upozorni na velke skoky verzie, ktore treba vyskusat.
"""
import json
import os
import re
import subprocess
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Spekac007/create-aestro-pack (GitHub Actions)"}
# verziu Minecraftu (1.21, 1.21.1, mc1.21.1) z cisla verzie vyhodime, aby neplietla porovnanie
MC_RE = re.compile(r"(?<![\d.])(?:mc)?1\.21(?:\.\d+)?(?!\d)", re.I)
PRE_RE = re.compile(r"(?<![a-z])(?:alpha|beta|pre|rc)", re.I)


def vkey(s):
    """(hlavne cisla, cisla predbeznej verzie, je predbezna) - napr. 4.0.1 vs 4-beta.11"""
    s = MC_RE.sub(" ", s)
    m = PRE_RE.search(s)
    core_s, pre_s = (s[:m.start()], s[m.start():]) if m else (s, "")
    return ([int(x) for x in re.findall(r"\d+", core_s)],
            [int(x) for x in re.findall(r"\d+", pre_s)], bool(m))


def compare(a, b):
    """-1 ak a < b, 0 ak rovnake, 1 ak a > b"""
    ca, pa, ia = vkey(a)
    cb, pb, ib = vkey(b)
    n = max(len(ca), len(cb))
    ca, cb = ca + [0] * (n - len(ca)), cb + [0] * (n - len(cb))
    if ca != cb:
        return -1 if ca < cb else 1
    if ia != ib:
        return -1 if ia else 1  # beta/rc je pred plnou verziou
    if pa != pb:
        return -1 if pa < pb else 1
    return 0


def head_toml(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True)
    return tomllib.loads(r.stdout) if r.returncode == 0 else None


out = subprocess.run(
    ["git", "-c", "core.quotepath=false", "diff", "--name-only", "-z", "HEAD",
     "--", "mods", "resourcepacks", "shaderpacks"],
    capture_output=True, text=True, check=True).stdout
pairs = []
for path in filter(None, out.split("\0")):
    if not path.endswith(".pw.toml") or not Path(path).exists():
        continue
    old = head_toml(path)
    if not old:
        continue
    new = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    om = old.get("update", {}).get("modrinth", {})
    nm = new.get("update", {}).get("modrinth", {})
    if om.get("version") and nm.get("version") and om["version"] != nm["version"]:
        pairs.append((path, new.get("name", path), om["version"], nm["version"]))

info = {}
if pairs:
    ids = sorted({p[2] for p in pairs} | {p[3] for p in pairs})
    q = urllib.parse.quote(json.dumps(ids))
    req = urllib.request.Request(f"https://api.modrinth.com/v2/versions?ids={q}", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        info = {v["id"]: v["version_number"] for v in json.load(r)}

skipped, hints = [], []
for path, name, old_id, new_id in pairs:
    ov, nv = info.get(old_id, ""), info.get(new_id, "")
    co, cn = vkey(ov)[0], vkey(nv)[0]
    if not co or not cn:
        continue
    if compare(nv, ov) < 0:
        subprocess.run(["git", "checkout", "HEAD", "--", path], check=True)
        skipped.append(f"- ⏸️ **{name}**: ponúkaná verzia `{nv}` je staršia ako súčasná `{ov}`, preskočené")
    elif cn[0] != co[0]:
        hints.append(f"- ⚠️ **{name}**: `{ov}` → `{nv}` (veľká zmena verzie, vyskúšaj hru!)")

text = ""
if skipped:
    text += "### Preskočené (staršia verzia)\n" + "\n".join(skipped) + "\n"
if hints:
    text += "### Pozor na tieto\n" + "\n".join(hints) + "\n"
if text:
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(text)
