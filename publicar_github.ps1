# Crea en GitHub un repositorio NUEVO y PUBLICO; nunca sobrescribe uno existente.
# Ejecutar desde el directorio del proyecto o invocar con su ruta completa.
[CmdletBinding()]
param([string]$NombreRepositorio = 'laboratorio-matematica-fisica-ingenieria')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Requerir-Comando([string]$Nombre, [string]$Ayuda) {
    if (-not (Get-Command $Nombre -ErrorAction SilentlyContinue)) { throw "Falta $Nombre. $Ayuda" }
}
function Ejecutar([string]$Tarea, [scriptblock]$Accion) {
    & $Accion
    if ($LASTEXITCODE -ne 0) { throw "Fallo: $Tarea (codigo $LASTEXITCODE)" }
}
Requerir-Comando 'git' 'winget install -e --id Git.Git ; despues reabrir PowerShell.'
Requerir-Comando 'gh' 'winget install -e --id GitHub.cli ; despues reabrir PowerShell.'
if (-not (Test-Path -LiteralPath './README.md')) { throw 'No se encontro README.md en el proyecto.' }
if (Test-Path -LiteralPath './.git') { throw 'Ya existe .git en esta carpeta; se evita publicar o sobrescribir sin revisar.' }

& gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Iniciando sesion GitHub (se abrira el navegador)...' -ForegroundColor Cyan
    Ejecutar 'Autenticacion GitHub' { gh auth login --web --git-protocol https }
}
Ejecutar 'Configurar credenciales Git' { gh auth setup-git }
$Usuario = (& gh api user --jq .login).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Usuario)) { throw 'No se pudo leer el usuario GitHub.' }
$NombreCompleto = "$Usuario/$NombreRepositorio"

# Confirmar que el nombre este libre. Nunca hace push a un repo ya existente.
$Existe = (& gh repo view $NombreCompleto --json name --jq .name 2>$null)
if ($LASTEXITCODE -eq 0) { throw "Ya existe https://github.com/$NombreCompleto. No se modifico." }

Write-Host "PUBLICANDO NUEVO REPOSITORIO PUBLICO: https://github.com/$NombreCompleto" -ForegroundColor Yellow
Ejecutar 'git init' { git init -b main }
$NombreGit = (& git config --get user.name)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($NombreGit)) {
    Ejecutar 'Identidad git local' { git config --local user.name $Usuario }
}
$EmailGit = (& git config --get user.email)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($EmailGit)) {
    $IdGit = (& gh api user --jq .id).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo obtener el id de GitHub para el correo noreply.' }
    Ejecutar 'Correo git local' { git config --local user.email "$IdGit+$Usuario@users.noreply.github.com" }
}
Ejecutar 'Agregar archivos' { git add --all }
Ejecutar 'Primer commit' { git commit -m 'Initial commit: open science engineering learning lab' }
Ejecutar 'Crear y subir repo PUBLICO' {
    gh repo create $NombreCompleto --public --source=. --remote=origin --push `
      --description 'Laboratorio abierto de matematica, fisica e ingenieria: teoria, proyectos, pruebas y divulgacion'
}
Ejecutar 'Verificar publicacion' { gh repo view $NombreCompleto --json url --jq .url }
Write-Host "LISTO: https://github.com/$NombreCompleto" -ForegroundColor Green
