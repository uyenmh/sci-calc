import re

class Calculator:
    """A class that calculates the solution to the given mathematical expression
        and returns it as an integer.
    """
    def __init__(self, input):
        """The class constructor. Tokenizes the infix into RPN.

        Args:
            input (str): The mathematical expression given by the user.
        """
        self.input = input
        self.output_queue = []
        self.operator_stack = []
        self.tokens = []

        self.tokenize_input()
        self.convert_infix_to_rpn()

    def tokenize_input(self):
        """Tokenizes the given mathematical expression into a list of tokens.
        """
        pattern = r'(\d+\.\d+|\d+|[()+\-×÷])'
        self.tokens = re.findall(pattern, self.input)

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
