"""
JARVIS Green Hacker Voice & Spatial Calculator - Desktop GUI Edition (Tkinter)
Powered by Ashish's Calculation Engine (ashish.py)
"""

import os
import sys
import ctypes
import subprocess
import threading
import platform
import tkinter as tk
from tkinter import font
import ashish

class JarvisHackerCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS // Green Hacker OS Calculator")
        self.root.geometry("400x610")
        self.root.resizable(False, False)
        self.root.configure(bg="#020804")

        # Calculator State
        self.current_value = "0"
        self.first_operand = None
        self.operator = None
        self.reset_display = False
        self.history = []

        # Background Audio State (audio.mp3) - 500% Volume Autoplay
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_file = os.path.join(base_dir, "audio.mp3")
        for c in ["audio.mp3", "audio.mp3.mpeg"]:
            p = os.path.join(base_dir, c)
            if os.path.exists(p):
                self.audio_file = p
                break
        self.is_playing_bgm = False
        self.bgm_proc = None
        self.bgm_thread = None
        self.stop_bgm_event = threading.Event()
        self.winmm = ctypes.windll.winmm if hasattr(ctypes, 'windll') else None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Hacker Fonts
        self.title_font = font.Font(family="Consolas", size=10, weight="bold")
        self.display_font = font.Font(family="Consolas", size=26, weight="bold")
        self.sub_font = font.Font(family="Consolas", size=10)
        self.cmd_font = font.Font(family="Consolas", size=10)
        self.btn_font = font.Font(family="Consolas", size=14, weight="bold")
        self.op_font = font.Font(family="Consolas", size=16, weight="bold")

        self.setup_ui()
        self.bind_keys()
        self.start_bgm()

    def setup_ui(self):
        # Header Telemetry Bar
        top_bar = tk.Frame(self.root, bg="#020804", padx=16, pady=6)
        top_bar.pack(fill=tk.X)

        title_lbl = tk.Label(
            top_bar,
            text="◈ JARVIS.OS // CORE ACTIVE",
            font=self.title_font,
            fg="#00ff66",
            bg="#020804"
        )
        title_lbl.pack(side=tk.LEFT)

        self.bgm_btn = tk.Button(
            top_bar,
            text="▶ BGM: OFF",
            command=self.toggle_bgm,
            font=font.Font(family="Consolas", size=8, weight="bold"),
            bg="#041408",
            fg="#00ff66",
            activebackground="#00ff66",
            activeforeground="#020804",
            relief="solid",
            bd=1,
            padx=6,
            pady=1,
            cursor="hand2"
        )
        self.bgm_btn.pack(side=tk.RIGHT, padx=(0, 8))

        self.status_lbl = tk.Label(
            top_bar,
            text="SYS.ONLINE",
            font=font.Font(family="Consolas", size=8, weight="bold"),
            fg="#39ff14",
            bg="#020804"
        )
        self.status_lbl.pack(side=tk.RIGHT)

        # Holographic Display Screen (Green Phosphor CRT effect)
        screen_outer = tk.Frame(self.root, bg="#00ff66", padx=1.5, pady=1.5)
        screen_outer.pack(fill=tk.X, padx=16, pady=(0, 8))

        disp_frame = tk.Frame(screen_outer, bg="#041207", padx=14, pady=12)
        disp_frame.pack(fill=tk.BOTH, expand=True)

        self.expr_label = tk.Label(
            disp_frame,
            text="",
            font=self.sub_font,
            fg="#4ade80",
            bg="#041207",
            anchor="e"
        )
        self.expr_label.pack(fill=tk.X)

        self.display_label = tk.Label(
            disp_frame,
            text="0",
            font=self.display_font,
            fg="#00ff66",
            bg="#041207",
            anchor="e"
        )
        self.display_label.pack(fill=tk.X)

        # Command Input Bar
        cmd_bar = tk.Frame(self.root, bg="#020804", padx=16, pady=4)
        cmd_bar.pack(fill=tk.X)

        self.cmd_entry = tk.Entry(
            cmd_bar,
            font=self.cmd_font,
            bg="#041207",
            fg="#00ff66",
            insertbackground="#00ff66",
            relief="solid",
            bd=1
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.cmd_entry.insert(0, "JARVIS cmd: e.g. 'what is 25 plus 75'")
        self.cmd_entry.bind("<FocusIn>", self.on_cmd_focus_in)
        self.cmd_entry.bind("<Return>", lambda e: self.execute_voice_command())

        exec_btn = tk.Button(
            cmd_bar,
            text="RUN",
            command=self.execute_voice_command,
            font=font.Font(family="Consolas", size=9, weight="bold"),
            bg="#00ff66",
            fg="#020804",
            activebackground="#39ff14",
            activeforeground="#020804",
            relief="flat",
            bd=0,
            padx=10,
            cursor="hand2"
        )
        exec_btn.pack(side=tk.RIGHT)

        # Keypad Grid
        btn_frame = tk.Frame(self.root, bg="#020804")
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(6, 12))

        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btn_frame.columnconfigure(j, weight=1)

        # Green Hacker Layout
        buttons = [
            ("AC", 0, 0, self.on_clear, "#2a0a0a", "#450a0a", "#f87171"),
            ("DEL", 0, 1, self.on_delete, "#061f0c", "#0a3014", "#86efac"),
            ("±", 0, 2, self.on_toggle_sign, "#061f0c", "#0a3014", "#86efac"),
            ("÷", 0, 3, lambda: self.on_operator("/"), "#093315", "#0e4d20", "#00ff66"),

            ("7", 1, 0, lambda: self.on_digit("7"), "#041408", "#082910", "#f0fdf4"),
            ("8", 1, 1, lambda: self.on_digit("8"), "#041408", "#082910", "#f0fdf4"),
            ("9", 1, 2, lambda: self.on_digit("9"), "#041408", "#082910", "#f0fdf4"),
            ("×", 1, 3, lambda: self.on_operator("*"), "#093315", "#0e4d20", "#00ff66"),

            ("4", 2, 0, lambda: self.on_digit("4"), "#041408", "#082910", "#f0fdf4"),
            ("5", 2, 1, lambda: self.on_digit("5"), "#041408", "#082910", "#f0fdf4"),
            ("6", 2, 2, lambda: self.on_digit("6"), "#041408", "#082910", "#f0fdf4"),
            ("−", 2, 3, lambda: self.on_operator("-"), "#093315", "#0e4d20", "#00ff66"),

            ("1", 3, 0, lambda: self.on_digit("1"), "#041408", "#082910", "#f0fdf4"),
            ("2", 3, 1, lambda: self.on_digit("2"), "#041408", "#082910", "#f0fdf4"),
            ("3", 3, 2, lambda: self.on_digit("3"), "#041408", "#082910", "#f0fdf4"),
            ("+", 3, 3, lambda: self.on_operator("+"), "#093315", "#0e4d20", "#00ff66"),

            ("0", 4, 0, lambda: self.on_digit("0"), "#041408", "#082910", "#f0fdf4"),
            (".", 4, 1, self.on_dot, "#041408", "#082910", "#f0fdf4"),
            ("=", 4, 2, self.on_equal, "#00ff66", "#39ff14", "#020804", 2),
        ]

        for item in buttons:
            text = item[0]
            row = item[1]
            col = item[2]
            cmd = item[3]
            bg = item[4]
            active_bg = item[5]
            fg = item[6]
            colspan = item[7] if len(item) > 7 else 1

            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                font=self.op_font if text in ["+", "−", "×", "÷", "="] else self.btn_font,
                bg=bg,
                fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief="solid",
                bd=1,
                cursor="hand2"
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    def on_cmd_focus_in(self, event):
        if "JARVIS cmd" in self.cmd_entry.get():
            self.cmd_entry.delete(0, tk.END)

    def execute_voice_command(self):
        query = self.cmd_entry.get().strip()
        if not query or "JARVIS cmd" in query:
            return

        self.status_lbl.config(text="PROCESSING", fg="#a3e635")
        parsed = ashish.parse_voice_command(query)

        if not parsed:
            self.status_lbl.config(text="ERROR", fg="#ef4444")
            self.current_value = "invalid input"
            self.display_label.config(fg="#ef4444")
            self.update_display()
            return

        if parsed["action"] == "play_audio":
            self.start_bgm()
            self.status_lbl.config(text="AUDIO.500%", fg="#39ff14")
            return

        if parsed["action"] == "pause_audio":
            self.stop_bgm()
            self.status_lbl.config(text="AUDIO.OFF", fg="#eab308")
            return

        if parsed["action"] == "volume_500":
            self.start_bgm()
            self.status_lbl.config(text="VOL: 500%", fg="#39ff14")
            return

        if parsed["action"] == "clear":
            self.on_clear()
            self.status_lbl.config(text="CLEARED", fg="#39ff14")
            return

        if parsed["action"] == "delete":
            self.on_delete()
            self.status_lbl.config(text="DELETED", fg="#39ff14")
            return

        if parsed["action"] == "direct_result":
            res = parsed["res"]
            self.expr_label.config(text=f"{parsed['display']} =")
            self.current_value = str(res)
            self.display_label.config(fg="#00ff66")
            self.status_lbl.config(text="RESULT", fg="#39ff14")
            self.reset_display = True
            self.update_display()
            return

        if parsed["action"] == "calculate":
            res = ashish.calculate(parsed["a"], parsed["op"], parsed["b"])
            self.expr_label.config(text=f"{parsed['display']} =")
            self.current_value = str(res)
            self.display_label.config(fg="#00ff66" if res != "cannot divide" else "#ef4444")
            self.status_lbl.config(text="RESULT", fg="#39ff14")
            self.reset_display = True
            self.update_display()

    def on_digit(self, digit):
        if self.reset_display or self.current_value in ["cannot divide", "invalid input"]:
            self.current_value = digit
            self.reset_display = False
        else:
            if self.current_value == "0":
                self.current_value = digit
            else:
                if len(self.current_value) < 16:
                    self.current_value += digit
        self.update_display()

    def on_dot(self):
        if self.reset_display or self.current_value in ["cannot divide", "invalid input"]:
            self.current_value = "0."
            self.reset_display = False
        elif "." not in self.current_value:
            self.current_value += "."
        self.update_display()

    def on_toggle_sign(self):
        if self.current_value in ["0", "cannot divide", "invalid input"]:
            return
        if self.current_value.startswith("-"):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = "-" + self.current_value
        self.update_display()

    def on_delete(self):
        if self.current_value in ["cannot divide", "invalid input"] or self.reset_display:
            self.on_clear()
            return
        if len(self.current_value) <= 1 or (len(self.current_value) == 2 and self.current_value.startswith("-")):
            self.current_value = "0"
        else:
            self.current_value = self.current_value[:-1]
        self.update_display()

    def on_clear(self):
        self.current_value = "0"
        self.first_operand = None
        self.operator = None
        self.reset_display = False
        self.expr_label.config(text="")
        self.display_label.config(fg="#00ff66")
        self.status_lbl.config(text="ONLINE", fg="#39ff14")
        self.update_display()

    def on_operator(self, op):
        if self.current_value in ["cannot divide", "invalid input"]:
            return

        op_symbols = {"+": "+", "-": "−", "*": "×", "/": "÷"}

        if self.operator and not self.reset_display:
            self.on_equal(auto_chain=True)

        self.first_operand = self.current_value
        self.operator = op
        self.reset_display = True
        self.expr_label.config(text=f"{self.first_operand} {op_symbols.get(op, op)}")

    def on_equal(self, auto_chain=False):
        if not self.operator or self.first_operand is None:
            return

        op_symbols = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        symbol = op_symbols.get(self.operator, self.operator)

        res = ashish.calculate(self.first_operand, self.operator, self.current_value)

        if res == "cannot divide" or res == "invalid input":
            self.current_value = str(res)
            self.display_label.config(fg="#ef4444")
            self.expr_label.config(text=f"{self.first_operand} {symbol} {self.current_value}")
            self.operator = None
            self.first_operand = None
            self.reset_display = True
            self.status_lbl.config(text="ERROR", fg="#ef4444")
            self.update_display()
            return

        formatted_res = str(res)

        if not auto_chain:
            self.expr_label.config(text=f"{self.first_operand} {symbol} {self.current_value} =")
            self.operator = None
            self.status_lbl.config(text="RESULT", fg="#39ff14")
        else:
            self.expr_label.config(text=f"{formatted_res} {symbol}")

        self.history.append(f"{self.first_operand} {symbol} {self.current_value} = {formatted_res}")
        self.current_value = formatted_res
        self.display_label.config(fg="#00ff66")
        self.reset_display = True
        self.update_display()

    def update_display(self):
        length = len(self.current_value)
        if length > 12:
            self.display_font.config(size=18)
        elif length > 8:
            self.display_font.config(size=22)
        else:
            self.display_font.config(size=26)

        self.display_label.config(text=self.current_value)

    def bind_keys(self):
        for digit in "0123456789":
            self.root.bind(digit, lambda e, d=digit: self.on_digit(d) if e.widget != self.cmd_entry else None)
        self.root.bind(".", lambda e: self.on_dot() if e.widget != self.cmd_entry else None)
        self.root.bind("+", lambda e: self.on_operator("+") if e.widget != self.cmd_entry else None)
        self.root.bind("-", lambda e: self.on_operator("-") if e.widget != self.cmd_entry else None)
        self.root.bind("*", lambda e: self.on_operator("*") if e.widget != self.cmd_entry else None)
        self.root.bind("/", lambda e: self.on_operator("/") if e.widget != self.cmd_entry else None)
        self.root.bind("<Return>", lambda e: self.on_equal() if e.widget != self.cmd_entry else None)
        self.root.bind("=", lambda e: self.on_equal() if e.widget != self.cmd_entry else None)
        self.root.bind("<BackSpace>", lambda e: self.on_delete() if e.widget != self.cmd_entry else None)
        self.root.bind("<Escape>", lambda e: self.on_clear())

    def start_bgm(self):
        if self.is_playing_bgm or not os.path.exists(self.audio_file):
            return
        self.is_playing_bgm = True
        self.stop_bgm_event.clear()

        def bgm_worker():
            while not self.stop_bgm_event.is_set():
                try:
                    if platform.system() == "Darwin":
                        # macOS native afplay with 500% volume (-v 5)
                        self.bgm_proc = subprocess.Popen(["afplay", "-v", "5", self.audio_file])
                        self.bgm_proc.wait()
                    elif self.winmm:
                        self.winmm.mciSendStringW(f'open "{self.audio_file}" type mpegvideo alias jarvis_bgm', None, 0, None)
                        self.winmm.mciSendStringW('setaudio jarvis_bgm volume to 1000', None, 0, None)
                        self.winmm.mciSendStringW('play jarvis_bgm repeat', None, 0, None)
                        break
                    else:
                        self.bgm_proc = subprocess.Popen(
                            ["ffplay", "-nodisp", "-autoexit", "-volume", "500", self.audio_file],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self.bgm_proc.wait()
                except Exception as e:
                    print("BGM audio loop exception:", e)
                    break

        self.bgm_thread = threading.Thread(target=bgm_worker, daemon=True)
        self.bgm_thread.start()
        self.bgm_btn.config(text="⏹ BGM: 500%", bg="#ef4444", fg="#ffffff")
        self.status_lbl.config(text="AUDIO 500%", fg="#39ff14")

    def stop_bgm(self):
        self.is_playing_bgm = False
        self.stop_bgm_event.set()
        if self.bgm_proc:
            try:
                self.bgm_proc.terminate()
            except Exception:
                pass
            self.bgm_proc = None
        if self.winmm:
            try:
                self.winmm.mciSendStringW('stop jarvis_bgm', None, 0, None)
                self.winmm.mciSendStringW('close jarvis_bgm', None, 0, None)
            except Exception:
                pass
        self.bgm_btn.config(text="▶ BGM: OFF", bg="#041408", fg="#00ff66")
        self.status_lbl.config(text="SYS.ONLINE", fg="#39ff14")

    def toggle_bgm(self):
        if self.is_playing_bgm:
            self.stop_bgm()
        else:
            self.start_bgm()

    def on_close(self):
        self.stop_bgm()
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = JarvisHackerCalculatorGUI(app_root)
    app_root.mainloop()
