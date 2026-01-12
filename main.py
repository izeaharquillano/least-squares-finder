import numpy as np
import tkinter as tk

import solver
import utils


class LeastSquaresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Least Squares Solver")


if __name__ == "__main__":
    root = tk.Tk()
    app = LeastSquaresApp(root)
    root.mainloop()
