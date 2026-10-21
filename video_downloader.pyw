# -*- coding: utf-8 -*-
"""
Video Downloader Mini — video_downloader.pyw
Версия: 2.2  (PySide6 / Qt6)

Изменения 2.2:
- 🔄 Обновление с GitHub (общий модуль gh_update 1.1.0): ⚙ → «🔄 Обновление с GitHub…» —
  токен «только чтение», ветка, автопроверка (через 30 с после запуска и каждые N ч),
  скачивание с анимацией, установка поверх (yt-dlp.exe, ffmpeg, логи и загрузки не
  трогаются; заменённые файлы — в backup/v<версия>), перезапуск. Есть новая версия —
  кнопка «⬆ X.Y» рядом с ⚙ и пометка в меню. Настройки — в QSettings, как остальные.
- 📄 Главный файл переименован: video_downloader_app_v2.1.pyw → video_downloader.pyw
  (имя с номером версии ломало обновление). Версия — только внутри (APP_VERSION).

Изменения 2.1:
- 🛡 Проверка «без звука» больше не трогает чужие файлы: проверяются только
  файлы, созданные текущей загрузкой (yt-dlp сообщает путь через --print).
- 🛑 Кнопка «Отмена» и корректное закрытие окна во время загрузки/сканирования
  (процесс yt-dlp убивается, QThread дожидается завершения).
- 🔒 Открытие папки на Linux/macOS без os.system (нет инъекции через имя).
- 🎯 Выбранный в списке формат теперь реально качается (H.264 — только fallback).
- Python-модуль: --no-playlist, MP3 из AUDIO_SOURCE_FORMAT, проверка звука.
- ffprobe без мигающей консоли; «Диагностика форматов» в фоне, без зависания UI.
- Прогресс не скачет 0→100 дважды; ошибка определяется по префиксу «ERROR:».
- Fallback MP3→оригинал сбрасывается после каждой загрузки; признак ошибки
  ffprobe сужен.
- Кэш поиска зависимостей, ротация логов (хранятся последние 20),
  проверка SHA256 для yt-dlp.exe, автозагрузка ffmpeg — только с согласия.
- Чистка: мёртвый код, импорты, docstring.

Изменения 0.3.06:
- 🧹 Убраны две видимые кнопки справа: «Форматы» и «Зависимости».
  Диагностика и ручное обновление оставлены в меню ⚙, а зависимости
  по-прежнему готовятся автоматически рядом с программой.

Изменения 0.3.05:
- 🔇 ФИКС немого TikTok-видео. HEVC/bytevc1-варианты TikTok больше не выбираются
  как «лучшие», потому что они могут сохраняться без звука. Сначала выбирается
  H.264/MP4 с аудиодорожкой, даже если качество ниже.
- ✅ После скачивания видео приложение проверяет файл через локальный ffprobe.
  Если аудиодорожки нет — файл помечается как .noaudio и показывается ошибка,
  а не «успешно скачано».
- 🎵 MP3 теперь извлекается из аудио-only, а если его нет — из безопасного
  H.264-видео со звуком; больше не выбирается video-only как «аудио».
- 🧯 Исправлен краш fallback-аудио: поле _audio_original_fallback_used теперь
  создаётся при запуске окна.

Изменения 0.3.04:
- 🔊 Видео теперь качается только в варианте с аудиодорожкой. Если TikTok отдаёт
  video-only формат, приложение не сохраняет немое видео, а пробует безопасный
  fallback `best*[vcodec!=none][acodec!=none]`.
- 🧯 Исправлен fallback «Только аудио оригинал»: раньше он ошибочно уходил как
  видеоформат и давал `Requested format is not available`. Теперь это настоящий
  режим аудио без MP3-перекодирования.
- 🗂 Разведены имена файлов: видео сохраняется с суффиксом `[video]`, аудио —
  с суффиксом `[audio]`, чтобы аудио не цеплялось к уже скачанному video-only mp4.

Изменения 0.3.03:
- 🛑 Убраны лишние автоперекачки. Если yt-dlp.exe уже лежит рядом с программой —
  он НЕ скачивается заново. Автообновление yt-dlp теперь только вручную через ⚙.
- 🔎 ffmpeg/ffprobe ищутся не только в ./ffmpeg, но и во вложенных папках
  типа ./ffmpeg/*/bin — чтобы не качать архив повторно из-за структуры распаковки.
- 🎵 При ошибке TikTok/ffprobe на MP3 сначала сохраняется оригинальный аудиофайл,
  а не начинается повторная загрузка ffmpeg.zip.

Изменения 0.3.02:
- 📁 Папка загрузок по умолчанию теперь рядом с программой: ./downloads/.
  И видео, и аудио без ручного выбора сохраняются туда, а не в системные Downloads.
- 🔁 Автообновление yt-dlp больше не перекачивает свежий локальный yt-dlp.exe
  снова и снова при ошибках TikTok: если файл только что скачан/обновлён,
  повторная автоперекачка блокируется. Ручной пункт ⚙ «Обновить yt-dlp» остался.
- 🧱 Все автозависимости и результаты теперь разложены рядом с проектом:
  ./yt-dlp.exe, ./ffmpeg/, ./logs/, ./downloads/.

Изменения 0.3.01:
- 🔒 Полностью отключён поиск системных yt-dlp из PATH/WinGet на Windows.
  Программа использует только yt-dlp.exe рядом с собой; если его нет —
  сама скачивает в папку приложения до сканирования и скачивания.
- 🔒 Python-модуль yt_dlp на Windows больше не используется как fallback,
  чтобы приложение не брало установленное на ПК окружение вместо локального
  движка.
- 🚦 При запуске и перед любым действием проверяется только локальный комплект:
  ./yt-dlp.exe + ./ffmpeg/ffmpeg.exe + ./ffmpeg/ffprobe.exe. Пока комплект
  готовится, нажатые действия ставятся в очередь.
- 🎵 Для TikTok-аудио добавлен аварийный fallback: если MP3-постобработка
  снова падает на ffprobe, программа повторяет скачивание только звука без
  перекодирования, чтобы файл всё равно был сохранён.

Изменения 0.3.00:
- 🧩 Жёстко локальные зависимости на Windows: yt-dlp.exe, ffmpeg.exe и
  ffprobe.exe больше не берутся из PATH/WinGet для скачивания и MP3.
  Если рядом с программой их нет — приложение само скачивает их в свою папку.
- ⏳ Если при вставке ссылки ещё идёт автоустановка зависимостей, сканирование
  не стартует через старый внешний yt-dlp, а ждёт завершения и запускается само.
- 🔁 Если нажать «Скачать видео» или «Скачать только звук» во время подготовки,
  действие ставится в очередь и продолжается автоматически после установки.
- 🧯 Уменьшена нагрузка на Qt при скачивании больших бинарников: прогресс
  зависимостей обновляется с троттлингом, чтобы окно не закрывалось/не подвисало.
- 🎵 MP3-извлечение теперь выполняется только через локальную пару
  ./ffmpeg/ffmpeg.exe + ./ffmpeg/ffprobe.exe.

Изменения 0.2.99:
- 🧾 Добавлены логи рядом с программой: папка ./logs/, файл latest.log и
  отдельный файл запуска video_downloader_0.2.99_YYYYMMDD_HHMMSS.log.
  В лог пишутся запуск, пути к yt-dlp/ffmpeg/ffprobe, нормализация URL,
  команды yt-dlp, вывод yt-dlp, ошибки потоков и аварийные падения.
- 🧯 Добавлены перехватчики sys.excepthook / threading.excepthook / Qt-log /
  faulthandler, чтобы при закрытии/краше оставался след в логе.
- 🧵 Исправлена опасная замена активного QThread сканирования форматов: старый
  ProbeWorker больше не уничтожается, пока реально работает.

Изменения 0.2.98:
- 🧹 Нормализация TikTok-ссылок: варианты с `?is_from_webapp=1` и
  `&sender_device=pc` приводятся к чистому виду `/video/<id>`, поэтому
  обе ссылки работают одинаково при сканировании, скачивании видео и звука.
- 🤖 Зависимости теперь чинятся автоматически: если рядом с программой нет
  локального свежего yt-dlp.exe или полной пары ffmpeg.exe+ffprobe.exe,
  приложение само скачивает их рядом с собой перед загрузкой и продолжает
  выбранное действие.
- 🔁 При ошибках устаревшего TikTok-экстрактора или ffprobe больше не нужно
  нажимать подтверждения: приложение один раз само обновляет нужный компонент
  и повторяет скачивание.

Изменения 0.2.97:
- 🛠 ФИКС TikTok / старого yt-dlp из чужой папки. Если yt-dlp.exe найден
  только в PATH или в старой папке другой версии приложения — теперь
  приложение автоматически докачивает свежий yt-dlp.exe рядом с текущим
  файлом и использует именно его.
- 🛠 ФИКС MP3 / ffprobe. Раньше считалось, что ffmpeg найден, даже если
  рядом не было ffprobe.exe; из-за этого появлялась ошибка
  «unable to obtain file audio codec with ffprobe». Теперь ffmpeg считается
  рабочим только парой ffmpeg.exe + ffprobe.exe, а неполная сборка
  автоматически заменяется локальной полной сборкой.
- 🔄 При ошибке ffprobe приложение предлагает перекачать ffmpeg/ffprobe.

Изменения 0.2.96:
- 🔄 ОБНОВЛЕНИЕ yt-dlp. Старый bundled yt-dlp.exe часто ломается, когда
  сайт (TikTok/YouTube/…) меняет выдачу — yt-dlp пишет «Confirm you are
  on the latest version using yt-dlp -U». Теперь:
    • в меню ⚙ есть пункт «🔄 Обновить yt-dlp» — качает свежий
      yt-dlp.exe рядом с программой (приоритетнее старого из PATH);
    • при ошибке скачивания, похожей на устаревший экстрактор
      («Unexpected response», «please report this issue» и т.п.),
      приложение само предлагает обновить yt-dlp и повторить загрузку.
  Защита от зацикливания: после авто-обновления повтор делается один раз.

Изменения 0.2.95:
- 📦 АВТО-ЗАГРУЗКА ЗАВИСИМОСТЕЙ РЯДОМ С ПРОГРАММОЙ. На чистой машине,
  где нет ни yt-dlp, ни ffmpeg, приложение само скачивает их в свою
  папку при старте (и по кнопке «⬇ Зависимости»):
    • yt-dlp.exe  ← github.com/yt-dlp/yt-dlp (releases/latest)
    • ffmpeg.exe + ffprobe.exe ← github.com/yt-dlp/FFmpeg-Builds
      (распаковываются в подпапку ./ffmpeg/)
  После загрузки движки подхватываются без перезапуска, лейблы статуса
  обновляются вживую. Загрузка идёт в фоне (QThread) с прогрессом.
  Авто-загрузка бинарников — только Windows; на Linux/macOS показывается
  подсказка (pip / пакетный менеджер).
- 🧹 Чистка: убран неиспользуемый импорт QSize и две мёртвые переменные
  в меню стилей (pyflakes-замечания).

Изменения 0.2.94:
- 💬 Кнопки «Скачать видео» и «Скачать только звук» при блокировке во
  время сканирования форматов меняют ТЕКСТ на «⏳ Идёт сканирование,
  подождите...» — серый фон не всегда заметен на тёмной теме.
  После сканирования возвращается оригинальный текст.

Изменения 0.2.93:
- 🏷 Фикс лейбла «Win7-режим» на Win10/11. Если используется
  системный yt-dlp.exe из PATH (не bundled yt-dlp_win7.exe) — лейбл
  показывает «✓ yt-dlp.exe (внешний)» вместо вводящего в заблуждение
  «Win7-режим». Логика работы НЕ изменилась — субпроцесс к yt-dlp.exe
  всегда приоритетнее модуля, потому что чаще он свежее.

Изменения 0.2.92:
- 🐛 Фикс наложения «Папка» поверх «Качество». В 0.2.91 minWidth=420
  для combo был больше доступного места при минимальной ширине окна.
  Теперь stretch-only схема — Qt сам распределит ширину.
  Также увеличил минимальную ширину окна до 840px.

Изменения 0.2.91:
- 🎨 Перекомпоновка строки «Качество / Папка»:
    • Дропдаун «Качество» — широкий (виден весь длинный лейбл формата);
    • Поле «Папка» — компактное, прижато к правому краю.

Изменения 0.2.9:
- 🎯 АВТО-СКАНИРОВАНИЕ ФОРМАТОВ при вставке URL.
  Как только в поле URL появляется ссылка — фоновый поток запускает
  `yt-dlp -J` (JSON dump) и парсит ВСЕ доступные форматы для конкретного
  видео. Результат заполняется в дропдаун «Качество» в виде списка
  типа «1080p mp4 H.264 + 128k AAC — 104 MB» (с явным размером).
- 🏆 Авто-выбор лучшего: предпочитается H.264+AAC, max разрешение,
  затем mp4 контейнер. Так что по умолчанию ты сразу качаешь max
  совместимый формат, без ручной возни.
- 🔒 Кнопка «Скачать видео» залочена пока идёт сканирование. После
  сканирования автоматически разблокируется.
- 🛡 Дефолтные «Лучшее качество / 720p / ...» пресеты остаются
  как fallback если сканирование упало (плохой URL / нет интернета).

Изменения 0.2.8:
- 🔍 Кнопка «Форматы» — диагностика: запускает `yt-dlp -F <URL>` и
  показывает в окне все доступные форматы для текущей ссылки. Помогает
  понять, что РЕАЛЬНО видит yt-dlp (максимальное разрешение, наличие
  H.264 / AV1, наличие AAC / Opus, отдельные потоки vs single-stream).

Изменения 0.2.7:
- 🧹 После успешного скачивания и нажатия «ОК»:
    • поле URL очищается и фокус в него;
    • зелёная полоса прогресса гарантированно сбрасывается в 0 (reset + repaint);
    • статус «Готово к новой ссылке.»
- 🔒 Во время скачивания дополнительно блокируются поле URL, выбор папки и
  выбор качества — чтобы случайно не менять параметры активной загрузки.
  (Кнопки «Скачать видео»/«Звук» уже блокировались.)

Изменения 0.2.6:
- 🪟 Поддержка Windows 7 через nicolaasjan/yt-dlp standalone exe.
  Если рядом с программой лежит `yt-dlp_win7.exe` (или `yt-dlp.exe`) —
  скачивание идёт через него как subprocess (CLI). Это позволяет
  использовать актуальный YouTube-экстрактор даже на Python 3.8 / Win7,
  где обычный модуль yt_dlp (max 2024.10.22) уже не работает с YouTube.
- 🔁 Авто-выбор движка скачивания:
    1) bundled `yt-dlp_win7.exe` / `yt-dlp.exe`  → subprocess (Win7-режим)
    2) `import yt_dlp`                           → как раньше (Win10+)
- 📺 Прогресс берётся из stdout yt-dlp через --progress-template
  с разделителем «|» — точный процент, скорость, ETA.

Изменения 0.2.5:
- 🔧 Полностью переработан поиск ffmpeg. Теперь приложение само находит
  ffmpeg в любом из мест:
    1) sys._MEIPASS (когда exe собран PyInstaller с --add-binary)
    2) рядом с exe / скриптом
    3) в подпапке ./ffmpeg/ или ./bin/
    4) в PATH
  И передаёт явный путь в yt-dlp через `ffmpeg_location` — больше не
  «ffmpeg not found», даже если он лежит рядом с exe.
- 🎬 Если ffmpeg вообще не найден — приложение НЕ падает, а тихо
  переключается на формат «best» (одиночный файл без слияния).
  В статусе пишется предупреждение.
- 🎵 «Скачать только звук» работает БЕЗ ffmpeg — скачает оригинальный
  аудиоформат (m4a/webm) без перекодирования в MP3.

Изменения 0.2.4:
- Первая кнопка переименована в «Скачать видео».
- Качество по умолчанию: «Лучшее качество».
- MP3 320 kbps (при наличии ffmpeg).

Зависимости:
    python -m pip install -U PySide6 yt-dlp
"""

