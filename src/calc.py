import re
import math

class Calculator:
    """A class that calculates the solution to the given mathematical expression
        and returns it as an integer.
    """
    def __init__(self):
        """The class constructor. Initializes the calculator.
        """
        self.input = ""
        self.reformatted_input = ""
        self.output_queue = []
        self.operator_stack = []
        self.tokens = []
        self.left_parenthesis = 0
        self.right_parenthesis = 0
        self.operators = ["+", "-", "×", "÷"]
        self.functions = ["√", "sin", "cos", "tan", "sin⁻¹", "cos⁻¹", "tan⁻¹"]
        self.radians = True

    def insert_input(self, user_input):
        """Tokenizes the infix into RPN.

        Args:
            user__input (str): The mathematical expression given by the user.
        """
        self.input = user_input
        self.reformatted_input = ""
        self.output_queue = []
        self.operator_stack = []
        self.tokens = []

        self.reformat_input()
        self.tokenize_input()
        self.convert_infix_to_rpn()

    def check_validity_of_input(self, current_input, addition_to_input):
        """Checks if the given character is valid with the existing input.

        Args:
            current_input (str): The existing input.
            addition_to_input (str): The character to be added to the input.

        Returns:
            str: An error message if there is one, otherwise nothing.
        """
        message = ""

        pattern = r'(\d?+\.\d+|\d+|[()+\-×÷])'
        temp_tokens = re.findall(pattern, current_input)

        if current_input:
            if current_input[-1] in "+-×÷" and addition_to_input in "+-×÷":
                message = "Two consecutive operators not allowed."
            elif (
                (self.left_parenthesis > self.right_parenthesis)
                and current_input[-1] == "("
                and addition_to_input == ")"
            ):
                message = "Parenthesis cannot be left empty."
            elif current_input[-1] == "(" and addition_to_input == "×":
                message = "The multiplication sign is not valid after left parenthesis."
            elif current_input[-1] == "(" and addition_to_input == "÷":
                message = "The division sign is not valid after left parenthesis."
            elif current_input[-1] in "+-×÷" and addition_to_input == ")":
                message = "A right parenthesis is not valid after an operator."
            elif (
                (current_input[-1] == "." and addition_to_input == ".")
                or ("." in temp_tokens[-1] and addition_to_input == ".")
            ):
                message = "Invalid number. A number can only contain one dot."
        elif not current_input and addition_to_input in "×÷":
            if addition_to_input == "×":
                message = "The expression can't start with a multiplication sign."
            else:
                message = "The expression can't start with a division sign."

        if self.left_parenthesis <= self.right_parenthesis and addition_to_input == ")":
            message = "Insert a left parenthesis first."

        if message == "":
            if addition_to_input == "(" or addition_to_input[:-1] in self.functions:
                self.left_parenthesis += 1
            elif (
                addition_to_input == ")"
                and (self.left_parenthesis > self.right_parenthesis)
            ):
                self.right_parenthesis += 1

        return message

    def reformat_input(self):
        """Reformats a valid mathematical expression for easier tokenization.
        """
        prev_prev_char = ""
        prev_char = ""

        for index, char in enumerate(self.input):
            if index == 0:
                self.reformatted_input += char
            elif index == 1 and prev_char in "+-":
                if char in "1234567890.":
                    self.reformatted_input += char
                elif char == "(":
                    self.reformatted_input += f"1 × {char}"
            elif prev_prev_char == "(" and prev_char in "+-" and char in "1234567890.":
                self.reformatted_input += char
            elif prev_char in "1234567890" and char in "1234567890.":
                self.reformatted_input += char
            elif prev_char == "." and char in "1234567890":
                self.reformatted_input += char
            elif prev_char in "1234567890" and char == "(":
                self.reformatted_input += f" × {char}"
            elif prev_char == ")" and char in "1234567890.":
                self.reformatted_input += f" × {char}"
            elif prev_char in "1234567890." and char == "√":
                self.reformatted_input += f" × {char}"
            elif prev_char in "1234567890." and char in "sct":
                self.reformatted_input += f" × {char}"
            elif prev_char in "sct" and char in "ioa":
                self.reformatted_input += char
            elif prev_prev_char in "sct" and prev_char in "ioa" and char in "ns":
                self.reformatted_input += char
            elif prev_prev_char in "ioa" and prev_char in "ns" and char == "⁻":
                self.reformatted_input += char
            elif prev_prev_char in "ns" and prev_char == "⁻" and char == "¹":
                self.reformatted_input += char
            else:
                self.reformatted_input += f" {char}"

            prev_prev_char = prev_char
            prev_char = char

        if self.left_parenthesis > self.right_parenthesis and prev_char in "1234567890.":
            missing_parenthesis = self.left_parenthesis - self.right_parenthesis
            self.reformatted_input += missing_parenthesis*" )"
            self.right_parenthesis += missing_parenthesis

    def tokenize_input(self):
        """Tokenizes the given mathematical expression into a list of tokens.
        """
        self.tokens = self.reformatted_input.split()

    def convert_infix_to_rpn(self):
        """Converts the given mathematical expression (from token format) into RPN.
        """
        precedence = {"(": 0,
                      "+": 1,
                      "-": 1,
                      "×": 2,
                      "÷": 2,
                      "√": 3,
                      "sin": 3,
                      "cos": 3,
                      "tan": 3,
                      "sin⁻¹": 3,
                      "cos⁻¹": 3,
                      "tan⁻¹": 3
                      }

        for token in self.tokens:
            match token:
                case "+" | "-" | "×" | "÷" | "√" | "sin" | "cos" | "tan" | "sin⁻¹" | "cos⁻¹" | "tan⁻¹":
                    while len(self.operator_stack) > 0:
                        operator = self.operator_stack[-1]
                        if precedence[token] > precedence[operator] or operator == "(":
                            break
                        self.operator_stack.pop()
                        self.output_queue.append(operator)
                    self.operator_stack.append(token)
                case "(":
                    self.operator_stack.append(token)
                case ")":
                    while len(self.operator_stack) > 0:
                        operator = self.operator_stack[-1]
                        if operator == "(":
                            self.operator_stack.pop()
                            break
                        self.operator_stack.pop()
                        self.output_queue.append(operator)
                    if len(self.operator_stack) > 0:
                        operator = self.operator_stack[-1]
                        if operator in self.functions:
                            self.operator_stack.pop()
                            self.output_queue.append(operator)
                case _:
                    self.output_queue.append(token)

        while len(self.operator_stack) > 0:
            operator = self.operator_stack.pop()
            self.output_queue.append(operator)

    def calculate(self):
        """Evaluates the given mathematical expression in RPN.

        Returns:
            int or str: The result of the given mathematical expression if valid,
            or an error message otherwise.
        """
        solution = []

        match self.tokens[-1]:
            case "+" | "-" | "×" | "÷":
                return "The expression can't end with an operator."
            case "(":
                return "Parenthesis cannot be left empty."

        trig_functions = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sin⁻¹": math.asin,
            "cos⁻¹": math.acos,
            "tan⁻¹": math.atan
        }

        for output in self.output_queue:
            if output not in self.operators and output not in self.functions:
                solution.append(float(output))
            elif output in self.functions:
                number = solution.pop()
                match output:
                    case "√":
                        if number < 0:
                            return "The square root of a negative number can't be calculated."

                        number_after_sqrt = math.sqrt(number)
                        solution.append(number_after_sqrt)
                    case "sin" | "cos" | "tan":
                        trig_function = trig_functions[output]

                        if self.radians is True:
                            number_after_trig_function = trig_function(number)
                        else:
                            number_after_trig_function = trig_function(math.radians(number))
                        solution.append(number_after_trig_function)
                    case "sin⁻¹" | "cos⁻¹" | "tan⁻¹":
                        trig_function = trig_functions[output]

                        if output in ("sin⁻¹","cos⁻¹") and (number < -1 or number > 1):
                            return f"{output} function requires a value between -1 and 1."

                        if self.radians is True:
                            number_after_trig_function = trig_function(number)
                        else:
                            number_after_trig_function = math.degrees(trig_function(number))
                        solution.append(number_after_trig_function)
            else:
                second_number = solution.pop()
                first_number = solution.pop()
                match output:
                    case "+":
                        number_after_addition = first_number + second_number
                        solution.append(number_after_addition)
                    case "-":
                        number_after_subtraction = first_number - second_number
                        solution.append(number_after_subtraction)
                    case "×":
                        number_after_multiplication = first_number * second_number
                        solution.append(number_after_multiplication)
                    case "÷":
                        number_after_division = first_number / second_number
                        solution.append(number_after_division)

        solution = solution[0]

        if solution.is_integer():
            solution = int(solution)

        return solution
