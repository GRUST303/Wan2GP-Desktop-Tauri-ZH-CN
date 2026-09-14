param(
  [Parameter(Mandatory=$true)]
  [string]$UpstreamPath
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $UpstreamPath).Path
Push-Location $root
try {
  if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw 'npm/Node.js not found.' }
  if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) { throw 'Rust/cargo not found. Install Rustup first.' }
  Write-Host '[1/3] Installing JS build dependency...' -ForegroundColor Cyan
  npm ci
  Write-Host '[2/3] Validating localization JS...' -ForegroundColor Cyan
  node --check .\src\i18n-zh-cn.js
  Write-Host '[3/3] Building Tauri Windows packages...' -ForegroundColor Cyan
  npm run tauri build
  Write-Host ''
  Write-Host '[OK] Build complete. Check src-tauri\target\release\bundle\' -ForegroundColor Green
} finally {
  Pop-Location
}