APP_VERSION = "2.2"
APP_NAME = "Video Downloader Mini"
APP_AUTHOR = "RomzesPRA-2026"

import os
import hashlib
import json
import shutil
import re
import subprocess
import sys
import traceback
import urllib.request
from urllib.parse import urlsplit, urlunsplit
import zipfile
from pathlib import Path
import datetime
import faulthandler
import logging
import platform
import tempfile
import threading
import time

from PySide6.QtCore import Qt, QThread, Signal, QSettings, QTimer, qInstallMessageHandler
from PySide6.QtGui import QGuiApplication, QAction, QActionGroup, QPalette, QColor, QIcon, QPixmap, QPainter, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QFileDialog,
    QMessageBox, QGroupBox, QSizePolicy, QStyleFactory, QMenu, QToolButton,
    QDialog, QPlainTextEdit, QDialogButtonBox,
)

try:
    import yt_dlp
except Exception:
    yt_dlp = None


# TikTok часто отдаёт высокий HEVC/bytevc1 mp4 как будто с AAC, но файл выходит
# без звука. Поэтому безопасный порядок: сначала H.264/AVC с аудио, и только
# потом любые другие форматы с аудио. Лучше чуть ниже качество, чем немое видео.
H264_WITH_AUDIO_FORMAT = (
    "best*[vcodec^=avc1][acodec!=none]/"
    "best*[vcodec=h264][acodec!=none]/"
    "best[vcodec^=avc1][acodec!=none]/"
    "best[vcodec=h264][acodec!=none]"
)
VIDEO_WITH_AUDIO_FALLBACK = (
    H264_WITH_AUDIO_FORMAT +
    "/best*[vcodec!=none][acodec!=none]/best[vcodec!=none][acodec!=none]"
)
AUDIO_SOURCE_FORMAT = (
    "bestaudio[vcodec=none][acodec!=none]/"
    "bestaudio[acodec!=none][vcodec=none]/" +
    H264_WITH_AUDIO_FORMAT +
    "/best*[vcodec!=none][acodec!=none]/best[vcodec!=none][acodec!=none]"
)
AUDIO_ORIGINAL_FORMAT = AUDIO_SOURCE_FORMAT

QUALITY_PRESETS = {
    # Важно: без голого fallback `b/best`, чтобы не сохранять немое video-only.
    "Лучшее качество": VIDEO_WITH_AUDIO_FALLBACK,
    "2160p / 4K": "bv*[height<=2160]+ba/best*[height<=2160][vcodec!=none][acodec!=none]/best[height<=2160][vcodec!=none][acodec!=none]",
    "1440p": "bv*[height<=1440]+ba/best*[height<=1440][vcodec!=none][acodec!=none]/best[height<=1440][vcodec!=none][acodec!=none]",
    "1080p": "bv*[height<=1080]+ba/best*[height<=1080][vcodec!=none][acodec!=none]/best[height<=1080][vcodec!=none][acodec!=none]",
    "720p": "bv*[height<=720]+ba/best*[height<=720][vcodec!=none][acodec!=none]/best[height<=720][vcodec!=none][acodec!=none]",
    "480p": "bv*[height<=480]+ba/best*[height<=480][vcodec!=none][acodec!=none]/best[height<=480][vcodec!=none][acodec!=none]",
    "360p": "bv*[height<=360]+ba/best*[height<=360][vcodec!=none][acodec!=none]/best[height<=360][vcodec!=none][acodec!=none]",
    "Только аудио MP3": AUDIO_ORIGINAL_FORMAT,
}


def is_audio_quality(name):
    return name in ("Только аудио MP3", "Только аудио оригинал")


def _looks_hevc_or_tiktok_bytevc1(fmt):
    t = (fmt or "").lower()
    return any(x in t for x in ("bytevc1", "h265", "hevc", "hev1", "hvc1"))


def force_video_with_audio_format(fmt):
    """Возвращает формат, который не должен сохранять немое видео.

    Для TikTok НЕ доверяем HEVC/bytevc1: yt-dlp может считать его single
    с AAC, но на выходе получается mp4 без звука. Поэтому такие варианты
    заменяются на безопасный H.264-first fallback.
    """
    fmt = (fmt or "").strip()
    if not fmt:
        return VIDEO_WITH_AUDIO_FALLBACK
    if _looks_hevc_or_tiktok_bytevc1(fmt):
        return VIDEO_WITH_AUDIO_FALLBACK
    if "+" in fmt:
        return fmt
    if "[acodec" in fmt or "+ba" in fmt or "bestaudio" in fmt:
        # Формат уже требует аудио — выбор пользователя первым, H.264 как запас.
        return f"{fmt}/{H264_WITH_AUDIO_FORMAT}"
    # Одиночный format_id: сам ID только если в нём есть аудио, иначе H.264.
    return f"{fmt}[vcodec!=none][acodec!=none]/{H264_WITH_AUDIO_FORMAT}"


def normalize_video_url(url):
    """Приводит ссылку к виду, который стабильнее понимает yt-dlp.

    Для TikTok убираем мусорные query-параметры (`is_from_webapp`,
    `sender_device`, `t`, `_r` и т.п.) и оставляем чистую ссылку на
    `/video/<id>`. Поэтому оба варианта:
      • .../video/ID?is_from_webapp=1
      • .../video/ID?is_from_webapp=1&sender_device=pc
    идут в yt-dlp одинаково.
    """
    text = (url or "").strip().strip('"\'')
    if not text:
        return ""
    text = text.replace("\ufeff", "").replace("\u200b", "")

    # В URL пробелы невалидны; чаще всего это мусор из копирования.
    text = re.sub(r"\s+", "", text)

    if text.lower().startswith("www."):
        text = "https://" + text

    try:
        parts = urlsplit(text)
    except Exception:
        return text

    host = (parts.netloc or "").lower()
    if "tiktok.com" in host:
        m = re.search(r"/video/(\d+)", parts.path)
        if m:
            # Сохраняем username/path до ID, но убираем query/fragment.
            clean_path = parts.path[:m.end()].rstrip("/")
            scheme = parts.scheme or "https"
            clean = urlunsplit((scheme, parts.netloc, clean_path, "", ""))
            if clean != text:
                logging.info("normalize_url: %s -> %s", text, clean)
            return clean

    return text


# ---------------- Парсинг форматов из yt-dlp -J ----------------

def _human_size(n):
    if not n:
        return ""
    n = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def _codec_short(c):
    if not c:
        return "?"
    c = c.lower()
    if c.startswith("avc1") or c == "h264":
        return "H.264"
    if c.startswith("av01"):
        return "AV1"
    if c.startswith("vp9"):
        return "VP9"
    if c.startswith("vp09"):
        return "VP9"
    if c.startswith("hev1") or c.startswith("hvc1"):
        return "HEVC"
    if c.startswith("mp4a"):
        return "AAC"
    if c == "opus":
        return "Opus"
    if c == "mp3":
        return "MP3"
    if c == "vorbis":
        return "Vorbis"
    return c.split(".")[0]


def _tv_score(vcodec, acodec, ext):
    """Очки TV-совместимости (больше = лучше для TV).
    H.264 + AAC mp4 = идеал, AV1 + Opus webm = плохо."""
    score = 0
    v = (vcodec or "").lower()
    a = (acodec or "").lower()
    e = (ext or "").lower()
    if v.startswith("avc1") or v == "h264":
        score += 100
    elif v.startswith("hev1") or v.startswith("hvc1"):
        score += 50
    elif v.startswith("vp9") or v.startswith("vp09"):
        score += 20
    elif v.startswith("av01"):
        score += 5
    if a.startswith("mp4a") or a == "aac":
        score += 50
    elif a == "mp3":
        score += 30
    elif a == "opus":
        score += 5
    if e == "mp4":
        score += 10
    return score


def build_quality_options(formats):
    """Из списка форматов yt-dlp строит список вариантов для дропдауна.
    Возвращает список tuple (label, format_string).

    Делается так:
      • Группируем video-only форматы по (height, vcodec, ext)
      • Для каждого выбираем лучший аудио-фит (AAC если есть, иначе any)
      • Формат-строку строим в виде "<vid_id>+<aud_id>"
      • Также добавляем pre-merged single-stream форматы как есть
    """
    if not formats:
        return []

    video_only = [f for f in formats if f.get("vcodec") and f.get("vcodec") != "none"
                  and (not f.get("acodec") or f.get("acodec") == "none")]
    audio_only = [f for f in formats if f.get("acodec") and f.get("acodec") != "none"
                  and (not f.get("vcodec") or f.get("vcodec") == "none")]
    progressive = [f for f in formats if f.get("vcodec") and f.get("vcodec") != "none"
                   and f.get("acodec") and f.get("acodec") != "none"]

    # Лучший AAC-аудио (для TV-совместимости).
    def best_audio_for(want_codec_starts=None):
        cands = audio_only[:]
        if want_codec_starts:
            cands = [a for a in cands if (a.get("acodec") or "").lower().startswith(want_codec_starts)]
        if not cands:
            return None
        cands.sort(key=lambda a: -(a.get("abr") or a.get("tbr") or 0))
        return cands[0]

    best_aac = best_audio_for("mp4a")
    best_any_audio = best_audio_for(None)

    options = []  # list of (sort_key, label, fmt_string)

    for vf in video_only:
        h = vf.get("height") or 0
        if h <= 0:
            continue
        ext = vf.get("ext") or ""
        vcodec = vf.get("vcodec") or ""
        vshort = _codec_short(vcodec)
        # Для H.264 / mp4 берём AAC аудио (TV-friendly).
        # Для остального — лучшее доступное аудио.
        if vshort == "H.264" and best_aac:
            af = best_aac
        elif ext == "mp4" and best_aac:
            af = best_aac
        else:
            af = best_any_audio or best_aac
        if not af:
            continue
        ashort = _codec_short(af.get("acodec") or "")
        v_size = vf.get("filesize") or vf.get("filesize_approx") or 0
        a_size = af.get("filesize") or af.get("filesize_approx") or 0
        total = (v_size or 0) + (a_size or 0)
        size_str = f" — {_human_size(total)}" if total else ""

        fps = vf.get("fps")
        fps_str = f" {int(fps)}fps" if fps and fps > 30 else ""

        tv_ok = "📺" if _tv_score(vcodec, af.get("acodec"), ext) >= 150 else ""
        label = f"{tv_ok}{h}p {ext} {vshort}{fps_str} + {ashort}{size_str}"
        fmt_str = f"{vf['format_id']}+{af['format_id']}"
        score = (h, _tv_score(vcodec, af.get("acodec"), ext),
                 (vf.get("tbr") or 0) + (af.get("abr") or 0))
        options.append((score, label, fmt_str))

    # Progressive (single-stream) — берём только нормальные (не mhtml/storyboard).
    # TikTok HEVC/bytevc1 пропускаем: он часто скачивается без звука, даже если
    # yt-dlp в JSON пишет acodec=aac.
    for pf in progressive:
        h = pf.get("height") or 0
        if h <= 0:
            continue
        ext = pf.get("ext") or ""
        if ext in ("mhtml", ""):
            continue
        vcodec_raw = pf.get("vcodec") or ""
        fmt_id = pf.get("format_id") or ""
        if _looks_hevc_or_tiktok_bytevc1(vcodec_raw) or _looks_hevc_or_tiktok_bytevc1(fmt_id):
            logging.debug("skip risky progressive format without reliable audio: id=%s vcodec=%s", fmt_id, vcodec_raw)
            continue
        vshort = _codec_short(vcodec_raw)
        ashort = _codec_short(pf.get("acodec") or "")
        size = pf.get("filesize") or pf.get("filesize_approx") or 0
        size_str = f" — {_human_size(size)}" if size else ""
        tv_ok = "📺" if _tv_score(pf.get("vcodec"), pf.get("acodec"), ext) >= 150 else ""
        label = f"{tv_ok}{h}p {ext} {vshort} + {ashort} (single){size_str}"
        score = (h, _tv_score(pf.get("vcodec"), pf.get("acodec"), ext) + 40,
                 pf.get("tbr") or 0)
        safe_fmt = f"{fmt_id}[vcodec!=none][acodec!=none]/{H264_WITH_AUDIO_FORMAT}"
        options.append((score, label, safe_fmt))

    # Всегда добавляем безопасный авто-режим. Он нужен, если сайт врёт про acodec
    # у высокого HEVC/bytevc1 и список форматов выглядит лучше, чем есть на деле.
    options.append(((10**9, 10**9, 10**9), "✅ Авто: видео со звуком (H.264/MP4)", VIDEO_WITH_AUDIO_FALLBACK))

    # Дедупликация по лейблу + сортировка по убыванию качества
    seen = set()
    unique = []
    for s, lab, fs in sorted(options, key=lambda x: x[0], reverse=True):
        if lab in seen:
            continue
        seen.add(lab)
        unique.append((lab, fs))
    return unique


# ---------------- Поиск ffmpeg ----------------


