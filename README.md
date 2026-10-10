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

## Pre kamošov s TLauncherom

1. V TLauncheri si cez **TL MODS** vytvor modpack `Create Aestro`: Minecraft 1.21.1, NeoForge (najnovšia 21.1.x). Módy doň nepridávaj.
2. TLauncher zavri, rozbaľ `Create-Aestro-TLAUNCHER.zip` (pošlem ti ho) a spusti `PRIPOJIT-TLAUNCHER.bat`.
3. Vyber číslo modpacku. Módy sa hneď stiahnu z packu.
4. Otvor TLauncher, vyber modpack a spusti hru. Odvtedy sa pack aktualizuje sám pri každom štarte.

Funguje to aj pre existujúci modpack so svetom (svety a nastavenia ostanú). Podrobnosti sú v `NAVOD-TLAUNCHER.txt` v zipe.

---

## Správa packu

Všetko sa robí v priečinku `Documents\create-aestro-pack`. Otvor ho v Prieskumníkovi, do adresného riadku napíš `cmd` a stlač Enter. Terminál sa otvorí rovno v správnom priečinku.

Packwiz je v `Documents\packwiz-tools\packwiz.exe`. Ak je tento priečinok v PATH, stačí písať `packwiz`. Inak treba písať celú cestu `%USERPROFILE%\Documents\packwiz-tools\packwiz.exe`. `update.bat` ho nájde v oboch prípadoch.

### Pridať mód (alebo resource pack)

