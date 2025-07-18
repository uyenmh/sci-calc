import tkinter as tk
from tkinter import ttk, messagebox
from calc import Calculator

class CalculatorUI:
    """A class responsible for the UI of the calculator.
    """
    def __init__(self, root):
        """The class constructor. Initializes the window for the calculator.

        Args:
            root (tkinter.Tk): The root to initialize the window for the calculator. 
        """
        self.root = root
        self.entry = None

        self.calculator_view()

    def calculator_view(self):
        """Configures the elements of the calculator window. 
        """
        self.root.title("Scientific Calculator")
        self.root.geometry("700x350")

        mainframe = ttk.Frame(self.root)
        mainframe.pack()

        self.entry = tk.Entry(mainframe, state="disabled")
        self.entry.grid(row=0, column=0, columnspan=3, sticky="we")

        button_style = ttk.Style()
        button_style.configure("my.TButton", font=("Montserrat", 10))

        no1_button = ttk.Button(mainframe, style="my.TButton", text="1", command=lambda: self.add_to_entry("1"))
        no2_button = ttk.Button(mainframe, style="my.TButton", text="2", command=lambda: self.add_to_entry("2"))
        no3_button = ttk.Button(mainframe, style="my.TButton", text="3", command=lambda: self.add_to_entry("3"))
        no4_button = ttk.Button(mainframe, style="my.TButton", text="4", command=lambda: self.add_to_entry("4"))
        no5_button = ttk.Button(mainframe, style="my.TButton", text="5", command=lambda: self.add_to_entry("5"))
        no6_button = ttk.Button(mainframe, style="my.TButton", text="6", command=lambda: self.add_to_entry("6"))
        no7_button = ttk.Button(mainframe, style="my.TButton", text="7", command=lambda: self.add_to_entry("7"))
        no8_button = ttk.Button(mainframe, style="my.TButton", text="8", command=lambda: self.add_to_entry("8"))
        no9_button = ttk.Button(mainframe, style="my.TButton", text="9", command=lambda: self.add_to_entry("9"))
        no0_button = ttk.Button(mainframe, style="my.TButton", text="0", command=lambda: self.add_to_entry("0"))

        clear_button = ttk.Button(mainframe, style="my.TButton", text="C", command=lambda: self.clear_entry())
        delete_button = ttk.Button(mainframe, style="my.TButton", text="del", command=lambda: self.delete_last_char())
        enter_button = ttk.Button(mainframe, style="my.TButton", text="enter", command=lambda: self.calculate_input())

        plus_button = ttk.Button(mainframe, style="my.TButton", text="+", command=lambda: self.add_to_entry("+"))
        minus_button = ttk.Button(mainframe, style="my.TButton", text="-", command=lambda: self.add_to_entry("-"))
        times_button = ttk.Button(mainframe, style="my.TButton", text="×", command=lambda: self.add_to_entry("×"))
        divide_button = ttk.Button(mainframe, style="my.TButton", text="÷", command=lambda: self.add_to_entry("÷"))
        equal_to_button = ttk.Button(mainframe, style="my.TButton", text="=", command=lambda: self.add_to_entry("="))
        dot_button = ttk.Button(mainframe, style="my.TButton", text=".", command=lambda: self.add_to_entry("."))
        start_parenthesis_button = ttk.Button(mainframe, style="my.TButton", text="(", command=lambda: self.add_to_entry("("))
        end_parenthesis_button = ttk.Button(mainframe, style="my.TButton", text=")", command=lambda: self.add_to_entry(")"))

        no1_button.grid(row=4, column=0)
        no2_button.grid(row=4, column=1)
        no3_button.grid(row=4, column=2)
        no4_button.grid(row=3, column=0)
        no5_button.grid(row=3, column=1)
        no6_button.grid(row=3, column=2)
        no7_button.grid(row=2, column=0)
        no8_button.grid(row=2, column=1)
        no9_button.grid(row=2, column=2)
        no0_button.grid(row=5, column=1)

        clear_button.grid(row=1, column=0)
        delete_button.grid(row=5, column=0)
        enter_button.grid(row=0, column=3)

        plus_button.grid(row=4, column=3)
        minus_button.grid(row=3, column=3)
        times_button.grid(row=2, column=3)
        divide_button.grid(row=1, column=3)
        equal_to_button.grid(row=5, column=3)
        dot_button.grid(row=5, column=2)
        start_parenthesis_button.grid(row=1, column=1)
        end_parenthesis_button.grid(row=1, column=2)

    def add_to_entry(self, input):
        """Adds the given character into the input field of the calculator.

        Args:
            input (str): The given character that will be added onto the input field.
        """
        self.entry.config(state="normal")
        self.entry.insert(tk.END, input)
        self.entry.config(state="disabled")

    def clear_entry(self):
        """Clears the input field of the calculator.
        """
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.config(state="disabled")

    def delete_last_char(self):
        """Deletes the last character from input field of the calculator.
        """
        self.entry.config(state="normal")
        self.entry.delete(self.entry.index(tk.END) - 1)
        self.entry.config(state="disabled")

    def calculate_input(self):
        """Calculates the solution to the given input (mathematical expression).
        """
        input = self.entry.get()
        calc = Calculator(input)
        solution = calc.calculate()

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, solution)
        self.entry.config(state="disabled")
