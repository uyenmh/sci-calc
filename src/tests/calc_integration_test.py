from unittest.mock import patch
import tkinter as tk
import unittest
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
