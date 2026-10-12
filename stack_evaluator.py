"""DCOMP320 Assignment 1 - Stack-based expression evaluator.

Reads expressions from input.txt (separated by lines made of dashes),
evaluates each one with stacks, and writes the results to output.txt.
"""


class Stack:
    """A simple stack (Last In, First Out) built on a Python list."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def apply_operator(operators, values):
    """Pop one operator and two values, calculate, push the result."""
    if values.size() < 2:
        raise ValueError("malformed expression")
    op = operators.pop()
    right = values.pop()
    left = values.pop()
    if op == "+":
        values.push(left + right)
    elif op == "-":
        values.push(left - right)
    elif op == "*":
        values.push(left * right)
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        values.push(left / right)


def evaluate_expression(expression):
    """Evaluate one expression string and return the numeric result."""
    values = Stack()      # holds numbers
    operators = Stack()   # holds operators and '('
    i = 0
    expect_number = True  # True when a number (or '(') should come next

    while i < len(expression):
        ch = expression[i]

        if ch == " ":
            i += 1
            continue

        # A number (digits, decimal point), or a minus sign meaning negative
        if ch.isdigit() or ch == "." or (ch == "-" and expect_number):
            start = i
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            try:
                values.push(float(expression[start:i]))
            except ValueError:
                raise ValueError("bad number '" + expression[start:i] + "'")
            expect_number = False
            continue

        if ch == "(":
            operators.push(ch)
            expect_number = True
        elif ch == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operators, values)
            if operators.is_empty():
                raise ValueError("unmatched ')'")
            operators.pop()  # remove the '('
            expect_number = False
        elif ch in PRECEDENCE:
            while (not operators.is_empty() and operators.peek() != "("
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[ch]):
                apply_operator(operators, values)
            operators.push(ch)
            expect_number = True
        else:
            raise ValueError("invalid character '" + ch + "'")
        i += 1

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("unmatched '('")
        apply_operator(operators, values)

    if values.size() != 1:
        raise ValueError("malformed expression")
    return values.pop()


def format_result(number):
    """Show whole numbers without .0 (13.0 -> 13)."""
    if number == int(number):
        return str(int(number))
    return str(round(number, 4))


def is_separator(line):
    """A separator line contains only dashes (e.g. -----)."""
    return len(line) > 0 and set(line) == {"-"}


def process_file(input_path, output_path):
    """Read input file, evaluate each expression, write output file."""
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    output_lines = []
    for line in lines:
        if line == "":
            continue
        if is_separator(line):
            output_lines.append(line)      # keep the same separator
            continue
        try:
            output_lines.append(format_result(evaluate_expression(line)))
        except Exception as error:
            output_lines.append("Error: " + str(error))

    with open(output_path, "w") as f:
        f.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    process_file("input.txt", "output.txt")
    print("Done. Results written to output.txt")