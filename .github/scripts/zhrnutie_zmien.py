"""Pripravi zmeny na commit a vypise, ktore mody/packy sa zmenili (stara -> nova verzia).
Pocet zmien zapise do GITHUB_OUTPUT ako "pocet"."""
import os
import subprocess
import tomllib
from pathlib import Path


def filename(text):
    return tomllib.loads(text).get("filename", "?")


def head_filename(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True)
    return filename(r.stdout) if r.returncode == 0 else "?"


subprocess.run(["git", "add", "-A"], check=True)
out = subprocess.run(
    ["git", "-c", "core.quotepath=false", "diff", "--cached", "--name-status", "-z",
     "--", "mods", "resourcepacks", "shaderpacks"],
    capture_output=True, text=True, check=True).stdout
parts = out.split("\0")
lines = []
i = 0
while i + 1 < len(parts):
    st, path = parts[i], parts[i + 1]
    i += 2
    if not path.endswith(".pw.toml"):
        continue
    if st == "M":
        lines.append(f"- `{head_filename(path)}` → `{filename(Path(path).read_text(encoding='utf-8'))}`")
    elif st == "A":
        lines.append(f"- ➕ `{filename(Path(path).read_text(encoding='utf-8'))}` (nové)")
    elif st == "D":
        lines.append(f"- ➖ `{head_filename(path)}`")

text = (f"### Aktualizácie ({len(lines)})\n" + "\n".join(lines) + "\n") if lines else "### Všetko je aktuálne\n"
print(text)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
        fh.write(text)
if os.environ.get("GITHUB_OUTPUT"):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
        fh.write(f"pocet={len(lines)}\n")
