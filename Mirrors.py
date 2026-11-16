#БИБЛИОТЕКИ ИМПОРТИРУЕМ
import time
import os
import textwrap 
import sys
import yt_dlp
import urllib.request
import urllib.error

from rich.markup import escape
from rich.live import Live

#1)ШОБИ РИСОВАТЬ
from rich.console import Console 

#2)ШОБИ КРАСЯВУЮ ЗАГРУЗКУ ДЕЛАТЬ
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

#3)ШОБИ КРАСЯВЫЙ БАННЕР ДЕЛАТЬ
from rich.panel import Panel

#4)ШОБИ ССЫЛОЧКИ КЛИКАБЕЛЬНЫЕ ДЕЛАТЬ ВЫ ВЫВОДЕ ОТВЕТА
from rich.prompt import Prompt

#5)ШОБИ ТАБЛИЧКИ ДЕЛАТЬ
from rich.table import Table

#6)А ЭТО ШОБИ ПРИВЯЗКУ ПО КРАЯМ ДЕЛАТ
from rich.align import Align

#7)ШОБИ КРУТЫЕ ЗАГОЛОВКИ ДЕЛАТЬ ЧТОБИ МНОГА ТЕКСТА ПОДДЕРЖИВАЛОСЯ
from rich.text import Text

#8)ШОБИ РАЗДЕЛИТЕЛИ ДЕЛАТ
from rich.rule import Rule

#9)ШОБИ ЯЧЕЙКИ ДЕЛАТ
from rich import box    


#НАСТРОЙКИ ДЛЯ WINDOWS CMD, LINUX И TERMUX
if os.name == "nt":
    os.system("chcp 65001 > nul")

for stream in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding = "utf-8", errors = "replace")
        except (ValueError, OSError):
            pass


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


#ТО ЧТО БУДЕТ КРАСИВО РИСОВАТЬ
console = Console()
clear_screen()

#СОЗДАЕМ ПАПКУ
SAVE_DIR = "MirrorsDownloads"
os.makedirs(SAVE_DIR, exist_ok = True)

class QuietLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def friendly_error(error):
    error_text = str(error).lower()

    if "unsupported url" in error_text:
        return "Ссылка не поддерживается."
    if "requested format is not available" in error_text or "format is not available" in error_text:
        return "Доступный формат видео не найден."
    if "sign in" in error_text or "login" in error_text or "authentication" in error_text:
        return "Для этого видео требуется авторизация."
    if "private video" in error_text:
        return "Видео закрыто или доступно только владельцу."
    if "age-restricted" in error_text:
        return "Видео имеет возрастное ограничение."
    if "ffmpeg" in error_text:
        return "Для объединения видео и аудио нужен FFmpeg."
    if isinstance(error, yt_dlp.utils.DownloadError):
        return "Не удалось скачать видео. Проверьте ссылку или доступность видео."
    if isinstance(error, urllib.error.HTTPError):
        return "Ссылка недоступна: ошибка сервера."
    if isinstance(error, urllib.error.URLError):
        return "Не удалось открыть ссылку. Проверьте интернет и адрес."

    return "Не удалось выполнить загрузку. Проверьте ссылку."



#ЗАГРУЗОЧКА ТАКАЯ 
with Progress(
    SpinnerColumn(style = "#afff00"),
    TextColumn("[#00ff88] {task.description}"),
    BarColumn(complete_style = "#afff00"),
    TextColumn("[#e2e8f0]{task.percentage:>3.0f}%"),
    console = console,
    transient = True
) as progress:

    task = progress.add_task("Инициализация модулей...", total = 100)
    for step in range(100):
        time.sleep(0.02)
        if step == 30:
            progress.update(task, description = "Подключение к серверам...")
        elif step == 70:
            progress.update(task, description = "Загрузка интерфейса...")

        progress.advance(task, 1)


