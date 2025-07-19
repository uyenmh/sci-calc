import unittest
import tkinter as tk

from calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.input = "4 ÷ 2 + ( 6 - 2 )"
        self.calc = Calculator(self.input)

    def test_tokenize_input_with_positive_numbers(self):
        desired_tokens = ["4", "÷", "2", "+", "(", "6", "-", "2", ")"]

        self.assertEqual(self.calc.tokens, desired_tokens) 

    def test_convert_infix_to_rpn_with_positive_numbers(self):
        desired_output_queue = ["4", "2", "÷", "6", "2", "-", "+"]

        self.assertEqual(self.calc.output_queue, desired_output_queue)

    def test_calculate_with_positive_numbers(self):
        desired_solution = 6

        self.assertEqual(self.calc.calculate(), desired_solution)