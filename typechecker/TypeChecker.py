#!/usr/bin/python
import sys
from collections import defaultdict

from parser.ast import AST
from typechecker.SymbolTable import SymbolTable
from .Types import *


class NodeVisitor:

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


range_types = [IntegerType, FloatType]

types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

standard_ops = ['+', '-', '*', '/']
matrix_ops = ['.+', '.-', '.*', './']
relation_ops = ['<', '>', '>=', '<=', '==', '!=']
assign_ops = ['+=', '-=', '*=', '/=']

for op in standard_ops + assign_ops:
    types[op][type(IntegerType)][type(FloatType)] = type(FloatType)
    types[op][type(FloatType)][type(IntegerType)] = type(FloatType)
    types[op][type(FloatType)][type(FloatType)] = type(FloatType)
    types[op][type(IntegerType)][type(IntegerType)] = type(IntegerType)
    types[op][type(MatrixType)][type(MatrixType)] = type(MatrixType)

for op in matrix_ops:
    types[op][type(MatrixType)][type(MatrixType)] = type(MatrixType)

for op in relation_ops:
    types[op][type(IntegerType)][type(FloatType)] = type(FloatType)
    types[op][type(FloatType)][type(IntegerType)] = type(FloatType)
    types[op][type(FloatType)][type(FloatType)] = type(FloatType)
    types[op][type(IntegerType)][type(IntegerType)] = type(IntegerType)

types['+'][type(StringType)][type(StringType)] = type(StringType)

types['\''][type(MatrixType)][None] = type(MatrixType)
types['-'][type(MatrixType)][None] = type(MatrixType)
types['-'][type(IntegerType)][None] = type(IntegerType)
types['-'][type(FloatType)][None] = type(FloatType)


