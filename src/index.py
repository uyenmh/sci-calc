import tkinter as tk
from ui.calc_ui import CalculatorUI


def main():
    root = tk.Tk()
    CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()