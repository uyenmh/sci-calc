import unittest
import math
import tkinter as tk

from calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.input = "-4÷2+(6-2)×1"
        self.calc = Calculator()
        self.calc.insert_input(self.input)

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

    def test_check_validity_of_input_using_right_parenthesis_after_operator(self):
        message = self.calc.check_validity_of_input(self.input, "(")

        if message == "":
            self.input += "("

        self.input += "1+"

        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "A right parenthesis is not valid after an operator.")

    def test_check_validity_of_input_using_multiple_dots(self):
        self.input += "."
        message = self.calc.check_validity_of_input(self.input, ".")

        self.assertEqual(message, "Enter a valid number. A number can only contain one dot.")

        message = ""
        self.input += "19"
        message = self.calc.check_validity_of_input(self.input, ".")

        self.assertEqual(message, "Enter a valid number. A number can only contain one dot.")


    def test_check_validity_of_input_using_multiplication_first(self):
        self.input = ""

        message = self.calc.check_validity_of_input(self.input, "×")

        self.assertEqual(message, "The expression can't start with a multiplication sign.")

    def test_check_validity_of_input_using_division_first(self):
        self.input = ""

        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "The expression can't start with a division sign.")

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

    def test_reformat_input_with_sqrt(self):
        self.input = "2√(5+3)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "2 × √ ( 5 + 3 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_trig_functions(self):
        self.input = "2sin(4+5)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "2 × sin ( 4 + 5 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_inverse_trig_functions(self):
        self.input = "4+3cos⁻¹(-1)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "4 + 3 × cos⁻¹ ( -1 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_adding_right_parenthesis_to_end(self):
        self.input = "(2+4-tan(20"
        self.calc.left_parenthesis += 2
        self.calc.insert_input(self.input)
        desired_reformatted_input = "( 2 + 4 - tan ( 20 ) )"

        print(self.calc.left_parenthesis, self.calc.right_parenthesis)

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_tokenize_input_with_whole_numbers(self):
        desired_tokens = ["-4", "÷", "2", "+", "(", "6", "-", "2", ")", "×", "1"]

        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_tokenize_input_with_floats(self):
        self.input = "0.3782-34.543"
        self.calc.insert_input(self.input)
        desired_tokens = ["0.3782", "-", "34.543"]
    
        self.assertEqual(self.calc.tokens, desired_tokens)
    
    def test_tokenize_inputs_with_functions(self):
        self.input = "2+cos(5-3)÷√(6)"
        self.calc.insert_input(self.input)
        desired_tokens = ["2", "+", "cos", "(", "5", "-", "3", ")", "÷", "√", "(", "6", ")"]
                          
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_convert_infix_to_rpn_with_numbers(self):
        self.input = "-4÷2.15+(6-2)×0.876"
        self.calc.insert_input(self.input)
        desired_rpn = ["-4", "2.15", "÷", "6", "2", "-", "0.876", "×", "+"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_convert_infix_to_rpn_with_functions(self):
        self.input = "cos(60)-√(9)"
        self.calc.insert_input(self.input)
        desired_rpn = ["60", "cos", "9", "√", "-"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_calculate_with_whole_numbers(self):
        desired_solution = -4 / 2 + ( 6 - 2 ) * 1

        self.assertEqual(self.calc.calculate(), desired_solution)

    def test_calculate_with_expression_ending_in_operator(self):
        self.input = "2+2-"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "The expression can't end with an operator."

        self.assertEqual(output, desired_output)

    def test_calculate_with_expression_ending_in_left_parenthesis(self):
        self.input = "2+1("
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Parenthesis cannot be left empty."

        self.assertEqual(output, desired_output)

    def test_calculate_with_negative_sqrt(self):
        self.input = "√(1-9)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "The square root of a negative number can't be calculated."

        self.assertEqual(output, desired_output)

    def test_calculate_with_positive_sqrt(self):
        self.input = "√(9)+15"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = math.sqrt(9) + 15

        self.assertEqual(output, desired_output)

    def test_calculate_with_trig_functions_in_radians(self):
        self.input = "sin(5)+cos(2)-tan(7)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = math.sin(5) + math.cos(2) - math.tan(7)

        self.assertEqual(output, desired_output)

    def test_calculate_with_trig_functions_in_degrees(self):
        self.input = "sin(60)-cos(30)+tan(0)"
        self.calc.insert_input(self.input)
        self.calc.radians = False
        output = self.calc.calculate()
        desired_output = math.sin(math.radians(60)) - math.cos(math.radians(30)) + math.tan(math.radians(0))

        self.assertEqual(output, desired_output)

    def test_calculate_with_inverse_trig_functions_in_radians(self):
        self.input = "sin⁻¹(0.5)+cos⁻¹(-0.2)+tan⁻¹(0)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = math.asin(0.5) + math.acos(-0.2) + math.atan(0)

        self.assertEqual(output, desired_output)

    def test_calculate_with_inverse_trig_functions_in_degrees(self):
        self.input = "sin⁻¹(-0.3)+cos⁻¹(-0.2)+tan⁻¹(0.01)"
        self.calc.insert_input(self.input)
        self.calc.radians = False
        output = self.calc.calculate()
        desired_output = math.degrees(math.asin(-0.3)) + math.degrees(math.acos(-0.2)) + math.degrees(math.atan(0.01))

        self.assertEqual(output, desired_output)

    def test_calculate_with_invalid_number_in_asin_acos(self):
        self.input = "sin⁻¹(20)+cos⁻¹(-0.2)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "sin⁻¹ and cos⁻¹ functions require a value between -1 and 1."

        self.assertEqual(output, desired_output)
