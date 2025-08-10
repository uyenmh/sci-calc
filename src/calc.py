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
        self.functions = ["√", "sin⁻¹", "cos⁻¹", "tan⁻¹", "sin", "cos", "tan", "min", "max"]
        self.radians = True
        self.min_count = 0
        self.max_count = 0
        self.commas = 0
        self.equality_status = False
        self.variable_to_save = None
        self.variables = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
            "f": None,
            "g": None,
            "h": None,
            "i": None,
            "j": None
        }

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

    def check_validity_of_input(self, current_input, addition_to_input):
        """Checks if the given character is valid with the existing input.

        Args:
            current_input (str): The existing input.
            addition_to_input (str): The character to be added to the input.

        Returns:
            str: An error message if there is one, otherwise nothing.
        """
        message = ""

        pattern = r'(sin|cos|tan|min|max|\d?\.\d+|\d+|[a-j()+\-×÷=])'
        temp_tokens = re.findall(pattern, current_input)

        if current_input:
            if current_input[-1] in "+-×÷" and addition_to_input in "+-×÷":
                message = "Two consecutive operators not allowed."
            elif (self.left_parenthesis > self.right_parenthesis) \
                 and current_input[-1] == "(" \
                 and addition_to_input == ")":
                message = "Parenthesis cannot be left empty."
            elif current_input[-1] == "(" and addition_to_input == "×":
                message = "The multiplication sign is not valid after left parenthesis."
            elif current_input[-1] == "(" and addition_to_input == "÷":
                message = "The division sign is not valid after left parenthesis."
            elif current_input[-1] in "+-×÷" and addition_to_input == ")":
                message = "A right parenthesis is not valid after an operator."
            elif (current_input[-1] == "." and addition_to_input == ".") \
                 or (temp_tokens and "." in temp_tokens[-1] and addition_to_input == "."):
                message = "Enter a valid number. A number can only contain one dot."
            elif current_input[-1] not in "1234567890.)" and addition_to_input == ",":
                message = "Enter a numerical value before a comma."
            elif current_input[-1] == "," and addition_to_input in "×÷":
                message = "Operators not allowed after a comma."
            elif self.equality_status is True and addition_to_input == "=":
                message = "Only one equal to sign is allowed in an equation."
            elif self.left_parenthesis != self.right_parenthesis and addition_to_input == "=":
                message = "Close all parenthesis first."
            elif (current_input[-1] not in "1234567890.)" \
                 and current_input[-1] not in self.variables) \
                 and addition_to_input == "=":
                message = "Enter a variable or a value before an equal to sign."
            elif current_input[-1] == "=" and addition_to_input in "×÷":
                message = "Operators not allowed after an equal to sign."
            elif not any(v in temp_tokens for v in self.variables) \
                 and current_input[-1] == "=" \
                 and addition_to_input not in self.variables:
                message = "Enter a variable to save value to."
            elif not any(v in temp_tokens[:-2] for v in self.variables) \
                 and len(current_input) >= 2 and current_input[-2] == "=" \
                 and current_input[-1] in self.variables \
                 and addition_to_input in self.variables:
                message = "Unexpected character after variable."
            elif len(current_input) > 3 and current_input[-2] == "=" \
                 and current_input[-1] in self.variables \
                 and addition_to_input in self.variables:
                message = "Unexpected character after variable."
        elif not current_input and addition_to_input in "×÷":
            if addition_to_input == "×":
                message = "The expression can't start with a multiplication sign."
            else:
                message = "The expression can't start with a division sign."
        elif not current_input and addition_to_input == "=":
            message = "Enter a variable or a value first."

        if self.left_parenthesis <= self.right_parenthesis and addition_to_input == ")":
            message = "Insert a left parenthesis first."

        if addition_to_input == "," and (self.min_count + self.max_count) <= self.commas:
            message = "Comma must separate exactly two values in a min or max function."

        if message == "":
            if addition_to_input == "(" or addition_to_input[:-1] in self.functions:
                self.left_parenthesis += 1
                if addition_to_input[:-1] == "min":
                    self.min_count += 1
                elif addition_to_input[:-1] == "max":
                    self.max_count += 1
            elif (
                addition_to_input == ")"
                and (self.left_parenthesis > self.right_parenthesis)
            ):
                self.right_parenthesis += 1
            elif addition_to_input == ",":
                self.commas += 1
            elif addition_to_input == "=":
                self.equality_status = True

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
            elif prev_char == ")" and char in "1234567890.sct":
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
            elif prev_char in "1234567890.)" and char == "m":
                self.reformatted_input += f" × {char}"
            elif prev_char == "m" and char in "ia":
                self.reformatted_input += char
            elif prev_prev_char == "m" and prev_char in "ia" and char in "nx":
                self.reformatted_input += char
            elif prev_char in self.variables and char in self.variables:
                self.reformatted_input += f" × {char}"
            elif prev_char in "1234567890.)" and char in self.variables:
                self.reformatted_input += f" × {char}"
            elif prev_char in self.variables and char in "1234567890(":
                self.reformatted_input += f" × {char}"
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

        if "=" in self.tokens:
            equal_sign_index = self.tokens.index("=")
            if len(self.tokens) == 3 and self.tokens[0] in self.variables \
                 and self.tokens[-1] in self.variables:
                first_variable = self.tokens[0]
                second_variable = self.tokens[-1]
                if self.variables[first_variable] and not self.variables[second_variable]:
                    self.variable_to_save = self.tokens.pop()
                    self.tokens.pop()
                elif not self.variables[first_variable] and self.variables[second_variable]:
                    self.variable_to_save = self.tokens.pop(0)
                    self.tokens.pop(0)
                elif self.variables[first_variable] and self.variables[second_variable]:
                    self.variable_to_save = self.tokens.pop(0)
                    self.tokens.pop(0)
            elif equal_sign_index == 1:
                self.variable_to_save = self.tokens.pop(0)
                self.tokens.pop(0)
            elif equal_sign_index == (len(self.tokens) - 2):
                self.variable_to_save = self.tokens.pop()
                self.tokens.pop()

        self.convert_infix_to_rpn()

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
                      "tan⁻¹": 3,
                      "min": 3,
                      "max": 3
                      }

        for token in self.tokens:
            match token:
                case "+" | "-" | "×" | "÷" | "√" | "sin" | "cos" | "tan" | "sin⁻¹" | "cos⁻¹" | "tan⁻¹" | "min" | "max":
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
                case ",":
                    while len(self.operator_stack) > 0:
                        operator = self.operator_stack[-1]
                        if (
                            (self.operator_stack[-2] == "min" or self.operator_stack[-2] == "max")
                            and operator == "("
                        ):
                            break
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
            case ",":
                return "Enter a second value for the min or max function."

        for i, token in enumerate(self.output_queue):
            if token in self.variables:
                if self.variables[token] is None:
                    return f"Variable {token} not found."
                self.output_queue[i] = self.variables[token]

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
            elif output in self.functions[:7]:
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
                            return "sin⁻¹ and cos⁻¹ functions require a value between -1 and 1."

                        if self.radians is True:
                            number_after_trig_function = trig_function(number)
                        else:
                            number_after_trig_function = math.degrees(trig_function(number))
                        solution.append(number_after_trig_function)
            else:
                if output in ("min", "max") and len(solution) < 2:
                    return "Enter two values for each min or max function."

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
                    case "min" | "max":
                        if (self.min_count + self.max_count) > self.commas:
                            return "Enter two values for each min or max function."

                        if output == "min":
                            number_after_function = min(first_number, second_number)
                        else:
                            number_after_function = max(first_number, second_number)
                        solution.append(number_after_function)

        solution = solution[0]

        if solution.is_integer():
            solution = int(solution)

        if self.variable_to_save:
            self.variables[self.variable_to_save] = solution
            solution = f"{self.variable_to_save}={solution}"

        self.variable_to_save = None

        return solution
