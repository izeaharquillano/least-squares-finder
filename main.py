import numpy as np
import tkinter as tk
import sys
from tkinter import messagebox
from tkmacosx import Button

import solver
import utils


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

        try:
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w, "help", "none")
        except tk.TclError:
            pass

        tw.configure(bg="white", padx=1, pady=1)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify='left',
                         background="white", foreground="#2d373d",
                         relief='flat', highlightthickness=0,
                         padx=8, pady=4,
                         font=("Arial", 11, "bold"))
        label.pack()

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class LeastSquaresApp:
    def __init__(self, root):
        self.root = root
        self.entries_matrix = []

        self.root.title("Least Squares Solver")
        self.root.configure(bg="#37444c")
        self.root.resizable(True, True)

        main_frame = tk.Frame(root, bg="#37444c")
        main_frame.pack(padx=50, pady=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.mode_var = tk.StringVar(value="linear")
        mode_frame = tk.Frame(main_frame, bg="#37444c")
        mode_frame.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Radiobutton(mode_frame, text="Linear System Mode", variable=self.mode_var,
                       value="linear", bg="#37444c", fg="white", selectcolor="#2d373d",
                       activebackground="#37444c", activeforeground="white",
                       command=self.refresh_grid).pack(side="left", padx=10)

        tk.Radiobutton(mode_frame, text="Augmented Matrix Mode", variable=self.mode_var,
                       value="plain", bg="#37444c", fg="white", selectcolor="#2d373d",
                       activebackground="#37444c", activeforeground="white",
                       command=self.refresh_grid).pack(side="left", padx=10)

        tk.Label(main_frame, text="Number of Equations (m):", bg="#37444c", fg="white", font=("Arial", 11))\
                .grid(row=1, column=0, sticky="e", pady=2, padx=5)
        self.entry_m = tk.Entry(main_frame, width=5, bg="#2d373d", fg="white",
                                insertbackground="white", font=("Arial", 11))
        self.entry_m.grid(row=1, column=1, sticky="w", pady=2)
        ToolTip(self.entry_m, "m = # of equations / rows")

        tk.Label(main_frame, text="Number of Unknowns (n):", bg="#37444c", fg="white", font=("Arial", 11))\
                .grid(row=2, column=0, sticky="e", pady=2, padx=5)
        self.entry_n = tk.Entry(main_frame, width=5, bg="#2d373d", fg="white",
                                insertbackground="white", font=("Arial", 11))
        self.entry_n.grid(row=2, column=1, sticky="w", pady=2)
        ToolTip(self.entry_n, "n = # of unknowns / columns")

        self.matrix_frame = tk.Frame(main_frame, bg="#37444c")
        self.matrix_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="n")

        if sys.platform == "darwin":
            Button(main_frame, borderless=1, text="Confirm Size", command=self.generate_matrix_ui,
                        bg="#2d373d", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
            self.solve_button = Button(main_frame, borderless=1, text="Solve", command=self.solve_ls,
                                        bg="#2d373d", fg="white", font=("Arial", 12, "bold"))
        else:
            tk.Button(main_frame, text="Confirm Size", command=self.generate_matrix_ui,
                        bg="#2d373d", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
            self.solve_button = tk.Button(main_frame, text="Solve", command=self.solve_ls,
                                        bg="#2d373d", fg="white", font=("Arial", 12, "bold"))

        tk.Frame(main_frame, height=2, bg="white").grid(row=4, column=0, columnspan=2, sticky="we", pady=5)

        # tk.Frame(main_frame, height=2, bg="white").grid(row=6, column=0, columnspan=2, sticky="we", pady=5)

        # tk.Label(main_frame, text="Display Matrix:", bg="#37444c", fg="white", font=("Arial", 11, "bold")).grid(row=7, column=0, columnspan=2, pady=(5,0))
        # self.matrix_display_label = tk.Label(main_frame, text="", bg="#37444c", fg="white", font=("Arial", 11), justify="center")
        # self.matrix_display_label.grid(row=8, column=0, columnspan=2, pady=5)

        tk.Frame(main_frame, height=2, bg="white").grid(row=9, column=0, columnspan=2, sticky="we", pady=5)

        tk.Label(main_frame, text="Least Squares Solution Vector:", bg="#37444c", fg="white", font=("Arial", 11, "bold")).grid(row=10, column=0, columnspan=2, pady=(5,0))
        self.solution_label = tk.Label(main_frame, text="", justify="center", bg="#37444c", fg="white", font=("Arial", 12))
        self.solution_label.grid(row=11, column=0, columnspan=2, pady=5)

        tk.Label(main_frame, text="Least Squares Error:", bg="#37444c", fg="white", font=("Arial", 11, "bold")).grid(row=12, column=0, columnspan=2, pady=(5,0))
        self.error_label = tk.Label(main_frame, text="", justify="center", bg="#37444c", fg="white", font=("Arial", 11))
        self.error_label.grid(row=13, column=0, columnspan=2, pady=5)

        self.solve_button.grid(row=14, column=0, columnspan=2, pady=20)

    def refresh_grid(self):
        if self.entry_m.get() and self.entry_n.get():
            self.generate_matrix_ui()

    def generate_matrix_ui(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries_matrix = []
        mode = self.mode_var.get()

        try:
            m = int(self.entry_m.get())
            n = int(self.entry_n.get())
            if m <= 0 or n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter valid positive integers for m and n.")
            return

        header_text = "Linear System Input:" if mode == "linear" else "Augmented Matrix Input:"
        tk.Label(self.matrix_frame, text=header_text, bg="#37444c", fg="white", font=("Arial", 11, "bold"))\
                .grid(row=0, column=0, columnspan=50, pady=5)

        for i in range(m):
            row_entries = []
            col = 0
            for j in range(n):
                e = tk.Entry(self.matrix_frame, width=5, bg="#2d373d", fg="white",
                             insertbackground="white", font=("Arial", 11))
                e.grid(row=i+1, column=col, padx=2, pady=2)
                row_entries.append(e)
                col += 1

                if mode == "linear":
                    tk.Label(self.matrix_frame, text=f"x{utils.subscript(j+1)}", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+1, column=col)
                    col += 1
                    if j < n-1:
                        tk.Label(self.matrix_frame, text="+", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+1, column=col)
                        col += 1
                else:
                    if j == n - 1:
                        tk.Label(self.matrix_frame, text=" | ", bg="#37444c", fg="white", font=("Arial", 11, "bold")).grid(row=i+1, column=col)
                        col += 1

            if mode == "linear":
                tk.Label(self.matrix_frame, text="=", bg="#37444c", fg="white", font=("Arial", 11)).grid(row=i+1, column=col)
                col += 1

            e_rhs = tk.Entry(self.matrix_frame, width=5, bg="#1a2226", fg="white",
                             insertbackground="white", font=("Arial", 11))
            e_rhs.grid(row=i+1, column=col, padx=2)
            row_entries.append(e_rhs)
            self.entries_matrix.append(row_entries)

        self.root.update_idletasks()
        self.root.geometry("")

    def solve_ls(self):
        try:
            if not self.entries_matrix:
                return

            matrix_data = []
            for row in self.entries_matrix:
                row_values = [float(e.get()) for e in row]
                matrix_data.append(row_values)

            aug_matrix = np.array(matrix_data)
            A, b = utils.split_aug_mat(aug_matrix)

            x_hat = solver.get_ls_xhat(A, b)
            ls_error = solver.get_ls_error(A, b, x_hat)

            vector_rows = []
            for i, val in enumerate(x_hat.flatten()):
                vector_rows.append(f"x̂{utils.subscript(i+1)} = [ {float(val):>10.4f} ]")

            self.solution_label.config(text="\n".join(vector_rows))
            self.error_label.config(text=f"{float(ls_error):.6f}")
            # self.matrix_display_label.config(text=np.array2string(aug_matrix, precision=2, separator=', '))

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all matrix entries are valid numbers.")
        except Exception as e:
            messagebox.showerror("Solver Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LeastSquaresApp(root)
    root.mainloop()
