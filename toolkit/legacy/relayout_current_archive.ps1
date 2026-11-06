# Shorten current archive directory names, using native PowerShell moves only.
$ErrorActionPreference = 'Stop'
$archiveRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../01_Compute_Chips/01_NVIDIA/reference_metrial')).Path
$expectedRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../01_Compute_Chips/01_NVIDIA/reference_metrial'))
if ($archiveRoot -ne $expectedRoot) { throw 'Unexpected archive root' }
if (Test-Path -LiteralPath (Join-Path $archiveRoot '../.reference_download.lock')) { throw 'Downloader is still active' }
$layoutMoves = @()
foreach ($categoryName in @('webpages','documents','data')) {
    $categoryPath = Join-Path $archiveRoot $categoryName
    if (-not (Test-Path -LiteralPath $categoryPath)) { continue }
    foreach ($directoryItem in Get-ChildItem -LiteralPath $categoryPath -Directory) {
        if ($directoryItem.Attributes.HasFlag([IO.FileAttributes]::ReparsePoint)) { throw 'Reparse point rejected' }
        if ($directoryItem.Name -notmatch '^(.*)--([a-f0-9]{16})$') { throw 'Unexpected material directory name' }
        $labelPart = $Matches[1] -creplace '^NVIDIA_', ''
        $hashPart = $Matches[2]
        $nameBudget = [Math]::Min(32,200-$categoryPath.Length-19)
        if ($nameBudget -lt 1) { throw 'Project path too long' }
        if ($labelPart.Length -gt $nameBudget) { $labelPart = $labelPart.Substring(0,$nameBudget) }
        $destinationPath = [IO.Path]::GetFullPath((Join-Path $categoryPath ($labelPart + '--' + $hashPart)))
        $sourcePath = $directoryItem.FullName
        if ($sourcePath -eq $destinationPath) { continue }
        if (-not $sourcePath.StartsWith($archiveRoot + '\',[StringComparison]::OrdinalIgnoreCase) -or -not $destinationPath.StartsWith($archiveRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Move outside archive rejected' }
        if (Test-Path -LiteralPath $destinationPath) { throw 'Destination already exists' }
        Move-Item -LiteralPath $sourcePath -Destination $destinationPath
        $layoutMoves += @{from=$sourcePath;to=$destinationPath}
    }
}
ConvertTo-Json -InputObject @($layoutMoves) -Depth 4 | Set-Content -LiteralPath (Join-Path $archiveRoot '_registry/layout_moves.json') -Encoding utf8
Write-Output ('Shortened directories: ' + $layoutMoves.Count)