1. Nájdi mód na [modrinth.com](https://modrinth.com). Jeho „slug" je posledná časť adresy, napr. `modrinth.com/mod/sodium` → `sodium`.
2. Pridaj ho:
   ```
   packwiz modrinth add sodium
   ```
   - Keď sa opýta na závislosti (dependencies), daj `Y`.
   - Packwiz sám vyberie verziu pre 1.21.1 + NeoForge. Ak taká neexistuje, povie to a nič nepridá.
   - Resource pack sa pridáva rovnako a sám sa uloží do `resourcepacks\`.
3. Ak mód na Modrinthe nie je, skús CurseForge (celá adresa módu):
   ```
   packwiz curseforge add https://www.curseforge.com/minecraft/mc-mods/NAZOV
   ```
4. Pošli zmenu kamošom:
   ```
   update.bat "Pridany mod Sodium"
   ```

### Odobrať mód

Názov je meno súboru v `mods\` bez `.pw.toml`, napr. `mods\sodium.pw.toml` → `sodium`:

```
packwiz remove sodium
update.bat "Odobraty Sodium"
```

### Aktualizovať módy

**Odporúčam robiť to cez GitHub:** Actions → **Aktualizovať módy** (pozri [Cez GitHub](#cez-github-bez-počítača-aj-z-mobilu)). Má poistky, ktoré `packwiz update` na PC nemá:

- **Nezníži verziu.** Packwiz berie verziu podľa dátumu zverejnenia, takže by napr. Rhino (potrebuje ho KubeJS) zmenil z 2101.2.8 na staršiu 2101.2.7.
- **Skontroluje resource packy na 1.21.1** a nefunkčnú novú verziu nevezme.

Na PC to ide takto, ale potom si pozorne pozri, čo sa zmenilo (`git diff`):

```
packwiz update sodium
packwiz update --all
update.bat "Update modov"
```

Nová verzia môže niečo rozbiť, takže hru potom vyskúšaj.

### Na čo si dať pozor

- **Po každej zmene si hru spusti** a skontroluj, či sa načíta. Ak padá, mód odober a znova spusti `update.bat`.
- **Nikdy nedávaj do packu `.jar` súbory ručne** (ani cez web GitHubu), vždy cez `packwiz ... add` alebo Actions → **Pridať mód**.
- **Resource packy Better 3D Beds a Os' Colorful Grasses sú pripnuté** (`packwiz pin`) na verzie, ktoré fungujú na 1.21.1. Neodopínaj ich. Modrinth pri nich tvrdí, že novšie verzie sú kompatibilné, ale nie sú.
- **Modrinth niekedy uvádza zlé verzie** aj pri resource packoch. Ak sa pack v hre nenačíta, pozri v jeho zipe `pack.mcmeta`. Pre 1.21.1 musí podporovať `pack_format` 34.

### Configy

Configy daj do `config\` v tomto priečinku (rovnaká štruktúra ako `minecraft\config` v inštancii) a spusti `update.bat "Configy"`.

Všetky súbory v `config\` majú v `index.toml` príznak `preserve = true`. Pridáva ho `update.bat` cez `preserve-configs.ps1`. Kamoš dostane config z packu len vtedy, keď ho ešte nemá, takže sa mu neprepíšu vlastné nastavenia.

Ak chceš nejaký config kamošom **vynútiť** (aj tým, čo ho už majú), pridaj jeho cestu do zoznamu `$vynimky` na začiatku `preserve-configs.ps1` (napr. `'config/create-client.toml'`) a spusti `update.bat`. KubeJS skripty `preserve` nemajú, tie sa aktualizujú vždy.

`config\sounds\chat.json` (je v ňom meno hráča) a `kubejs\config\web_server.json` (súkromný token) sa zámerne nenahrávajú. Sú v `.gitignore` aj `.packwizignore`.

### Ako vyskúšať zmeny pred pushnutím

```
packwiz serve
```

Potom v testovacej inštancii v Prisme zmeň Pre-launch command na `http://localhost:8080/pack.toml`.

### Čo robí update.bat

`packwiz refresh` → `preserve-configs.ps1` → `packwiz refresh` → `git add -A` → `git commit -m "<správa>"` → `git push`. Ak push neprejde, lebo niekto iný medzitým pushol, sám zmeny spojí (`git pull --rebase -X theirs`), prepočíta index a pushne znova. GitHub Pages sa obnoví do 1–2 minút a kamoši dostanú zmeny pri ďalšom spustení hry.

---

## Cez GitHub, bez počítača (aj z mobilu)

Na stránke repa klikni na **Actions**, vľavo vyber akciu, vpravo **Run workflow**, vyplň políčka a znova **Run workflow**. Za 1–2 minúty je zmena v packu a kamoši ju dostanú pri ďalšom spustení hry.

- **Pridať mód**: do políčka napíš slug alebo odkaz (`sodium` alebo `https://modrinth.com/mod/sodium`) a vyber Modrinth alebo CurseForge. Závislosti sa pridajú samy. Pri resource packu overí, že naozaj funguje na 1.21.1. Ak najnovšia verzia nefunguje, vezme najnovšiu fungujúcu.
- **Odobrať mód**: napíš názov, teda meno súboru `.pw.toml` bez prípony (napr. `sodium`). Ak ho napíšeš zle, beh zlyhá a v logu je zoznam všetkých názvov.
- **Aktualizovať módy**: políčko nechaj prázdne pre všetky módy, alebo napíš názov jedného. **Najprv zaškrtni „Len ukázať"**: beh nič neuloží, len v súhrne behu (klikni na beh) ukáže, čo by sa aktualizovalo. Potom ho spusti znova bez zaškrtnutia.
  - Pripnuté súbory (`packwiz pin`) sa preskočia.
  - Ponúkanú staršiu verziu a nefunkčný resource pack preskočí sám a napíše to do súhrnu.
  - Pri veľkých skokoch verzie (napr. 2.x → 3.x) dá do súhrnu „Pozor na tieto". Tie po uložení určite vyskúšaj v hre.
- **Obnoviť index**: beží sám po každom pushi. Keď cez web upravíš napr. config, index sa prepočíta sám a zmenu dostanú aj hráči.

Zelená fajka znamená hotovo, červený krížik chybu (klikni na beh a pozri log). Ak by niekto cez web nahral do `mods\` alebo `resourcepacks\` priamo `.jar`/`.zip`, **Obnoviť index** zlyhá a upozorní na to. Surové súbory hráčom nepôjdu, treba ich zmazať a mód pridať cez **Pridať mód**.

Aj po pridaní cez GitHub si hru vyskúšaj. Ak potom robíš zmeny aj na PC, najprv daj `git pull`. Ak zabudneš, `update.bat` to spojí sám.

---

## Keď pack spravuje niekto iný (zástup)

Najjednoduchšie: majiteľ ho pridá ako collaboratora (bod 1) a kamarát potom používa tlačidlá z časti [Cez GitHub](#cez-github-bez-počítača-aj-z-mobilu). Nič si nemusí inštalovať. Body 2 a 3 sú len pre prácu na PC.

### 1. Majiteľ repa povolí prístup (raz)

Na GitHube: tento repo → **Settings** → **Collaborators** → **Add people** → zadaj GitHub meno kamaráta. Kamarát pozvánku prijme (príde mu e-mailom alebo ju uvidí na GitHube).

### 2. Kamarát si pripraví počítač (raz)

1. Nainštaluje Git:
   ```
   winget install --id Git.Git -e
   ```
2. Stiahne packwiz z <https://nightly.link/packwiz/packwiz/workflows/go/main> (súbor „Windows 64-bit.zip"). `packwiz.exe` rozbalí presne do `C:\Users\<jeho meno>\Documents\packwiz-tools\`, tam ho `update.bat` nájde sám.
3. V **novom** termináli si nastaví meno pre git:
   ```
   git config --global user.name "JehoMeno"
   git config --global user.email "jeho@email.sk"
   ```
4. V priečinku `Documents` si stiahne pack:
   ```
   git clone https://github.com/Spekac007/create-aestro-pack.git
   ```
   Vznikne mu `Documents\create-aestro-pack`, rovnaký ako má majiteľ.

### 3. Pridávanie módov

1. **Pred každou prácou** si stiahne najnovší stav, aby neprepísal zmeny ostatných:
   ```
   git pull
   ```
2. Potom presne podľa časti [Správa packu](#správa-packu) vyššie: `packwiz modrinth add ...` a `update.bat "sprava"`.
   - Bez packwizu v PATH píše ručné príkazy s celou cestou, napr. `%USERPROFILE%\Documents\packwiz-tools\packwiz.exe modrinth add sodium`.
   - Pri prvom `update.bat` sa mu otvorí prehliadač s prihlásením na GitHub. Prihlási sa raz a potom už nie.

### Keď je správcov viac

- Pred prácou vždy `git pull` a ideálne naraz robí zmeny len jeden.
- Ak predsa niekto pushol medzitým, `update.bat` to vyrieši sám. Napíše „Push nepresiel ... Spajam ich s tvojimi", stiahne cudzie zmeny, pri konflikte nechá tie tvoje, prepočíta index a pushne znova.
- Ak napíše `CHYBA: zmeny sa nepodarilo spojit automaticky`, spusti `git rebase --abort` a ozvi sa majiteľovi packu. Tvoje zmeny ostanú v lokálnom commite, nič sa nestratí.
