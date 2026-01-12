import tkinter as tk
from tkinter import messagebox

# ---------------- Tooltip class ----------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="lightyellow", relief='solid', borderwidth=1,
                         font=("Arial", 10))
        label.pack()

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# ---------------- Helper: Subscript function ----------------
def subscript(number):
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(sub_map)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Layered Least Squares GUI (Polished)")
root.configure(bg="#37444c")
root.resizable(True, True)

# Main container frame
main_frame = tk.Frame(root, bg="#37444c")
main_frame.pack(padx=50, pady=20, fill="both", expand=True)

# ---------------- Layer 1: m & n input ----------------
tk.Label(main_frame, text="Number of Equations (m):", bg="#37444c", fg="white", font=("Arial", 11))\
    .grid(row=0, column=0, sticky="w", pady=2)
entry_m = tk.Entry(main_frame, width=5, bg="#2d373d", fg="white", font=("Arial", 11))
entry_m.grid(row=0, column=1, sticky="w", pady=2)
ToolTip(entry_m, "m = # of equations / rows")

tk.Label(main_frame, text="Number of Unknowns (n):", bg="#37444c", fg="white", font=("Arial", 11))\
    .grid(row=1, column=0, sticky="w", pady=2)
entry_n = tk.Entry(main_frame, width=5, bg="#2d373d", fg="white", font=("Arial", 11))
entry_n.grid(row=1, column=1, sticky="w", pady=2)
ToolTip(entry_n, "n = # of unknowns / columns")

# Confirm Size button
tk.Button(main_frame, text="Confirm Size", command=lambda: generate_matrix_ui(), 
          bg="#2d373d", fg="white", font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=2, pady=10)

# Separator
tk.Frame(main_frame, height=2, bg="white").grid(row=3, column=0, columnspan=20, sticky="we", pady=5)

# ---------------- Layer 2: Matrix Input Section ----------------
matrix_frame = tk.Frame(main_frame, bg="#37444c")
matrix_frame.grid(row=4, column=0, columnspan=20, pady=10, sticky="w")

tk.Label(matrix_frame, text="Augmented Matrix Input:", bg="#37444c", fg="white", font=("Arial", 11, "bold"))\
    .grid(row=0, column=0, columnspan=20, pady=5)

# Generate Matrix Layout button (stays visible)
generate_button = tk.Button(matrix_frame, text="Generate Matrix Layout", bg="#2d373d", fg="white", font=("Arial", 11, "bold"))
generate_button.grid(row=1, column=0, columnspan=20, pady=10)

entries_matrix = []  # list to store Entry references
brace_label = None

def generate_matrix_ui():
    global entries_matrix, brace_label

    # Only clear previous matrix if Confirm Size pressed
    for widget in matrix_frame.winfo_children():
        if widget not in [generate_button, matrix_frame.grid_slaves(row=0, column=0)[0]]:
            widget.destroy()
    entries_matrix = []

    try:
        m = int(entry_m.get())
        n = int(entry_n.get())
        if m <= 0 or n <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Please enter valid positive integers for m and n.")
        return

    # Curly brace visual: always ⎧ at top, ⎩ at bottom, | in between
    if m == 1:
        brace_text = "⎧\n⎩"
    elif m == 2:
        brace_text = "⎧\n⎩"
    else:
        brace_text = "⎧\n" + "\n".join(["|"]*(m-2)) + "\n⎩"

    brace_label = tk.Label(matrix_frame, text=brace_text, bg="#37444c", fg="white", font=("Arial", 20), justify="left")
    brace_label.grid(row=2, column=0, rowspan=m, sticky="ns", padx=5)

    # Matrix entries
    for i in range(m):
        row_entries = []
        col = 1
        for j in range(n):
            e = tk.Entry(matrix_frame, width=4, bg="#2d373d", fg="white", font=("Arial", 11))
            e.grid(row=i+2, column=col, padx=2, pady=2)
            row_entries.append(e)
            col += 1
            tk.Label(matrix_frame, text=f"x{subscript(j+1)}", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+2, column=col)
            col += 1
            if j < n-1:
                tk.Label(matrix_frame, text="+", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+2, column=col)
                col += 1

        tk.Label(matrix_frame, text="=", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+2, column=col)
        col += 1
        e_rhs = tk.Entry(matrix_frame, width=4, bg="#2d373d", fg="white", font=("Arial", 11))
        e_rhs.grid(row=i+2, column=col, padx=2)
        row_entries.append(e_rhs)
        entries_matrix.append(row_entries)

    root.update_idletasks()
    root.geometry("")  # dynamic resize

generate_button.config(command=generate_matrix_ui)

# Separator
tk.Frame(main_frame, height=2, bg="white").grid(row=5, column=0, columnspan=20, sticky="we", pady=5)

# ---------------- Layer 3: Display Matrix ----------------
tk.Label(main_frame, text="Display Matrix (placeholder):", bg="#37444c", fg="white", font=("Arial", 11, "bold")).grid(row=6, column=0, padx=10, sticky="w")
matrix_display_label = tk.Label(main_frame, text="", bg="#37444c", fg="white", font=("Courier", 11), justify="left")
matrix_display_label.grid(row=7, column=0, padx=20, sticky="w")

# Separator
tk.Frame(main_frame, height=2, bg="white").grid(row=8, column=0, columnspan=20, sticky="we", pady=5)

# ---------------- Layer 4: Results ----------------
tk.Label(main_frame, text="Least Squares Solution Vector:", bg="#37444c", fg="white", font=("Courier", 11, "bold"), anchor="w").grid(row=9, column=0, padx=10, sticky="w")
solution_label = tk.Label(main_frame, text="", justify="left", bg="#37444c", fg="white", font=("Courier", 11))
solution_label.grid(row=10, column=0, padx=20, sticky="w")

tk.Label(main_frame, text="Least Squares Error:", bg="#37444c", fg="white", font=("Courier", 11, "bold"), anchor="w").grid(row=11, column=0, padx=10, sticky="w")
error_label = tk.Label(main_frame, text="", justify="left", bg="#37444c", fg="white", font=("Courier", 11))
error_label.grid(row=12, column=0, padx=20, sticky="w")

root.mainloop()