#СЕРВИСЫ
items = [
    ("\\[1]", "Скачать Видео", "VIDEO-MP4"),
    ("\\[2]", "Скачать Аудио", "AUDIO-MP3"),
    ("\\[3]", "Скачать фото/превью", "JPG"),
    ("", "", ""),
    ("\\[0]", "Выход из программы", "EXIT")
]
#БАНЕРОЧЕК))
BANNER = textwrap.dedent("""
            ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗
            ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
            ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝███████╗
            ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗╚════██║
            ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║███████║
            ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
        """).strip("\n")#УБИРАЕТ ЛИШНИЕ ПРОБЕЛЫ

if console.width >= 100:
    banner_content = Align.center(Text(BANNER, style ="#afff00", no_wrap = False))
else:
    banner_content = Align.center(Text("♦ M I R R O R S ♦", style = "#afff00"))

#ПАНЕЛЬ БАННЕРА ОБВОДКА И ПОДЗАГОЛОВОК
header = Panel(
    banner_content,
    box = box.ROUNDED,
    border_style = "#4b6e00",
    subtitle = "[#afff00]EXPERIMENTAL PROGRAM[/#afff00]",
    subtitle_align = "right"
)


#РАЗДЕЛИТЕЛЬ МЕЖДУ БАННЕРОМ И ТАБЛИЧКОЙ))
divider = Rule("[#afff00]Приятного пользования[/#afff00]", style = "#4b6e00")


#ТАБЛИЧКА
menu_table = Table(
    box = None, #ЯЧЕЙКИ
    expand = True,
    header_style = "#afff00",
    padding = (0, 1)
)

menu_table.add_column("ID",style = "#afff00", justify = "center", width = 6)
menu_table.add_column("Действие", style = "#e2e8f0")
menu_table.add_column("Тег", style = "#64748b", justify = "right")

#ДОБАВЛЕНИЕ ИНФОРМАЦИИ ИЗ СПИСКА
for item_id,platform,tag in items:
    menu_table.add_row(item_id, platform, tag)

def make_menu_panel(width: int) -> Panel:
    panel_height = 11 if width >= 70 else None
    return Panel(
        menu_table,
        title = "[not dim #afff00]♦ ФУНКЦИИ ♦[/]",
        border_style = "#4b6e00",
        box = box.ROUNDED,
        padding = (0, 2),
        width = width,
        height = panel_height
    )

# ПАНЕЛЬ СПРАВА
def make_status_panel(status = "Ожидание команды...", percent = 0.0, speed = "-", logs = None, width: int = None) -> Panel:
    if logs is None:
        logs = ["[#94a3b8]Система готова к работе.[/]"]

    panel_width = width or console.width
    bar_width = max(5, min(20, panel_width - 25))
    grid = Table.grid(expand = True, padding = (0, 0))
    grid.add_row(f"[bold #e2e8f0]Статус:[/] [bold #afff00]{status}[/]")
    filled = min(bar_width, int(bar_width * (percent / 100)))
    bar = "█" * filled + "░" * (bar_width - filled)
    grid.add_row(f"[bold #e2e8f0]Прогресс:[/] [#afff00]{bar}[/] [bold #e2e8f0]{percent:.1f}%[/]")
    grid.add_row(f"[bold #e2e8f0]Скорость:[/] [#64748b]{speed}[/]")
    grid.add_row(f"[dim #4b6e00]{'─' * max(10, min(28, panel_width - 10))}[/dim #4b6e00]")

    for line in logs[-3:]:
        grid.add_row(f"[#afff00]>[/] [#e2e8f0]{line}[/]")

    panel_height = 11 if panel_width >= 70 else None
    return Panel(
        grid,
        title = "[not dim bold #afff00] ♦ СТАТУС И ПРОЦЕСС ♦ [/]",
        border_style = "#4b6e00",
        box = box.ROUNDED,
        padding = (0, 2),
        width = width,
        height = panel_height
    )

