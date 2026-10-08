# Create Aestro – modpack

Minecraft **1.21.1**, **NeoForge 21.1.250**, 143 módov. Pack sa kamošom aktualizuje sám pri každom spustení hry (packwiz + GitHub Pages).

Adresa packu: `https://spekac007.github.io/create-aestro-pack/pack.toml`

---

## Pre kamošov: inštalácia

1. Stiahni si `Create-Aestro.zip` (pošlem ti ho).
2. Prism Launcher → **Pridať inštanciu** (Add Instance) → **Importovať** (Import) → vyber zip → OK.
3. Spusti inštanciu (volá sa `Create-Aestro`). Pri prvom spustení sa stiahnu všetky módy (cca 700 MB), chvíľu to trvá.
4. Hotovo. Pri každom ďalšom spustení sa pack sám aktualizuje, nič neriešiš.

Ak pri spustení vyskočí okno `packwiz-installer-bootstrap` s chybou sťahovania (napr. `Connection reset`), je to len výpadok spojenia s GitHubom: daj OK a spusti hru znova.

Ak by sa niekedy objavilo okno, že treba niečo stiahnuť ručne, klikni na odkaz, stiahni súbor a daj ho tam, kam okno ukazuje.

---

## Pre mňa: správa packu

Všetko sa robí v tomto priečinku (`Documents\create-aestro-pack`). Otvor v ňom terminál (v Prieskumníkovi do adresného riadku napíš `cmd` a Enter).

Packwiz je v `Documents\packwiz-tools\packwiz.exe`. Ak nie je v PATH, píš namiesto `packwiz` celú cestu:
`%USERPROFILE%\Documents\packwiz-tools\packwiz.exe`

### Pridať mód

```
packwiz modrinth add sodium
packwiz modrinth add https://modrinth.com/mod/sodium
packwiz curseforge add https://www.curseforge.com/minecraft/mc-mods/jei
```

Keď sa opýta na závislosti (dependencies), daj `Y`. Potom:

```
update.bat "Pridany mod Sodium"
```

### Odobrať mód

Názov je meno súboru v `mods\` bez `.pw.toml` (napr. `mods\sodium.pw.toml` → `sodium`):

```
packwiz remove sodium
update.bat "Odobraty Sodium"
```

### Aktualizovať módy

```
packwiz update sodium
packwiz update --all
update.bat "Update modov"
```

`--all` aktualizuje všetko naraz. Pred tým, ako to pushneš, je dobré to vyskúšať, lebo nová verzia môže niečo rozbiť.

### Configy

Configy daj do `config\` v tomto priečinku (rovnaká štruktúra ako `minecraft\config` v inštancii) a spusti `update.bat "Configy"`.

### Ako vyskúšať zmeny pred pushnutím

```
packwiz serve
```

Potom v testovacej inštancii v Prisme zmeň Pre-launch command na `http://localhost:8080/pack.toml`.

### Čo robí update.bat

`packwiz refresh` → `git add -A` → `git commit -m "<správa>"` → `git push`. GitHub Pages sa obnoví do 1–2 minút a kamoši dostanú zmeny pri ďalšom spustení hry.
