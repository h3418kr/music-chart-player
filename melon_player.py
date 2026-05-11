#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
멜론 차트 100 유튜브 오디오 플레이어
의존: pip install -r requirements.txt  +  VLC Media Player 설치
"""

import sys
import os
import random
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
from bs4 import BeautifulSoup
import yt_dlp
import time

# ─── 사전 요구사항 검사 ───────────────────────────────────────────────────────

VLC_DIRS = [
    r"C:\Program Files\VideoLAN\VLC",
    r"C:\Program Files (x86)\VideoLAN\VLC",
]

def _find_vlc() -> str | None:
    for d in VLC_DIRS:
        if os.path.isfile(os.path.join(d, "libvlc.dll")):
            return d
    return None

def _fix_vlc_path(vlc_dir: str):
    os.environ["PATH"] = vlc_dir + os.pathsep + os.environ.get("PATH", "")
    os.environ["VLC_PLUGIN_PATH"] = os.path.join(vlc_dir, "plugins")
    try:
        os.add_dll_directory(vlc_dir)
    except Exception:
        pass

def _check_internet() -> bool:
    try:
        requests.get("https://www.google.com", timeout=4)
        return True
    except Exception:
        return False

class RequirementsDialog(tk.Tk):
    """실행 전 사전 요구사항을 안내하는 다이얼로그."""

    BG    = "#0d0d1a"
    CARD  = "#16162a"
    OK    = "#22c55e"
    FAIL  = "#ef4444"
    WARN  = "#f59e0b"
    TEXT  = "#f0f0ff"
    SUB   = "#8888aa"
    PINK  = "#e84393"

    def __init__(self, vlc_ok: bool, net_ok: bool):
        super().__init__()
        self.title("멜론 차트 100 플레이어 — 시작 전 확인")
        self.geometry("480x380")
        self.configure(bg=self.BG)
        self.resizable(False, False)
        self.result = False  # True → 앱 실행, False → 종료

        self.vlc_ok = vlc_ok
        self.net_ok = net_ok
        self._build()
        # 모두 OK면 자동으로 닫기
        if vlc_ok and net_ok:
            self.after(800, self._proceed)

    def _build(self):
        # 헤더
        hdr = tk.Frame(self, bg="#13132b", height=54)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="🍈  멜론 차트 100 플레이어",
                 font=("Malgun Gothic", 15, "bold"),
                 bg="#13132b", fg=self.PINK).pack(side="left", padx=18, pady=12)

        tk.Label(self, text="실행에 필요한 항목을 확인합니다.",
                 font=("Malgun Gothic", 10), bg=self.BG, fg=self.SUB
                 ).pack(pady=(14, 8))

        # 항목 카드
        card = tk.Frame(self, bg=self.CARD, pady=12, padx=20)
        card.pack(fill="x", padx=20)

        self._row(card, "VLC Media Player",
                  "설치됨" if self.vlc_ok else "설치 필요",
                  self.vlc_ok,
                  None if self.vlc_ok else ("다운로드", "https://www.videolan.org/vlc/"))

        self._row(card, "인터넷 연결",
                  "연결됨" if self.net_ok else "연결 안 됨 (유튜브 재생 불가)",
                  self.net_ok, None)

        # 안내 문구
        if not self.vlc_ok:
            msg = ("VLC Media Player 를 설치한 뒤\n"
                   "이 프로그램을 다시 실행하세요.")
            tk.Label(self, text=msg, font=("Malgun Gothic", 10),
                     bg=self.BG, fg=self.WARN, justify="center"
                     ).pack(pady=(14, 0))

        # 버튼
        bf = tk.Frame(self, bg=self.BG)
        bf.pack(side="bottom", pady=20)

        can_run = self.vlc_ok  # 인터넷은 없어도 일단 실행은 허용
        if can_run:
            tk.Button(bf, text="▶  실행하기",
                      font=("Malgun Gothic", 11, "bold"),
                      bg=self.PINK, fg="white", relief="flat",
                      cursor="hand2", padx=20, pady=8,
                      activebackground="#c03070",
                      command=self._proceed).pack(side="left", padx=8)

        tk.Button(bf, text="닫기",
                  font=("Malgun Gothic", 10),
                  bg=self.CARD, fg=self.SUB, relief="flat",
                  cursor="hand2", padx=16, pady=8,
                  command=self.destroy).pack(side="left", padx=8)

    def _row(self, parent, label: str, status: str, ok: bool, link):
        row = tk.Frame(parent, bg=self.CARD)
        row.pack(fill="x", pady=5)

        icon  = "✅" if ok else "❌"
        color = self.OK if ok else self.FAIL

        tk.Label(row, text=icon, font=("Segoe UI Emoji", 13),
                 bg=self.CARD).pack(side="left", padx=(0, 8))
        tk.Label(row, text=label, font=("Malgun Gothic", 11, "bold"),
                 bg=self.CARD, fg=self.TEXT).pack(side="left")
        tk.Label(row, text=status, font=("Malgun Gothic", 9),
                 bg=self.CARD, fg=color).pack(side="left", padx=10)

        if link:
            text, url = link
            btn = tk.Button(row, text=f"  {text}  ",
                            font=("Malgun Gothic", 9),
                            bg="#1e3a5f", fg="#60b4ff",
                            relief="flat", cursor="hand2",
                            command=lambda u=url: webbrowser.open(u))
            btn.pack(side="right")

    def _proceed(self):
        self.result = True
        self.destroy()


def _run_requirements_check() -> bool:
    """요구사항을 확인하고 OK면 True 반환."""
    vlc_dir = _find_vlc()
    net_ok  = _check_internet()

    # 모두 OK면 다이얼로그 없이 바로 통과
    if vlc_dir and net_ok:
        _fix_vlc_path(vlc_dir)
        return True

    # 문제가 있으면 다이얼로그 표시
    dlg = RequirementsDialog(vlc_ok=bool(vlc_dir), net_ok=net_ok)
    dlg.mainloop()

    if dlg.result and vlc_dir:
        _fix_vlc_path(vlc_dir)
        return True
    return False


if not _run_requirements_check():
    sys.exit(0)

# VLC import (경로 설정 완료 후)
try:
    import vlc
except (ImportError, OSError) as _e:
    tk.Tk().withdraw()
    messagebox.showerror("VLC 로드 실패",
        f"VLC 가 설치되어 있지만 불러올 수 없습니다.\n\n원인: {_e}\n\n"
        "VLC 를 재설치한 뒤 다시 시도하세요.")
    sys.exit(1)

# ─── 상수 ────────────────────────────────────────────────────────────────────

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")

def _headers(referer: str) -> dict:
    return {
        "User-Agent":      UA,
        "Referer":         referer,
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

MELON_URL = "https://www.melon.com/chart/index.htm"
HEADERS   = _headers("https://www.melon.com/")

BG      = "#0d0d1a"
CARD    = "#16162a"
ACCENT  = "#e84393"
ACCENT2 = "#ff6b9d"
TEXT    = "#f0f0ff"
SUBTEXT = "#8888aa"
FONT_KR   = "Malgun Gothic"
FONT_ICON = "Segoe UI Emoji"


# ─── 유틸 ────────────────────────────────────────────────────────────────────

def fmt_time(ms: int) -> str:
    if ms <= 0:
        return "0:00"
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"


# ─── 멜론 스크래퍼 ────────────────────────────────────────────────────────────

def fetch_melon_chart() -> list[dict]:
    resp = requests.get(MELON_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    songs = []
    for row in soup.select("tr.lst50, tr.lst100"):
        rank_el  = row.select_one(".rank")
        title_el = row.select_one(".ellipsis.rank01 a")
        artist_els = row.select(".ellipsis.rank02 .checkEllipsis a") \
                     or row.select(".ellipsis.rank02 a")
        if not (rank_el and title_el):
            continue
        try:
            rank = int("".join(filter(str.isdigit, rank_el.text)))
        except ValueError:
            continue
        songs.append({
            "rank":   rank,
            "title":  title_el.text.strip(),
            "artist": ", ".join(a.text.strip() for a in artist_els) or "알 수 없음",
        })
    songs.sort(key=lambda x: x["rank"])
    return songs


# ─── Genie 스크래퍼 ──────────────────────────────────────────────────────────

def fetch_genie_chart() -> list[dict]:
    songs = []
    for page in (1, 2):  # Genie는 페이지당 50곡, 200곡까지 → 100곡만 가져오기
        url = f"https://www.genie.co.kr/chart/top200?pg={page}"
        resp = requests.get(url, headers=_headers("https://www.genie.co.kr/"), timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for row in soup.select("tr.list"):
            rank_el  = row.select_one(".number")
            title_el = row.select_one("a.title")
            artist_el = row.select_one("a.artist")
            if not (rank_el and title_el):
                continue
            try:
                rank = int("".join(filter(str.isdigit, rank_el.contents[0].strip())))
            except (ValueError, IndexError):
                continue
            songs.append({
                "rank":   rank,
                "title":  title_el.text.strip(),
                "artist": (artist_el.text.strip() if artist_el else "알 수 없음"),
            })
            if len(songs) >= 100:
                break
        if len(songs) >= 100:
            break
    songs.sort(key=lambda x: x["rank"])
    return songs[:100]


# ─── Bugs 스크래퍼 ───────────────────────────────────────────────────────────

def fetch_bugs_chart() -> list[dict]:
    url = "https://music.bugs.co.kr/chart"
    resp = requests.get(url, headers=_headers("https://music.bugs.co.kr/"), timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    songs = []
    for row in soup.select("table.list.trackList tbody tr"):
        rank_el = row.select_one("div.ranking strong")
        title_el = row.select_one("p.title a")
        artist_el = row.select_one("p.artist a")
        if not (rank_el and title_el):
            continue
        try:
            rank = int(rank_el.text.strip())
        except ValueError:
            continue
        songs.append({
            "rank":   rank,
            "title":  title_el.text.strip(),
            "artist": (artist_el.text.strip() if artist_el else "알 수 없음"),
        })
    songs.sort(key=lambda x: x["rank"])
    return songs[:100]


# ─── Billboard Hot 100 스크래퍼 ──────────────────────────────────────────────

def fetch_billboard_chart() -> list[dict]:
    url = "https://www.billboard.com/charts/hot-100/"
    resp = requests.get(url, headers=_headers("https://www.billboard.com/"), timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    songs = []
    for i, item in enumerate(soup.select("ul.o-chart-results-list-row"), start=1):
        title_el = item.select_one("h3.c-title")
        artist_el = item.select_one("span.c-label.a-no-trucate") \
                    or item.select_one("span.c-label")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        artist = artist_el.get_text(strip=True) if artist_el else "Unknown"
        if not title:
            continue
        songs.append({"rank": i, "title": title, "artist": artist})
        if len(songs) >= 100:
            break
    return songs


# ─── kworb (Spotify / YouTube) 스크래퍼 ──────────────────────────────────────

def _fetch_kworb_table(url: str, referer: str) -> list[dict]:
    resp = requests.get(url, headers=_headers(referer), timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    songs = []
    table = soup.select_one("table.sortable") or soup.select_one("table")
    if not table:
        return songs
    rows = table.select("tbody tr") or table.select("tr")
    rank = 0
    for row in rows:
        cells = row.select("td")
        if not cells:
            continue
        # 컬럼 레이아웃이 페이지마다 다름 → " - "가 들어있는 셀을 자동으로 찾음
        info_text = None
        for c in cells:
            t = c.get_text(" ", strip=True)
            if " - " in t and not t.replace(",", "").replace(".", "").isdigit():
                info_text = t
                break
        if not info_text:
            continue
        artist, title = info_text.split(" - ", 1)
        if not title.strip():
            continue
        rank += 1
        songs.append({"rank": rank, "title": title.strip(), "artist": artist.strip()})
        if rank >= 100:
            break
    return songs


def fetch_spotify_chart() -> list[dict]:
    # kworb 스포티파이 글로벌 일간 차트
    return _fetch_kworb_table(
        "https://kworb.net/spotify/country/global_daily.html",
        "https://kworb.net/"
    )


def fetch_youtube_chart() -> list[dict]:
    # kworb 유튜브 뮤직비디오 일간 차트
    return _fetch_kworb_table(
        "https://kworb.net/youtube/topvideos.html",
        "https://kworb.net/"
    )


# ─── 차트 소스 정의 ──────────────────────────────────────────────────────────

CHART_SOURCES = {
    "melon":     {"name": "🍈 Melon",          "fetch": fetch_melon_chart},
    "genie":     {"name": "🎵 Genie",          "fetch": fetch_genie_chart},
    "bugs":      {"name": "🐛 Bugs",           "fetch": fetch_bugs_chart},
    "billboard": {"name": "📊 Billboard Hot 100", "fetch": fetch_billboard_chart},
    "spotify":   {"name": "🎧 Spotify Global", "fetch": fetch_spotify_chart},
    "youtube":   {"name": "▶ YouTube Top",     "fetch": fetch_youtube_chart},
}


# ─── yt-dlp 스트리밍 ─────────────────────────────────────────────────────────

_stream_cache: dict[int, str] = {}
_cache_lock = threading.Lock()


def _ydl_opts(player_clients: list[str]) -> dict:
    return {
        # 오디오 전용 포맷만 선택 (m4a > webm > 기타) — 영상 포맷은 절대 받지 않음
        "format":      "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio",
        "quiet":       True,
        "no_warnings": True,
        "noplaylist":  True,
        "extractor_args": {"youtube": {"player_client": player_clients}},
    }


def get_stream_url(song: dict) -> str | None:
    """yt-dlp로 유튜브 스트림 URL 추출 (다운로드 없음).

    YouTube 봇 차단을 우회하기 위해 여러 player_client 조합을 순차 시도한다.
    """
    query = f"ytsearch1:{song['artist']} {song['title']}"
    # 우선순위 순서 — android+web이 가장 안정적
    client_chains = [
        ["android", "web"],
        ["android"],
        ["android_vr", "web"],
        ["tv", "ios"],
        ["mweb"],
    ]
    for clients in client_chains:
        try:
            with yt_dlp.YoutubeDL(_ydl_opts(clients)) as ydl:
                info = ydl.extract_info(query, download=False)
            if not info:
                continue
            entry = info["entries"][0] if "entries" in info else info
            url = entry.get("url") if entry else None
            if url:
                return url
        except Exception:
            continue
    return None


# ─── 메인 앱 ──────────────────────────────────────────────────────────────────

class MelonPlayer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎶 차트 100 플레이어")
        self.root.geometry("580x870")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        plugin_path = os.environ.get("VLC_PLUGIN_PATH", "")
        # 오디오 전용 + 저지연 버퍼링
        vlc_args = [
            "--no-video", "--quiet", "--no-xlib",
            "--network-caching=500",   # 네트워크 버퍼 (기본 1000ms)
            "--file-caching=300",
            "--live-caching=300",
        ]
        if plugin_path:
            vlc_args.append(f"--plugin-path={plugin_path}")
        self.vlc_inst = vlc.Instance(*vlc_args)
        self.player   = self.vlc_inst.media_player_new()
        self.player.audio_set_volume(80)

        self.songs:       list[dict] = []
        self.current_idx: int        = -1
        self.seeking:     bool       = False
        self.end_handled: bool       = False
        self.shuffle:        bool       = False
        self.repeat:         str        = "off"   # "off" | "all" | "one"
        self.history:        list[int]  = []      # 셔플 이전 곡 히스토리
        self.shuffle_queue:  list[int]  = []      # 미리 정해진 셔플 순서
        self.shuffle_pos:    int        = -1      # shuffle_queue 안 현재 위치
        self.chart_key:      str        = "melon"
        self._load_lock               = threading.Lock()

        self._build_ui()
        self._start_ticker()
        self._load_chart_async()

        self.root.protocol("WM_DELETE_WINDOW", self._on_quit)
        self.root.mainloop()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _build_ui(self):
        s = ttk.Style(); s.theme_use("clam")
        for n in ("P", "V"):
            s.configure(f"{n}.Horizontal.TScale", background=CARD,
                        troughcolor="#252540", sliderthickness=14,
                        sliderrelief="flat", borderwidth=0)

        hdr = tk.Frame(self.root, bg="#13132b", height=58)
        hdr.pack(fill="x"); hdr.pack_propagate(False)

        tk.Label(hdr, text="🎶 차트 100",
                 font=(FONT_KR, 16, "bold"), bg="#13132b", fg=ACCENT
                 ).pack(side="left", padx=(18, 10), pady=14)

        # 차트 선택 드롭다운
        s_combo = ttk.Style()
        s_combo.configure("Chart.TCombobox",
                          fieldbackground=CARD, background=CARD,
                          foreground=TEXT, arrowcolor=ACCENT,
                          selectbackground=CARD, selectforeground=TEXT,
                          borderwidth=0)
        self.var_chart = tk.StringVar(value=CHART_SOURCES[self.chart_key]["name"])
        self.cb_chart = ttk.Combobox(
            hdr, textvariable=self.var_chart, state="readonly", width=18,
            font=(FONT_KR, 9), style="Chart.TCombobox",
            values=[v["name"] for v in CHART_SOURCES.values()]
        )
        self.cb_chart.pack(side="left", pady=14)
        self.cb_chart.bind("<<ComboboxSelected>>", self._on_chart_changed)

        tk.Button(hdr, text="↻", font=(FONT_KR, 11),
                  bg="#13132b", fg=SUBTEXT, relief="flat", cursor="hand2", bd=0,
                  activebackground="#1e1e38", activeforeground=TEXT,
                  command=self._load_chart_async
                  ).pack(side="right", padx=8)
        self.lbl_status = tk.Label(hdr, text="시작 중...",
                                    font=(FONT_KR, 8), bg="#13132b", fg=SUBTEXT)
        self.lbl_status.pack(side="right", padx=(0, 6))

        card = tk.Frame(self.root, bg=CARD, pady=14)
        card.pack(fill="x", padx=14, pady=(14, 6))

        tk.Label(card, text="NOW  PLAYING",
                 font=(FONT_KR, 8, "bold"), bg=CARD, fg=ACCENT).pack()

        self.lbl_rank = tk.Label(card, text="#--",
                                  font=(FONT_KR, 13, "bold"), bg=CARD, fg=ACCENT2)
        self.lbl_rank.pack(pady=(3, 0))

        self.lbl_title = tk.Label(card, text="차트를 불러오는 중입니다...",
                                   font=(FONT_KR, 15, "bold"),
                                   bg=CARD, fg=TEXT, wraplength=530)
        self.lbl_title.pack(pady=(2, 0))

        self.lbl_artist = tk.Label(card, text="",
                                    font=(FONT_KR, 11), bg=CARD, fg=SUBTEXT)
        self.lbl_artist.pack(pady=(1, 10))

        pf = tk.Frame(card, bg=CARD)
        pf.pack(fill="x", padx=22, pady=(0, 2))
        self.var_prog = tk.DoubleVar()
        self.scale_prog = ttk.Scale(pf, from_=0, to=100, variable=self.var_prog,
                                     style="P.Horizontal.TScale",
                                     command=self._on_seek_drag)
        self.scale_prog.pack(fill="x")
        self.scale_prog.bind("<ButtonRelease-1>", self._on_seek_release)

        tf = tk.Frame(card, bg=CARD)
        tf.pack(fill="x", padx=22, pady=(0, 4))
        self.lbl_cur = tk.Label(tf, text="0:00", font=(FONT_KR, 8), bg=CARD, fg=SUBTEXT)
        self.lbl_cur.pack(side="left")
        self.lbl_tot = tk.Label(tf, text="0:00", font=(FONT_KR, 8), bg=CARD, fg=SUBTEXT)
        self.lbl_tot.pack(side="right")

        cf = tk.Frame(card, bg=CARD)
        cf.pack(pady=8)
        icon_btn = dict(bg=CARD, fg=TEXT, relief="flat", cursor="hand2",
                        bd=0, highlightthickness=0,
                        activebackground=CARD, activeforeground=ACCENT2)
        self.btn_shuffle = tk.Button(cf, text="🔀", font=(FONT_ICON, 13),
                                      command=self._toggle_shuffle, **icon_btn)
        self.btn_shuffle.pack(side="left", padx=8)
        tk.Button(cf, text="⏮", font=(FONT_ICON, 16),
                  command=self._prev, **icon_btn).pack(side="left", padx=10)
        self.btn_play = tk.Button(cf, text="⏸", font=(FONT_ICON, 22),
                                   bg=ACCENT, fg="white", relief="flat",
                                   cursor="hand2", bd=0, highlightthickness=0,
                                   activebackground="#c03070", activeforeground="white",
                                   padx=12, pady=4, command=self._toggle_play)
        self.btn_play.pack(side="left", padx=10)
        tk.Button(cf, text="⏭", font=(FONT_ICON, 16),
                  command=self._next, **icon_btn).pack(side="left", padx=10)
        self.btn_repeat = tk.Button(cf, text="🔁", font=(FONT_ICON, 13),
                                     command=self._cycle_repeat, **icon_btn)
        self.btn_repeat.pack(side="left", padx=8)

        vf = tk.Frame(card, bg=CARD)
        vf.pack(pady=(2, 4))
        tk.Label(vf, text="🔊", font=(FONT_ICON, 11), bg=CARD, fg=SUBTEXT).pack(side="left")
        self.var_vol = tk.IntVar(value=80)
        ttk.Scale(vf, from_=0, to=100, variable=self.var_vol, length=160,
                  style="V.Horizontal.TScale",
                  command=lambda v: self.player.audio_set_volume(int(float(v)))
                  ).pack(side="left", padx=8)

        lf = tk.Frame(self.root, bg=BG)
        lf.pack(fill="both", expand=True, padx=14, pady=(4, 14))
        tk.Label(lf, text="차트 순위  (더블클릭으로 재생)",
                 font=(FONT_KR, 9), bg=BG, fg=SUBTEXT
                 ).pack(anchor="w", pady=(0, 5))

        lb_wrap = tk.Frame(lf, bg=CARD, highlightthickness=1,
                           highlightbackground="#2a2a44")
        lb_wrap.pack(fill="both", expand=True)
        sb = tk.Scrollbar(lb_wrap, bg=CARD, troughcolor=CARD, relief="flat", width=10)
        sb.pack(side="right", fill="y")
        self.listbox = tk.Listbox(lb_wrap, yscrollcommand=sb.set,
                                   bg=CARD, fg=TEXT,
                                   selectbackground=ACCENT, selectforeground="white",
                                   font=(FONT_KR, 10),
                                   relief="flat", activestyle="none",
                                   borderwidth=0, highlightthickness=0)
        self.listbox.pack(fill="both", expand=True)
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<Double-Button-1>", self._on_list_dclick)

        # 출처/저작권 명시
        disclaimer = tk.Frame(lf, bg=BG)
        disclaimer.pack(fill="x", pady=(8, 0))
        tk.Label(
            disclaimer,
            text="ⓘ  차트: melon · genie · bugs · billboard · kworb   |   오디오: youtube.com",
            font=(FONT_KR, 8), bg=BG, fg=SUBTEXT
        ).pack(anchor="w")
        tk.Label(
            disclaimer,
            text="본 프로그램은 개인 감상 목적의 비공식 도구이며,\n"
                 "모든 음원의 저작권은 원저작자에게 있습니다.",
            font=(FONT_KR, 8), bg=BG, fg="#666688", justify="left"
        ).pack(anchor="w", pady=(2, 0))

    # ── 차트 로드 ─────────────────────────────────────────────────────────────

    def _load_chart_async(self):
        src = CHART_SOURCES[self.chart_key]
        self._set_status(f"{src['name']} 수집 중...")
        threading.Thread(target=self._do_load_chart, daemon=True).start()

    def _do_load_chart(self):
        src = CHART_SOURCES[self.chart_key]
        try:
            songs = src["fetch"]()
            if not songs:
                raise ValueError("곡 목록 비어있음 (사이트 구조 변경 가능)")
            self.songs = songs
            with _cache_lock:
                _stream_cache.clear()
            self.root.after(0, self._populate_list)
            if self.current_idx < 0:
                self.root.after(0, lambda: self._play_index(0))
            self._set_status(f"✓ {len(songs)}곡 로드 완료")
        except Exception as exc:
            self._set_status(f"차트 오류: {exc}")

    def _on_chart_changed(self, _event=None):
        # 선택된 이름으로 키 찾기
        selected = self.var_chart.get()
        for k, v in CHART_SOURCES.items():
            if v["name"] == selected:
                if k == self.chart_key:
                    return
                self.chart_key = k
                break
        # 재생 정지 + 상태 리셋 + 새 차트 로드
        self.player.stop()
        self.current_idx = -1
        self.history.clear()
        self.btn_play.config(text="▶")
        self.lbl_rank.config(text="#--")
        self.lbl_title.config(text="차트를 불러오는 중입니다...")
        self.lbl_artist.config(text="")
        self.var_prog.set(0)
        self.lbl_cur.config(text="0:00")
        self.lbl_tot.config(text="0:00")
        self._load_chart_async()

    def _populate_list(self):
        self.listbox.delete(0, "end")
        for s in self.songs:
            self.listbox.insert("end", f"  {s['rank']:>3}위   {s['artist']}  —  {s['title']}")

    # ── 재생 ─────────────────────────────────────────────────────────────────

    def _play_index(self, idx: int, push_history: bool = True):
        if not (0 <= idx < len(self.songs)):
            return

        # 셔플 모드 이전곡 추적: 이미 같은 곡 연속이면 추가 안 함
        if push_history and idx != self.current_idx:
            self.history.append(idx)
            if len(self.history) > 100:
                self.history.pop(0)

        # 셔플 큐 위치 동기화 (사용자가 리스트 더블클릭 등으로 점프했을 때)
        if self.shuffle and self.shuffle_queue:
            if idx in self.shuffle_queue:
                self.shuffle_pos = self.shuffle_queue.index(idx)
            else:
                self._rebuild_shuffle_queue(start_with=idx)

        self.current_idx = idx
        self.end_handled = False
        song = self.songs[idx]

        self.lbl_rank.config(text=f"#{song['rank']}")
        self.lbl_title.config(text=song["title"])
        self.lbl_artist.config(text=song["artist"])
        self.btn_play.config(text="⏸")
        self.var_prog.set(0)
        self.lbl_cur.config(text="0:00")
        self.lbl_tot.config(text="0:00")
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(idx)
        self.listbox.see(idx)

        self.player.stop()
        threading.Thread(target=self._load_and_play, args=(idx, song), daemon=True).start()

    def _load_and_play(self, idx: int, song: dict):
        self._set_status(f"스트림 연결 중: {song['artist']} - {song['title']}")

        with _cache_lock:
            url = _stream_cache.pop(idx, None)

        if not url:
            url = get_stream_url(song)

        if not url:
            self._set_status(f"'{song['title']}' 스트림 연결 실패 → 3초 후 다음 곡")
            self.root.after(3000, self._next)
            return

        if self.current_idx != idx:
            return

        media = self.vlc_inst.media_new(url)
        media.add_option(":no-video")    # 영상 출력 차단 (오디오만 재생)
        media.add_option(":http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        self.player.set_media(media)
        self.player.play()
        self._set_status(f"▶  #{song['rank']}  {song['artist']} - {song['title']}")

        # 다음 3곡 스트림 URL 미리 가져오기 (셔플이면 셔플 순서대로)
        self._prefetch_upcoming()

    def _prefetch_url(self, song: dict, idx: int):
        with _cache_lock:
            if idx in _stream_cache:
                return
        url = get_stream_url(song)
        if url:
            with _cache_lock:
                _stream_cache[idx] = url

    def _toggle_play(self):
        state = self.player.get_state()
        if state == vlc.State.Playing:
            self.player.pause()
            self.btn_play.config(text="▶")
        elif state == vlc.State.Paused:
            self.player.play()
            self.btn_play.config(text="⏸")
        elif self.current_idx >= 0:
            self._play_index(self.current_idx)

    def _prev(self):
        # 셔플 모드: 히스토리에서 이전 곡으로 이동
        if self.shuffle and len(self.history) >= 2:
            self.history.pop()                      # 현재 곡 제거
            prev_idx = self.history[-1]             # 이전 곡
            self._play_index(prev_idx, push_history=False)
        else:
            self._play_index(self.current_idx - 1)

    def _next(self, auto: bool = False):
        # 자동 전환 + repeat=one : 현재 곡 다시 재생
        if auto and self.repeat == "one" and self.current_idx >= 0:
            self._play_index(self.current_idx, push_history=False)
            return

        if self.shuffle and self.shuffle_queue:
            self.shuffle_pos += 1
            if self.shuffle_pos >= len(self.shuffle_queue):
                if self.repeat == "all":
                    random.shuffle(self.shuffle_queue)
                    self.shuffle_pos = 0
                else:
                    self._set_status("재생 목록 끝")
                    return
            self._play_index(self.shuffle_queue[self.shuffle_pos])
            return

        next_idx = self.current_idx + 1
        if next_idx >= len(self.songs):
            if self.repeat == "all":
                next_idx = 0
            else:
                self._set_status("재생 목록 끝")
                return
        self._play_index(next_idx)

    def _toggle_shuffle(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            self._rebuild_shuffle_queue(start_with=self.current_idx)
            self.btn_shuffle.config(fg=ACCENT2)
            self._set_status("🔀 셔플 ON")
            # 새 셔플 순서 기준으로 다음 곡 미리 가져오기
            self._prefetch_upcoming()
        else:
            self.shuffle_queue = []
            self.shuffle_pos = -1
            self.btn_shuffle.config(fg=TEXT)
            self._set_status("셔플 OFF")

    def _rebuild_shuffle_queue(self, start_with: int = -1):
        """모든 곡 인덱스를 무작위로 섞고, start_with를 맨 앞에 두기."""
        queue = list(range(len(self.songs)))
        random.shuffle(queue)
        if 0 <= start_with < len(self.songs):
            if start_with in queue:
                queue.remove(start_with)
            queue.insert(0, start_with)
        self.shuffle_queue = queue
        self.shuffle_pos = 0 if queue else -1

    def _upcoming_indices(self, count: int = 3) -> list[int]:
        """현재 이후 재생될 곡 인덱스들 (prefetch 용)."""
        result = []
        if self.shuffle and self.shuffle_queue:
            for offset in range(1, count + 1):
                pos = self.shuffle_pos + offset
                if pos < len(self.shuffle_queue):
                    result.append(self.shuffle_queue[pos])
                elif self.repeat == "all" and self.shuffle_queue:
                    # 끝나면 처음으로 (전체 반복 시)
                    wrap = (pos - len(self.shuffle_queue)) % len(self.shuffle_queue)
                    result.append(self.shuffle_queue[wrap])
        else:
            for offset in range(1, count + 1):
                ni = self.current_idx + offset
                if ni < len(self.songs):
                    result.append(ni)
                elif self.repeat == "all" and self.songs:
                    result.append((ni) % len(self.songs))
        return result

    def _prefetch_upcoming(self):
        for ni in self._upcoming_indices(3):
            threading.Thread(
                target=self._prefetch_url,
                args=(self.songs[ni], ni),
                daemon=True
            ).start()

    def _cycle_repeat(self):
        # off → all → one → off
        order = {"off": "all", "all": "one", "one": "off"}
        self.repeat = order[self.repeat]
        if self.repeat == "off":
            self.btn_repeat.config(text="🔁", fg=TEXT)
            self._set_status("반복 OFF")
        elif self.repeat == "all":
            self.btn_repeat.config(text="🔁", fg=ACCENT2)
            self._set_status("🔁 전체 반복")
        else:  # one
            self.btn_repeat.config(text="🔂", fg=ACCENT2)
            self._set_status("🔂 한 곡 반복")

    def _on_list_dclick(self, _event):
        sel = self.listbox.curselection()
        if sel:
            self._play_index(sel[0])

    # ── 진행 바 ───────────────────────────────────────────────────────────────

    def _on_seek_drag(self, _val):
        self.seeking = True

    def _on_seek_release(self, _event):
        self.player.set_position(self.var_prog.get() / 100.0)
        self.seeking = False

    # ── 타이머 ────────────────────────────────────────────────────────────────

    def _start_ticker(self):
        self._tick()

    def _tick(self):
        state = self.player.get_state()
        if state == vlc.State.Playing and not self.seeking:
            self.var_prog.set(self.player.get_position() * 100)
            self.lbl_cur.config(text=fmt_time(self.player.get_time()))
            self.lbl_tot.config(text=fmt_time(self.player.get_length()))
        elif state == vlc.State.Ended and not self.end_handled:
            self.end_handled = True
            self.root.after(600, lambda: self._next(auto=True))
        self.root.after(900, self._tick)

    # ── 공통 ─────────────────────────────────────────────────────────────────

    def _set_status(self, text: str):
        self.root.after(0, lambda: self.lbl_status.config(text=text))

    def _on_quit(self):
        self.player.stop()
        self.root.destroy()


if __name__ == "__main__":
    MelonPlayer()
