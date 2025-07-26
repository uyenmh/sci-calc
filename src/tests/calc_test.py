import unittest
import tkinter as tk

from calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.input = "-4÷2+(6-2)×1"
        self.calc = Calculator(self.input)

    def test_check_validity_of_input_using_consecutive_operators(self):
        message = self.calc.check_validity_of_input(self.input, "+")

        if message == "":
            self.input += "+"

        message = self.calc.check_validity_of_input(self.input, "-")

        self.assertEqual(message, "Two consecutive operators not allowed.")

    def test_check_validity_of_input_using_empty_parenthesis(self):
        message = self.calc.check_validity_of_input(self.input, "(")

        if message == "":
            self.input += "("

        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "Parenthesis cannot be left empty.")

    def test_check_validity_of_input_using_multiplication_after_left_parenthesis(self):
        message = self.calc.check_validity_of_input(self.input, "(")

        if message == "":
            self.input += "("

        message = self.calc.check_validity_of_input(self.input, "×")

        self.assertEqual(message, "The multiplication sign is not valid after left parenthesis.")

    def test_check_validity_of_input_using_division_after_left_parenthesis(self):
        message = self.calc.check_validity_of_input(self.input, "(")

        if message == "":
            self.input += "("

        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "The division sign is not valid after left parenthesis.")

    def test_check_validity_of_input_using_multiplication_first(self):
        self.input = ""

        message = self.calc.check_validity_of_input(self.input, "×")

        self.assertEqual(message, "The expression cannot start with a multiplication sign.")

    def test_check_validity_of_input_using_division_first(self):
        self.input = ""

        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "The expression cannot start with a division sign.")

    def test_check_validity_of_input_using_right_parenthesis_before_left(self):
        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "Insert a left parenthesis first.")

    def test_check_validity_of_input_using_right_parenthesis_first(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "Insert a left parenthesis first.")
    
    def test_left_parenthesis_counter(self):
        self.input = ""
        self.calc.check_validity_of_input(self.input, "(")

        self.assertEqual(self.calc.left_parenthesis, 1)

        self.calc.check_validity_of_input(self.input, "(")
        self.calc.check_validity_of_input(self.input, "(")

        self.assertEqual(self.calc.left_parenthesis, 3)

    def test_right_parenthesis_counter(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, "(")
        if message == "":
            self.input += "("

        message = self.calc.check_validity_of_input(self.input, "(")
        if message == "":
            self.input += "("

        self.calc.check_validity_of_input(self.input, "3")
        if message == "":
            self.input += "3"

        self.calc.check_validity_of_input(self.input, ")")
        if message == "":
            self.input += ")"

        self.assertEqual(self.calc.right_parenthesis, 1)

        self.calc.check_validity_of_input(self.input, ")")
        if message == "":
            self.input += ")"

        self.assertEqual(self.calc.right_parenthesis, 2)

        self.calc.check_validity_of_input(self.input, ")")
        if message == "":
            self.input += ")"

        self.assertEqual(self.calc.right_parenthesis, 2)

    def test_insert_input(self):
        self.assertEqual(self.calc.input, self.input)
        self.assertEqual(self.calc.reformatted_input, "-4 ÷ 2 + ( 6 - 2 ) × 1")
        self.assertEqual(self.calc.tokens, ["-4", "÷", "2", "+", "(", "6", "-", "2", ")", "×", "1"])
        self.assertEqual(self.calc.output_queue, ["-4", "2", "÷", "6", "2", "-", "1", "×", "+"])

        new_input = "1+2+3"
        self.calc.insert_input(new_input)

        self.assertEqual(self.calc.input, new_input)
        self.assertEqual(self.calc.reformatted_input, "1 + 2 + 3")
        self.assertEqual(self.calc.tokens, ["1", "+", "2", "+", "3"])
        self.assertEqual(self.calc.output_queue, ["1", "2", "+", "3", "+"])

    def test_reformat_input_with_plusminus_around_parenthesis(self):
        self.input = "-(+3-2)+((5+3)-4)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "-1 × ( +3 - 2 ) + ( ( 5 + 3 ) - 4 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_numbers_around_parenthesis(self):
        self.input = "2(3+1)5"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "2 × ( 3 + 1 ) × 5"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_floats(self):
        self.input = "-1.57+0.83674-(-.001)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "-1.57 + 0.83674 - ( -.001 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_tokenize_input_with_whole_numbers(self):
        desired_tokens = ["-4", "÷", "2", "+", "(", "6", "-", "2", ")", "×", "1"]

        self.assertEqual(self.calc.tokens, desired_tokens) 

    def test_convert_infix_to_rpn_with_whole_numbers(self):
        desired_output_queue = ["-4", "2", "÷", "6", "2", "-", "1", "×", "+"]

        self.assertEqual(self.calc.output_queue, desired_output_queue)

    def test_calculate_with_whole_numbers(self):
        desired_solution = 2

        self.assertEqual(self.calc.calculate(), desired_solution)