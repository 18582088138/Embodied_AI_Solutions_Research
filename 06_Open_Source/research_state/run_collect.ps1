param([string]$AdditionalManifest)
$ErrorActionPreference = 'Stop'
$researchPacUrl = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings').AutoConfigURL
if ($researchPacUrl) {
    $researchPacResponse = Invoke-WebRequest -Uri $researchPacUrl -TimeoutSec 15
    $researchPacText = if ($researchPacResponse.Content -is [byte[]]) { [Text.Encoding]::UTF8.GetString($researchPacResponse.Content) } else { [string]$researchPacResponse.Content }
    $researchProxyMatch = [regex]::Match($researchPacText,'return "PROXY ([a-zA-Z0-9.:-]+)";\s*\}\s*$')
    if ($researchProxyMatch.Success) { $env:REFERENCE_DOWNLOAD_PROXY = 'http://' + $researchProxyMatch.Groups[1].Value }
}
# Read user connection settings at runtime; never persist proxy coordinates.
if ($AdditionalManifest) { python -u (Join-Path $PSScriptRoot 'collect.py') $AdditionalManifest }
else { python -u (Join-Path $PSScriptRoot 'collect.py') }
exit $LASTEXITCODE
