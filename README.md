# Video_downloader

**Video Downloader Mini v2.2** — скачивание видео и звука (MP3) по ссылке на базе yt-dlp (PySide6 / Qt6, Windows 10/11).

## Запуск
Двойной клик по `video_downloader.pyw`. yt-dlp.exe и ffmpeg программа скачает рядом с собой сама (ffmpeg — с согласия).
Зависимости для запуска из исходников: `python -m pip install -U PySide6 yt-dlp`.

> С версии 2.2 главный файл называется `video_downloader.pyw` (раньше — `video_downloader_app_v2.1.pyw`).
> Ярлыки на старое имя нужно поменять, старый файл можно удалить.

## Обновление с GitHub
⚙ → «🔄 Обновление с GitHub…». Нужен токен GitHub «только чтение» (Contents: Read-only) на репозиторий
Video_downloader — кнопка «?» покажет по шагам, как его получить. Программа сама проверяет новую версию
(через 30 с после запуска и дальше по выбору «Каждые»), рядом с ⚙ появляется «⬆ X.Y»; ставит — только по кнопке
«Обновить», затем перезапуск. yt-dlp.exe, ffmpeg, логи и загрузки не трогаются, заменённые файлы копируются
в `backup/v<старая версия>/`.

## Файлы
- `video_downloader.pyw` — программа (журнал изменений — в начале файла)
- `gh_update.py`, `gh_update_qt.py`, `gh_update_help.py` — обновление с GitHub (общий модуль)
- `test_gh_update.pyw` — тесты модуля обновления (без сети)
- `release/video_downloader_vX.Y.zip` — архив последней версии
