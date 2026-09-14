param(
  [Parameter(Mandatory=$true)]
  [string]$UpstreamPath
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $UpstreamPath).Path
$index = Join-Path $root 'src\index.html'
$targetJs = Join-Path $root 'src\i18n-zh-cn.js'
$sourceJs = Join-Path $PSScriptRoot '..\src\i18n-zh-cn.js'
$marker = '<!-- WAN2GP-ZHCN-PATCH -->'
$scriptTag = "  <!-- WAN2GP-ZHCN-PATCH -->`r`n  <script src=`"i18n-zh-cn.js`" defer></script>"

if (-not (Test-Path $index)) { throw "Not a Wan2GP Desktop Tauri source tree: missing $index" }
if (-not (Test-Path $sourceJs)) { throw "Patch payload missing: $sourceJs" }

Copy-Item $sourceJs $targetJs -Force
$html = Get-Content $index -Raw -Encoding UTF8

if ($html -notmatch [regex]::Escape($marker)) {
  $backup = "$index.zhcn.bak"
  if (-not (Test-Path $backup)) { Copy-Item $index $backup }
  $needle = '<script src="app.js" defer></script>'
  if ($html.Contains($needle)) {
    $html = $html.Replace($needle, $needle + "`r`n" + $scriptTag)
  } elseif ($html.Contains('</body>')) {
    $html = $html.Replace('</body>', $scriptTag + "`r`n</body>")
  } else {
    throw 'Could not find an injection point in src/index.html'
  }
  Set-Content $index $html -Encoding UTF8
  Write-Host '[OK] Injected Simplified Chinese bilingual UI layer.' -ForegroundColor Green
} else {
  Write-Host '[OK] Patch marker already present; refreshed i18n-zh-cn.js only.' -ForegroundColor Green
}

$refIndex = Join-Path $root 'reference\renderer\index.html'
if (Test-Path $refIndex) {
  $refJs = Join-Path $root 'reference\renderer\i18n-zh-cn.js'
  Copy-Item $sourceJs $refJs -Force
  $refHtml = Get-Content $refIndex -Raw -Encoding UTF8
  if ($refHtml -notmatch [regex]::Escape($marker)) {
    $refBackup = "$refIndex.zhcn.bak"
    if (-not (Test-Path $refBackup)) { Copy-Item $refIndex $refBackup }
    $refNeedle = '<script src="app.js"></script>'
    if ($refHtml.Contains($refNeedle)) {
      $refInjection = $refNeedle + "`r`n  <!-- WAN2GP-ZHCN-PATCH -->`r`n  <script src=`"i18n-zh-cn.js`"></script>"
      $refHtml = $refHtml.Replace($refNeedle, $refInjection)
      Set-Content $refIndex $refHtml -Encoding UTF8
    }
  }
}

Write-Host ''
Write-Host 'Next: run scripts\build-windows.ps1 -UpstreamPath <path>' -ForegroundColor Cyan
