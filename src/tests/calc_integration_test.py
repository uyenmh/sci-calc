from unittest.mock import patch
import tkinter as tk
import unittest
import math
from ui.calc_ui import CalculatorUI

class TestCalculatorIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = CalculatorUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("tkinter.messagebox.showerror")
    def test_add_to_entry_insert_invalid_input(self, mock_error):
        self.app.add_to_entry("×")
        mock_error.assert_called_once()

        self.app.add_to_entry("=")
        self.assertEqual(mock_error.call_count, 2)

        self.app.add_to_entry("(")
        self.app.add_to_entry(")")
        self.assertEqual(mock_error.call_count, 3)

    @patch("tkinter.messagebox.showerror")
    def test_add_to_entry_dot_first(self, mock_error):
        self.app.add_to_entry(".")
        mock_error.assert_not_called()

        entry = self.app.entry.get()
        desired_entry = "0."
        self.assertEqual(entry, desired_entry)

    def test_clear_entry(self):
        self.app.add_to_entry("cos(")
        self.app.add_to_entry("2")
        self.app.add_to_entry(")")
        self.app.add_to_entry("+")
        self.app.add_to_entry("2")

        entry = self.app.entry.get()
        desired_entry = "cos(2)+2"
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 1)
        self.assertEqual(self.app.calc.right_parenthesis, 1)

        self.app.clear_entry()
        entry = self.app.entry.get()
        desired_entry = ""
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 0)
        self.assertEqual(self.app.calc.right_parenthesis, 0)

    def test_delete_last_char(self):
        self.app.add_to_entry("a")
        self.app.add_to_entry("=")
        self.app.add_to_entry("√(")
        self.app.add_to_entry("cos(")
        self.app.add_to_entry("sin⁻¹(")
        self.app.add_to_entry("min(")
        self.app.add_to_entry("3")
        self.app.add_to_entry(",")

        entry = self.app.entry.get()
        desired_entry = "a=√(cos(sin⁻¹(min(3,"
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 4)
        self.assertTrue(self.app.calc.equality_status)
        self.assertEqual(self.app.calc.min_count, 1)
        self.assertEqual(self.app.calc.commas, 1)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a=√(cos(sin⁻¹(min(3"
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.commas, 0)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a=√(cos(sin⁻¹(min("
        self.assertEqual(entry, desired_entry)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a=√(cos(sin⁻¹("
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.min_count, 0)
        self.assertEqual(self.app.calc.left_parenthesis, 3)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a=√(cos("
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 2)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a=√("
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 1)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a="
        self.assertEqual(entry, desired_entry)
        self.assertEqual(self.app.calc.left_parenthesis, 0)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = "a"
        self.assertEqual(entry, desired_entry)
        self.assertFalse(self.app.calc.equality_status)

        self.app.delete_last_char()
        entry = self.app.entry.get()
        desired_entry = ""
        self.assertEqual(entry, desired_entry)

    def test_calculate_input_with_simple_calculation(self):
        self.app.add_to_entry("3")
        self.app.add_to_entry("-")
        self.app.add_to_entry("9")
        
        self.app.calculate_input()
        desired_output = 3-9
        self.assertEqual(self.app.entry.get(), str(desired_output))

    def test_calculate_input_with_functions(self):
        self.app.add_to_entry("sin(")
        self.app.add_to_entry(".")
        self.app.add_to_entry("3")
        self.app.add_to_entry("4")
        self.app.add_to_entry("5")
        self.app.add_to_entry("-")
        self.app.add_to_entry("2")
        self.app.add_to_entry("max(")
        self.app.add_to_entry("4")
        self.app.add_to_entry(",")
        self.app.add_to_entry("7")
        self.app.add_to_entry(")")
        self.app.add_to_entry(")")
        self.app.add_to_entry("(")
        self.app.add_to_entry("(")
        self.app.add_to_entry("2")
        self.app.add_to_entry(")")
        self.app.add_to_entry(")")
        self.app.add_to_entry("min(")
        self.app.add_to_entry("sin(")
        self.app.add_to_entry("8")
        self.app.add_to_entry(".")
        self.app.add_to_entry("5")
        self.app.add_to_entry("3")
        self.app.add_to_entry("+")
        self.app.add_to_entry("2")
        self.app.add_to_entry(".")
        self.app.add_to_entry("4")
        self.app.add_to_entry(")")
        self.app.add_to_entry(",")
        self.app.add_to_entry("tan(")
        self.app.add_to_entry("5")
        self.app.add_to_entry("2")
        self.app.add_to_entry("4")
        self.app.add_to_entry(".")
        self.app.add_to_entry("1")
        self.app.add_to_entry("-")
        self.app.add_to_entry("4")
        self.app.add_to_entry("2")
        self.app.add_to_entry(")")
        self.app.add_to_entry("+")
        self.app.add_to_entry("7")
        self.app.add_to_entry(")")

        self.app.calculate_input()
        desired_output = math.sin(0.345-2*max(4,7))*((2))*min(math.sin(8.53+2.4),math.tan(5-24.1-42)+7)

        self.assertEqual(self.app.entry.get(), str(desired_output))

    def test_calculate_input_many_times(self):
        self.app.add_to_entry("4")
        self.app.add_to_entry(".")
        self.app.add_to_entry("0")
        self.app.add_to_entry("1")
        self.app.add_to_entry("(")
        self.app.add_to_entry("2")
        self.app.add_to_entry("+")
        self.app.add_to_entry("7")
        self.app.add_to_entry(")")

        self.app.calculate_input()
        desired_output = 4.01*(2+7)

        self.assertEqual(self.app.entry.get(), str(desired_output))

        self.app.add_to_entry("-")
        self.app.add_to_entry("4")
        self.app.add_to_entry("+")
        self.app.add_to_entry("0")
        self.app.add_to_entry(".")
        self.app.add_to_entry("6")

        self.app.calculate_input()
        desired_output = desired_output-4+0.6

        self.assertEqual(self.app.entry.get(), str(desired_output))

        self.app.add_to_entry("max(")
        self.app.add_to_entry("9")
        self.app.add_to_entry(",")
        self.app.add_to_entry("0")
        self.app.add_to_entry(")")

        self.app.calculate_input()
        desired_output = desired_output * max(9,0)

        self.assertEqual(self.app.entry.get(), str(desired_output))

    @patch("tkinter.messagebox.showerror")
    def test_calculate_input_with_many_parenthesis(self, mock_error):
        self.app.add_to_entry("5")
        self.app.add_to_entry("(")
        self.app.add_to_entry("2")
        self.app.add_to_entry("-")
        self.app.add_to_entry("4")
        self.app.add_to_entry("+")
        self.app.add_to_entry("0")

        self.app.calculate_input()
        mock_error.assert_called_once()

        self.app.add_to_entry(")")
        self.app.add_to_entry("(")
        self.app.add_to_entry("(")
        self.app.add_to_entry("7")
        self.app.add_to_entry(".")
        self.app.add_to_entry("1")
        self.app.add_to_entry("2")
        self.app.add_to_entry("-")
        self.app.add_to_entry("3")
        self.app.add_to_entry("4")
        self.app.add_to_entry(")")
        self.app.add_to_entry("÷")
        self.app.add_to_entry("4")
        self.app.add_to_entry(".")
        self.app.add_to_entry("5")

        self.app.calculate_input()
        self.assertEqual(mock_error.call_count, 2)

        self.app.add_to_entry(")")
        self.app.calculate_input()
        desired_output = 5*(2-4+0)*((7.12-34)/4.5)

        self.assertEqual(self.app.entry.get(), str(desired_output))

    @patch("tkinter.messagebox.showerror")
    def test_calculate_input_with_error_msg(self, mock_error):
        self.app.add_to_entry("2")
        self.app.add_to_entry("+")

        self.app.calculate_input()
        mock_error.assert_called_once()

    def test_toggle_radians_and_degrees(self):
        self.assertEqual(self.app.rad_deg_button.cget("text"), "deg")
        self.assertTrue(self.app.calc.radians)

        self.app.toggle_radians_and_degrees()
        self.assertEqual(self.app.rad_deg_button.cget("text"), "rad")
        self.assertFalse(self.app.calc.radians)
