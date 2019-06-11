class Node:
    pass


class CodeBlock(Node):
    def __init__(self, node=None, line=0):

        if node is None:
            self.children = []
        if isinstance(node, Node):
            self.children = [node]
        elif type(node) == list:
            self.children = node
        elif type(node) == CodeBlock:
            self.children = node.children
        else:
            raise ValueError("Passed argument is invalid")

        self.line = line

    def __add__(self, node):
        if type(node) == Node:
            return CodeBlock(self.children + [node])
        elif type(node) == list:
            return CodeBlock(self.children + node)
        elif type(node) == CodeBlock:
            return CodeBlock(self.children + node.children)

        raise ValueError("Passed argument is invalid")


class IntegerNumber(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class FloatNumber(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class StringValue(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class Variable(Node):
    def __init__(self, name, line=0):
        self.name = name
        self.line = line


class BinaryExpression(Node):
    def __init__(self, op, left, right, line=0):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class UnaryExpression(Node):
    def __init__(self, op, right, line=0):
        self.op = op
        self.right = right
        self.line = line


class Matrix(Node):
    def __init__(self, value=None, line=0):

        if type(value) == Matrix:
            self.children = value.children

        elif type(value) == list:
            nam_of_matrices_in_row = len(list(filter(lambda l: type(l) == Matrix, value)))

            # Only if passed `rows` is row of matrices or values. Don't accept mixed.
            if nam_of_matrices_in_row == 0 or nam_of_matrices_in_row == len(value):
                self.children = value
            else:
                raise ValueError("Passed value is not a row or list of rows.")
        else:
            raise ValueError("Passed value is not a row or list of rows.")

        self.line = line

    def __add__(self, other):
        if type(other) == Matrix:
            return Matrix(self.children + other.children, line=self.line)
        else:
            return Matrix(self.children + [other], line=self.line)


class ReturnStatement(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class BreakStatement(Node):
    def __init__(self, line=0):
        self.line = line


class ContinueStatement(Node):
    def __init__(self, line=0):
        self.line = line


class ElementAccessExpression(Node):
    def __init__(self, variable, index, line=0):
        self.variable = variable
        self.index = index
        self.line = line


class IfStatement(Node):
    def __init__(self, condition, code_block, else_statement=None, line=0):
        self.condition = condition

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block

        if else_statement is None or type(else_statement) in [IfStatement, CodeBlock]:
            self.else_statement = else_statement

        self.line = line


class WhileStatement(Node):
    def __init__(self, condition, code_block, line=0):
        self.condition = condition

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block
        self.line = line


class RangeExpression(Node):
    def __init__(self, left, right, line=0):
        self.left = left
        self.right = right
        self.line = line


class ForStatement(Node):
    def __init__(self, iteration_variable_range, code_block, line=0):
        self.iteration_variable_range = iteration_variable_range

        if type(code_block) != CodeBlock:
            raise ValueError('Passed code_block argument have to be of CodeBlock type')

        self.code_block = code_block
        self.line = line


class TransposeStatement(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class PrintStatement(Node):
    def __init__(self, values, line=0):
        if type(values) != list:
            raise ValueError("PrintStatement accepts only a list of values to print.")

        self.values = values
        self.line = line


class ZerosStatement(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class OnesStatement(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class EyeStatement(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class ListOfIntegers(Node):
    def __init__(self, value, line=0):
        if type(value) == list:
            self.children = value
        elif type(value) == int:
            self.children = [value]
        elif isinstance(value, ListOfIntegers):
            self.children = value.children
        else:
            raise ValueError("Passed value is not valid.")

        self.line = line

    def __add__(self, other):
        if type(other) == int:
            return ListOfIntegers(self.children + [other], line=self.line)
        elif type(other) == list:
            return ListOfIntegers(self.children + other, line=self.line)
        elif isinstance(other, ListOfIntegers):
            return ListOfIntegers(self.children + other.children, line=self.line)
        else:
            raise ValueError("Passed value is not valid.")


class Error(Node):
    def __init__(self, line=0):
        self.line = line

from parser.ast.TreePrinter import TreePrinter
