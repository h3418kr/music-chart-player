@echo off
chcp 65001 >nul
echo =============================================
echo   멜론 차트 100 플레이어 - 설치 및 실행
echo =============================================
echo.

:: Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python 이 설치되어 있지 않습니다.
    echo   https://www.python.org 에서 Python 3.10 이상 설치 후 재시도하세요.
    pause
    exit /b 1
)

:: VLC 확인
if not exist "C:\Program Files\VideoLAN\VLC\vlc.exe" (
    if not exist "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" (
        echo [경고] VLC Media Player 가 감지되지 않았습니다.
        echo   https://www.videolan.org 에서 무료로 설치하세요.
        echo   설치 후 이 파일을 다시 실행하세요.
        pause
        exit /b 1
    )
)

:: 패키지 설치
echo [1/2] 패키지 설치 중...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [오류] 패키지 설치 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)

echo [2/2] 앱 실행 중...
echo.
python melon_player.py

pause