def build_panels(status = "Ожидание команды...", percent = 0.0, speed = "-", logs = None) -> Table:
    available_width = max(20, console.width - 2)
    menu_width = max(20, (available_width - 1) // 2)
    menu_panel = make_menu_panel(menu_width)

    panels_grid = Table.grid(expand = True)
    if console.width >= 150:
        right_panel = make_status_panel(status, percent, speed, logs, available_width - menu_width - 1)
        panels_grid.add_row(menu_panel, right_panel)
    else:
        right_panel = make_status_panel(status, percent, speed, logs, available_width)
        panels_grid.add_row(menu_panel)
        panels_grid.add_row(right_panel)
    return panels_grid



def show_screen(status = "Ожидание команды...", percent = 0.0, speed = "-", logs = None):
    clear_screen()
    console.print(header)
    console.print(divider)
    console.print(build_panels(status, percent, speed, logs))

logs_history = ["[#94a3b8]Система готова к работе.[/]"]

while True:
    show_screen(logs = logs_history)

    choice = Prompt.ask(
        "\n[bold #afff00]MIRRORS >[/] [bold #e2e8f0]Выберите действие[/]",
        choices = ["1", "2", "3", "0"]
    )

    if choice == "0":
        console.print("\n[bold #afff00]Выход из программы... До встречи![/]")
        break

    url = Prompt.ask("[bold #afff00]MIRRORS >[/] [bold #e2e8f0]Вставьте ссылку[/]").strip()
    logs_history.append(f"Запрос ссылки: {url[:28]}...")
    show_screen(status = "Получение данных...", logs = logs_history)

    try:
        is_direct_image = choice == "3" and url.split("?")[0].lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"))

        if is_direct_image:
            info = {}
            title = os.path.splitext(os.path.basename(url.split("?")[0]))[0] or "image"
            logs_history.append(f"Найдено фото: [bold #afff00]{title[:22]}...[/]")
        else:
            with yt_dlp.YoutubeDL({"quiet":True, "no_warnings": True, "logger": QuietLogger()}) as ydl:
                info = ydl.extract_info(url, download = False)
                title = info.get("title", "Без названия")
                logs_history.append(f"Найдено: [bold #afff00]{title[:26]}...[/]")

        clear_screen()
        console.print(header)
        console.print(divider)

        with Live(build_panels("Подготовка...", 0.0, "-", logs_history), console = console, refresh_per_second = 10) as live:

            def progress_hook(d):
                if d["status"] == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    downloaded = d.get("downloaded_bytes", 0)
                    pct = (downloaded / total * 100) if total > 0 else 0.0
                    spd = d.get("_speed_str", "—").strip()
                    live.update(build_panels("Скачивание...", pct, spd, logs_history))
                elif d["status"] == "finished":
                    live.update(build_panels("Обработка файла...", 100.0, "Готово", logs_history))

            if choice == "1":  # Скачать Видео (совместимый H.264 MP4)
                ydl_opts = {
                    "format": "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/b[ext=mp4]/bv*+ba/b",
                    "merge_output_format": "mp4",
                    "outtmpl": os.path.join(SAVE_DIR, "%(title)s.%(ext)s"),
                    "concurrent_fragment_downloads": 16,
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "no_warnings": True,
                    "logger": QuietLogger(),
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            elif choice == "2":  # Скачать Аудио (MP3)
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(SAVE_DIR, "%(title)s.%(ext)s"),
                    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "no_warnings": True,
                    "logger": QuietLogger(),
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            elif choice == "3":  # Скачать Фото / Превью
                img_url = url if is_direct_image else (info.get("thumbnail") or url)
                safe_name = "".join(c for c in title if c.isalnum() or c in " _-").strip()
                req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as resp, open(os.path.join(SAVE_DIR, f"{safe_name or 'preview'}.jpg"), "wb") as out_file:
                    out_file.write(resp.read())
                live.update(build_panels("Завершено!", 100.0, "Мгновенно", logs_history))

        logs_history.append(f"[bold #afff00]Файл сохранён в {SAVE_DIR}![/]")
        show_screen(status="Завершено!", percent=100.0, speed="—", logs=logs_history)

    except Exception as e:
        err_text = escape(friendly_error(e))
        logs_history.append(f"[bold #FF003C]Ошибка: {err_text}[/]")
        show_screen(status="Ошибка!", percent=0.0, speed="—", logs=logs_history)

   
    console.input("\n[#94a3b8]Нажмите Enter, чтобы продолжить...[/]")
