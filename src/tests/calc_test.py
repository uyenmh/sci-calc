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

    def test_check_validity_of_input_operator_before_comma(self):
        self.input = "min(3+"
        self.calc.min_count = 1
        message = self.calc.check_validity_of_input(self.input, ",")

        self.assertEqual(message, "Enter a numerical value before a comma.")

    def test_check_validity_of_input_operator_after_comma(self):
        self.input = "max(3+2,"
        self.calc.max_count = 1
        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "Operators not allowed after a comma.")

    def test_check_validity_of_input_two_equal_signs(self):
        self.input = "a="
        self.calc.equality_status = True
        message = self.calc.check_validity_of_input(self.input, "=")

        self.assertEqual(message, "Only one equal to sign is allowed in an equation.")

    def test_check_validity_of_input_equal_sign_and_open_parenthesis(self):
        self.input = "(1+2+3"
        self.calc.left_parenthesis = 1
        message = self.calc.check_validity_of_input(self.input, "=")

        self.assertEqual(message, "Close all parenthesis first.")

    def test_check_validity_of_input_operator_before_equal_sign(self):
        self.input = "5-"
        message = self.calc.check_validity_of_input(self.input, "=")

        self.assertEqual(message, "Enter a variable or a value before an equal to sign.")

    def test_check_validity_of_input_operator_after_equal_sign(self):
        self.input = "b="
        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "Operators not allowed after an equal to sign.")

    def test_check_validity_of_input_equal_sign_but_no_given_variable(self):
        self.input = "1+2+3="
        message = self.calc.check_validity_of_input(self.input, "1")

        self.assertEqual(message, "Enter a variable to save value to.")

    def test_check_validity_of_input_consecutive_variables_on_one_side(self):
        self.input = "1+2=c"
        message = self.calc.check_validity_of_input(self.input, "c")

        self.assertEqual(message, "Unexpected character after variable.")

    def test_check_validity_of_input_variables_on_both_sides(self):
        self.input = "a3=f"
        message = self.calc.check_validity_of_input(self.input, "a")

        self.assertEqual(message, "Unexpected character after variable.")

    def test_check_validity_of_input_using_multiplication_first(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, "×")

        self.assertEqual(message, "The expression can't start with a multiplication sign.")

    def test_check_validity_of_input_using_division_first(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, "÷")

        self.assertEqual(message, "The expression can't start with a division sign.")

    def test_check_validity_of_input_equal_sign_first(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, "=")

        self.assertEqual(message, "Enter a variable or a value first.")

    def test_check_validity_of_input_using_right_parenthesis_before_left(self):
        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "Insert a left parenthesis first.")

    def test_check_validity_of_input_using_right_parenthesis_first(self):
        self.input = ""
        message = self.calc.check_validity_of_input(self.input, ")")

        self.assertEqual(message, "Insert a left parenthesis first.")

    def test_check_validity_of_input_comma_without_min_or_max(self):
        message = self.calc.check_validity_of_input(self.input, ",")

        self.assertEqual(message, "Comma must separate exactly two values in a min or max function.")

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

    def test_min_count(self):
        message = self.calc.check_validity_of_input(self.input, "min(")

        if message == "":
            self.input += "min("

        self.assertEqual(self.calc.min_count, 1)

        message = self.calc.check_validity_of_input(self.input, "min(")

        if message == "":
            self.input += "min("

        self.assertEqual(self.calc.min_count, 2)
    
    def test_max_count(self):
        message = self.calc.check_validity_of_input(self.input, "max(")

        if message == "":
            self.input += "max("

        self.assertEqual(self.calc.max_count, 1)

        message = self.calc.check_validity_of_input(self.input, "max(")

        if message == "":
            self.input += "max("

        self.assertEqual(self.calc.max_count, 2)

    def test_comma_count(self):
        self.input = "min(3"
        self.calc.min_count = 1
        
        self.assertEqual(self.calc.commas, 0)

        self.calc.check_validity_of_input(self.input, ",")

        self.assertEqual(self.calc.commas, 1)

    def test_equality_status(self):
        self.calc.check_validity_of_input(self.input, "=")

        self.assertTrue(self.calc.equality_status)

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

    def test_reformat_input_with_min_after_number(self):
        self.input = "2min(6,3)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "2 × min ( 6 , 3 )"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_max_after_number(self):
        self.input = "0max(3,10)"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "0 × max ( 3 , 10 )"
    
        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_variables_and_numbers(self):
        self.input = "1a×9efg6-5"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "1 × a × 9 × e × f × g × 6 - 5"

        self.assertEqual(self.calc.reformatted_input, desired_reformatted_input)

    def test_reformat_input_with_alot_of_parenthesis(self):
        self.input = "5+(34.435+((35-326.35))+355+33)((2-14))+6+(((35+77)))35"
        self.calc.insert_input(self.input)
        desired_reformatted_input = "5 + ( 34.435 + ( ( 35 - 326.35 ) ) + 355 + 33 ) × ( ( 2 - 14 ) ) + 6 + ( ( ( 35 + 77 ) ) ) × 35"

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

    def test_tokenize_inputs_with_variable_to_save_first(self):
        self.input = "a=3+2"
        self.calc.insert_input(self.input)
        desired_tokens = ["3", "+", "2"]

        self.assertEqual(self.calc.variable_to_save, "a")
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_tokenize_inputs_with_variable_to_save_last(self):
        self.input = "1+2+3=d"
        self.calc.insert_input(self.input)
        desired_tokens = ["1", "+", "2", "+", "3"]

        self.assertEqual(self.calc.variable_to_save, "d")
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_tokenize_inputs_with_variables_on_both_sides_right_variable_not_set(self):
        self.calc.variables["a"] = 2
        self.input = "a=b"
        self.calc.insert_input(self.input)
        desired_tokens = ["a"]

        self.assertEqual(self.calc.variable_to_save, "b")
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_tokenize_inputs_with_variables_on_both_sides_left_variable_not_set(self):
        self.calc.variables["b"] = 10
        self.input = "a=b"
        self.calc.insert_input(self.input)
        desired_tokens = ["b"]

        self.assertEqual(self.calc.variable_to_save, "a")
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_tokenize_inputs_with_variables_on_both_sides_both_variables_set(self):
        self.calc.variables["a"] = 1
        self.calc.variables["b"] = 2
        self.input = "a=b"
        self.calc.insert_input(self.input)
        desired_tokens = ["b"]

        self.assertEqual(self.calc.variable_to_save, "a")
        self.assertEqual(self.calc.tokens, desired_tokens)

    def test_convert_infix_to_rpn_with_numbers(self):
        self.input = "-4÷2.15+(6-2)×0.876"
        self.calc.insert_input(self.input)
        desired_rpn = ["-4", "2.15", "÷", "6", "2", "-", "0.876", "×", "+"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_convert_infix_to_rpn_with_trig_functions(self):
        self.input = "cos(60)-√(9)"
        self.calc.insert_input(self.input)
        desired_rpn = ["60", "cos", "9", "√", "-"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_convert_infix_to_rpn_with_min_max_functions(self):
        self.input = "min(1+2+3,max(2,4+7))"
        self.calc.insert_input(self.input)
        desired_rpn = ["1", "2", "+", "3", "+", "2", "4", "7", "+", "max", "min"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_convert_infix_to_rpn_with_many_parenthesis(self):
        self.input = "(5-3+32((1+40+4-24(0.24+2.34))(4.3-2.13)))"
        self.calc.insert_input(self.input)
        desired_rpn = ["5", "3", "-", "32", "1", "40", "+", "4", "+", "24", "0.24", "2.34", "+", "×", "-", "4.3", "2.13", "-", "×", "×", "+"]

        self.assertEqual(self.calc.output_queue, desired_rpn)

    def test_conver_infix_to_rpn_with_multiple_functions(self):
        self.input = "sin(max(4.2-0.33,cos(5+9-3))-√(3+7-1))"
        self.calc.insert_input(self.input)
        desired_rpn = ["4.2", "0.33", "-", "5", "9", "+", "3", "-", "cos", "max", "3", "7", "+", "1", "-", "√", "-", "sin"]

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
        self.input = "2+1"
        self.calc.insert_input(self.input)
        self.calc.check_validity_of_input(self.input, "(")
        output = self.calc.calculate()
        desired_output = "Close all parenthesis."

        self.assertEqual(output, desired_output)

    def test_calculate_with_expression_ending_in_comma(self):
        self.input = "min(5,"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Enter a second value for the min or max function."

        self.assertEqual(output, desired_output)

    def test_calculate_with_no_valid_variables(self):
        self.input = "a+2"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Variable a not found."

        self.assertEqual(output, desired_output)

    def test_calculate_with_valid_variables(self):
        self.calc.variables["a"] = 2
        self.input = "a+2"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = 4

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

    def test_calculate_with_one_value_for_min(self):
        self.input = "min(3)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Enter two values for each min or max function."

        self.assertEqual(output, desired_output)

    def test_calculate_min(self):
        self.input = "min(-2,9)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = min(-2,9)

        self.assertEqual(output, desired_output)

    def test_calculate_max(self):
        self.input = "max(-2,9)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = max(-2,9)

        self.assertEqual(output, desired_output)

    def test_calculate_minmax_with_not_enough_values(self):
        self.input = "min(1+2,3+4+max(5))"
        self.calc.min_count = 1
        self.calc.max_count = 1
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Enter two values for each min or max function."

        self.assertEqual(output, desired_output)

    def test_calculate_while_setting_new_variable(self):
        self.input = "a=2+2"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        value = 2+2
        desired_output = f"a={value}"

        self.assertEqual(output, desired_output)

    def test_calculate_with_saved_variables(self):
        self.calc.variables["a"] = 2
        self.calc.variables["b"] = 0
        self.input = "a+b+3"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        a = 2
        b = 0
        desired_output = a+b+3

        self.assertEqual(output, desired_output)

    def test_calculate_with_several_functions(self):
        self.input = "√(max(cos(3×0.58+3.2),4+7÷2))"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = math.sqrt(max(math.cos(3*0.58+3.2),4+7/2))
                                                
        self.assertEqual(output, desired_output)

    def test_calculate_with_alot_of_parenthesis(self):
        self.input = "(5+27((7.49-2.902)×0.793)sin(5.30+(7.24-0.89))(0.3849÷1.45)5.30-6.01)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = (5+27*((7.49-2.902)*0.793)*math.sin(5.30+(7.24-0.89))*(0.3849/1.45)*5.30-6.01)
                                                               
        self.assertEqual(output, desired_output)

    def test_calculate_with_parenthesis_and_functions(self):
        self.input = "sin(0.345-2.587max(4,7))((2))min(sin(8.53+2.43),tan(5.3-24.1-42)+7.493)"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = math.sin(0.345-2.587*max(4,7))*((2))*min(math.sin(8.53+2.43),math.tan(5.3-24.1-42)+7.493)

        self.assertEqual(output, desired_output)

    def test_calculate_with_parenthesis_functions_and_variables(self):
        self.input = "(5+27((7.49-2.902)×0.793)sin(5.30+(7.24-0.89))(0.3849÷1.45)5.30-6.01)=a"
        self.calc.insert_input(self.input)
        self.calc.calculate()

        self.input = "b=sin(0.345-2.587max(4,7))((2))min(sin(8.53+2.43),tan(5.3-24.1-42)+7.493)"
        self.calc.insert_input(self.input)
        self.calc.calculate()

        a = (5+27*((7.49-2.902)*0.793)*math.sin(5.30+(7.24-0.89))*(0.3849/1.45)*5.30-6.01)
        b = math.sin(0.345-2.587*max(4,7))*((2))*min(math.sin(8.53+2.43),math.tan(5.3-24.1-42)+7.493)

        self.input = "a+b"
        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = a+b

        self.assertEqual(output, desired_output)

    def test_calculate_with_missing_parenthesis(self):
        self.input = "(5+27((7.49-2.902)×0.793)sin(5.30+(7.24-0.89))(0.3849÷1.45)5.30-6.01"

        for char in self.input:
            if char == "(":
                self.calc.left_parenthesis += 1
            elif char == ")":
                self.calc.right_parenthesis += 1

        self.calc.insert_input(self.input)
        output = self.calc.calculate()
        desired_output = "Close all parenthesis."

        self.assertEqual(output, desired_output)
