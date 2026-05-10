# 🍈 멜론 차트 100 플레이어

멜론(Melon) 실시간 차트 TOP 100을 자동으로 가져와 YouTube 오디오로 순차 재생하는 데스크톱 플레이어입니다.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## ✨ 주요 기능

- 🎵 멜론 실시간 차트 TOP 100 자동 수집
- ▶️ 순차 자동 재생 (다음 곡으로 자연스럽게 전환)
- ⚡ 다음 곡 스트림 URL 미리 가져오기로 끊김 없는 재생
- 🎨 다크 테마 GUI (tkinter 기반)
- 💾 다운로드 없이 **스트리밍 방식** (디스크 공간 절약)
- 🔊 음량 조절, 진행 바 탐색, 이전/다음 곡 컨트롤

---

## 📦 설치 및 실행

### 사전 요구사항
- **Python 3.10 이상** — [python.org](https://www.python.org)
- **VLC Media Player** — [videolan.org](https://www.videolan.org/vlc/)

### 소스에서 실행
```powershell
pip install -r requirements.txt
python melon_player.py
```

### 실행 파일 빌드 (Windows)
```powershell
pip install pyinstaller
python -m PyInstaller melon_player.spec
# → dist/멜론차트100플레이어.exe 생성
```

---

## 🛠 사용 기술

| 영역 | 라이브러리 |
|------|------------|
| 차트 스크래핑 | `requests` + `beautifulsoup4` |
| YouTube 검색/스트림 추출 | `yt-dlp` |
| 오디오 재생 | `python-vlc` (VLC Media Player) |
| GUI | `tkinter` |

---

## ⚖️ 면책 조항 (Disclaimer)

본 프로그램은 **개인 학습 및 감상 목적**으로 제작된 비공식 도구입니다.

- 차트 데이터는 [melon.com](https://www.melon.com)에서, 오디오는 [youtube.com](https://www.youtube.com)에서 가져옵니다.
- **모든 음원의 저작권은 원저작자 및 권리자에게 있습니다.**
- 본 프로그램은 어떠한 음원도 다운로드하거나 저장하지 않으며, 스트리밍만 수행합니다.
- 본 프로그램은 Melon, YouTube, 또는 어떤 음반사와도 제휴 관계가 없습니다.
- **상업적 사용을 금지합니다.**

### 🚨 Takedown Policy

If you are a rights holder (Melon / Kakao, YouTube / Google, a record label, an artist, or their authorized representative) and you believe this project infringes upon your rights, please contact the maintainer.

**Upon receiving a legitimate takedown request, this project will be removed promptly.**

저작권자, 플랫폼 운영사(멜론/카카오, 유튜브/구글), 음반사, 아티스트 또는 그 대리인으로부터 정당한 삭제 요청이 있을 경우 **즉시 본 프로젝트를 비공개/삭제 처리**합니다.

📧 Contact: GitHub Issues 또는 저장소 관리자에게 직접 연락해 주세요.

---

## 📜 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)로 배포됩니다.

단, MIT 라이선스는 **본 소프트웨어 코드 자체**에만 적용됩니다.
스트리밍되는 음원, 멜론 차트 데이터 등 외부 콘텐츠의 저작권은 각 권리자에게 있습니다.

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube 콘텐츠 추출
- [VLC](https://www.videolan.org/) — 미디어 재생 엔진
- [Melon Chart](https://www.melon.com/chart/) — 차트 데이터 출처
