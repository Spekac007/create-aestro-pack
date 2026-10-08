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

Resource packy si zapni v hre: Options → Resource Packs.

## Pre kamošov, čo už majú svoju inštanciu (svet, nastavenia)

1. Stiahni si `Create-Aestro-PRIPOJENIE.zip` (pošlem ti ho) a rozbaľ ho.
2. Úplne zavri Prism Launcher a spusti `PRIPOJIT.bat`.
3. Vyber číslo svojej inštancie. Skript presunie `mods` do zálohy, pridá bootstrap a nastaví Pre-launch command.
4. Spusti inštanciu v Prisme, módy sa stiahnu z packu.

Svety, `options.txt`, JourneyMap a tvoje configy ostanú. Podrobnosti a ručný postup sú v `NAVOD.txt` v zipe.

---

## Pre mňa: správa packu

Všetko sa robí v tomto priečinku (`Documents\create-aestro-pack`). Otvor v ňom terminál (v Prieskumníkovi do adresného riadku napíš `cmd` a Enter).

Packwiz je v `Documents\packwiz-tools\packwiz.exe` a tento priečinok je v PATH, takže stačí písať `packwiz`. Na inom PC treba buď pridať priečinok do PATH, alebo písať celú cestu `%USERPROFILE%\Documents\packwiz-tools\packwiz.exe`.

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

Všetky súbory v `config\` majú v `index.toml` príznak `preserve = true` (pridáva ho `update.bat` cez `preserve-configs.ps1`). Kamoš dostane config z packu len vtedy, keď ho ešte nemá, takže sa mu neprepíšu vlastné nastavenia. Ak chceš nejaký config kamošom **vynútiť** (aj tým, čo ho už majú), pridaj jeho cestu do zoznamu `$vynimky` na začiatku `preserve-configs.ps1` (napr. `'config/create-client.toml'`) a spusti `update.bat`. KubeJS skripty `preserve` nemajú, tie sa aktualizujú vždy.

`config\sounds\chat.json` (je v ňom tvoje meno) a `kubejs\config\web_server.json` (súkromný token) sa zámerne nenahrávajú, sú v `.gitignore` aj `.packwizignore`.

### Ako vyskúšať zmeny pred pushnutím

```
packwiz serve
```

Potom v testovacej inštancii v Prisme zmeň Pre-launch command na `http://localhost:8080/pack.toml`.

### Čo robí update.bat

`packwiz refresh` → `preserve-configs.ps1` → `packwiz refresh` → `git add -A` → `git commit -m "<správa>"` → `git push`. GitHub Pages sa obnoví do 1–2 minút a kamoši dostanú zmeny pri ďalšom spustení hry.
