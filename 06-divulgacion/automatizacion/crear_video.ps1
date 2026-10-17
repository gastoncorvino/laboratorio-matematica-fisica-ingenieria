param(
    [ValidateSet('001','003')][string]$Episodio = '001',
    [ValidateSet('es','en')][string]$Idioma = 'es',
    [ValidateSet('v2','v3')][string]$Modelo = 'v2',
    [switch]$Maqueta,
    [switch]$SoloValidar,
    [double]$Cfg = 0.25,
    [int]$Primeras = 0
)
$ErrorActionPreference = 'Stop'
$Carpeta = $PSScriptRoot
$Venv = Join-Path $env:LOCALAPPDATA 'LaboratorioVoz\.venv\Scripts\python.exe'
$Referencia = Join-Path $env:LOCALAPPDATA 'LaboratorioVoz\referencias\muestra_voz_personal.wav'
$Guion = Join-Path $Carpeta "guiones\episodio_${Episodio}_${Idioma}.json"
if ($Maqueta) { $Tipo = 'maqueta' } elseif ($Primeras -gt 0) { $Tipo = 'prueba' } else { $Tipo = 'final' }
$Salida = Join-Path $env:LOCALAPPDATA "LaboratorioVoz\videos\episodio_${Episodio}_${Idioma}_${Tipo}"
if (-not (Test-Path -LiteralPath $Venv)) { throw "Falta el entorno Python instalado: $Venv" }
if (-not (Test-Path -LiteralPath $Guion)) { throw "Falta el guion: $Guion" }
if (-not $Maqueta -and -not $SoloValidar -and -not (Test-Path -LiteralPath $Referencia)) {
    throw 'No existe la muestra original guardada de forma local.'
}
if (-not $SoloValidar -and -not (Get-Command 'ffmpeg' -ErrorAction SilentlyContinue)) {
    throw 'No se encontro ffmpeg en PATH.'
}
$parametros = @((Join-Path $Carpeta 'crear_video.py'), '--guion', $Guion, '--salida', $Salida, '--referencia', $Referencia, '--modelo', $Modelo, '--cfg', [string]::Format([System.Globalization.CultureInfo]::InvariantCulture, '{0}', $Cfg))
if ($Maqueta) { $parametros += '--maqueta' }
if ($Primeras -gt 0) { $parametros += @('--primeras', [string]$Primeras) }
if ($SoloValidar) { $parametros += '--validar' }
Write-Host "`nEPISODIO $Episodio / IDIOMA $Idioma / PRIVADO" -ForegroundColor Cyan
Write-Host "Voz artificial basada en referencia propia; referencia local, sin GitHub."
& $Venv @parametros
if ($LASTEXITCODE -ne 0) { throw "Fallo la generacion (codigo $LASTEXITCODE)" }
if (-not $SoloValidar) { Write-Host "`nArchivo(s) generados: $Salida" -ForegroundColor Green; Start-Process explorer.exe -ArgumentList ('"' + $Salida + '"') }
