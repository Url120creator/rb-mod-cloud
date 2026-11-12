import os
import sys
import shutil
import threading
import subprocess
import urllib.request
import tkinter as tk

APP_NAME = "RB Mod Hub"
EXE_NAME = "rb_mod_hub.exe"
GITHUB_EXE_URL = "https://github.com/Url120creator/rb-mod-cloud/releases/latest/download/rb_mod_hub.exe"
REQUIRED_LIBS = [
    ("customtkinter", "customtkinter"),
    ("pillow", "PIL"),
    ("keyboard", "keyboard"),
]

BG_DARK = "#0A0D1A"
CARD_BG = "#12172B"
CARD_BORDER = "#242F56"
ACCENT_PURPLE = "#7B4DFF"
ACCENT_CYAN = "#00E5FF"
TEXT_MAIN = "#F3F6FF"
TEXT_DIM = "#8E9BC3"
SUCCESS_GREEN = "#2EE59D"
WARN_YELLOW = "#FFD166"


def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)


class SpaceInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Установка {APP_NAME}")
        self.geometry("580x470")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)

        ico = resource_path("icon.ico")
        if os.path.exists(ico):
            try:
                self.iconbitmap(ico)
            except Exception:
                pass

        self.install_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "RB_Mod_Hub")
        self.installed_exe = os.path.join(self.install_dir, EXE_NAME)
        self.is_installing = False
        self.is_finished = False

        self._center_window(580, 470)
        self._build_ui()

    def _center_window(self, w: int, h: int):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _build_ui(self):
        # Верхняя шапка
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=28, pady=(24, 10))

        logo = tk.Canvas(header, width=54, height=54, bg=BG_DARK, highlightthickness=0)
        logo.pack(side="left", padx=(0, 14))
        logo.create_oval(4, 4, 50, 50, fill="#161D38", outline=ACCENT_PURPLE, width=2)
        logo.create_oval(14, 14, 40, 40, fill=ACCENT_PURPLE, outline="")
        logo.create_arc(6, 20, 48, 34, start=160, end=220, style="arc", outline=ACCENT_CYAN, width=3)

        title_box = tk.Frame(header, bg=BG_DARK)
        title_box.pack(side="left", fill="y")
        tk.Label(title_box, text="RB MOD HUB", font=("Segoe UI", 18, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(anchor="w")
        tk.Label(title_box, text="Мастер установки и проверки библиотек", font=("Segoe UI", 10), fg=TEXT_DIM, bg=BG_DARK).pack(anchor="w")

        # Карточка этапов
        card = tk.Frame(self, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=12)

        tk.Label(card, text="КОМПОНЕНТЫ И ЗАВИСИМОСТИ", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=CARD_BG).pack(anchor="w", padx=18, pady=(14, 8))

        self.step_labels = {}
        steps = [
            ("python", "Среда Python и менеджер пакетов pip"),
            ("customtkinter", "Библиотека CustomTkinter (интерфейс)"),
            ("pillow", "Библиотека Pillow (графика и иконки)"),
            ("keyboard", "Библиотека Keyboard (горячие клавиши)"),
            ("app", "Установка файлов RB Mod Hub и ярлыка"),
        ]

        for key, title in steps:
            row = tk.Frame(card, bg=CARD_BG)
            row.pack(fill="x", padx=18, pady=5)
            tk.Label(row, text=title, font=("Segoe UI", 10), fg=TEXT_MAIN, bg=CARD_BG).pack(side="left")
            status = tk.Label(row, text="Ожидание", font=("Segoe UI", 9, "bold"), fg=TEXT_DIM, bg=CARD_BG)
            status.pack(side="right")
            self.step_labels[key] = status

        # Прогресс-бар
        prog_wrap = tk.Frame(self, bg=BG_DARK)
        prog_wrap.pack(fill="x", padx=28, pady=(4, 6))

        self.status_text = tk.Label(prog_wrap, text="Нажмите «Установить» для проверки системы", font=("Segoe UI", 9), fg=TEXT_DIM, bg=BG_DARK)
        self.status_text.pack(anchor="w", pady=(0, 6))

        self.prog_canvas = tk.Canvas(prog_wrap, height=10, bg="#171E36", highlightthickness=0)
        self.prog_canvas.pack(fill="x")
        self.prog_fill = self.prog_canvas.create_rectangle(0, 0, 0, 10, fill=ACCENT_CYAN, width=0)

        # Кнопка действия
        btn_wrap = tk.Frame(self, bg=BG_DARK)
        btn_wrap.pack(fill="x", padx=28, pady=(12, 22))

        self.action_btn = tk.Button(
            btn_wrap,
            text="Установить RB Mod Hub",
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF",
            bg=ACCENT_PURPLE,
            activebackground="#6236E8",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            height=2,
            command=self._on_button_click,
        )
        self.action_btn.pack(fill="x")

    def _set_progress(self, percent: int, message: str):
        def update():
            w = self.prog_canvas.winfo_width() or 524
            self.prog_canvas.coords(self.prog_fill, 0, 0, int(w * percent / 100), 10)
            self.status_text.config(text=message)
        self.after(0, update)

    def _set_step(self, key: str, text: str, color: str):
        self.after(0, lambda: self.step_labels[key].config(text=text, fg=color))

    def _on_button_click(self):
        if self.is_finished:
            if os.path.exists(self.installed_exe):
                subprocess.Popen([self.installed_exe], cwd=self.install_dir)
            self.destroy()
            return

        if not self.is_installing:
            self.is_installing = True
            self.action_btn.config(state="disabled", text="Идёт проверка и установка...", bg="#2A3356")
            threading.Thread(target=self._run_install, daemon=True).start()

    def _run_install(self):
        no_win = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        # 1. Проверка Python
        self._set_progress(12, "Поиск Python в системе...")
        self._set_step("python", "Проверка...", WARN_YELLOW)
        py_exe = shutil.which("python") or shutil.which("py")

        if py_exe:
            self._set_step("python", "✔ Найден", SUCCESS_GREEN)
            # 2. Проверка и установка недостающих библиотек
            for idx, (pkg_name, import_name) in enumerate(REQUIRED_LIBS):
                pct = 25 + idx * 15
                self._set_progress(pct, f"Проверка библиотеки {pkg_name}...")
                self._set_step(pkg_name, "Проверка...", WARN_YELLOW)

                check = subprocess.run(
                    [py_exe, "-c", f"import {import_name}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=no_win,
                )
                if check.returncode == 0:
                    self._set_step(pkg_name, "✔ Установлена", SUCCESS_GREEN)
                else:
                    self._set_progress(pct + 5, f"Скачивание {pkg_name} через pip...")
                    self._set_step(pkg_name, "Установка...", WARN_YELLOW)
                    inst = subprocess.run(
                        [py_exe, "-m", "pip", "install", "--prefer-binary", pkg_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=no_win,
                    )
                    if inst.returncode == 0:
                        self._set_step(pkg_name, "✔ Докачана", SUCCESS_GREEN)
                    else:
                        self._set_step(pkg_name, "⚠ Ошибка pip", WARN_YELLOW)
        else:
            self._set_step("python", "✔ Встроено в EXE", SUCCESS_GREEN)
            for pkg_name, _ in REQUIRED_LIBS:
                self._set_step(pkg_name, "✔ Встроено в EXE", SUCCESS_GREEN)

        # 3. Копирование или загрузка RB Mod Hub
        self._set_progress(75, "Установка RB Mod Hub...")
        self._set_step("app", "Копирование...", WARN_YELLOW)
        os.makedirs(self.install_dir, exist_ok=True)

        bundled_exe = resource_path(EXE_NAME)
        if os.path.exists(bundled_exe):
            shutil.copy2(bundled_exe, self.installed_exe)
        else:
            self._set_progress(80, "Скачивание последней версии с GitHub...")
            urllib.request.urlretrieve(GITHUB_EXE_URL, self.installed_exe)

        bundled_ico = resource_path("icon.ico")
        installed_ico = os.path.join(self.install_dir, "icon.ico")
        if os.path.exists(bundled_ico):
            shutil.copy2(bundled_ico, installed_ico)

        # 4. Создание ярлыка на Рабочем столе
        self._set_progress(92, "Создание ярлыка на Рабочем столе...")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        lnk_path = os.path.join(desktop, f"{APP_NAME}.lnk")
        ps_cmd = (
            f'$ws = New-Object -ComObject WScript.Shell; '
            f'$s = $ws.CreateShortcut("{lnk_path}"); '
            f'$s.TargetPath = "{self.installed_exe}"; '
            f'$s.WorkingDirectory = "{self.install_dir}"; '
            f'$s.IconLocation = "{installed_ico}"; '
            f'$s.Save()'
        )
        subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd], creationflags=no_win)

        self._set_step("app", "✔ Установлено", SUCCESS_GREEN)
        self._set_progress(100, "Установка полностью завершена!")
        self.is_installing = False
        self.is_finished = True
        self.after(0, lambda: self.action_btn.config(state="normal", text="Запустить RB Mod Hub", bg=SUCCESS_GREEN, fg="#08121E"))


if __name__ == "__main__":
    app = SpaceInstaller()
    app.mainloop()
