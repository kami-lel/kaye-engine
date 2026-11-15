# install.ps1: put the Claude Code prompt structure into %USERPROFILE%\.claude
# and enable its plugins in VS Code. Follows docs/installer-algorithm-doc.md
# (Claude VS Code Plugin); takes no argument and reads no setting.

$ErrorActionPreference = 'Stop'

$Payload = Join-Path $PSScriptRoot 'payload'
$Claude = [System.IO.Path]::GetFullPath((Join-Path $env:USERPROFILE '.claude'))
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Fail([string]$Message) {
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

function Read-Json([string]$Path) {
    try {
        $text = [System.IO.File]::ReadAllText($Path, $Utf8)
        $value = ConvertFrom-Json -InputObject $text
    } catch {
        Fail "$Path is not valid JSON: $($_.Exception.Message)"
    }
    return $value
}

function Get-RelativeFiles([string]$Root) {
    $full = [System.IO.Path]::GetFullPath($Root).TrimEnd('\')
    return @(Get-ChildItem -LiteralPath $Root -Recurse -File -Force |
        ForEach-Object { $_.FullName.Substring($full.Length + 1) } |
        Sort-Object)
}

function Test-SameTree([string]$A, [string]$B) {
    $filesA = Get-RelativeFiles $A
    $filesB = Get-RelativeFiles $B
    if (($filesA -join "`n") -ne ($filesB -join "`n")) { return $false }
    foreach ($file in $filesA) {
        $hashA = (Get-FileHash -LiteralPath (Join-Path $A $file) -Algorithm SHA256).Hash
        $hashB = (Get-FileHash -LiteralPath (Join-Path $B $file) -Algorithm SHA256).Hash
        if ($hashA -ne $hashB) { return $false }
    }
    return $true
}

function Test-SameFile([string]$A, [string]$B) {
    return (Get-FileHash -LiteralPath $A -Algorithm SHA256).Hash -eq
        (Get-FileHash -LiteralPath $B -Algorithm SHA256).Hash
}

function New-Token { return [guid]::NewGuid().ToString('N').Substring(0, 8) }

try {
    # 0 locate
    $folders = @()
    if (Test-Path -LiteralPath $Payload -PathType Container) {
        $folders = @(Get-ChildItem -LiteralPath $Payload -Directory |
            Where-Object {
                Test-Path -LiteralPath (Join-Path $_.FullName '.claude-plugin\marketplace.json') -PathType Leaf
            })
    }
    if ($folders.Count -ne 1) {
        Fail 'expected exactly 1 marketplace folder in payload'
    }
    $M = $folders[0].Name  # marketplace folder name

    # 1 preflight: no write before every check passes
    $newPrompt = Join-Path $Payload 'CLAUDE.md'
    if (-not (Test-Path -LiteralPath $newPrompt -PathType Leaf)) {
        Fail 'payload has no CLAUDE.md'
    }
    $manifest = Read-Json (Join-Path $folders[0].FullName '.claude-plugin\marketplace.json')
    $nameProp = $manifest.PSObject.Properties['name']
    $pluginsProp = $manifest.PSObject.Properties['plugins']
    if ($null -eq $nameProp -or $nameProp.Value -isnot [string] -or $null -eq $pluginsProp) {
        Fail 'marketplace.json lacks a name or a plugins list'
    }
    $Name = $nameProp.Value  # marketplace name, keys settings.json
    if ($Name -ne $M) { Fail 'marketplace name differs from its folder name' }
    $Plugins = @()
    foreach ($plugin in @($pluginsProp.Value)) {
        $p = $null
        if ($plugin -is [pscustomobject]) { $p = $plugin.PSObject.Properties['name'] }
        if ($null -eq $p -or $p.Value -isnot [string] -or $p.Value -eq '') {
            Fail 'marketplace lists no plugin, or one has no name'
        }
        $Plugins += $p.Value
    }
    if ($Plugins.Count -eq 0) { Fail 'marketplace lists no plugin, or one has no name' }

    $settingsPath = Join-Path $Claude 'settings.json'
    if (Test-Path -LiteralPath $settingsPath -PathType Leaf) {
        $settings = Read-Json $settingsPath
    } else {
        $settings = [pscustomobject]@{}
    }
    $badType = $settings -isnot [pscustomobject]
    if (-not $badType) {
        foreach ($key in @('extraKnownMarketplaces', 'enabledPlugins')) {
            $prop = $settings.PSObject.Properties[$key]
            if ($null -ne $prop -and $prop.Value -isnot [pscustomobject]) { $badType = $true }
        }
    }
    if ($badType) { Fail 'settings.json has a key of the wrong type' }

    if (-not (Test-Path -LiteralPath $Claude -PathType Container)) {
        New-Item -ItemType Directory -Path $Claude | Out-Null
    }

    # 2 CLAUDE.md
    $oldPrompt = Join-Path $Claude 'CLAUDE.md'
    if (-not (Test-Path -LiteralPath $oldPrompt -PathType Leaf)) {
        Copy-Item -LiteralPath $newPrompt -Destination $oldPrompt
        Write-Host 'CLAUDE.md: created'
    } elseif (-not (Test-SameFile $oldPrompt $newPrompt)) {
        $stamp = Get-Date -Format 'yyyyMMddHHmmss'
        $bak = Join-Path $Claude "CLAUDE.md.$stamp.bak"
        $count = 1
        while (Test-Path -LiteralPath $bak) {
            $count++
            $bak = Join-Path $Claude "CLAUDE.md.$stamp-$count.bak"
        }
        Copy-Item -LiteralPath $oldPrompt -Destination $bak
        $tmp = Join-Path $Claude "CLAUDE.md.tmp-$(New-Token)"
        Copy-Item -LiteralPath $newPrompt -Destination $tmp
        Move-Item -LiteralPath $tmp -Destination $oldPrompt -Force
        Write-Host "CLAUDE.md: replaced, backup $(Split-Path -Leaf $bak)"
    } else {
        Write-Host 'CLAUDE.md: unchanged'
    }

    # 3 marketplace swap
    $src = $folders[0].FullName
    $dest = Join-Path $Claude $M
    if ((Test-Path -LiteralPath $dest -PathType Container) -and (Test-SameTree $src $dest)) {
        Write-Host "$M/: unchanged"
    } else {
        $token = New-Token
        $tmp = Join-Path $Claude "$M.new-$token"
        $old = Join-Path $Claude "$M.old-$token"
        try {
            Copy-Item -LiteralPath $src -Destination $tmp -Recurse
            if (Test-Path -LiteralPath $dest) { Move-Item -LiteralPath $dest -Destination $old }
            try {
                Move-Item -LiteralPath $tmp -Destination $dest
            } catch {
                if (Test-Path -LiteralPath $old) { Move-Item -LiteralPath $old -Destination $dest }
                throw
            }
        } catch {
            if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
            Fail "could not replace marketplace folder: $($_.Exception.Message)"
        }
        if (Test-Path -LiteralPath $old) { Remove-Item -LiteralPath $old -Recurse -Force }
        Write-Host "$M/: replaced"
    }

    # 4 settings.json: add missing keys only, never change an existing one
    $entry = [pscustomobject]@{
        source = [pscustomobject]@{ source = 'directory'; path = $dest }
    }
    $added = @()
    if ($null -eq $settings.PSObject.Properties['extraKnownMarketplaces']) {
        Add-Member -InputObject $settings -NotePropertyName 'extraKnownMarketplaces' -NotePropertyValue ([pscustomobject]@{})
    }
    $known = $settings.extraKnownMarketplaces
    $existing = $known.PSObject.Properties[$Name]
    if ($null -eq $existing) {
        Add-Member -InputObject $known -NotePropertyName $Name -NotePropertyValue $entry
        $added += "marketplace $Name"
    } elseif ((ConvertTo-Json -InputObject $existing.Value -Compress -Depth 10) -ne (ConvertTo-Json -InputObject $entry -Compress -Depth 10)) {
        Write-Host "settings.json: kept existing marketplace $Name"
    }
    if ($null -eq $settings.PSObject.Properties['enabledPlugins']) {
        Add-Member -InputObject $settings -NotePropertyName 'enabledPlugins' -NotePropertyValue ([pscustomobject]@{})
    }
    $enabled = $settings.enabledPlugins
    foreach ($plugin in $Plugins) {
        $key = "$plugin@$Name"
        if ($null -eq $enabled.PSObject.Properties[$key]) {
            Add-Member -InputObject $enabled -NotePropertyName $key -NotePropertyValue $true
            $added += $key
        }
    }
    if ($added.Count -gt 0) {
        $text = (ConvertTo-Json -InputObject $settings -Depth 20) + "`n"
        $tmp = Join-Path $Claude "settings.json.tmp-$(New-Token)"
        [System.IO.File]::WriteAllText($tmp, $text, $Utf8)
        Move-Item -LiteralPath $tmp -Destination $settingsPath -Force
        Write-Host ('settings.json: added ' + ($added -join ', '))
    } else {
        Write-Host 'settings.json: unchanged'
    }

    # 5 done
    Write-Host 'restart VS Code'
} catch {
    Fail $_.Exception.Message
}
