# Creates deploy.zip for manual upload to Hugging Face Space (dragonguide)
$root = $PSScriptRoot
$zip = Join-Path $root "deploy.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }

$items = @(
    "main.py", "brain.py", "config.py", "ui_theme.py", "ingest.py",
    "download_docs.py", "deploy_hf.py", "requirements.txt", "packages.txt",
    "README.md", "DEPLOY.md", ".gitignore",
    ".streamlit", "data", "vectorstore"
)

$staging = Join-Path $env:TEMP "dragonguide-deploy"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $staging $item) -Recurse -Force
    }
}

$hfReadme = @"
---
title: DragonGuide
emoji: 🐉
colorFrom: '#07294D'
colorTo: '#FFC600'
sdk: streamlit
sdk_version: 1.45.1
app_file: main.py
pinned: true
---

# DragonGuide — Drexel University Academic AI

Set Space secret: **OPENAI_API_KEY**
"@

Set-Content -Path (Join-Path $staging "README.md") -Value $hfReadme -Encoding UTF8
Compress-Archive -Path "$staging\*" -DestinationPath $zip -Force
Remove-Item $staging -Recurse -Force
Write-Host "Created: $zip"
