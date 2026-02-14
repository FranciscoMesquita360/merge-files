# install.ps1
$repo = "FranciscoMesquita360/merge-files"
$binaryName = "merge-windows.exe"

Write-Host "🚀 Installing 'merge' command for Windows..." -ForegroundColor Cyan

# 1. Get URL
$api = "https://api.github.com/repos/$repo/releases/latest"
$url = (Invoke-RestMethod -Uri $api).assets | Where-Object { $_.name -eq $binaryName } | Select-Object -ExpandProperty browser_download_url

# 2. Setup install folder
$installPath = "$HOME\.merge-tool"
if (!(Test-Path $installPath)) { New-Item -ItemType Directory -Path $installPath }

# 3. Download and RENAME to merge.exe
Invoke-WebRequest -Uri $url -OutFile "$installPath\merge.exe"

# 4. Update PATH if needed
$path = [Environment]::GetEnvironmentVariable("Path", "User")
if ($path -notlike "*$installPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$path;$installPath", "User")
    Write-Host "⚠️ PATH updated. Please restart your terminal." -ForegroundColor Yellow
}

Write-Host "✅ Done! You can now use the command: merge" -ForegroundColor Green