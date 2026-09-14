param(
  [Parameter(Mandatory=$true)]
  [string]$UpstreamPath
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $UpstreamPath).Path
foreach ($rel in @('src\index.html','reference\renderer\index.html')) {
  $file = Join-Path $root $rel
  $bak = "$file.zhcn.bak"
  if (Test-Path $bak) {
    Copy-Item $bak $file -Force
    Remove-Item $bak -Force
    Write-Host "[OK] Restored $rel" -ForegroundColor Green
  }
}
foreach ($rel in @('src\i18n-zh-cn.js','reference\renderer\i18n-zh-cn.js')) {
  $file = Join-Path $root $rel
  if (Test-Path $file) { Remove-Item $file -Force }
}
