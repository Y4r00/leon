# Buduje/aktualizuje aplikację Android (Capacitor) z plików webowych.
# Użycie:  prawy klik -> Run with PowerShell   ALBO w terminalu:  .\build_android.ps1
# Wymaga: Node.js + Android Studio (z Android SDK).

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

Write-Host "==> Przygotowuję folder www (pliki aplikacji)..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path ".\www" | Out-Null
Copy-Item -Force ".\index.html"              ".\www\index.html"
Copy-Item -Force ".\manifest.json"           ".\www\manifest.json"
Copy-Item -Force ".\sw.js"                    ".\www\sw.js"
Copy-Item -Force ".\icon-192.png"            ".\www\icon-192.png"
Copy-Item -Force ".\icon-512.png"            ".\www\icon-512.png"
Copy-Item -Force ".\icon-512-maskable.png"   ".\www\icon-512-maskable.png"

if (-not (Test-Path ".\package.json")) {
  Write-Host "==> Pierwsza konfiguracja Capacitora..." -ForegroundColor Cyan
  npm init -y | Out-Null
  npm install @capacitor/core @capacitor/android @capacitor/local-notifications @capacitor/splash-screen
  npm install -D @capacitor/cli @capacitor/assets
  npx cap init "Dziennik Malucha" "pl.dziennikmalucha.app" --web-dir www
}

if (-not (Test-Path ".\android")) {
  Write-Host "==> Dodaję platformę Android..." -ForegroundColor Cyan
  npx cap add android
}

# --- Ikona aplikacji + splash (z @capacitor/assets) ---
Write-Host "==> Generuję ikonę aplikacji i splash screen..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path ".\assets" | Out-Null
Copy-Item -Force ".\icon-512.png" ".\assets\icon.png"
Copy-Item -Force ".\splash.png"   ".\assets\splash.png"
Copy-Item -Force ".\splash.png"   ".\assets\splash-dark.png"
try {
  npx @capacitor/assets generate --android --iconBackgroundColor "#070d1a" --splashBackgroundColor "#070d1a" --splashBackgroundColorDark "#070d1a"
} catch {
  Write-Host "   (pominięto auto-generację ikon — można zrobić ręcznie w Android Studio)" -ForegroundColor Yellow
}

# --- Ikona powiadomienia (biała sylwetka) do folderów drawable ---
Write-Host "==> Wgrywam ikonę powiadomienia (ic_stat_icon_config_sample)..." -ForegroundColor Cyan
$resBase = ".\android\app\src\main\res"
$map = @{
  "drawable-mdpi"    = ".\notif-24.png"
  "drawable-hdpi"    = ".\notif-36.png"
  "drawable-xhdpi"   = ".\notif-48.png"
  "drawable-xxhdpi"  = ".\notif-72.png"
  "drawable-xxxhdpi" = ".\notif-96.png"
}
foreach ($folder in $map.Keys) {
  $dir = Join-Path $resBase $folder
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  Copy-Item -Force $map[$folder] (Join-Path $dir "ic_stat_icon_config_sample.png")
}

Write-Host "==> Synchronizuję pliki z projektem Android..." -ForegroundColor Cyan
npx cap sync

Write-Host "==> Otwieram Android Studio. Tam: Build -> Build APK(s)." -ForegroundColor Green
npx cap open android
