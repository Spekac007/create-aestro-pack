# Oznaci configy v index.toml ako "preserve = true": packwiz-installer ich hracovi
# zapise len vtedy, ked ich este nema, takze mu neprepise jeho vlastne nastavenia.
# Ak chces, aby sa niektory config kamosom naozaj prepisal, pridaj ho do $vynimky.
# Spusta ho update.bat, rucne netreba.
$vynimky = @(
    # 'config/priklad.toml'
)

$idx = Join-Path $PSScriptRoot 'index.toml'
$text = [IO.File]::ReadAllText($idx)
$parts = [regex]::Split($text, '(?m)(?=^\[\[files\]\]\r?$)')
$zmeny = 0
$out = foreach ($p in $parts) {
    if ($p -match '(?m)^file = "(config/[^"]+)"') {
        $f = $Matches[1]
        $ma = $p -match '(?m)^preserve = true\r?$'
        if ($vynimky -contains $f) {
            if ($ma) { $p = $p -replace '(?m)^preserve = true\r?\n?', ''; $zmeny++ }
        } elseif (-not $ma) {
            $p = $p -replace '(?m)^(hash = "[^"]*")(\r?\n|$)', "`$1`npreserve = true`$2"; $zmeny++
        }
    }
    $p
}
if ($zmeny -gt 0) { [IO.File]::WriteAllText($idx, (-join $out), (New-Object Text.UTF8Encoding $false)) }
Write-Host "preserve-configs: $zmeny zmien"