def _app_dir():
    """Папка, где лежит exe/скрипт."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _downloads_dir():
    """Папка загрузок рядом с программой: ./downloads/."""
    try:
        d = _app_dir() / "downloads"
        d.mkdir(parents=True, exist_ok=True)
        return d
    except Exception:
        # Последний fallback, чтобы приложение не падало, если папка программы read-only.
        d = Path.home() / "Downloads" / "VideoDownloaderMini"
        d.mkdir(parents=True, exist_ok=True)
        return d


def _is_fresh_file(path, min_size=1024 * 1024, max_age_seconds=12 * 60 * 60):
    """True, если файл существует, похож на полноценный бинарник и был создан недавно."""
    try:
        p = Path(path)
        return p.is_file() and p.stat().st_size >= min_size and (time.time() - p.stat().st_mtime) < max_age_seconds
    except Exception:
        return False


def _local_ytdlp_is_fresh():
    """Блокирует бесконечные автоперекачки yt-dlp при одинаковой ошибке сайта."""
    p = find_local_ytdlp_exe()
    return bool(p and _is_fresh_file(p))


# ---------------- Логи / диагностика ----------------
LOG_FILE = None
LOG_LATEST_FILE = None
_FAULTHANDLER_FILE = None


def _safe_log_dir():
    """Папка логов рядом с программой. Если прав нет — fallback во временную."""
    try:
        d = _app_dir() / "logs"
        d.mkdir(parents=True, exist_ok=True)
        return d
    except Exception:
        d = Path(tempfile.gettempdir()) / "VideoDownloaderMini_logs"
        d.mkdir(parents=True, exist_ok=True)
        return d


LOG_KEEP = 20


def _rotate_logs(log_dir, keep=LOG_KEEP):
    """Оставляет только последние `keep` логов запусков."""
    try:
        logs = sorted(Path(log_dir).glob("video_downloader_*.log"),
                      key=lambda p: p.stat().st_mtime, reverse=True)
        for old in logs[max(0, keep - 1):]:
            try:
                old.unlink()
            except OSError:
                pass
    except Exception:
        pass


def _setup_logging():
    """Создаёт лог текущего запуска и latest.log."""
    global LOG_FILE, LOG_LATEST_FILE, _FAULTHANDLER_FILE
    log_dir = _safe_log_dir()
    _rotate_logs(log_dir)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    LOG_FILE = log_dir / f"video_downloader_{APP_VERSION}_{stamp}.log"
    LOG_LATEST_FILE = log_dir / "latest.log"

    fmt = "%(asctime)s.%(msecs)03d [%(levelname)s] %(threadName)s %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    handlers = []
    for path in (LOG_FILE, LOG_LATEST_FILE):
        try:
            handlers.append(logging.FileHandler(path, mode="w", encoding="utf-8"))
        except Exception:
            pass
    try:
        logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt=datefmt,
                            handlers=handlers, force=True)
    except TypeError:
        logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt=datefmt,
                            handlers=handlers)

    try:
        _FAULTHANDLER_FILE = open(LOG_FILE, "a", encoding="utf-8", errors="replace")
        faulthandler.enable(file=_FAULTHANDLER_FILE, all_threads=True)
    except Exception:
        pass

    logging.info("=== START %s v%s ===", APP_NAME, APP_VERSION)
    logging.info("app_dir=%s", _app_dir())
    logging.info("cwd=%s", Path.cwd())
    logging.info("python=%s", sys.version.replace("\n", " "))
    logging.info("platform=%s", platform.platform())
    logging.info("executable=%s", sys.executable)
    logging.info("frozen=%s", getattr(sys, "frozen", False))
    logging.info("log_file=%s", LOG_FILE)


def _log_uncaught(exc_type, exc_value, exc_tb):
    logging.critical("UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_tb))
    try:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    except Exception:
        pass


def _log_thread_exception(args):
    logging.critical("UNCAUGHT THREAD EXCEPTION: %s", getattr(args, "thread", None),
                     exc_info=(args.exc_type, args.exc_value, args.exc_traceback))


def _qt_message_handler(mode, context, message):
    try:
        mode_name = getattr(mode, "name", str(mode))
        logging.getLogger("qt").warning("%s %s:%s %s", mode_name,
                                        getattr(context, "file", ""),
                                        getattr(context, "line", ""), message)
    except Exception:
        pass


def _install_crash_hooks():
    sys.excepthook = _log_uncaught
    if hasattr(threading, "excepthook"):
        threading.excepthook = _log_thread_exception
    try:
        qInstallMessageHandler(_qt_message_handler)
    except Exception:
        logging.exception("Не смог установить Qt message handler")


def _hidden_kwargs():
    """kwargs для subprocess: на Windows без мигающего консольного окна."""
    if not sys.platform.startswith("win"):
        return {}
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE
    return {"startupinfo": si, "creationflags": subprocess.CREATE_NO_WINDOW}


def _kill_process_tree(proc):
    """Убивает yt-dlp вместе с дочерним ffmpeg."""
    if proc is None or proc.poll() is not None:
        return
    try:
        if sys.platform.startswith("win"):
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                           capture_output=True, timeout=10, **_hidden_kwargs())
        else:
            proc.kill()
    except Exception:
        logging.exception("kill process failed")
        try:
            proc.kill()
        except Exception:
            pass


def _open_path(path):
    """Открыть файл/папку системным приложением (без shell)."""
    path = str(path)
    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def _cmd_for_log(cmd):
    try:
        return " ".join(str(x) for x in cmd)
    except Exception:
        return repr(cmd)




def _ffmpeg_tool_names():
    """Имена бинарников ffmpeg/ffprobe для текущей ОС."""
    if sys.platform.startswith("win"):
        return "ffmpeg.exe", "ffprobe.exe"
    return "ffmpeg", "ffprobe"


def _has_ffmpeg_pair(folder):
    """True только если в папке есть и ffmpeg, и ffprobe.
    Для MP3/постобработки yt-dlp нужен именно ffprobe; одного ffmpeg мало.
    """
    try:
        d = Path(folder)
        ffmpeg_name, ffprobe_name = _ffmpeg_tool_names()
        return (d / ffmpeg_name).is_file() and (d / ffprobe_name).is_file()
    except Exception:
        return False


def _find_ffmpeg_pair_in_tree(root, max_depth=4):
    """Ищет ffmpeg+ffprobe внутри root, включая вложенные bin-папки.
    Это защищает от повторной загрузки, если архив был распакован не прямо
    в ./ffmpeg, а в ./ffmpeg/<имя_сборки>/bin.
    """
    try:
        root = Path(root)
        if not root.exists():
            return None
        if _has_ffmpeg_pair(root):
            return str(root)
        root_resolved = root.resolve()
        # Сначала частые варианты, чтобы не бегать по большому дереву.
        for rel in ("bin", "ffmpeg", "ffmpeg/bin"):
            d = root / rel
            if _has_ffmpeg_pair(d):
                return str(d)
        for ffmpeg_name in ("ffmpeg.exe", "ffmpeg"):
            for ffmpeg_path in root.rglob(ffmpeg_name):
                try:
                    rel_depth = len(ffmpeg_path.parent.resolve().relative_to(root_resolved).parts)
                except Exception:
                    rel_depth = 99
                if rel_depth > max_depth:
                    continue
                if _has_ffmpeg_pair(ffmpeg_path.parent):
                    return str(ffmpeg_path.parent)
    except Exception:
        logging.exception("_find_ffmpeg_pair_in_tree failed for %s", root)
    return None


_DEP_CACHE = {}
_DEP_CACHE_TTL = 5.0


def _cached(key, func):
    """Кэш поиска зависимостей на несколько секунд (rglob по диску не дёшев)."""
    now = time.monotonic()
    hit = _DEP_CACHE.get(key)
    if hit and now - hit[0] < _DEP_CACHE_TTL:
        return hit[1]
    val = func()
    _DEP_CACHE[key] = (now, val)
    return val


def clear_dep_cache():
    _DEP_CACHE.clear()


def find_ffmpeg():
    return _cached("ffmpeg", _find_ffmpeg_uncached)


def _find_ffmpeg_uncached():
    """Ищет рабочую пару ffmpeg + ffprobe.
    На Windows для стабильности используем только локальные бинарники рядом
    с программой: ./ffmpeg/, ./bin/ или PyInstaller bundle. PATH/WinGet не
    принимается, потому что именно внешний ffprobe дал падение MP3.
    Возвращает путь к ПАПКЕ с бинарниками (yt-dlp ожидает именно папку) или None.
    """
    ffmpeg_name, ffprobe_name = _ffmpeg_tool_names()

    candidates = []

    # 1) PyInstaller --add-binary "ffmpeg.exe;." / "ffprobe.exe;."
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass))

    # 2) Рядом с exe / скриптом
    base = _app_dir()
    candidates.append(base)

    # 3) Подпапки ./ffmpeg/, ./ffmpeg/bin/, ./bin/
    for sub in ("ffmpeg", "ffmpeg/bin", "bin"):
        candidates.append(base / sub)

    for d in candidates:
        if _has_ffmpeg_pair(d):
            logging.debug("find_ffmpeg: found local pair in %s", d)
            return str(Path(d))

    # Если ./ffmpeg уже есть, но распакован во вложенную папку, тоже считаем рабочим.
    nested = _find_ffmpeg_pair_in_tree(base / "ffmpeg")
    if nested:
        logging.debug("find_ffmpeg: found nested local pair in %s", nested)
        return nested

    # На Windows НЕ берём PATH/WinGet. Всё нужное должно лежать рядом.
    if sys.platform.startswith("win"):
        logging.debug("find_ffmpeg: local ffmpeg+ffprobe not found; PATH ignored on Windows")
        return None

    # На Linux/macOS допускаем системную пару из PATH.
    found_ffmpeg = shutil.which(ffmpeg_name)
    found_ffprobe = shutil.which(ffprobe_name)
    if found_ffmpeg and found_ffprobe:
        fdir = Path(found_ffmpeg).parent
        pdir = Path(found_ffprobe).parent
        if fdir == pdir and _has_ffmpeg_pair(fdir):
            return str(fdir)

    return None


def ensure_ffmpeg_in_path():
    """Если рабочая пара ffmpeg+ffprobe найдена — добавляет папку в PATH.
    Возвращает путь к папке (или None если пара не найдена).
    """
    folder = find_ffmpeg()
    if folder:
        cur = os.environ.get("PATH", "")
        if folder not in cur:
            os.environ["PATH"] = folder + os.pathsep + cur
    return folder


# Папка с ffmpeg (заполняется в main() через refresh_dependencies()).
FFMPEG_DIR = None


# ---------------- Поиск bundled yt-dlp.exe (для Win7-режима) ----------------

def _ytdlp_names():
    return ("yt-dlp_win7.exe", "yt-dlp.exe", "yt-dlp_win7", "yt-dlp")


def _ytdlp_local_bases():
    bases = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        bases.append(Path(meipass))
    bases.append(_app_dir())
    bases.append(_app_dir() / "yt-dlp")
    bases.append(_app_dir() / "bin")
    return bases


def _is_valid_ytdlp_file(path):
    """Минимальная проверка, что это не пустой/битый .part-файл."""
    try:
        p = Path(path)
        if not p.is_file():
            return False
        if p.name.lower().endswith(".part"):
            return False
        # Нормальный standalone yt-dlp.exe сейчас сильно больше 1 МБ.
        return p.stat().st_size >= 1024 * 1024
    except Exception:
        return False


def find_local_ytdlp_exe():
    return _cached("ytdlp", _find_local_ytdlp_exe_uncached)


def _find_local_ytdlp_exe_uncached():
    """Ищет yt-dlp рядом с текущим приложением, без PATH."""
    for base in _ytdlp_local_bases():
        for name in _ytdlp_names():
            p = base / name
            if _is_valid_ytdlp_file(p):
                return str(p)
            if p.exists():
                logging.warning("find_local_ytdlp_exe: игнорирую подозрительный файл %s size=%s",
                                p, p.stat().st_size if p.is_file() else "not-file")
    return None


def is_local_ytdlp_exe(path):
    """True, если yt-dlp лежит рядом с текущим приложением, а не в чужой папке/PATH."""
    if not path:
        return False
    try:
        resolved = Path(path).resolve()
        for base in _ytdlp_local_bases():
            try:
                resolved.relative_to(Path(base).resolve())
                return True
            except ValueError:
                continue
    except Exception:
        pass
    return False


def find_ytdlp_exe():
    """Ищет standalone yt-dlp[_win7] только рядом с текущим приложением.

    На Windows PATH/WinGet/глобальные Python Scripts специально игнорируются:
    приложение должно само скачать yt-dlp.exe рядом с собой и работать только
    через локальный файл.
    """
    local = find_local_ytdlp_exe()
    if local:
        return local
    logging.debug("find_ytdlp_exe: local yt-dlp not found; PATH ignored")
    return None


def can_use_python_ytdlp_module():
    """Python-модуль yt_dlp разрешён только не на Windows.

    На Windows используем исключительно локальный yt-dlp.exe рядом с программой,
    чтобы не зависеть от того, что установлено на ПК.
    """
    return (not sys.platform.startswith("win")) and (yt_dlp is not None)


# Путь к локальному yt-dlp (заполняется в main() через refresh_dependencies()).
YTDLP_EXE = None


# ---------------- Авто-загрузка зависимостей рядом с программой ----------------
# Стабильные «latest» ссылки GitHub (редиректят на актуальный ассет).
YTDLP_EXE_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
YTDLP_SUMS_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/SHA2-256SUMS"
# Официальные ffmpeg-сборки самого yt-dlp (рекомендованы в README yt-dlp).
FFMPEG_ZIP_URL = (
    "https://github.com/yt-dlp/FFmpeg-Builds/releases/latest/download/"
    "ffmpeg-master-latest-win64-gpl.zip"
)


def refresh_dependencies():
    """Перечитать наличие yt-dlp.exe и ffmpeg после возможной загрузки.
    Обновляет глобальные YTDLP_EXE и FFMPEG_DIR."""
    global YTDLP_EXE, FFMPEG_DIR
    clear_dep_cache()
    FFMPEG_DIR = ensure_ffmpeg_in_path()
    YTDLP_EXE = find_ytdlp_exe()
    logging.info("refresh_dependencies: ytdlp=%s ffmpeg_dir=%s", YTDLP_EXE, FFMPEG_DIR)
    return YTDLP_EXE, FFMPEG_DIR


class DependencyWorker(QThread):
    """Фоновая докачка недостающих бинарников (yt-dlp.exe, ffmpeg) в папку
    рядом с программой. Только Windows; на других ОС просто рапортует.

    force_ytdlp=True — перекачать yt-dlp.exe заново (обновление до latest).
    force_ffmpeg=True — перекачать ffmpeg.exe + ffprobe.exe заново."""
    progress = Signal(float)
    status = Signal(str)
    done = Signal()

    def __init__(self, force_ytdlp=False, force_ffmpeg=False, skip_ffmpeg=False, parent=None):
        super().__init__(parent)
        self.force_ytdlp = force_ytdlp
        self.force_ffmpeg = force_ffmpeg
        self.skip_ffmpeg = skip_ffmpeg
        self.errors = []

    def _fetch_text(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")

    def _expected_ytdlp_sha256(self):
        """SHA256 yt-dlp.exe из официального SHA2-256SUMS (None если не получилось)."""
        try:
            for line in self._fetch_text(YTDLP_SUMS_URL).splitlines():
                parts = line.split()
                if len(parts) == 2 and parts[1].lstrip("*") == "yt-dlp.exe":
                    return parts[0].lower()
        except Exception:
            logging.exception("не смог получить SHA2-256SUMS")
        return None

    def _download(self, url, dest, label, expected_sha256=None):
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        req = urllib.request.Request(
            url, headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"}
        )
        logging.info("download_start: %s -> %s", url, dest)
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        with urllib.request.urlopen(req, timeout=60) as resp:
            try:
                total = int(resp.headers.get("Content-Length") or 0)
            except (TypeError, ValueError):
                total = 0
            read = 0
            last_emit = 0.0
            last_logged_mb = -1
            sha = hashlib.sha256()
            with open(tmp, "wb") as f:
                while True:
                    if self.isInterruptionRequested():
                        raise RuntimeError("отменено")
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
                    sha.update(chunk)
                    read += len(chunk)
                    now = time.monotonic()
                    if total:
                        self.progress.emit(min(100.0, read * 100.0 / total))
                    # Не спамим Qt тысячами сигналов при скачивании ffmpeg.zip.
                    if now - last_emit >= 0.25:
                        tail = f" / {_human_size(total)}" if total else ""
                        self.status.emit(f"{label}: {_human_size(read)}{tail}")
                        last_emit = now
                    mb = int(read // (1024 * 1024))
                    if mb >= 1 and mb % 10 == 0 and mb != last_logged_mb:
                        logging.info("download_progress: %s %s%s", label, _human_size(read),
                                     f" / {_human_size(total)}" if total else "")
                        last_logged_mb = mb
        if expected_sha256:
            got = sha.hexdigest().lower()
            if got != expected_sha256:
                try:
                    tmp.unlink()
                except OSError:
                    pass
                raise RuntimeError(f"SHA256 не совпал ({got[:12]}… ≠ {expected_sha256[:12]}…)")
            logging.info("sha256 OK: %s", dest)
        os.replace(tmp, dest)
        logging.info("download_done: %s", dest)
        self.status.emit(f"{label}: готово")
        self.progress.emit(100.0)

    def _download_ffmpeg(self, dest_dir):
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        tmpzip = dest_dir / "_ffmpeg_download.zip"
        self._download(FFMPEG_ZIP_URL, tmpzip, "ffmpeg.zip")
        self.status.emit("Распаковка ffmpeg...")
        extracted = []
        with zipfile.ZipFile(tmpzip) as z:
            for member in z.namelist():
                base = os.path.basename(member)
                if base.lower() in ("ffmpeg.exe", "ffprobe.exe"):
                    # Сначала во временный файл, потом атомарная замена.
                    part = dest_dir / (base + ".part")
                    with z.open(member) as src, open(part, "wb") as out:
                        shutil.copyfileobj(src, out)
                    os.replace(part, dest_dir / base)
                    extracted.append(base.lower())
        try:
            tmpzip.unlink()
        except OSError:
            pass
        missing = [x for x in ("ffmpeg.exe", "ffprobe.exe") if x not in extracted]
        if missing:
            raise RuntimeError("не найдено в скачанном архиве: " + ", ".join(missing))

    def run(self):
        logging.info("DependencyWorker.run force_ytdlp=%s force_ffmpeg=%s",
                     self.force_ytdlp, self.force_ffmpeg)
        is_win = sys.platform.startswith("win")
        target = _app_dir()
        errors = []

        local_ytdlp = find_local_ytdlp_exe()
        if local_ytdlp and not self.force_ytdlp:
            logging.info("DependencyWorker: yt-dlp уже рядом, не скачиваю: %s", local_ytdlp)
            self.status.emit("yt-dlp.exe уже лежит рядом — не скачиваю повторно.")
        elif self.force_ytdlp or local_ytdlp is None:
            if is_win:
                try:
                    verb = "Обновляю" if self.force_ytdlp else "Скачиваю"
                    self.status.emit(f"{verb} yt-dlp.exe...")
                    # Кладём свежий рядом с программой — он приоритетнее
                    # любого старого yt-dlp.exe из PATH.
                    expected = self._expected_ytdlp_sha256()
                    if not expected:
                        raise RuntimeError("не удалось получить SHA256 для проверки yt-dlp.exe")
                    self._download(YTDLP_EXE_URL, target / "yt-dlp.exe", "yt-dlp.exe",
                                   expected_sha256=expected)
                except Exception as exc:
                    logging.exception("DependencyWorker yt-dlp failed")
                    traceback.print_exc()
                    errors.append(f"yt-dlp: {exc}")
            else:
                errors.append("yt-dlp: авто-загрузка только для Windows "
                              "(установи: pip install -U yt-dlp)")

        local_ffmpeg = find_ffmpeg()
        if self.skip_ffmpeg and not self.force_ffmpeg:
            logging.info("DependencyWorker: ffmpeg пропущен (пользователь отказался)")
        elif local_ffmpeg and not self.force_ffmpeg:
            logging.info("DependencyWorker: ffmpeg+ffprobe уже рядом, не скачиваю: %s", local_ffmpeg)
            self.status.emit("ffmpeg + ffprobe уже лежат рядом — не скачиваю повторно.")
        elif self.force_ffmpeg or local_ffmpeg is None:
            if is_win:
                try:
                    self.status.emit("Скачиваю ffmpeg + ffprobe...")
                    self._download_ffmpeg(target / "ffmpeg")
                except Exception as exc:
                    logging.exception("DependencyWorker ffmpeg failed")
                    traceback.print_exc()
                    errors.append(f"ffmpeg: {exc}")
            else:
                errors.append("ffmpeg: установи через пакетный менеджер ОС")

        refresh_dependencies()
        self.errors = list(errors)
        if errors:
            logging.error("DependencyWorker done with errors: %s", errors)
            self.status.emit("Загрузка завершена с замечаниями: " + " | ".join(errors))
        else:
            logging.info("DependencyWorker done OK")
            self.status.emit("Зависимости на месте.")
        self.done.emit()


# ---------------- Стили / темы ----------------
SYSTEM_DEFAULT = "Системный по умолчанию"

# Кастомные палитры (Qt стиль = Fusion + кастомный QPalette).
CUSTOM_PALETTES = {
    "Fusion Light": {
        "Window":          "#f0f0f0",
        "WindowText":      "#202020",
        "Base":            "#ffffff",
        "AlternateBase":   "#e9e9e9",
        "Text":            "#202020",
        "Button":          "#e8e8e8",
        "ButtonText":      "#202020",
        "Highlight":       "#3874f2",
        "HighlightedText": "#ffffff",
        "ToolTipBase":     "#ffffe1",
        "ToolTipText":     "#202020",
        "PlaceholderText": "#888888",
        "Link":            "#1e64ff",
    },
    "Fusion Dark": {
        "Window":          "#2b2b2b",
        "WindowText":      "#e6e6e6",
        "Base":            "#1e1e1e",
        "AlternateBase":   "#2a2a2a",
        "Text":            "#e6e6e6",
        "Button":          "#353535",
        "ButtonText":      "#e6e6e6",
        "Highlight":       "#2a82da",
        "HighlightedText": "#ffffff",
        "ToolTipBase":     "#3a3a3a",
        "ToolTipText":     "#e6e6e6",
        "PlaceholderText": "#888888",
        "Link":            "#56a8ff",
    },
    "Solarized Light": {
        "Window":          "#fdf6e3",
        "WindowText":      "#073642",
        "Base":            "#fffbf0",
        "AlternateBase":   "#eee8d5",
        "Text":            "#073642",
        "Button":          "#eee8d5",
        "ButtonText":      "#073642",
        "Highlight":       "#268bd2",
        "HighlightedText": "#fdf6e3",
        "PlaceholderText": "#93a1a1",
        "Link":            "#268bd2",
    },
    "Solarized Dark": {
        "Window":          "#002b36",
        "WindowText":      "#eee8d5",
        "Base":            "#073642",
        "AlternateBase":   "#0a3540",
        "Text":            "#eee8d5",
        "Button":          "#0e3a44",
        "ButtonText":      "#eee8d5",
        "Highlight":       "#268bd2",
        "HighlightedText": "#fdf6e3",
        "PlaceholderText": "#7a8e8e",
        "Link":            "#2aa198",
    },
    "Nord": {
        "Window":          "#2e3440",
        "WindowText":      "#eceff4",
        "Base":            "#3b4252",
        "AlternateBase":   "#434c5e",
        "Text":            "#eceff4",
        "Button":          "#4c566a",
        "ButtonText":      "#eceff4",
        "Highlight":       "#88c0d0",
        "HighlightedText": "#2e3440",
        "PlaceholderText": "#8a93a3",
        "Link":            "#81a1c1",
    },
    "Dracula": {
        "Window":          "#282a36",
        "WindowText":      "#f8f8f2",
        "Base":            "#1e1f29",
        "AlternateBase":   "#343746",
        "Text":            "#f8f8f2",
        "Button":          "#44475a",
        "ButtonText":      "#f8f8f2",
        "Highlight":       "#bd93f9",
        "HighlightedText": "#1e1f29",
        "PlaceholderText": "#8c8e9b",
        "Link":            "#8be9fd",
    },
    "Monokai": {
        "Window":          "#272822",
        "WindowText":      "#f8f8f2",
        "Base":            "#1d1e19",
        "AlternateBase":   "#2f312a",
        "Text":            "#f8f8f2",
        "Button":          "#3e3d32",
        "ButtonText":      "#f8f8f2",
        "Highlight":       "#fd971f",
        "HighlightedText": "#272822",
        "PlaceholderText": "#90917f",
        "Link":            "#a6e22e",
    },
    "High Contrast": {
        "Window":          "#000000",
        "WindowText":      "#ffffff",
        "Base":            "#000000",
        "AlternateBase":   "#1a1a1a",
        "Text":            "#ffffff",
        "Button":          "#101010",
        "ButtonText":      "#ffffff",
        "Highlight":       "#ffff00",
        "HighlightedText": "#000000",
        "PlaceholderText": "#bbbbbb",
        "Link":            "#00e5ff",
    },
}


def _palette_role(name):
    return getattr(QPalette.ColorRole, name)


def apply_style(app, style_name, default_style_name, default_palette):
    """Применить выбранный стиль ко всему приложению."""
    if style_name == SYSTEM_DEFAULT:
        if default_style_name:
            app.setStyle(default_style_name)
        app.setPalette(default_palette)
        return

    if style_name in QStyleFactory.keys():
        app.setStyle(style_name)
        app.setPalette(app.style().standardPalette())
        return

    if style_name in CUSTOM_PALETTES:
        if "Fusion" in QStyleFactory.keys():
            app.setStyle("Fusion")
        spec = CUSTOM_PALETTES[style_name]
        pal = QPalette()
        for role_name, hex_color in spec.items():
            try:
                role = _palette_role(role_name)
            except AttributeError:
                continue
            pal.setColor(role, QColor(hex_color))
        # Производные роли для рамок/тени.
        base = QColor(spec.get("Window", "#888888"))
        pal.setColor(QPalette.ColorRole.Light,    base.lighter(130))
        pal.setColor(QPalette.ColorRole.Midlight, base.lighter(115))
        pal.setColor(QPalette.ColorRole.Mid,      base.darker(115))
        pal.setColor(QPalette.ColorRole.Dark,     base.darker(150))
        pal.setColor(QPalette.ColorRole.Shadow,   base.darker(200))
        app.setPalette(pal)


def make_gear_icon(size=18, fg="#404040"):
    """Простая иконка-шестерёнка через QPainter (без внешних ресурсов)."""
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.TextAntialiasing, True)
    f = QFont()
    f.setPointSize(int(size * 0.7))
    p.setFont(f)
    p.setPen(QColor(fg))
    p.drawText(0, 0, size, size, Qt.AlignCenter, "⚙")
    p.end()
    return QIcon(pm)


# ---------------- Воркер сканирования форматов ----------------
def run_interruptible(thread, cmd, timeout):
    """subprocess с возможностью прервать через thread.requestInterruption().
    Возвращает (rc, stdout, stderr); rc=None — прервано."""
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
        text=True, encoding="utf-8", errors="replace", **_hidden_kwargs(),
    )
    deadline = time.monotonic() + timeout
    while True:
        try:
            out, err = proc.communicate(timeout=0.3)
            return proc.returncode, out or "", err or ""
        except subprocess.TimeoutExpired:
            if thread.isInterruptionRequested():
                _kill_process_tree(proc)
                proc.communicate()
                return None, "", ""
            if time.monotonic() > deadline:
                _kill_process_tree(proc)
                proc.communicate()
                raise


class ProbeWorker(QThread):
    """Фоновое сканирование форматов yt-dlp -J. Не блокирует UI."""
    done = Signal(list, str)   # list of format-dicts, title
    failed = Signal(str)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = normalize_video_url(url)

    def run(self):
        try:
            logging.info("ProbeWorker.run url=%s", self.url)
            if YTDLP_EXE:
                cmd = [YTDLP_EXE, "-J", "--no-playlist", "--no-warnings", self.url]
            elif can_use_python_ytdlp_module():
                cmd = [sys.executable, "-m", "yt_dlp", "-J", "--no-playlist", "--no-warnings", self.url]
            else:
                self.failed.emit("локальный yt-dlp.exe ещё не подготовлен")
                return

            logging.info("ProbeWorker cmd: %s", _cmd_for_log(cmd))
            rc, out, err = run_interruptible(self, cmd, timeout=60)
            if rc is None:
                logging.info("ProbeWorker interrupted")
                return
            logging.info("ProbeWorker rc=%s stdout_len=%s stderr_len=%s",
                         rc, len(out or ""), len(err or ""))
            if err:
                logging.debug("ProbeWorker stderr: %s", err[:8000])
            if rc != 0:
                self.failed.emit(err.splitlines()[-1][:200] if err.strip() else f"yt-dlp exit code {rc}")
                return
            try:
                data = json.loads(out)
            except json.JSONDecodeError as exc:
                self.failed.emit(f"Не смог разобрать JSON: {exc}")
                return
            formats = data.get("formats") or []
            title = data.get("title") or ""
            self.done.emit(formats, title)
        except subprocess.TimeoutExpired:
            logging.exception("ProbeWorker timeout")
            self.failed.emit("Таймаут сканирования (60 сек)")
        except Exception as exc:
            logging.exception("ProbeWorker failed")
            self.failed.emit(str(exc))


class FormatsListWorker(QThread):
    """yt-dlp -F в фоне для «Диагностики форматов» (UI не зависает)."""
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.cmd = cmd

    def run(self):
        try:
            rc, out, err = run_interruptible(self, self.cmd, timeout=60)
            if rc is None:
                return
            self.done.emit((out or "") + (("\n" + err) if err else ""))
        except subprocess.TimeoutExpired:
            self.failed.emit("yt-dlp не отвечает за 60 секунд.")
        except Exception as exc:
            logging.exception("FormatsListWorker failed")
            self.failed.emit(f"Не удалось запустить yt-dlp:\n{exc}")


# ---------------- Проверка результата ----------------
def ffprobe_has_stream(path, ffmpeg_dir, stream_selector):
    """True/False — есть ли поток; None — проверить невозможно."""
    if not ffmpeg_dir:
        return None
    probe = Path(ffmpeg_dir) / _ffmpeg_tool_names()[1]
    if not probe.exists():
        return None
    cmd = [
        str(probe), "-v", "error",
        "-select_streams", stream_selector,
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        str(path),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=20, **_hidden_kwargs())
        logging.info("ffprobe verify %s %s rc=%s out=%r err=%r", stream_selector, path,
                     r.returncode, (r.stdout or "")[:200], (r.stderr or "")[:200])
        return r.returncode == 0 and bool((r.stdout or "").strip())
    except Exception:
        logging.exception("ffprobe verify failed: %s", path)
        return None


def mark_bad_noaudio(paths):
    for p in paths:
        try:
            p = Path(p)
            bad = p.with_name(p.name + ".noaudio")
            if bad.exists():
                bad.unlink()
            p.rename(bad)
            logging.warning("renamed no-audio file: %s -> %s", p, bad)
        except Exception:
            logging.exception("failed to rename no-audio file: %s", p)


def verify_outputs_have_audio(paths, ffmpeg_dir, is_audio_mode):
    """Проверяет ТОЛЬКО файлы этой загрузки. Возвращает текст ошибки или None."""
    files = [Path(p) for p in paths if p and Path(p).is_file()]
    if not files or not ffmpeg_dir:
        return None
    bad = [p for p in files if ffprobe_has_stream(p, ffmpeg_dir, "a:0") is False]
    if not bad:
        return None
    mark_bad_noaudio(bad)
    if is_audio_mode:
        return ("Ошибка: сайт отдал файл без аудиодорожки. Файл помечен .noaudio; "
                "нужен другой формат/обновление yt-dlp вручную через ⚙.")
    return ("Ошибка: скачанное видео оказалось без звука. Файл помечен .noaudio; "
            "программа не считает такую загрузку успешной.")


def resolve_format(quality_name):
    """quality_name → (format-строка, is_audio_mode)."""
    is_audio_mode = is_audio_quality(quality_name)
    if is_audio_mode:
        return AUDIO_SOURCE_FORMAT, True
    # Пресет по имени или уже готовая format-строка от ProbeWorker.
    fmt = QUALITY_PRESETS.get(quality_name, quality_name)
    return force_video_with_audio_format(fmt), False


class ProgressMerger:
    """Склеивает прогресс нескольких потоков (видео+аудио) в один 0→100."""

    def __init__(self, streams):
        self.streams = max(1, streams)
        self.phase = 0
        self.last = 0.0

    def feed(self, pct):
        if pct + 50 < self.last and self.phase + 1 < self.streams:
            self.phase += 1
        self.last = pct
        return min(100.0, (self.phase * 100.0 + pct) / self.streams)


def _stream_count(fmt, is_audio_mode):
    return 1 if is_audio_mode else (2 if "+" in (fmt or "") else 1)


class DownloadCancelled(Exception):
    pass


# ---------------- Воркер (Python-модуль yt_dlp, не Windows) ----------------
class DownloadWorker(QThread):
    progress = Signal(float)
    status = Signal(str)
    finished_ok = Signal()
    failed = Signal(str)
    cancelled = Signal()

    def __init__(self, url, folder, quality_name, parent=None):
        super().__init__(parent)
        self.url = normalize_video_url(url)
        self.folder = folder
        self.quality_name = quality_name
        self._cancel = False
        self._outputs = []
        self._merger = ProgressMerger(1)

    def cancel(self):
        self._cancel = True

    def _hook(self, data):
        if self._cancel:
            raise DownloadCancelled()
        st = data.get("status")
        if st == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes", 0)
            if total:
                pct = max(0.0, min(100.0, downloaded * 100.0 / total))
                self.progress.emit(self._merger.feed(pct))
            speed = (data.get("_speed_str") or "").strip()
            eta = (data.get("_eta_str") or "").strip()
            percent_str = (data.get("_percent_str") or "").strip()
            text = f"Скачивание: {percent_str}"
            if speed:
                text += f" | {speed}"
            if eta:
                text += f" | осталось {eta}"
            self.status.emit(text)
        elif st == "finished":
            self.status.emit("Файл скачан, обработка...")

    def _post_hook(self, filepath):
        self._outputs.append(filepath)

    def run(self):
        try:
            logging.info("DownloadWorker.run url=%s folder=%s quality=%s",
                         self.url, self.folder, self.quality_name)
            fmt, is_audio_mode = resolve_format(self.quality_name)
            suffix = "audio" if is_audio_mode else "video"
            outtmpl = str(Path(self.folder) / f"%(title).180B [%(id)s] [{suffix}].%(ext)s")

            ffmpeg_dir = ensure_ffmpeg_in_path()
            has_ffmpeg = ffmpeg_dir is not None

            ydl_opts = {
                "format": fmt,
                "outtmpl": outtmpl,
                "noplaylist": True,
                "windowsfilenames": True,
                "ignoreerrors": False,
                "progress_hooks": [self._hook],
                "post_hooks": [self._post_hook],
                "quiet": True,
                "no_warnings": False,
            }
            if has_ffmpeg:
                ydl_opts["ffmpeg_location"] = ffmpeg_dir

            if is_audio_mode:
                if self.quality_name == "Только аудио MP3" and has_ffmpeg:
                    ydl_opts["postprocessors"] = [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }]
                elif not has_ffmpeg:
                    self.status.emit("ffmpeg/ffprobe не найдены — скачиваю аудио без перекодирования в MP3...")
            else:
                if has_ffmpeg:
                    ydl_opts["merge_output_format"] = "mp4"
                else:
                    ydl_opts["format"] = VIDEO_WITH_AUDIO_FALLBACK
                    self.status.emit("ffmpeg/ffprobe не найдены — ищу одиночный видеофайл со звуком.")
            self._merger = ProgressMerger(_stream_count(ydl_opts["format"], is_audio_mode))

            logging.info("DownloadWorker opts: %s",
                         {k: v for k, v in ydl_opts.items() if k not in ("progress_hooks", "post_hooks")})
            self.status.emit("Скачивание...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            if self._cancel:
                self.cancelled.emit()
                return
            err = verify_outputs_have_audio(self._outputs, ffmpeg_dir, is_audio_mode)
            if err:
                self.failed.emit(err)
                return
            self.progress.emit(100.0)
            self.finished_ok.emit()
        except Exception as exc:
            if self._cancel:
                logging.info("DownloadWorker cancelled")
                self.cancelled.emit()
                return
            logging.exception("DownloadWorker failed")
            self.failed.emit(f"Ошибка: {exc}")


# ---------------- Воркер: subprocess к локальному yt-dlp.exe ----------------
class DownloadWorkerExe(QThread):
    """Скачивание через standalone yt-dlp.exe как subprocess."""
    progress = Signal(float)
    status = Signal(str)
    finished_ok = Signal()
    failed = Signal(str)
    cancelled = Signal()

    PROGRESS_TAG = "PYDL_PROGRESS"
    FILE_TAG = "PYDL_FILE"

    def __init__(self, url, folder, quality_name, ytdlp_exe, parent=None):
        super().__init__(parent)
        self.url = normalize_video_url(url)
        self.folder = folder
        self.quality_name = quality_name
        self.ytdlp_exe = ytdlp_exe
        self._proc = None
        self._cancel = False

    def cancel(self):
        self._cancel = True
        _kill_process_tree(self._proc)

    def _build_cmd(self, has_ffmpeg, ffmpeg_dir):
        fmt, is_audio_mode = resolve_format(self.quality_name)
        suffix = "audio" if is_audio_mode else "video"
        outtmpl = str(Path(self.folder) / f"%(title).180B [%(id)s] [{suffix}].%(ext)s")

        cmd = [
            self.ytdlp_exe,
            "--newline",
            "--no-colors",
            "--encoding", "utf-8",
            "--progress",
            # Машино-читаемая строка: tag|percent|downloaded|total|speed|eta
            "--progress-template",
            (
                f"download:{self.PROGRESS_TAG}|%(progress._percent_str)s"
                f"|%(progress._downloaded_bytes_str)s"
                f"|%(progress._total_bytes_str)s"
                f"|%(progress._speed_str)s"
                f"|%(progress._eta_str)s"
            ),
            # Итоговый путь файла этой загрузки — проверяем только его.
            "--print", f"after_move:{self.FILE_TAG}|%(filepath)s",
            "--windows-filenames",
            "--no-playlist",
            "-o", outtmpl,
        ]
        if has_ffmpeg:
            cmd.extend(["--ffmpeg-location", ffmpeg_dir])

        if is_audio_mode:
            cmd.extend(["-f", fmt])
            if self.quality_name == "Только аудио MP3" and has_ffmpeg:
                cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "320"])
        else:
            if has_ffmpeg:
                cmd.extend([
                    "-f", fmt,
                    "-S", "vcodec:h264,acodec:aac,ext:mp4:m4a,res",
                    "--merge-output-format", "mp4",
                ])
            else:
                fmt = VIDEO_WITH_AUDIO_FALLBACK
                cmd.extend(["-f", fmt])

        cmd.append(self.url)
        return cmd, fmt, is_audio_mode

    @staticmethod
    def _parse_percent(s):
        m = re.search(r"(\d+(?:\.\d+)?)\s*%", s)
        if not m:
            return None
        try:
            v = float(m.group(1))
            if 0.0 <= v <= 100.0:
                return v
        except ValueError:
            pass
        return None

    def run(self):
        try:
            logging.info("DownloadWorkerExe.run url=%s folder=%s quality=%s ytdlp=%s",
                         self.url, self.folder, self.quality_name, self.ytdlp_exe)
            ffmpeg_dir = ensure_ffmpeg_in_path()
            has_ffmpeg = ffmpeg_dir is not None
            cmd, fmt, is_audio_mode = self._build_cmd(has_ffmpeg, ffmpeg_dir)
            if is_audio_mode and not has_ffmpeg:
                self.status.emit("ffmpeg/ffprobe не найдены — скачиваю аудио без перекодирования в MP3...")
            elif not has_ffmpeg:
                self.status.emit("ffmpeg/ffprobe не найдены — ищу одиночный видеофайл со звуком...")
            logging.info("DownloadWorkerExe cmd: %s", _cmd_for_log(cmd))
            logging.info("DownloadWorkerExe cwd=%s has_ffmpeg=%s ffmpeg_dir=%s",
                         self.folder, has_ffmpeg, ffmpeg_dir)

            self.status.emit("Скачивание (yt-dlp.exe)...")
            merger = ProgressMerger(_stream_count(fmt, is_audio_mode))
            outputs = []
            if self._cancel:
                self.cancelled.emit()
                return
            self._proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                text=True, encoding="utf-8", errors="replace",
                cwd=self.folder, **_hidden_kwargs(),
            )
            last_error_line = ""
            for raw in self._proc.stdout:
                line = raw.rstrip()
                if not line:
                    continue
                logging.debug("yt-dlp: %s", line)
                if line.startswith(self.FILE_TAG + "|"):
                    outputs.append(line[len(self.FILE_TAG) + 1:].strip())
                    self.status.emit("Обработка...")
                elif self.PROGRESS_TAG in line:
                    idx = line.find(self.PROGRESS_TAG)
                    parts = line[idx:].split("|")
                    pct_str = parts[1].strip() if len(parts) > 1 else ""
                    downloaded = parts[2].strip() if len(parts) > 2 else ""
                    total = parts[3].strip() if len(parts) > 3 else ""
                    speed = parts[4].strip() if len(parts) > 4 else ""
                    eta = parts[5].strip() if len(parts) > 5 else ""
                    pct = self._parse_percent(pct_str)
                    if pct is not None:
                        self.progress.emit(merger.feed(pct))
                    text_parts = [f"Скачивание: {pct_str}"] if pct_str else ["Скачивание..."]
                    if merger.streams > 1:
                        text_parts[0] += f" (поток {merger.phase + 1}/{merger.streams})"
                    if downloaded and total:
                        text_parts.append(f"{downloaded}/{total}")
                    if speed and speed.lower() != "unknown":
                        text_parts.append(speed)
                    if eta and eta.lower() != "unknown":
                        text_parts.append(f"осталось {eta}")
                    self.status.emit(" | ".join(text_parts))
                elif line.startswith("ERROR:"):
                    last_error_line = line
                    self.status.emit(line[:200])
                elif line.startswith("WARNING:"):
                    self.status.emit(line[:200])
            rc = self._proc.wait()
            logging.info("DownloadWorkerExe rc=%s last_error=%s outputs=%s", rc, last_error_line, outputs)
            if self._cancel:
                self.cancelled.emit()
                return
            if rc == 0:
                err = verify_outputs_have_audio(outputs, ffmpeg_dir, is_audio_mode)
                if err:
                    self.failed.emit(err)
                    return
                self.progress.emit(100.0)
                self.finished_ok.emit()
            else:
                msg = last_error_line or f"yt-dlp.exe завершился с кодом {rc}"
                self.failed.emit(f"Ошибка: {msg}")
        except Exception as exc:
            if self._cancel:
                self.cancelled.emit()
                return
            logging.exception("DownloadWorkerExe failed")
            self.failed.emit(f"Ошибка: {exc}")


# ---------------- Окно ----------------
class VideoDownloaderWindow(QMainWindow):
    def __init__(self, app, default_style_name, default_palette):
        super().__init__()
        self.app = app
        self.default_style_name = default_style_name
        self.default_palette = QPalette(default_palette)
        self.settings = QSettings("AI_Modules", APP_NAME)

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(900, 420)
        self.setMinimumSize(840, 380)

        self.worker = None
        self._probe_worker = None
        self._old_probe_workers = []
        self._formats_worker = None
        self.is_downloading = False
        self._closing = False
        # Пользователь отказался от автозагрузки ffmpeg (~200 МБ) — не спрашиваем снова.
        self._ffmpeg_declined = self.settings.value("ffmpeg_declined", False, type=bool)

        self._build_ui()
        self._restore_style()
        self._quitting = False
        self.upd_dialog = self._build_update_dialog()

        # Авто-докачка недостающих зависимостей рядом с программой (Win).
        self._dep_worker = None
        self._last_quality = None        # последний запрошенный формат (для повтора)
        self._retry_quality = None       # что повторить после подготовки/обновления
        self._deps_retry_is_repair = False  # True только для автоповтора после ошибки
        self._update_retry_pending = False  # защита от зацикливания обновлений
        self._pending_probe_after_deps = False  # сканирование ссылки после автоустановки
        self._audio_original_fallback_used = False  # защита fallback MP3→оригинал
        QTimer.singleShot(400, lambda: self._fetch_dependencies(manual=False))

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(8)

        # Заголовок + шестерёнка
        header = QHBoxLayout()
        title = QLabel(f"{APP_NAME} v{APP_VERSION}")
        f = title.font(); f.setPointSize(13); f.setBold(True); title.setFont(f)
        header.addWidget(title)
        header.addStretch(1)

        self.style_btn = QToolButton()
        self.style_btn.setText("⚙")
        self.style_btn.setToolTip("Сменить стиль оформления")
        gf = self.style_btn.font(); gf.setPointSize(14); self.style_btn.setFont(gf)
        self.style_btn.setFixedSize(36, 32)
        self.style_btn.setPopupMode(QToolButton.InstantPopup)
        self.style_btn.setMenu(self._build_style_menu())
        # Убираем стрелку у меню
        self.style_btn.setStyleSheet("QToolButton::menu-indicator { image: none; width: 0; }")
        self.upd_btn = QPushButton("⬆")
        self.upd_btn.setFixedHeight(32)
        uf = self.upd_btn.font(); uf.setBold(True); self.upd_btn.setFont(uf)
        self.upd_btn.clicked.connect(self.show_update)
        self.upd_btn.hide()
        header.addWidget(self.upd_btn)
        header.addWidget(self.style_btn)
        root.addLayout(header)

        # Ссылка
        url_box = QGroupBox("Ссылка")
        url_lay = QHBoxLayout(url_box)
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Вставь URL видео (Ctrl+V) — форматы автоматически просканируются")
        self.url_edit.setClearButtonEnabled(True)
        self.url_edit.setFocus()
        # Авто-сканирование форматов при изменении URL.
        self.url_edit.textChanged.connect(self._on_url_changed)
        url_lay.addWidget(self.url_edit, 1)
        paste_btn = QPushButton("Вставить")
        paste_btn.clicked.connect(self.paste_url)
        url_lay.addWidget(paste_btn)
        self.paste_btn = paste_btn
        root.addWidget(url_box)

        # Настройки
        settings = QGridLayout()
        settings.setHorizontalSpacing(8)
        settings.setVerticalSpacing(6)
        settings.addWidget(QLabel("Качество:"), 0, 0)
        self.quality_combo = QComboBox()
        self._fill_combo_with_presets()
        self.quality_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.quality_combo.setMinimumWidth(280)
        settings.addWidget(self.quality_combo, 0, 1)

        settings.addWidget(QLabel("Папка:"), 0, 2)
        self.dir_edit = QLineEdit(str(_downloads_dir()))
        self.dir_edit.setClearButtonEnabled(True)
        self.dir_edit.setMinimumWidth(160)
        settings.addWidget(self.dir_edit, 0, 3)
        browse_btn = QPushButton("...")
        browse_btn.setFixedWidth(34)
        browse_btn.clicked.connect(self.choose_folder)
        settings.addWidget(browse_btn, 0, 4)
        self.browse_btn = browse_btn
        # Stretch: качество (3) растягивается больше чем папка (1).
        settings.setColumnStretch(1, 3)
        settings.setColumnStretch(3, 1)
        root.addLayout(settings)

        # Кнопки: две «скачать» по центру, «Открыть папку» справа
        actions = QHBoxLayout()
        actions.addStretch(1)

        self.download_btn = QPushButton("Скачать видео")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setMinimumWidth(220)
        df = self.download_btn.font(); df.setPointSize(11); df.setBold(True); self.download_btn.setFont(df)
        self.download_btn.clicked.connect(self.start_download)
        self._dl_btn_text = "Скачать видео"   # запоминаем оригинал
        actions.addWidget(self.download_btn)

        self.download_audio_btn = QPushButton("Скачать только звук")
        self.download_audio_btn.setMinimumHeight(40)
        self.download_audio_btn.setMinimumWidth(200)
        af = self.download_audio_btn.font(); af.setPointSize(11); af.setBold(True); self.download_audio_btn.setFont(af)
        self.download_audio_btn.setToolTip("Извлечь только звук в MP3 320 kbps (не зависит от выбранного качества)")
        self.download_audio_btn.clicked.connect(self.start_download_audio)
        self._dl_audio_btn_text = "Скачать только звук"   # запоминаем оригинал
        actions.addWidget(self.download_audio_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setToolTip("Остановить текущую загрузку")
        self.cancel_btn.clicked.connect(self.cancel_download)
        actions.addWidget(self.cancel_btn)

        actions.addStretch(1)

        self.open_folder_btn = QPushButton("Открыть папку")
        self.open_folder_btn.setMinimumHeight(40)
        self.open_folder_btn.clicked.connect(self.open_folder)
        actions.addWidget(self.open_folder_btn)
        root.addLayout(actions)

        # Прогресс
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        root.addWidget(self.progress)

        self.status_label = QLabel(f"Готово. Версия {APP_VERSION}")
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)

        # Статус ffmpeg при старте
        self.ff_lbl = QLabel()
        self.ff_lbl.setWordWrap(True)
        root.addWidget(self.ff_lbl)

        # Статус yt-dlp движка при старте
        self.yl_lbl = QLabel()
        self.yl_lbl.setWordWrap(True)
        root.addWidget(self.yl_lbl)

        self._refresh_dep_labels()

        hint = QLabel("Подсказка: Ctrl+V — вставить, правый клик на поле — контекстное меню.")
        hint.setStyleSheet("color: #888;")
        root.addWidget(hint)

        log_hint = QLabel(f"Лог: {LOG_FILE}")
        log_hint.setWordWrap(True)
        log_hint.setStyleSheet("color: #777;")
        root.addWidget(log_hint)
        self.log_hint = log_hint

        root.addStretch(1)

    # ----- меню стилей -----
    def _build_style_menu(self):
        menu = QMenu(self)
        self._style_group = QActionGroup(self)
        self._style_group.setExclusive(True)

        def add(name):
            a = QAction(name, self, checkable=True)
            a.triggered.connect(lambda _checked=False, n=name: self._apply_and_save(n))
            self._style_group.addAction(a)
            menu.addAction(a)
            self._style_actions[name] = a

        self._style_actions = {}

        add(SYSTEM_DEFAULT)
        menu.addSeparator()

        menu.addSection("Системные стили Qt")
        for name in QStyleFactory.keys():
            add(name)

        menu.addSeparator()
        menu.addSection("Темы")
        for name in CUSTOM_PALETTES.keys():
            add(name)

        menu.addSeparator()
        formats_action = QAction("🔍 Диагностика форматов", self)
        formats_action.triggered.connect(self.show_formats)
        menu.addAction(formats_action)

        update_action = QAction("🔄 Обновить yt-dlp", self)
        update_action.triggered.connect(
            lambda: self._fetch_dependencies(manual=True, force_ytdlp=True)
        )
        menu.addAction(update_action)

        update_ffmpeg_action = QAction("🔄 Обновить ffmpeg/ffprobe", self)
        update_ffmpeg_action.triggered.connect(
            lambda: self._fetch_dependencies(manual=True, force_ffmpeg=True)
        )
        menu.addAction(update_ffmpeg_action)

        menu.addSeparator()
        self.upd_action = QAction("🔄 Обновление с GitHub…", self)
        self.upd_action.setToolTip("Проверить и поставить новую версию программы из репозитория Video_downloader")
        self.upd_action.triggered.connect(self.show_update)
        menu.addAction(self.upd_action)

        menu.addSeparator()
        open_log_action = QAction("📄 Открыть текущий лог", self)
        open_log_action.triggered.connect(self.open_log_file)
        menu.addAction(open_log_action)

        open_logs_action = QAction("📁 Открыть папку логов", self)
        open_logs_action.triggered.connect(self.open_logs_folder)
        menu.addAction(open_logs_action)

        about_action = QAction("О программе…", self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)

        return menu

    # ----- обновление с GitHub (общий модуль gh_update) -----
    def _build_update_dialog(self):
        """Окно «⚙ → 🔄 Обновление с GitHub…» с общей вкладкой gh_update_qt.UpdatePage.
        Создаётся при старте и держится скрытым — так автопроверка идёт, даже если окно
        ни разу не открывали. Нет файлов gh_update*.py рядом — пункт меню неактивен."""
        try:
            import gh_update
            import gh_update_qt
        except Exception as e:
            logging.warning("обновление с GitHub недоступно: %s", e)
            self.upd_action.setEnabled(False)
            self.upd_action.setText("🔄 Обновление с GitHub (нет gh_update*.py рядом)")
            return None

        def colors():   # цвета текущей темы (палитра приложения) — смена темы подхватывается сама
            pal = QApplication.palette()
            return {"accent": pal.color(QPalette.ColorRole.Highlight).name(),
                    "text": pal.color(QPalette.ColorRole.WindowText).name(),
                    "dim": pal.color(QPalette.ColorRole.PlaceholderText).name(),
                    "panel": pal.color(QPalette.ColorRole.Base).name(),
                    "border": pal.color(QPalette.ColorRole.Mid).name()}
        gh_update_qt.set_colors(colors)
        target = gh_update.UpdateTarget(
            owner="romzespra-collab", repo="Video_downloader", name="video_downloader",
            current=APP_VERSION, app_dir=str(_app_dir()), main_file="video_downloader.pyw",
            changelog="", where="⚙ → 🔄 Обновление с GitHub")
        dlg = QDialog(self)
        dlg.setWindowTitle(f"{APP_NAME} — обновление с GitHub")
        dlg.resize(960, 460)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(0, 0, 0, 0)
        self.upd_page = gh_update_qt.UpdatePage(target, self._upd_get, self._upd_set,
                                                on_quit=self._quit_for_update, log=logging.info)
        self.upd_page.box.setFixedWidth(430)   # подписи кнопок не обрезаются при крупном шрифте
        self.upd_page.box.available.connect(self._update_available)
        lay.addWidget(self.upd_page)
        return dlg

    def _upd_get(self):
        s = self.settings
        try:
            every = int(s.value("upd_every_h", 12) or 12)
        except (TypeError, ValueError):
            every = 12
        return {"token": str(s.value("upd_token", "") or ""),
                "auto": s.value("upd_auto", True, type=bool),
                "branch": str(s.value("upd_branch", "main") or "main"),
                "every_h": every}

    def _upd_set(self, c):
        s = self.settings
        s.setValue("upd_token", c["token"])
        s.setValue("upd_auto", bool(c["auto"]))
        s.setValue("upd_branch", c["branch"] or "main")
        s.setValue("upd_every_h", int(c.get("every_h") or 12))
        s.sync()

    def show_update(self):
        if self.upd_dialog is not None:
            self.upd_dialog.show()
            self.upd_dialog.raise_()
            self.upd_dialog.activateWindow()

    def _update_available(self, ver):
        """На GitHub новая версия: кнопка «⬆ X.Y» в заголовке и пометка в меню ⚙."""
        self.upd_btn.setText(f"⬆ {ver}")
        self.upd_btn.setToolTip(f"Есть новая версия {ver} (у вас {APP_VERSION}) — открыть «Обновление с GitHub»")
        self.upd_btn.show()
        self.upd_action.setText(f"🔄 Обновление с GitHub — есть {ver}…")

    def _quit_for_update(self):
        """Новая копия уже запущена — закрыться полностью, без вопроса «прервать?»."""
        self._quitting = True
        self.close()
        QApplication.quit()

    def show_about(self):
        text = (
            f"<h3>{APP_NAME}</h3>"
            f"<p>Версия: <b>{APP_VERSION}</b></p>"
            f"<p>Автор: <b>{APP_AUTHOR}</b></p>"
            f"<p>Графический клиент для скачивания видео и аудио "
            f"на базе yt-dlp.</p>"
            f"<p><b>Сделано:</b></p>"
            f"<ul>"
            f"<li>Интерфейс полностью на PySide6 (Qt6).</li>"
            f"<li>Две кнопки: «Скачать видео» и «Скачать только звук» (MP3 320 kbps).</li>"
            f"<li>Выбор качества: от 360p до 4K, либо лучшее доступное (по умолчанию).</li>"
            f"<li>Скачивание в отдельном потоке (QThread) с прогрессом и статусом.</li>"
            f"<li>Меню оформления ⚙: системные стили Qt + темы "
            f"Fusion Light/Dark, Solarized Light/Dark, Nord, Dracula, Monokai, High Contrast.</li>"
            f"<li>Выбор темы сохраняется между запусками (QSettings).</li>"
            f"<li>Кнопка «Открыть папку» — быстрое открытие папки загрузок.</li>"
            f"</ul>"
            f"<p>Зависимости: <code>PySide6</code>, <code>yt-dlp</code>, "
            f"для склейки видео+аудио и MP3 — <code>ffmpeg</code> + <code>ffprobe</code>.</p>"
            f"<p>Лог: <code>{LOG_FILE}</code></p>"
        )
        QMessageBox.about(self, f"О программе — {APP_NAME}", text)

    def _apply_and_save(self, name):
        apply_style(self.app, name, self.default_style_name, self.default_palette)
        self.settings.setValue("style", name)
        if name in self._style_actions:
            self._style_actions[name].setChecked(True)

    def _restore_style(self):
        saved = self.settings.value("style", SYSTEM_DEFAULT, type=str)
        if saved not in self._style_actions:
            saved = SYSTEM_DEFAULT
        self._apply_and_save(saved)

    # ----- actions -----
    def _fill_combo_with_presets(self):
        """Заполняет дропдаун стандартными пресетами. userData = format-строка."""
        self.quality_combo.clear()
        for label, fmt in QUALITY_PRESETS.items():
            self.quality_combo.addItem(label, userData=fmt)
        # Дефолт — «Лучшее качество».
        self.quality_combo.setCurrentIndex(0)

    def _remember_old_probe_worker(self, worker):
        """Не даём QThread уничтожиться, пока он реально не завершился."""
        if worker is None:
            return
        try:
            if not worker.isRunning():
                worker.deleteLater()
                return
            if worker not in self._old_probe_workers:
                self._old_probe_workers.append(worker)
                worker.finished.connect(lambda w=worker: self._cleanup_old_probe_worker(w))
        except Exception:
            logging.exception("Не смог сохранить старый ProbeWorker")

    def _cleanup_old_probe_worker(self, worker):
        try:
            if worker in self._old_probe_workers:
                self._old_probe_workers.remove(worker)
            worker.deleteLater()
        except Exception:
            logging.exception("Не смог очистить старый ProbeWorker")

    def _on_url_changed(self, _text):
        """URL изменился — запускаем дебаунс-таймер на 600 мс, чтобы не
        дёргать yt-dlp на каждой букве."""
        logging.debug("url changed raw=%s", self.url_edit.text())
        if not hasattr(self, "_probe_timer"):
            self._probe_timer = QTimer(self)
            self._probe_timer.setSingleShot(True)
            self._probe_timer.setInterval(600)
            self._probe_timer.timeout.connect(self._start_probe)
        # Если старый поток ещё жив — просим остановиться, но НЕ уничтожаем объект.
        if self._probe_worker is not None:
            try:
                if self._probe_worker.isRunning():
                    logging.info("old ProbeWorker still running; keeping reference until finished")
                    self._probe_worker.requestInterruption()
                    self._remember_old_probe_worker(self._probe_worker)
                else:
                    self._probe_worker.deleteLater()
            except Exception:
                logging.exception("Ошибка при остановке ProbeWorker")
            self._probe_worker = None
        self._probe_timer.start()

    def _start_probe(self):
        """Запускает фоновое сканирование форматов для текущего URL."""
        raw_url = self.url_edit.text().strip()
        url = normalize_video_url(raw_url)
        logging.info("start_probe raw_url=%s normalized=%s", raw_url, url)
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            self._fill_combo_with_presets()
            self.download_btn.setEnabled(True)
            self.download_btn.setText(self._dl_btn_text)
            self.download_audio_btn.setEnabled(True)
            self.download_audio_btn.setText(self._dl_audio_btn_text)
            return
        if sys.platform.startswith("win"):
            # Не даём сканированию стартовать через старый внешний yt-dlp,
            # пока рядом с программой ещё скачиваются локальные зависимости.
            if getattr(self, "_dep_worker", None) is not None:
                self._pending_probe_after_deps = True
                self.download_btn.setEnabled(False)
                self.download_audio_btn.setEnabled(False)
                self.quality_combo.setEnabled(False)
                self.set_status("Идёт подготовка yt-dlp/ffmpeg рядом с программой — сканирование начнётся автоматически...")
                return
            if find_local_ytdlp_exe() is None or self._need_ffmpeg():
                self._pending_probe_after_deps = True
                self._fetch_dependencies(manual=False)
                return

        if YTDLP_EXE is None and not can_use_python_ytdlp_module():
            self.set_status("Жду установку локального yt-dlp.exe рядом с программой...")
            self._pending_probe_after_deps = True
            self._fetch_dependencies(manual=False)
            return

        # Лочим обе кнопки скачивания и меняем им текст.
        scanning_text = "⏳ Идёт сканирование, подождите..."
        self.download_btn.setEnabled(False)
        self.download_btn.setText(scanning_text)
        self.download_audio_btn.setEnabled(False)
        self.download_audio_btn.setText(scanning_text)
        self.quality_combo.clear()
        self.quality_combo.addItem("⏳ Сканирование форматов...", userData=None)
        self.quality_combo.setEnabled(False)
        self.set_status("Сканирование форматов...")

        self._probe_worker = ProbeWorker(url, parent=self)
        self._probe_worker.done.connect(self._on_probe_done)
        self._probe_worker.failed.connect(self._on_probe_failed)
        self._probe_worker.start()

    def _on_probe_done(self, formats, title):
        """Форматы получены — заполняем дропдаун."""
        worker = self.sender()
        if worker is not self._probe_worker:
            logging.info("ignore old ProbeWorker.done")
            return
        logging.info("probe_done title=%s formats=%s", title, len(formats or []))
        self._update_retry_pending = False
        self._pending_probe_after_deps = False
        self._probe_worker = None
        # Сигнал пришёл из run(): поток ещё жив — удалим после finished.
        self._remember_old_probe_worker(worker)
        self.quality_combo.setEnabled(True)
        opts = build_quality_options(formats)
        self.quality_combo.clear()
        if opts:
            for label, fmt_str in opts:
                self.quality_combo.addItem(label, userData=fmt_str)
            self.quality_combo.setCurrentIndex(0)
            self.set_status(f"Форматы загружены ({len(opts)} вариантов). "
                            f"Выбран лучший: {opts[0][0]}")
        else:
            self.quality_combo.addItem("✅ Авто: видео со звуком (H.264/MP4)", userData=VIDEO_WITH_AUDIO_FALLBACK)
            self.set_status("Форматы не получены, использую дефолт.")
        # Разблокируем кнопки и возвращаем текст.
        self.download_btn.setEnabled(True)
        self.download_btn.setText(self._dl_btn_text)
        self.download_audio_btn.setEnabled(True)
        self.download_audio_btn.setText(self._dl_audio_btn_text)

    def _on_probe_failed(self, error):
        worker = self.sender()
        if worker is not self._probe_worker:
            logging.info("ignore old ProbeWorker.failed: %s", error)
            return
        logging.warning("probe_failed: %s", error)
        self._probe_worker = None
        # Сигнал пришёл из run(): поток ещё жив — удалим после finished.
        self._remember_old_probe_worker(worker)
        self.quality_combo.setEnabled(True)
        self._fill_combo_with_presets()
        self.set_status(f"Не смог сканировать форматы: {error}. Использую пресеты.")
        self.download_btn.setEnabled(True)
        self.download_btn.setText(self._dl_btn_text)
        self.download_audio_btn.setEnabled(True)
        self.download_audio_btn.setText(self._dl_audio_btn_text)

        # Важно: больше НЕ перекачиваем yt-dlp автоматически на каждую ошибку TikTok.
        # Если файл уже есть рядом, повторная загрузка только вручную через ⚙.
        if (sys.platform.startswith("win")
                and not self._update_retry_pending
                and self._looks_outdated(error)):
            if find_local_ytdlp_exe():
                logging.warning("skip auto yt-dlp update: local yt-dlp.exe exists; manual update only")
                self.set_status("yt-dlp.exe уже лежит рядом — не перекачиваю. Использую пресеты; обновление только вручную через ⚙.")
            else:
                self._update_retry_pending = True
                self._pending_probe_after_deps = True
                self.set_status("Локального yt-dlp.exe нет — скачиваю один раз рядом с программой...")
                self._fetch_dependencies(manual=False)
                return

        self._update_retry_pending = False

    def paste_url(self):
        cb = QGuiApplication.clipboard()
        text = cb.text()
        if text:
            self.url_edit.setText(normalize_video_url(text))
        self.url_edit.setFocus()

    # ----- зависимости (yt-dlp / ffmpeg) -----
    def _refresh_dep_labels(self):
        """Обновить лейблы статуса ffmpeg/yt-dlp по текущим глобалам."""
        if FFMPEG_DIR:
            self.ff_lbl.setText(f"✓ локальные ffmpeg + ffprobe найдены: {FFMPEG_DIR}")
            self.ff_lbl.setStyleSheet("color: #2a8a2a;")
        else:
            self.ff_lbl.setText(
                "⚠ локальные ffmpeg/ffprobe ещё не найдены полной парой. "
                "Программа скачает их рядом с собой автоматически."
            )
            self.ff_lbl.setStyleSheet("color: #b86b00;")

        if YTDLP_EXE is not None:
            name = Path(YTDLP_EXE).name
            local_mark = "локальный" if is_local_ytdlp_exe(YTDLP_EXE) else "внешний/PATH"
            if "win7" in name.lower():
                self.yl_lbl.setText(f"🪟 Win7-режим: {name} ({local_mark}, subprocess) ← {YTDLP_EXE}")
            else:
                self.yl_lbl.setText(f"✓ yt-dlp.exe ({local_mark}, subprocess) ← {YTDLP_EXE}")
            self.yl_lbl.setStyleSheet("color: #2a6acd;")
        elif can_use_python_ytdlp_module():
            ver = getattr(getattr(yt_dlp, "version", None), "__version__", "?")
            self.yl_lbl.setText(f"✓ yt-dlp (Python-модуль, не Windows): {ver}")
            self.yl_lbl.setStyleSheet("color: #2a8a2a;")
        else:
            self.yl_lbl.setText(
                "⏳ локальный yt-dlp.exe ещё не найден. "
                "Программа скачает его рядом с собой автоматически."
            )
            self.yl_lbl.setStyleSheet("color: #b86b00;")

    def _need_ffmpeg(self):
        """ffmpeg нужен и ещё не скачан (если пользователь не отказался)."""
        return find_ffmpeg() is None and not self._ffmpeg_declined

    def _ask_ffmpeg_consent(self):
        ans = QMessageBox.question(
            self, "ffmpeg",
            "Для склейки видео+аудио, MP3 и проверки звука нужен ffmpeg + ffprobe "
            "(~200 МБ с github.com/yt-dlp/FFmpeg-Builds).\n\n"
            "Скачать рядом с программой?\n\n"
            "Без ffmpeg будут доступны только одиночные файлы со звуком. "
            "Скачать позже можно через ⚙ → «Обновить ffmpeg/ffprobe».",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes,
        )
        if ans == QMessageBox.Yes:
            return True
        self._ffmpeg_declined = True
        self.settings.setValue("ffmpeg_declined", True)
        return False

    def _fetch_dependencies(self, manual, force_ytdlp=False, force_ffmpeg=False, retry_quality=None):
        """Запустить фоновую докачку yt-dlp.exe / ffmpeg в папку программы.
        force_ytdlp=True — перекачать yt-dlp.exe заново (обновление).
        force_ffmpeg=True — перекачать ffmpeg.exe + ffprobe.exe заново.
        retry_quality — формат, который повторить после успешного обновления."""
        logging.info("fetch_dependencies manual=%s force_ytdlp=%s force_ffmpeg=%s retry_quality=%s",
                     manual, force_ytdlp, force_ffmpeg, retry_quality)
        if self._closing:
            return
        if self.is_downloading:
            if manual:
                QMessageBox.information(self, "Идёт скачивание",
                                        "Дождись окончания текущей загрузки.")
            return
        if getattr(self, "_dep_worker", None) is not None:
            if retry_quality is not None:
                self._retry_quality = retry_quality
                self._deps_retry_is_repair = self._deps_retry_is_repair or force_ytdlp or force_ffmpeg
                self.set_status("Зависимости уже скачиваются — после завершения продолжу загрузку...")
            return  # уже качаем

        need_ytdlp = force_ytdlp or (find_local_ytdlp_exe() is None)
        if force_ffmpeg and self._ffmpeg_declined:
            self._ffmpeg_declined = False
            self.settings.setValue("ffmpeg_declined", False)
        need_ffmpeg = force_ffmpeg or self._need_ffmpeg()
        if not need_ytdlp and not need_ffmpeg:
            if manual:
                QMessageBox.information(self, "Зависимости",
                                        "yt-dlp, ffmpeg и ffprobe уже лежат рядом с программой.")
            return

        if not sys.platform.startswith("win"):
            if manual:
                QMessageBox.information(
                    self, "Только Windows",
                    "Авто-загрузка бинарников реализована для Windows.\n\n"
                    "На этой ОС установи вручную:\n"
                    "  • yt-dlp:  pip install -U yt-dlp\n"
                    "  • ffmpeg:  пакетным менеджером системы."
                )
            return

        if need_ffmpeg and not force_ffmpeg and sys.platform.startswith("win"):
            if not self._ask_ffmpeg_consent():
                need_ffmpeg = False
                if not need_ytdlp:
                    self._refresh_dep_labels()
                    if retry_quality is not None:
                        self._start(retry_quality)
                    elif self._pending_probe_after_deps:
                        self._pending_probe_after_deps = False
                        self._start_probe()
                    return

        self._retry_quality = retry_quality
        self._deps_retry_is_repair = bool(retry_quality is not None and (force_ytdlp or force_ffmpeg))
        verb = "Обновление" if (force_ytdlp or force_ffmpeg) else "Загрузка"
        self.set_status(f"{verb} зависимостей рядом с программой...")
        self.download_btn.setEnabled(False)
        self.download_audio_btn.setEnabled(False)
        self.progress.setValue(0)

        self._dep_worker = DependencyWorker(force_ytdlp=force_ytdlp, force_ffmpeg=force_ffmpeg,
                                            skip_ffmpeg=not need_ffmpeg, parent=self)
        self._dep_worker.progress.connect(lambda p: self.progress.setValue(int(p)))
        self._dep_worker.status.connect(self.set_status)
        self._dep_worker.done.connect(self._on_deps_done)
        self._dep_worker.start()

    def _on_deps_done(self):
        dep_worker = self._dep_worker
        dep_errors = list(getattr(dep_worker, "errors", []) or [])
        self._dep_worker = None
        if dep_worker is not None:
            # done испускается внутри run(): удаляем только после реального завершения.
            dep_worker.finished.connect(dep_worker.deleteLater)
        if self._closing:
            return
        refresh_dependencies()
        self._refresh_dep_labels()
        self.progress.setValue(0)
        if not self.is_downloading:
            self.download_btn.setEnabled(True)
            self.download_btn.setText(self._dl_btn_text)
            self.download_audio_btn.setEnabled(True)
            self.download_audio_btn.setText(self._dl_audio_btn_text)
        # Повтор загрузки после обновления yt-dlp (ровно один раз).
        rq = self._retry_quality
        retry_is_repair = self._deps_retry_is_repair
        self._retry_quality = None
        self._deps_retry_is_repair = False
        if dep_errors:
            logging.error("dependency preparation failed; pending actions stopped: %s", dep_errors)
            self._pending_probe_after_deps = False
            self._update_retry_pending = False
            if rq is not None:
                QMessageBox.critical(self, "Зависимости", "Не удалось скачать зависимости рядом с программой.\n\n" + "\n".join(dep_errors) + f"\n\nЛог: {LOG_FILE}")
            return
        if rq is not None and not self.is_downloading:
            # Если автоустановка не смогла положить локальные бинарники — не уходим в цикл.
            if sys.platform.startswith("win"):
                missing = []
                if find_local_ytdlp_exe() is None:
                    missing.append("yt-dlp.exe")
                if self._need_ffmpeg():
                    missing.append("ffmpeg.exe/ffprobe.exe")
                if missing:
                    msg = "Не удалось подготовить рядом с программой: " + ", ".join(missing)
                    logging.error(msg)
                    self.set_status(msg)
                    QMessageBox.critical(self, "Зависимости", msg + f"\n\nЛог: {LOG_FILE}")
                    self._update_retry_pending = False
                    return
            self._update_retry_pending = bool(retry_is_repair)
            self._start(rq)
            return
        # Иначе — если в поле уже есть URL, пере-сканировать форматы.
        if self._pending_probe_after_deps or self.url_edit.text().strip():
            self._pending_probe_after_deps = False
            self._start_probe()

    def open_log_file(self):
        try:
            if LOG_FILE and Path(LOG_FILE).exists():
                _open_path(LOG_FILE)
            else:
                QMessageBox.information(self, "Лог", "Файл лога ещё не создан.")
        except Exception as exc:
            logging.exception("open_log_file failed")
            QMessageBox.warning(self, "Лог", f"Не смог открыть лог:\n{exc}")

    def open_logs_folder(self):
        try:
            folder = Path(LOG_FILE).parent if LOG_FILE else _safe_log_dir()
            folder.mkdir(parents=True, exist_ok=True)
            _open_path(folder)
        except Exception as exc:
            logging.exception("open_logs_folder failed")
            QMessageBox.warning(self, "Лог", f"Не смог открыть папку логов:\n{exc}")

    def _download_folder(self):
        """Текущая папка загрузок. Если поле пустое — вернуть ./downloads рядом с программой."""
        folder = self.dir_edit.text().strip()
        if not folder:
            folder = str(_downloads_dir())
            self.dir_edit.setText(folder)
        Path(folder).mkdir(parents=True, exist_ok=True)
        return folder

    def choose_folder(self):
        start = self.dir_edit.text().strip() or str(_downloads_dir())
        folder = QFileDialog.getExistingDirectory(self, "Папка для скачивания", start)
        if folder:
            self.dir_edit.setText(folder)

    def show_formats(self):
        """Диагностика: запустить yt-dlp -F <URL> и показать что доступно."""
        url = normalize_video_url(self.url_edit.text())
        if not url:
            QMessageBox.warning(self, "Нет ссылки", "Вставь ссылку в поле URL.")
            return
        if sys.platform.startswith("win"):
            if getattr(self, "_dep_worker", None) is not None:
                self._pending_probe_after_deps = True
                self.set_status("Идёт подготовка зависимостей — форматы проверю автоматически после неё...")
                return
            if find_local_ytdlp_exe() is None or self._need_ffmpeg():
                self._pending_probe_after_deps = True
                self._fetch_dependencies(manual=False)
                return
        if not YTDLP_EXE and not can_use_python_ytdlp_module():
            self._pending_probe_after_deps = True
            self._fetch_dependencies(manual=False)
            QMessageBox.information(self, "yt-dlp", "Сначала подготовлю локальный yt-dlp.exe рядом с программой.")
            return

        if YTDLP_EXE:
            cmd = [YTDLP_EXE, "-F", "--no-playlist", url]
        else:
            cmd = [sys.executable, "-m", "yt_dlp", "-F", "--no-playlist", url]
        if self._formats_worker is not None:
            self.set_status("Запрос форматов уже выполняется...")
            return
        self.set_status("Запрос форматов...")
        w = FormatsListWorker(cmd, parent=self)
        w.done.connect(lambda out, u=url: self._show_formats_dialog(u, out))
        w.failed.connect(lambda err: QMessageBox.warning(self, "Форматы", err))
        w.finished.connect(self._on_formats_worker_finished)
        self._formats_worker = w
        w.start()

    def _on_formats_worker_finished(self):
        w = self._formats_worker
        self._formats_worker = None
        if w is not None:
            w.deleteLater()

    def _show_formats_dialog(self, url, output):
        if self._closing:
            return
        self.set_status("Список форматов получен.")
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Доступные форматы — {url[:80]}")
        dlg.resize(960, 640)
        lay = QVBoxLayout(dlg)
        info = QLabel(
            "<b>Что искать:</b> в колонке RESOLUTION строки <code>1920x1080</code>, "
            "<code>1920x804</code>, <code>1280x720</code> и т.д. "
            "Если максимум = <code>640x360</code> или ниже — значит yt-dlp не видит "
            "высокие форматы (нужно обновить yt-dlp / yt-dlp_win7.exe). "
            "В колонке VCODEC: <code>avc1</code> = H.264 (TV-совместимо), "
            "<code>av01</code> = AV1 (старые TV не поддерживают), "
            "<code>vp9</code> = VP9. В ACODEC: <code>mp4a</code> = AAC (TV ok), "
            "<code>opus</code> = Opus (TV часто не понимает)."
        )
        info.setWordWrap(True)
        lay.addWidget(info)

        view = QPlainTextEdit()
        view.setReadOnly(True)
        view.setPlainText(output or "(пустой вывод)")
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.TypeWriter)
        mono.setPointSize(9)
        view.setFont(mono)
        lay.addWidget(view, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dlg.reject)
        lay.addWidget(buttons)
        dlg.exec()

    def open_folder(self):
        try:
            _open_path(self._download_folder())
        except Exception as exc:
            logging.exception("open_folder failed")
            QMessageBox.warning(self, "Папка", f"Не смог открыть папку:\n{exc}")

    def cancel_download(self):
        if self.worker is not None and self.is_downloading:
            logging.info("BUTTON: Отмена")
            self.cancel_btn.setEnabled(False)
            self.set_status("Отмена...")
            self.worker.cancel()

    def _on_cancelled(self):
        logging.info("download_cancelled")
        self.is_downloading = False
        self._audio_original_fallback_used = False
        self._update_retry_pending = False
        self._set_buttons_enabled(True)
        self.progress.reset()
        self.progress.setValue(0)
        self.set_status("Загрузка отменена.")

    def _on_worker_finished(self):
        w = self.sender()
        if w is self.worker:
            self.worker = None
        if w is not None:
            w.deleteLater()

    def closeEvent(self, event):
        busy = self.is_downloading or self._dep_worker is not None
        if busy and not self._quitting:
            ans = QMessageBox.question(
                self, "Выход", "Идёт загрузка. Прервать и выйти?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if ans != QMessageBox.Yes:
                event.ignore()
                return
        self._closing = True
        logging.info("closeEvent: stopping workers")
        if self.worker is not None:
            self.worker.cancel()
        threads = [self.worker, self._probe_worker, self._formats_worker, self._dep_worker]
        threads += list(self._old_probe_workers)
        for t in threads:
            if t is not None and t.isRunning():
                t.requestInterruption()
        for t in threads:
            if t is not None and t.isRunning() and not t.wait(15000):
                logging.warning("поток не завершился за 15 сек: %s — жёсткий выход", t)
                event.accept()
                logging.shutdown()
                os._exit(0)  # иначе Qt упадёт на уничтожении работающего QThread
        event.accept()

    def set_status(self, text):
        logging.debug("STATUS: %s", text)
        self.status_label.setText(text)

    def _validate(self):
        url = normalize_video_url(self.url_edit.text())
        if sys.platform.startswith("win") and find_local_ytdlp_exe() is None:
            QMessageBox.critical(
                self, "yt-dlp не подготовлен",
                "Локальный yt-dlp.exe ещё не лежит рядом с программой.\n\n"
                "Программа скачает его сама; после подготовки повтори действие."
            )
            return False
        if YTDLP_EXE is None and not can_use_python_ytdlp_module():
            QMessageBox.critical(
                self, "yt-dlp не найден",
                "Не найден локальный yt-dlp.exe рядом с программой."
            )
            return False
        if not url:
            QMessageBox.warning(self, "Нет ссылки", "Вставь ссылку на видео.")
            self.url_edit.setFocus()
            return False
        self._download_folder()
        return True

    def _set_buttons_enabled(self, enabled):
        # Кнопки скачивания
        self.download_btn.setEnabled(enabled)
        self.download_audio_btn.setEnabled(enabled)
        # Если включаем обратно — вернуть оригинальный текст
        # (на случай если он был "⏳ Скачивание..." или подобный).
        if enabled:
            self.download_btn.setText(self._dl_btn_text)
            self.download_audio_btn.setText(self._dl_audio_btn_text)
        else:
            self.download_btn.setText("⏳ Скачивание идёт...")
            self.download_audio_btn.setText("⏳ Скачивание идёт...")
        # Доп. блокировка ввода во время загрузки: чтобы случайно не менять
        # URL/папку/качество для уже запущенной задачи.
        self.cancel_btn.setEnabled(not enabled)
        self.url_edit.setEnabled(enabled)
        self.paste_btn.setEnabled(enabled)
        self.quality_combo.setEnabled(enabled)
        self.dir_edit.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)

    def _start(self, quality_name):
        logging.info("start_download_request quality=%s raw_url=%s", quality_name, self.url_edit.text())
        if self.is_downloading:
            logging.info("start_download_request ignored: already downloading")
            return

        url = normalize_video_url(self.url_edit.text())
        if not url:
            QMessageBox.warning(self, "Нет ссылки", "Вставь ссылку на видео.")
            self.url_edit.setFocus()
            return
        folder = self._download_folder()

        # Перед скачиванием на Windows всегда добиваем локальные зависимости:
        # yt-dlp.exe + ffmpeg.exe + ffprobe.exe рядом с текущей программой.
        if sys.platform.startswith("win"):
            need_ytdlp = find_local_ytdlp_exe() is None
            need_ffmpeg = self._need_ffmpeg()
            logging.info("pre-download dependency check: need_ytdlp=%s need_ffmpeg=%s local_ytdlp=%s ffmpeg=%s",
                         need_ytdlp, need_ffmpeg, find_local_ytdlp_exe(), find_ffmpeg())
            if need_ytdlp or need_ffmpeg:
                self._fetch_dependencies(manual=False, retry_quality=quality_name)
                return

        if not self._validate():
            return
        self._last_quality = quality_name
        self.is_downloading = True
        self._set_buttons_enabled(False)
        self.progress.setValue(0)
        self.set_status("Подготовка...")

        # Выбор движка: standalone yt-dlp.exe (Win7-режим) приоритетнее,
        # потому что на Win7 модуль yt_dlp устарел и YouTube не работает.
        if YTDLP_EXE is not None:
            self.worker = DownloadWorkerExe(
                url=url,
                folder=folder,
                quality_name=quality_name,
                ytdlp_exe=YTDLP_EXE,
                parent=self,
            )
        elif can_use_python_ytdlp_module():
            self.worker = DownloadWorker(
                url=url,
                folder=folder,
                quality_name=quality_name,
                parent=self,
            )
        else:
            self.is_downloading = False
            self._set_buttons_enabled(True)
            self.set_status("Локальный yt-dlp.exe ещё не подготовлен.")
            return
        self.worker.progress.connect(lambda p: self.progress.setValue(int(p)))
        self.worker.status.connect(self.set_status)
        self.cancel_btn.setEnabled(True)
        self.worker.finished_ok.connect(self._on_done)
        self.worker.failed.connect(self._on_failed)
        self.worker.cancelled.connect(self._on_cancelled)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    def start_download(self):
        logging.info("BUTTON: Скачать видео")
        # Берём userData (format-строку), а не label.
        fmt = self.quality_combo.currentData()
        if not fmt:
            QMessageBox.warning(self, "Нет формата",
                                "Подожди завершения сканирования форматов.")
            return
        self._start(fmt)

    def start_download_audio(self):
        logging.info("BUTTON: Скачать только звук")
        self._start("Только аудио MP3")

    def _on_done(self):
        logging.info("download_done")
        self.is_downloading = False
        self._update_retry_pending = False
        self._audio_original_fallback_used = False
        self._set_buttons_enabled(True)
        self.progress.setValue(100)
        self.set_status("Готово. Скачивание завершено.")
        QMessageBox.information(self, "Готово", "Скачивание завершено.")
        # После «ОК» — полный сброс: URL, прогресс, статус.
        self.url_edit.clear()
        self.url_edit.setFocus()
        self.progress.reset()
        self.progress.setValue(0)
        self.progress.repaint()
        self.set_status("Готово к новой ссылке.")

    @staticmethod
    def _looks_outdated(text):
        """Похоже ли сообщение об ошибке на устаревший экстрактор yt-dlp."""
        t = (text or "").lower()
        needles = (
            "unexpected response",
            "confirm you are on the latest version",
            "please report this issue",
            "yt-dlp -u",
            "unable to extract",
            "nsig extraction failed",
            "failed to extract",
        )
        return any(n in t for n in needles)

    @staticmethod
    def _looks_broken_ffprobe(text):
        """Похоже ли сообщение на проблему ffprobe/постобработки аудио."""
        t = (text or "").lower()
        needles = (
            "unable to obtain file audio codec with ffprobe",
            "ffprobe not found",
            "ffprobe and ffmpeg not found",
            "error: postprocessing:",
        )
        return any(n in t for n in needles)

    def _on_failed(self, text):
        logging.error("download_failed: %s", text)
        self.is_downloading = False
        self._set_buttons_enabled(True)
        self.progress.reset()
        self.progress.setValue(0)
        self.progress.repaint()
        self.set_status(text)

        # TikTok часто даёт странные postprocessing/ffprobe ошибки на MP3.
        # Сначала сохраняем оригинальный аудиофайл, а НЕ перекачиваем 211 МБ ffmpeg.zip.
        if (self._last_quality == "Только аудио MP3"
                and self._looks_broken_ffprobe(text)
                and not self._audio_original_fallback_used):
            self._audio_original_fallback_used = True
            self.set_status("MP3-постобработка упала на ffprobe — сохраняю оригинальный аудиофайл без перекодирования...")
            self._start("Только аудио оригинал")
            return
        # Fallback использован (или не нужен) — разрешаем его для следующих загрузок.
        self._audio_original_fallback_used = False

        # Авто-докачка только если файла реально НЕТ.
        # Принудительное обновление/переустановка — только вручную через ⚙.
        if (sys.platform.startswith("win")
                and not self._update_retry_pending
                and self._last_quality is not None):
            if self._looks_outdated(text):
                if find_local_ytdlp_exe():
                    logging.warning("skip auto yt-dlp repair: local yt-dlp.exe exists; manual update only")
                else:
                    self.set_status("Локального yt-dlp.exe нет — скачиваю один раз рядом с программой и повторяю...")
                    self._fetch_dependencies(manual=False, retry_quality=self._last_quality)
                    return
            if self._looks_broken_ffprobe(text):
                if find_ffmpeg():
                    logging.warning("skip auto ffmpeg repair: local ffmpeg+ffprobe exists; manual reinstall only")
                else:
                    self.set_status("Локального ffmpeg/ffprobe нет — скачиваю один раз рядом с программой и повторяю...")
                    self._fetch_dependencies(manual=False, retry_quality=self._last_quality)
                    return

        self._update_retry_pending = False
        extra = f"\n\nЛог: {LOG_FILE}" if LOG_FILE else ""
        QMessageBox.critical(self, "Ошибка", text + extra)


def main():
    _setup_logging()
    _install_crash_hooks()
    logging.info("main enter")
    refresh_dependencies()
    app = QApplication(sys.argv)
    try:  # после обновления: дождаться, пока закроется старая копия
        import gh_update
        gh_update.wait_previous(sys.argv)
    except ImportError:
        pass
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    default_style_name = app.style().objectName() if app.style() else ""
    default_palette = QPalette(app.palette())

    win = VideoDownloaderWindow(app, default_style_name, default_palette)
    win.show()
    rc = app.exec()
    logging.info("main exit rc=%s", rc)
    sys.exit(rc)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        logging.exception("FATAL in __main__")
        raise
