param(
    [string]$targetPath = ""
)

# Script Tu Dong Dong Bo Cheat Menu Sang Game Ren'Py
$Host.UI.RawUI.WindowTitle = "DONG BO CHEAT MENU REN'PY"
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          CONG CU TU DONG CAP NHAT CHEAT MENU CHO MOI GAME REN'PY" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$masterFile = Join-Path $PSScriptRoot "cheat_menu.rpy"

if (-not (Test-Path $masterFile)) {
    Write-Host "[LOI] Khong tim thay file Master: $masterFile" -ForegroundColor Red
    pause
    exit 1
}

$targetRoot = "G:\TeraBoxDownload\Ren'Py"
if ($targetPath -ne "" -and (Test-Path $targetPath)) {
    $targetRoot = $targetPath
    Write-Host "[*] Che do: Keo-Tha truc tiep thu muc game!" -ForegroundColor Magenta
}

Write-Host "[*] File Master: $masterFile" -ForegroundColor Green
Write-Host "[*] Thu muc quet: $targetRoot" -ForegroundColor Green
Write-Host "Dang quet va tu dong dong bo den cac game..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray

$masterConn = Join-Path $PSScriptRoot "00_cheat_connect.rpy"

$count = 0

# Neu nguoi dung keo tha dung thu muc game/
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

    Write-Host " [OK] Da cap nhat truc tiep: $destFile" -ForegroundColor Green
    $count = 1
} else {
    # Quet tat ca thu muc game con ben trong
    $gameDirs = Get-ChildItem -Path $targetRoot -Directory -Recurse -Filter "game" -ErrorAction SilentlyContinue
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

            $rel = $gdir.FullName.Replace($targetRoot, "").TrimStart("\/")
            Write-Host " [OK] Cap nhat: $rel\cheat_menu.rpy" -ForegroundColor Green
            $count++
        } catch {
            Write-Host " [BO QUA] Loi khi chep vao: $($gdir.FullName)" -ForegroundColor Red
        }
    }
}

Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host " [HOAN TAT] Da dong bo Cheat Menu moi nhat cho $count thu muc game!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ghi chu: Ho tro moi phien ban Ren'Py tu cu den moi nhat (Ren'Py 6, 7, 8.x, 9.x+)." -ForegroundColor Cyan
Write-Host ""