class TypeChecker(NodeVisitor):

    def __init__(self):
        super(TypeChecker, self).__init__()
        self.symbol_table = SymbolTable(None, "main")
        self.error_occurred = False
        self.loop_level = 0

    def visit_CodeBlock(self, node):
        children = node.children
        self.symbol_table = self.symbol_table.pushScope("code_block")
        for child in children:
            self.visit(child)
        self.symbol_table = self.symbol_table.popScope()
        return CodeBlockType()

    def visit_IntegerNumber(self, node):
        return IntegerType()

    def visit_FloatNumber(self, node):
        return FloatType()

    def visit_StringValue(self, node):
        return StringType()

    def visit_Variable(self, node):
        variable_type = self.symbol_table.get(node.name)
        if variable_type is None:
            print("{0}: Undefined variable".format(node.line), file=sys.stderr)
            self.error_occurred = True
            return ErrorType()

        return variable_type.value_type

    def visit_BinaryExpression(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op

        if op == '=':
            pass

        elif op in relation_ops:
            pass
        # else: rób to, co na dole

        if isinstance(left, ErrorType) or isinstance(right, ErrorType):
            self.error_occurred = 1
            return ErrorType()

        result_type = types[op][type(left)][type(right)]

        if result_type is not None:
            if isinstance(result_type, MatrixType):
                if left.lengths != right.lengths or left.value_type != right.value_type:
                    print("{0}: Different sizes of operand `{1}` parts!".format(node.line, op))
                    self.error_occurred = True
                    return ErrorType()
                else:
                    return left
            return result_type

        print("{0}: Incorrect types of operand `{1}` values!".format(node.line, op))
        self.error_occurred = True
        return ErrorType()

    def visit_UnaryExpression(self, node):
        var_type = self.visit(node.name)
        result_type = types['-'][type(var_type)][None]
        if result_type is not None:
            return result_type
        else:
            print("{} Incorrect type for unary minus expression!".format(node.line))
            self.error_occurred = True
            return ErrorType()

    def visit_Matrix(self, node):
        children = node.children
        if isinstance(children[0], AST.Matrix):
            if all(isinstance(c, AST.Matrix) for c in children):
                submatrixes_types = [self.visit(c) for c in children]
                first_type = type(submatrixes_types[0])
                if all(isinstance(c, first_type) for c in submatrixes_types):
                    return MatrixType(1 + children[0].dimensions, [len(children)] + children[0].lengths,
                                      children[0].value_type)

                print("{0}: Invalid matrix. Matrix can contain only submatrixes or values.".format(node.line),
                      file=sys.stderr)
                self.error_occurred = 1
                return ErrorType()

            print("{0}: Invalid matrix. Matrix can contain only submatrixes or values.".format(node.line),
                  file=sys.stderr)
            self.error_occurred = 1
            return ErrorType()

        if any(isinstance(c, AST.Matrix) for c in children):
            print("{0}: Invalid matrix. Matrix can contain only submatrixes or values.".format(node.line),
                  file=sys.stderr)
            self.error_occurred = 1
            return ErrorType()

        c_type = type(children[0])
        if not all(isinstance(c, c_type) for c in children):
            print("{0}: Invalid matrix. Matrix can contain only submatrixes or values of the same type.".format(
                node.line),
                file=sys.stderr)
            self.error_occurred = 1
            return ErrorType()

        return MatrixType(1, [len(children)], c_type)

    def visit_ReturnStatement(self, node):
        if node.value is not None:
            return self.visit(node.content)

    def visit_BreakStatement(self, node):
        if self.loop_level <= 0:
            print("{0}: Unexpected break statement outside of loop.".format(node.line), file=sys.stderr)
            self.error_occurred = 1

    def visit_ContinueStatement(self, node):
        if self.loop_level <= 0:
            print("{0}: Unexpected continue statement outside of loop.".format(node.line), file=sys.stderr)
            self.error_occurred = 1

    def visit_ElementAccessExpression(self, node):
        var_type = self.visit(node.variable)

        if isinstance(var_type, MatrixType):
            index_len = len(node.index)
            if index_len > var_type.dimensions:
                print("{0}: Too many dimensions specified in index list.".format(node.line))
                self.error_occurred = True
                return ErrorType()

            if index_len < var_type.dimensions:
                return MatrixType(var_type.dimensions - index_len,
                                  var_type.lengths[index_len:],
                                  var_type.value_type)

            for (x, y) in zip(node.index, var_type.lengths):
                if x > y:
                    print("{0}: Specified index is greater than matrix dimension.".format(node.line))
                    self.error_occurred = True
                    return ErrorType()

            return var_type.value_type

        print("{0}: Only matrices can be accessed using ranges.".format(node.line))
        self.error_occurred = True
        return ErrorType()

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.symbol_table.pushScope('if')
        self.visit(node.code_block)
        self.symbol_table.popScope()

        if node.else_statement is not None:
            self.symbol_table.pushScope('else')
            self.visit(node.else_statement)
            self.symbol_table.popScope()

    def visit_WhileStatement(self, node):
        self.loop_level += 1
        self.symbol_table = self.symbol_table.pushScope('while')

        self.visit(node.condition)
        self.visit(node.code_block)

        self.symbol_table = self.symbol_table.popScope()
        self.loop_level -= 1

    def visit_RangeExpression(self, node):
        value_type = self.visit(node.left)
        if isinstance(value_type, ErrorType) or value_type not in range_types:
            print("{0}: Incorrect range expression type!".format(node.line))
            self.error_occurred = True
            return ErrorType()
        value_type = self.visit(node.right)
        if isinstance(value_type, ErrorType) or value_type not in range_types:
            print("{0} Incorrect range expression type!".format(node.line))
            self.error_occurred = True
            return ErrorType()

        return value_type

    def visit_ForStatement(self, node):
        self.loop_level += 1
        self.symbol_table = self.symbol_table.pushScope('for')

        self.visit(node.iteration_variable_range)
        self.visit(node.code_block)

        self.symbol_table = self.symbol_table.popScope()
        self.loop_level -= 1

    def visit_TransposeStatement(self, node):
        var_type = self.visit(node.value)

        if isinstance(var_type, MatrixType):
            print("{0} Transpose can be applied only to matrices!".format(node.line))
            self.error_occurred = True
            return ErrorType()

        return MatrixType(var_type.dimensions, reversed(var_type.lengths))

    def visit_PrintStatement(self, node):
        for value in node.values:
            self.visit(value)

    def visit_ZerosStatement(self, node):
        if isinstance(node.value, int):
            return MatrixType(node.value, [node.value] * node.value)

        return ErrorType()

    def visit_OnesStatement(self, node):
        if isinstance(node.value, int):
            return MatrixType(node.value, [node.value] * node.value)

        return ErrorType()

    def visit_EyeStatement(self, node):
        if isinstance(node.value, int):
            return MatrixType(node.value, [node.value] * node.value)

        return ErrorType()

    def visit_ListOfIntegers(self, node):
        for child in node.children:
            if not isinstance(child, int):
                print("{0}: Unexpected continue statement outside of loop.".format(node.line), file=sys.stderr)
                self.error_occurred = True

    def visit_Error(self, node):
        return ErrorType()
