"""Overi zmenene resource packy (resourcepacks/*.pw.toml oproti poslednemu commitu),
ci ich Minecraft 1.21.1 (pack_format 34) naozaj nacita. Modrinth ma pri resource
packoch casto zle oznacene verzie. Ked nova verzia nefunguje, pouzije sa najnovsia
fungujuca; ked ziadna, ostane povodna (novy pack sa odstrani a skript skonci chybou).
"""
import io
import json
import os
import subprocess
import sys
import tomllib
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

FORMAT = 34  # resource pack format pre MC 1.21.1
MC = "1.21.1"
UA = {"User-Agent": "Spekac007/create-aestro-pack (GitHub Actions)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def compatible_url(url):
    """Vrati (True/False/None, popis); None = neda sa zistit."""
    try:
        data = get(url)
    except Exception as e:
        return None, f"nedá sa stiahnuť ({e})"
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            meta = json.loads(z.read("pack.mcmeta").decode("utf-8-sig"))
    except Exception as e:
        return None, f"nedá sa prečítať pack.mcmeta ({e})"
    pk = meta.get("pack", {})
    pf = pk.get("pack_format")
    if isinstance(pf, bool) or not isinstance(pf, (int, float)):
        return False, "chýba pack_format, pack je len pre novší Minecraft"
    sf = pk.get("supported_formats")
    if sf is None:
        return int(pf) == FORMAT, f"pack_format {pf}"
    if isinstance(sf, (int, float)):
        lo = hi = sf
    elif isinstance(sf, list) and len(sf) == 2:
        lo, hi = sf
    elif isinstance(sf, dict):
        lo, hi = sf.get("min_inclusive"), sf.get("max_inclusive")
    else:
        return None, f"neznámy supported_formats {sf!r}"
    try:
        return lo <= FORMAT <= hi, f"formáty {lo}–{hi}"
    except TypeError:
        return None, f"neznámy supported_formats {sf!r}"


def changed_files():
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "status", "--porcelain", "-z",
         "--untracked-files=all", "--", "resourcepacks"],
        capture_output=True, text=True, check=True).stdout
    res = []
    for entry in out.split("\0"):
        if len(entry) < 4:
            continue
        st, path = entry[:2], entry[3:]
        if path.endswith(".pw.toml") and Path(path).exists():
            res.append((path, st == "??" or "A" in st))
    return res


def head_toml(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True)
    return tomllib.loads(r.stdout) if r.returncode == 0 else None


summary = []
failed = False
for path, is_new in changed_files():
    t = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    name = t.get("name", path)
    url = t.get("download", {}).get("url")
    mr = t.get("update", {}).get("modrinth")
    if not url:
        summary.append(f"- ⚠️ **{name}**: nedá sa overiť (nie je z Modrinthu)")
        continue
    ok, why = compatible_url(url)
    if ok:
        summary.append(f"- ✅ **{name}**: `{t['filename']}` ({why})")
        continue
    if ok is None:
        summary.append(f"- ⚠️ **{name}**: {why}, nechávam tak")
        continue

    # Nova verzia nefunguje: najdi najnovsiu fungujucu (Modrinth vracia od najnovsej)
    head = None if is_new else head_toml(path)
    head_ver = (head or {}).get("update", {}).get("modrinth", {}).get("version")
    choice = None
    if mr:
        q = urllib.parse.quote(json.dumps([MC]))
        versions = json.loads(get(f"https://api.modrinth.com/v2/project/{mr['mod-id']}/version?game_versions={q}"))
        for v in versions:
            if v["id"] == mr.get("version"):
                continue
            if v["id"] == head_ver:
                choice = "head"
                break
            f = next((x for x in v["files"] if x.get("primary")), (v["files"] or [None])[0])
            if f and compatible_url(f["url"])[0]:
                choice = v
                break

    if choice == "head" or (choice is None and not is_new):
        subprocess.run(["git", "checkout", "HEAD", "--", path], check=True)
        summary.append(f"- ⏸️ **{name}**: nová verzia `{t['filename']}` nefunguje na 1.21.1 ({why}), ostáva pôvodná")
    elif choice:
        Path(path).unlink()
        subprocess.run(["packwiz", "-y", "modrinth", "add", "--project-id", mr["mod-id"],
                        "--version-id", choice["id"]], check=True)
        summary.append(f"- ↩️ **{name}**: najnovšia verzia nefunguje na 1.21.1 ({why}), "
                       f"použitá verzia `{choice['version_number']}`")
    else:
        Path(path).unlink()
        failed = True
        summary.append(f"- ❌ **{name}**: žiadna verzia nefunguje na Minecraft 1.21.1, pack sa nepridal")

if summary:
    text = "### Resource packy (kontrola pre MC 1.21.1)\n" + "\n".join(summary) + "\n"
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(text)
if failed:
    print("::error::Resource pack nefunguje na Minecraft 1.21.1, nič sa neuložilo.")
    sys.exit(1)
