"""
Emotional Support Chatbot - Tkinter GUI
Uses the same logic as emotional_support_chatbot.py
"""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from emotional_support_chatbot import (
    clean_input,
    create_action_plan,
    detect_emotion,
    generate_response,
    suggest_exercise,
)


def parse_intensity(text: str) -> int | None:
    m = re.search(r"\b(\d{1,2})\b", text.strip())
    if not m:
        return None
    v = int(m.group(1))
    if 1 <= v <= 10:
        return v
    return None


class EmotionalSupportApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Emotional Support Chatbot")
        self.root.minsize(520, 580)
        self.root.geometry("680x760")

        self.step = 0
        self.feeling = tk.StringVar()
        self.emotions = tk.StringVar()
        self.cause = tk.StringVar()
        self.intensity_var = tk.IntVar(value=5)
        self.duration = tk.StringVar()

        self._setup_style()
        self._build_shell()
        self.show_step(0)

    def _setup_style(self) -> None:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        self.bg = "#eef2f6"
        self.panel = "#ffffff"
        self.accent = "#3d6b7a"
        self.text_muted = "#5c6b7a"

        self.root.configure(bg=self.bg)
        try:
            self.font_title = ("Segoe UI", 16, "bold")
            self.font_body = ("Segoe UI", 11)
            self.font_small = ("Segoe UI", 9)
        except tk.TclError:
            self.font_title = ("TkDefaultFont", 16, "bold")
            self.font_body = ("TkDefaultFont", 11)
            self.font_small = ("TkDefaultFont", 9)

        style.configure("Header.TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.panel)
        style.configure("Title.TLabel", background=self.bg, foreground="#1a252f", font=self.font_title)
        style.configure("Muted.TLabel", background=self.bg, foreground=self.text_muted, font=self.font_small)
        style.configure("Q.TLabel", background=self.panel, foreground="#1a252f", font=self.font_body)
        style.configure("Accent.TButton", padding=(16, 8))
        style.map(
            "Accent.TButton",
            background=[("active", "#335d6a")],
        )
        try:
            style.configure("Accent.TButton", background=self.accent, foreground="white")
        except tk.TclError:
            pass

    def _build_shell(self) -> None:
        header = ttk.Frame(self.root, style="Header.TFrame", padding=(24, 20, 24, 8))
        header.pack(fill=tk.X)

        ttk.Label(
            header,
            text="Emotional Support Chatbot",
            style="Title.TLabel",
        ).pack(anchor=tk.W)

        ttk.Label(
            header,
            text="A supportive check-in - not a substitute for professional care in a crisis.",
            style="Muted.TLabel",
            wraplength=620,
        ).pack(anchor=tk.W, pady=(6, 0))

        self.content = ttk.Frame(self.root, style="Header.TFrame", padding=24)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.card = ttk.Frame(self.content, style="Card.TFrame", padding=20)
        self.card.pack(fill=tk.BOTH, expand=True)

        self.inner = ttk.Frame(self.card, style="Card.TFrame")
        self.inner.pack(fill=tk.BOTH, expand=True)

        self.btn_row = ttk.Frame(self.root, style="Header.TFrame", padding=(24, 8, 24, 20))
        self.btn_row.pack(fill=tk.X, side=tk.BOTTOM)

    def show_step(self, step: int) -> None:
        self.step = step
        for w in self.inner.winfo_children():
            w.destroy()

        if step == 0:
            self._step_welcome()
        elif step == 1:
            self._step_question(
                "How are you feeling today?",
                self.feeling,
                "Share a few words about your overall mood or energy.",
            )
        elif step == 2:
            self._step_question(
                "What emotions are you feeling?",
                self.emotions,
                "Name as many as you like (e.g. worry, sadness, irritation).",
            )
        elif step == 3:
            self._step_question(
                "What do you think caused this feeling, or what is on your mind?",
                self.cause,
                "There is no wrong answer - context helps.",
            )
        elif step == 4:
            self._step_intensity()
        elif step == 5:
            self._step_question(
                "How long have you felt this way?",
                self.duration,
                "e.g. since this morning, a few days, on and off for weeks.",
            )
        elif step == 6:
            self._step_results()

        self._rebuild_buttons()

    def _step_welcome(self) -> None:
        ttk.Label(
            self.inner,
            text="Welcome",
            style="Q.TLabel",
            font=self.font_title,
        ).pack(anchor=tk.W)

        body = (
            "This space is for a gentle emotional check-in.\n\n"
            "You will be asked a few short questions. Then you will see "
            "supportive words, a suggested exercise, and a simple 5-minute plan.\n\n"
            "Take your time. You can close the window anytime."
        )
        ttk.Label(
            self.inner,
            text=body,
            style="Q.TLabel",
            wraplength=580,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(12, 0))

    def _step_question(self, title: str, var: tk.StringVar, hint: str) -> None:
        ttk.Label(self.inner, text=title, style="Q.TLabel", font=self.font_title).pack(anchor=tk.W)
        ttk.Label(self.inner, text=hint, style="Q.TLabel", foreground=self.text_muted).pack(
            anchor=tk.W, pady=(4, 12)
        )
        entry = scrolledtext.ScrolledText(
            self.inner,
            height=6,
            wrap=tk.WORD,
            font=self.font_body,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#c5d0d8",
            highlightcolor=self.accent,
        )
        entry.pack(fill=tk.BOTH, expand=True)
        entry.insert("1.0", var.get())

        def on_key(_: object = None) -> None:
            var.set(entry.get("1.0", tk.END).rstrip())

        entry.bind("<KeyRelease>", on_key)
        self._current_entry = entry

    def _step_intensity(self) -> None:
        ttk.Label(
            self.inner,
            text="How intense is it?",
            style="Q.TLabel",
            font=self.font_title,
        ).pack(anchor=tk.W)
        ttk.Label(
            self.inner,
            text="1 = mild  |  10 = overwhelming",
            style="Q.TLabel",
            foreground=self.text_muted,
        ).pack(anchor=tk.W, pady=(4, 16))

        row = ttk.Frame(self.inner, style="Card.TFrame")
        row.pack(fill=tk.X)

        self.intensity_label = ttk.Label(
            row,
            text=str(self.intensity_var.get()),
            style="Q.TLabel",
            font=(self.font_body[0], 22, "bold"),
            width=3,
        )
        self.intensity_label.pack(side=tk.LEFT, padx=(0, 16))

        scale = ttk.Scale(
            row,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.intensity_var,
            command=lambda _: self._update_intensity_label(),
            length=420,
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._update_intensity_label()

        ttk.Label(
            self.inner,
            text="Drag the slider, or type a number 1-10 in the box below if you prefer.",
            style="Q.TLabel",
            foreground=self.text_muted,
            wraplength=560,
        ).pack(anchor=tk.W, pady=(16, 8))

        alt = ttk.Frame(self.inner, style="Card.TFrame")
        alt.pack(anchor=tk.W)
        ttk.Label(alt, text="Optional:", style="Q.TLabel").pack(side=tk.LEFT, padx=(0, 8))
        self.intensity_entry = ttk.Entry(alt, width=8, font=self.font_body)
        self.intensity_entry.pack(side=tk.LEFT)
        self.intensity_entry.bind("<KeyRelease>", self._maybe_sync_intensity_from_entry)

    def _update_intensity_label(self, *_args: object) -> None:
        if hasattr(self, "intensity_label"):
            try:
                v = int(round(float(self.intensity_var.get())))
            except (tk.TclError, ValueError, TypeError):
                v = 5
            v = max(1, min(10, v))
            self.intensity_label.config(text=str(v))

    def _maybe_sync_intensity_from_entry(self, _: object = None) -> None:
        raw = self.intensity_entry.get()
        p = parse_intensity(raw)
        if p is not None:
            self.intensity_var.set(p)
            self._update_intensity_label()

    def _step_results(self) -> None:
        feeling = self.feeling.get().strip()
        emotions = self.emotions.get().strip()
        cause = self.cause.get().strip()
        duration = self.duration.get().strip()

        try:
            raw_i = int(round(float(self.intensity_var.get())))
            intensity = raw_i if 1 <= raw_i <= 10 else None
        except (tk.TclError, ValueError, TypeError):
            intensity = None

        combined = f"{feeling} {emotions} {cause}"
        primary, _scores = detect_emotion(combined)

        summary = generate_response(primary, intensity)
        exercise = suggest_exercise(primary)
        plan = create_action_plan(primary, intensity, duration)

        ttk.Label(
            self.inner,
            text="Your check-in summary",
            style="Q.TLabel",
            font=self.font_title,
        ).pack(anchor=tk.W)

        ttk.Label(
            self.inner,
            text=f"Detected focus: {primary.replace('_', ' ').title()}",
            style="Q.TLabel",
            foreground=self.accent,
            font=("Segoe UI", 11, "italic"),
        ).pack(anchor=tk.W, pady=(6, 12))

        out = scrolledtext.ScrolledText(
            self.inner,
            height=22,
            wrap=tk.WORD,
            font=self.font_body,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#c5d0d8",
            state=tk.NORMAL,
        )
        out.pack(fill=tk.BOTH, expand=True)
        full = (
            "SUPPORTIVE SUMMARY\n"
            + "=" * 52
            + "\n\n"
            + summary
            + "\n\n\nSUGGESTED EXERCISE\n"
            + "=" * 52
            + exercise
            + "\n\n"
            + plan
        )
        out.insert(tk.END, full)
        out.configure(state=tk.DISABLED)

    def _rebuild_buttons(self) -> None:
        for w in self.btn_row.winfo_children():
            w.destroy()

        if self.step == 0:
            ttk.Button(
                self.btn_row,
                text="Start check-in",
                style="Accent.TButton",
                command=lambda: self.show_step(1),
            ).pack(side=tk.RIGHT)
            ttk.Button(self.btn_row, text="Exit", command=self._on_exit).pack(side=tk.RIGHT, padx=(0, 8))
            return

        if self.step == 6:
            ttk.Button(
                self.btn_row,
                text="New check-in",
                style="Accent.TButton",
                command=self._new_checkin,
            ).pack(side=tk.RIGHT)
            ttk.Button(self.btn_row, text="Exit", command=self._on_exit).pack(side=tk.RIGHT, padx=(0, 8))
            return

        ttk.Button(self.btn_row, text="Exit", command=self._on_exit).pack(side=tk.RIGHT)
        ttk.Button(
            self.btn_row,
            text="Back",
            command=self._go_back,
        ).pack(side=tk.RIGHT, padx=(0, 8))

        next_text = "Next" if self.step < 5 else "See support"
        ttk.Button(
            self.btn_row,
            text=next_text,
            style="Accent.TButton",
            command=self._go_next,
        ).pack(side=tk.RIGHT, padx=(0, 8))

    def _go_back(self) -> None:
        self._flush_current_field()
        if self.step > 1:
            self.show_step(self.step - 1)

    def _go_next(self) -> None:
        self._flush_current_field()
        if self.step < 5:
            self.show_step(self.step + 1)
        elif self.step == 5:
            self.show_step(6)

    def _flush_current_field(self) -> None:
        if self.step == 1 and hasattr(self, "_current_entry"):
            self.feeling.set(self._current_entry.get("1.0", tk.END).rstrip())
        elif self.step == 2 and hasattr(self, "_current_entry"):
            self.emotions.set(self._current_entry.get("1.0", tk.END).rstrip())
        elif self.step == 3 and hasattr(self, "_current_entry"):
            self.cause.set(self._current_entry.get("1.0", tk.END).rstrip())
        elif self.step == 5 and hasattr(self, "_current_entry"):
            self.duration.set(self._current_entry.get("1.0", tk.END).rstrip())
        elif self.step == 4:
            raw = ""
            if hasattr(self, "intensity_entry"):
                raw = self.intensity_entry.get().strip()
            parsed = parse_intensity(raw)
            if parsed is not None:
                self.intensity_var.set(parsed)

    def _new_checkin(self) -> None:
        self.feeling.set("")
        self.emotions.set("")
        self.cause.set("")
        self.intensity_var.set(5)
        self.duration.set("")
        self.show_step(1)

    def _on_exit(self) -> None:
        if messagebox.askokcancel("Exit", "Close the Emotional Support Chatbot?"):
            self.root.destroy()


def main() -> None:
    root = tk.Tk()
    EmotionalSupportApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
