class Node:
    pass


class CodeBlock(Node):
    def __init__(self, node=None):
        if node is None:
            self.value = []
        if isinstance(node, Node):
            self.value = [node]
        elif type(node) == list:
            self.value = node
        elif type(node) == CodeBlock:
            self.value = node.value
        else:
            raise ValueError("Passed argument is invalid")

    def __add__(self, node):
        if type(node) == Node:
            return CodeBlock(self.value + [node])
        elif type(node) == list:
            return CodeBlock(self.value + node)
        elif type(node) == CodeBlock:
            return CodeBlock(self.value + node.value)

        raise ValueError("Passed argument is invalid")


class IntegerNumber(Node):
    def __init__(self, value):
        self.value = value


class FloatNumber(Node):
    def __init__(self, value):
        self.value = value


class StringValue(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinaryExpression(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpression(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right


class Matrix(Node):
    def __init__(self, value=None):
        if value is None:
            self.value = []

        elif type(value) == Matrix:
            self.value = value.value

        elif type(value) == list:
            nam_of_matrices_in_row = len(list(filter(lambda l: type(l) == Matrix, value)))

            # Only if passed `rows` is row of matrices or values. Don't accept mixed.
            if nam_of_matrices_in_row == 0 or nam_of_matrices_in_row == len(value):
                self.value = value
                return
        else:
            raise ValueError("Passed value is not a row or list of rows.")

    def __add__(self, other):
        if type(other) == Matrix:
            return Matrix(self.value + other.value)
        else:
            return Matrix(self.value + [other])


class CallExpression(Node):
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments


class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value


class BreakStatement(Node):
    def __init__(self):
        pass


class ContinueStatement(Node):
    def __init__(self):
        pass


class ElementAccessExpression(Node):
    def __init__(self, variable, index):
        self.variable = variable
        self.index = index


class IfStatement(Node):
    def __init__(self, condition, code_block, else_statement=None):
        self.condition = condition

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block

        if else_statement is None or type(else_statement) in [IfStatement, CodeBlock]:
            self.else_statement = else_statement


class WhileStatement(Node):
    def __init__(self, condition, code_block):
        self.condition = condition

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block


class RangeExpression(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class ForStatement(Node):
    def __init__(self, iteration_variable_range, code_block):
        self.iteration_variable_range = iteration_variable_range

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block


class TransposeStatement(Node):
    def __init__(self, value):
        self.value = value


class PrintStatement(Node):
    def __init__(self, values):
        if type(values) != list:
            raise ValueError("PrintStatement accepts only a list of values to print.")

        self.values = values


class ZerosStatement(Node):
    def __init__(self, value):
        self.value = value


class OnesStatement(Node):
    def __init__(self, value):
        self.value = value


class EyeStatement(Node):
    def __init__(self, value):
        self.value = value


class Error(Node):
    def __init__(self):
        pass
