# 🎶 차트 100 플레이어

전 세계 6개 음원 차트의 실시간 TOP 100을 자동으로 가져와 YouTube 오디오로 순차 재생하는 데스크톱 플레이어입니다.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## 🎵 지원 차트

| 차트 | 출처 | 지역 |
|------|------|------|
| 🍈 **Melon** | melon.com | 🇰🇷 한국 |
| 🎵 **Genie** | genie.co.kr | 🇰🇷 한국 |
| 🐛 **Bugs** | music.bugs.co.kr | 🇰🇷 한국 |
| 📊 **Billboard Hot 100** | billboard.com | 🇺🇸 미국 |
| 🎧 **Spotify Global** | kworb.net | 🌎 글로벌 |
| ▶ **YouTube Top** | kworb.net | 🌎 글로벌 |

상단 드롭다운으로 차트를 자유롭게 전환할 수 있습니다.

---

## ✨ 주요 기능

- 🎵 6개 차트 TOP 100 자동 수집
- ▶️ 순차 자동 재생 (다음 곡으로 자연스럽게 전환)
- 🔀 셔플 재생 (랜덤 순서)
- 🔁 반복 재생 (전체 반복 / 한 곡 반복 / 끄기)
- ⚡ 다음 곡 스트림 URL 미리 가져오기로 끊김 없는 재생
- 🎨 다크 테마 GUI (tkinter 기반)
- 💾 다운로드 없이 **스트리밍 방식** (디스크 공간 절약)
- 🔊 음량 조절, 진행 바 탐색, 이전/다음 곡 컨트롤

---

## 📦 설치 및 실행

### 사전 요구사항
- **Python 3.10 이상** — [python.org](https://www.python.org)
- **VLC Media Player** — [videolan.org](https://www.videolan.org/vlc/)
  *(없으면 실행 시 자동으로 설치 안내 다이얼로그가 뜹니다)*

### 소스에서 실행
```powershell
pip install -r requirements.txt
python melon_player.py
```

### 실행 파일 빌드 (Windows)
```powershell
pip install pyinstaller
python -m PyInstaller melon_player.spec
# → dist/차트100플레이어.exe 생성
```

### Windows SmartScreen 안내
첫 실행 시 *"Windows의 PC 보호"* 경고가 나타날 수 있습니다.
**"추가 정보 → 실행"** 을 눌러주세요. 코드 서명을 하지 않은 오픈소스 빌드입니다.

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

- 차트 데이터는 각 음원 사이트(melon.com, genie.co.kr, music.bugs.co.kr, billboard.com, kworb.net)에서, 오디오는 [youtube.com](https://www.youtube.com)에서 가져옵니다.
- **모든 음원의 저작권은 원저작자 및 권리자에게 있습니다.**
- 본 프로그램은 어떠한 음원도 다운로드하거나 저장하지 않으며, 스트리밍만 수행합니다.
- 본 프로그램은 Melon, Genie, Bugs, Billboard, Spotify, YouTube, kworb 또는 어떤 음반사와도 제휴 관계가 없습니다.
- **상업적 사용을 금지합니다.**

### 🚨 Takedown Policy

If you are a rights holder (Melon / Kakao, Genie Music, NHN Bugs, Billboard, Spotify, YouTube / Google, kworb, a record label, an artist, or their authorized representative) and you believe this project infringes upon your rights, please contact the maintainer.

**Upon receiving a legitimate takedown request, this project will be removed promptly.**

저작권자, 플랫폼 운영사(멜론/카카오, 지니뮤직, NHN벅스, 빌보드, 스포티파이, 유튜브/구글, kworb), 음반사, 아티스트 또는 그 대리인으로부터 정당한 삭제 요청이 있을 경우 **즉시 본 프로젝트를 비공개/삭제 처리**합니다.

📧 Contact: GitHub Issues 또는 저장소 관리자에게 직접 연락해 주세요.

---

## 📜 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)로 배포됩니다.

단, MIT 라이선스는 **본 소프트웨어 코드 자체**에만 적용됩니다.
스트리밍되는 음원, 차트 데이터 등 외부 콘텐츠의 저작권은 각 권리자에게 있습니다.

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube 콘텐츠 추출
- [VLC](https://www.videolan.org/) — 미디어 재생 엔진
- [kworb.net](https://kworb.net/) — Spotify / YouTube 차트 집계
- 각 음원 사이트 — 차트 데이터 출처
