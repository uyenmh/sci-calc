import re

class Calculator:
    """A class that calculates the solution to the given mathematical expression
        and returns it as an integer.
    """
    def __init__(self, input=""):
        """The class constructor. Tokenizes the infix into RPN.

        Args:
            input (str): The mathematical expression given by the user.
        """
        self.input = input
        self.reformatted_input = ""
        self.output_queue = []
        self.operator_stack = []
        self.tokens = []
        self.left_parenthesis = 0
        self.right_parenthesis = 0

        self.reformat_input()
        self.tokenize_input()
        self.convert_infix_to_rpn()

    def insert_input(self, input):
        """Tokenizes the infix into RPN.

        Args:
            input (str): The mathematical expression given by the user.
        """
        self.input = input
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

        if current_input:
            if current_input[-1] in "+-×÷" and addition_to_input in "+-×÷":
                message = "Two consecutive operators not allowed."
            elif (self.left_parenthesis > self.right_parenthesis) and current_input[-1] == "(" and addition_to_input == ")":
                message = "Parenthesis cannot be left empty."
            elif current_input[-1] == "(" and addition_to_input == "×":
                message = "The multiplication sign is not valid after left parenthesis."
            elif current_input[-1] == "(" and addition_to_input == "÷":
                message = "The division sign is not valid after left parenthesis."
        elif not current_input and addition_to_input in "×÷":
            if addition_to_input == "×":
                message = "The expression cannot start with a multiplication sign."
            else:
                message = "The expression cannot start with a division sign."
        elif self.left_parenthesis <= self.right_parenthesis and addition_to_input == ")":
            message = "Insert a left parenthesis first."

        if message == "":
            if addition_to_input == "(":
                self.left_parenthesis += 1
            elif addition_to_input == ")" and (self.left_parenthesis > self.right_parenthesis):
                self.right_parenthesis += 1
            return
        else:
            return message

    def reformat_input(self):
        """Reformats a valid mathematical expression for easier tokenization.
        """
        prev_prev_elem = ""
        prev_elem = ""

        for i in range(len(self.input)):
            if len(self.reformatted_input) == 0:
                self.reformatted_input = f"{self.reformatted_input}{self.input[i]}"
            elif prev_elem in "+-" and self.input[i] == "(":
                if prev_elem == "+":
                    self.reformatted_input = f"{self.reformatted_input} 1 × {self.input[i]}"
                else:
                    self.reformatted_input = f"{self.reformatted_input[:-1]}+ -1 × {self.input[i]}"
            elif len(self.reformatted_input) == 1 and prev_elem in "+-":
                if self.input[i] in "1234567890.":
                    self.reformatted_input = f"{self.reformatted_input}{self.input[i]}"
                else:
                    self.reformatted_input = f"{self.reformatted_input} {self.input[i]}"
            elif prev_elem in "()" and self.input[i] in "+-":
                self.reformatted_input = f"{self.reformatted_input} {self.input[i]}"
            elif prev_prev_elem == "(" and prev_elem in "+-" and self.input[i] in "1234567890.":
                self.reformatted_input = f"{self.reformatted_input}{self.input[i]}"
            elif prev_elem in "1234567890" and self.input[i] in "1234567890.":
                self.reformatted_input = f"{self.reformatted_input}{self.input[i]}"
            elif prev_elem == "." and self.input[i] in "1234567890":
                self.reformatted_input = f"{self.reformatted_input}{self.input[i]}"
            elif prev_elem in "1234567890" and self.input[i] in "+-×÷)":
                self.reformatted_input = f"{self.reformatted_input} {self.input[i]}"
            elif prev_elem in "+-×÷(" and self.input[i] in "1234567890.":
                self.reformatted_input = f"{self.reformatted_input} {self.input[i]}"
            elif prev_elem in "1234567890" and self.input[i] == "(":
                self.reformatted_input = f"{self.reformatted_input} × {self.input[i]}"
            elif prev_elem == ")" and self.input[i] in "1234567890.":
                self.reformatted_input = f"{self.reformatted_input} × {self.input[i]}"
            else:
                self.reformatted_input = f"{self.reformatted_input} {self.input[i]}"

            prev_prev_elem = prev_elem
            prev_elem = self.input[i]

    def tokenize_input(self):
        """Tokenizes the given mathematical expression into a list of tokens.
        """
        self.tokens = self.reformatted_input.split()

    def convert_infix_to_rpn(self):
        """Converts the given mathematical expression (from token format) into RPN.
        """
        precedence = {"+": 1,
                      "-": 1,
                      "×": 2,
                      "÷": 2,
                      "(": 3}   

        for token in self.tokens:
            if token in "+-×÷":
                while len(self.operator_stack) > 0:
                    operator = self.operator_stack[-1]
                    if precedence[token] > precedence[operator] or operator == "(":
                        break
                    self.operator_stack.pop()
                    self.output_queue.append(operator)
                self.operator_stack.append(token)
            elif token == "(":
                self.operator_stack.append(token)
            elif token == ")":
                while len(self.operator_stack) > 0:
                    operator = self.operator_stack[-1]
                    if operator in "(":
                        self.operator_stack.pop()
                        break
                    else:
                        self.operator_stack.pop()
                        self.output_queue.append(operator)
            else:
                self.output_queue.append(token)

        while len(self.operator_stack) > 0:
            operator = self.operator_stack.pop()
            self.output_queue.append(operator)

    def calculate(self):
        """Calculates the solution of the given mathematical expression from the RPN.

        Returns:
            int: The solution of the given mathematical expression.
        """
        solution = []

        for output in self.output_queue:
            if output not in "+-×÷":
                solution.append(float(output))
            else:
                second_number = solution.pop()
                first_number = solution.pop()

            if output == "+":
                number_after_addition = first_number + second_number
                solution.append(number_after_addition)
            elif output == "-":
                number_after_subtraction = first_number - second_number
                solution.append(number_after_subtraction)   
            elif output == "×":
                number_after_multiplication = first_number * second_number
                solution.append(number_after_multiplication)
            elif output == "÷":
                number_after_division = first_number / second_number
                solution.append(number_after_division)

        solution = solution[0]

        if solution.is_integer():
            solution = int(solution)

        return solution
