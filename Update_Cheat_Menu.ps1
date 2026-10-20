param(
    [string]$targetPath = ""
)

# Automated Synchronization Script for Ren'Py Cheat Menu
$Host.UI.RawUI.WindowTitle = "SYNC REN'PY CHEAT MENU"
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "           REN'PY CHEAT MENU AUTO-SYNC & UPDATE TOOL" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$masterFile = Join-Path $PSScriptRoot "cheat_menu.rpy"

if (-not (Test-Path $masterFile)) {
    Write-Host "[ERROR] Master file not found: $masterFile" -ForegroundColor Red
    pause
    exit 1
}

$targetRoot = "G:\TeraBoxDownload\Ren'Py"
if ($targetPath -ne "" -and (Test-Path $targetPath)) {
    $targetRoot = $targetPath
    Write-Host "[*] Mode: Direct Drag-and-Drop Game Directory!" -ForegroundColor Magenta
}

Write-Host "[*] Master File: $masterFile" -ForegroundColor Green
Write-Host "[*] Scan Directory: $targetRoot" -ForegroundColor Green
Write-Host "Scanning and synchronizing to game directories..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray

$masterConn = Join-Path $PSScriptRoot "00_cheat_connect.rpy"
if (-not (Test-Path $masterConn)) {
    $masterConn = Join-Path $PSScriptRoot "cheat_connect.rpy"
}
$masterFont = Join-Path $PSScriptRoot "font.ttf"

$count = 0

# If user dragged-and-dropped the game/ folder directly
if ((Split-Path $targetRoot -Leaf) -ieq "game") {
    $destFile = Join-Path $targetRoot "cheat_menu.rpy"
    $destRpyc = Join-Path $targetRoot "cheat_menu.rpyc"
    Copy-Item -Path $masterFile -Destination $destFile -Force
    if (Test-Path $destRpyc) { Remove-Item -Path $destRpyc -Force -ErrorAction SilentlyContinue }

    if (Test-Path $masterConn) {
        $destConn = Join-Path $targetRoot "00_cheat_connect.rpy"
        $destConnRpyc = Join-Path $targetRoot "00_cheat_connect.rpyc"
        Copy-Item -Path $masterConn -Destination $destConn -Force
        if (Test-Path $destConnRpyc) { Remove-Item -Path $destConnRpyc -Force -ErrorAction SilentlyContinue }
    }

    if (Test-Path $masterFont) {
        $destFont = Join-Path $targetRoot "font.ttf"
        Copy-Item -Path $masterFont -Destination $destFont -Force
        Write-Host " [OK] Directly updated font: $destFont" -ForegroundColor Green
    }

    Write-Host " [OK] Directly updated: $destFile" -ForegroundColor Green
    $count = 1
} else {
    # Scan all child game/ directories (limit depth for lightning speed)
    $gameDirs = Get-ChildItem -Path $targetRoot -Directory -Recurse -Depth 3 -Filter "game" -ErrorAction SilentlyContinue
    foreach ($gdir in $gameDirs) {
        $destFile = Join-Path $gdir.FullName "cheat_menu.rpy"
        $destRpyc = Join-Path $gdir.FullName "cheat_menu.rpyc"
        try {
            Copy-Item -Path $masterFile -Destination $destFile -Force
            if (Test-Path $destRpyc) {
                Remove-Item -Path $destRpyc -Force -ErrorAction SilentlyContinue
            }

            if (Test-Path $masterConn) {
                $destConn = Join-Path $gdir.FullName "00_cheat_connect.rpy"
                $destConnRpyc = Join-Path $gdir.FullName "00_cheat_connect.rpyc"
                Copy-Item -Path $masterConn -Destination $destConn -Force
                if (Test-Path $destConnRpyc) { Remove-Item -Path $destConnRpyc -Force -ErrorAction SilentlyContinue }
            }

            if (Test-Path $masterFont) {
                $destFont = Join-Path $gdir.FullName "font.ttf"
                Copy-Item -Path $masterFont -Destination $destFont -Force
            }

            $rel = $gdir.FullName.Replace($targetRoot, "").TrimStart("\/")
            Write-Host " [OK] Updated: $rel\cheat_menu.rpy (with font.ttf)" -ForegroundColor Green
            $count++
        } catch {
            Write-Host " [SKIP] Error copying to: $($gdir.FullName)" -ForegroundColor Red
        }
    }
}

Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host " [DONE] Successfully synchronized Cheat Menu to $count game folder(s)!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Note: Compatible with all Ren'Py versions (Ren'Py 6, 7, 8.x, 9.x+)." -ForegroundColor Cyan
Write-Host ""
