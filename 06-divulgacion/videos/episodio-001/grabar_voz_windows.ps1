# Crea un WAV por escena con una voz espanola de Windows, si esta instalada.
# Funciona en Windows PowerShell 5.1 con System.Speech; no usa servicios externos.
# Se recomienda grabar voz propia para la publicacion final.
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
Add-Type -AssemblyName System.Speech
$sintetizador = New-Object System.Speech.Synthesis.SpeechSynthesizer
$espanol = $sintetizador.GetInstalledVoices() | Where-Object {
    $_.Enabled -and $_.VoiceInfo.Culture.Name -match '^es(-|$)'
} | Select-Object -First 1
if (-not $espanol) {
    throw 'No se encontro ninguna voz espanola compatible con System.Speech. Instalala en Configuracion de voz de Windows o graba tu propia voz.'
}
$sintetizador.SelectVoice($espanol.VoiceInfo.Name)
$sintetizador.Rate = 1
$lineas = Get-Content -LiteralPath 'guion.md' -Encoding UTF8
$escenas = @($lineas | Where-Object { $_ -match '^\|\s*[1-8]\s*\|' })
if ($escenas.Count -ne 8) { throw 'El guion debe contener ocho escenas.' }
$dest = Join-Path $PSScriptRoot 'render\voz_windows'
New-Item -ItemType Directory -Path $dest -Force | Out-Null
for ($i = 0; $i -lt 8; $i++) {
    $partes = $escenas[$i].Split('|')
    $texto = $partes[3].Trim()
    $salida = Join-Path $dest ('voz_{0:d2}.wav' -f ($i + 1))
    $sintetizador.SetOutputToWaveFile($salida)
    $sintetizador.Speak($texto)
    $sintetizador.SetOutputToNull()
    Write-Host "Escena $($i+1): $salida"
}
$sintetizador.Dispose()
Write-Host 'Se generaron ocho WAV. Importalos a Kdenlive, sincronizando con el storyboard.' -ForegroundColor Green
