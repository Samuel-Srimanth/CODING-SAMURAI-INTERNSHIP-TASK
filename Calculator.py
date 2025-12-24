import tkinter as tk
from tkinter import font as tkfont
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg="#1e1f29")
        self.geometry("360x520")
        self.minsize(320, 480)

        # fonts
        self.large_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.mid_font = tkfont.Font(family="Helvetica", size=16)
        self.small_font = tkfont.Font(family="Helvetica", size=12)

        self.expression = ""
        self._build_ui()

    def _build_ui(self):
        # Title
        title = tk.Label(self, text="Calculator", bg="#1e1f29", fg="#dfe7ff", font=self.mid_font)
        title.pack(pady=(12, 0))

        # Display
        display_frame = tk.Frame(self, bg="#1e1f29")
        display_frame.pack(fill="both", padx=16, pady=(8, 12))
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg="#2b2d3a",
            fg="#ffffff",
            font=self.large_font,
            padx=16,
            pady=24
        )
        display.pack(fill="both", expand=True)

        # Buttons container using grid (reliable layout)
        btn_frame = tk.Frame(self, bg="#1e1f29")
        btn_frame.pack(padx=12, pady=(0, 12), fill="both", expand=True)

        accent = "#7c5cff"
        btn_style = {"font": self.mid_font, "bd": 0, "relief": "flat",
                     "fg": "#f1f3ff", "bg": "#2f3140", "activebackground": "#3b3d50",
                     "activeforeground": "#ffffff", "cursor":"hand2", "padx":8, "pady":14}

        # Button layout map: (text, row, col, colspan)
        layout = [
            [("C",0,0,1), ("⌫",0,1,1), ("% ",0,2,1), ("/",0,3,1)],
            [("(",1,0,1), (")",1,1,1), ("√",1,2,1), ("*",1,3,1)],
            [("7",2,0,1), ("8",2,1,1), ("9",2,2,1), ("-",2,3,1)],
            [("4",3,0,1), ("5",3,1,1), ("6",3,2,1), ("+",3,3,1)],
            [("1",4,0,1), ("2",4,1,1), ("3",4,2,1), ("=",4,3,1)],
            [("±",5,0,1), ("0",5,1,2), (".",5,3,1)],
        ]

        for row in layout:
            for (text, r, c, colspan) in row:
                btn = tk.Button(btn_frame, text=text.strip(), **btn_style)
                # special colors
                if text.strip() in {"=", "+", "-", "*", "/", "√"}:
                    btn.configure(bg=accent, activebackground=accent)
                if text.strip() == "C":
                    btn.configure(bg="#ff6b6b", activebackground="#ff7b7b")
                if text.strip() == "⌫":
                    btn.configure(bg="#6b6f76")
                # place with grid
                btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=6, pady=6)
                btn.configure(command=lambda x=text.strip(): self.on_press(x))

        # Make grid cells expand evenly
        total_rows = 6
        total_cols = 4
        for i in range(total_rows):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(total_cols):
            btn_frame.columnconfigure(j, weight=1)

        # Footer
        footer = tk.Label(self, text="Safe · √ % ± parentheses", bg="#1e1f29", fg="#96a0c4", font=self.small_font)
        footer.pack(pady=(4,8))

    # Button handling
    def on_press(self, label):
        if label == "C":
            self.expression = ""
            self.display_var.set("0")
            return
        if label == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
            return
        if label == "=":
            self.calculate()
            return
        if label == "√":
            # if empty, ignore
            if not self.expression:
                return
            # wrap and evaluate
            try:
                val = eval(self.expression, {"math": math})
                result = math.sqrt(val)
                self.expression = str(result)
                self.display_var.set(self.expression)
            except:
                self.display_var.set("Error")
                self.expression = ""
            return
        if label == "%":
            # append /100 and evaluate
            if not self.expression:
                return
            self.expression += "/100"
            self.calculate()
            return
        if label == "±":
            if not self.expression:
                return
            # toggle sign of whole expression (simple approach)
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression)
            return

        # Normal append (digits/operators/.)
        self.expression += label
        self.display_var.set(self.expression)

    def calculate(self):
        if not self.expression:
            return
        # basic safety: avoid ending with operator
        if self.expression[-1] in "+-*/.":
            self.display_var.set("Error")
            self.expression = ""
            return
        try:
            result = eval(self.expression, {"math": math})
            # make integers look clean
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.display_var.set(self.expression)
        except:
            self.display_var.set("Error")
            self.expression = ""

if __name__ == "__main__":
    Calculator().mainloop()
