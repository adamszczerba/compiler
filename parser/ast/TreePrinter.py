from functools import wraps

from parser.ast import AST


def addToClass(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally
    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.CodeBlock)
    def printTree(self, indent=0):
        for statement in self.value:
            statement.printTree(indent)

    @addToClass(AST.IntegerNumber)
    def printTree(self, indent=0):
        print('|' * indent + str(self.value))

    @addToClass(AST.FloatNumber)
    def printTree(self, indent=0):
        print('|' * indent + str(self.value))

    @addToClass(AST.StringValue)
    def printTree(self, indent=0):
        print('|' * indent + r'"' + str(self.value) + r'"')

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print('|' * indent + str(self.name))

    @addToClass(AST.BinaryExpression)
    def printTree(self, indent=0):
        print('|' * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpression)
    def printTree(self, indent=0):
        print('|' * indent + self.op)
        self.right.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print('|' * indent + "MATRIX")

        for row in self.value:
            row.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print('|' * indent + "MATRIX")

        for row in self.value:
            row.printTree(indent + 1)

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent=0):
        print('|' * indent + "RETURN")
        self.value.printTree(indent + 1)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        print('|' * indent + "BREAK")

    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        print('|' * indent + "CONTINUE")

    @addToClass(AST.ElementAccessExpression)
    def printTree(self, indent=0):
        print('|' * indent + "REF")
        self.variable.printTree(indent + 1)
        self.index.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print('|' * indent + "IF")
        self.condition.printTree(indent + 1)
        print('|' * indent + "THEN")
        self.code_block.printTree(indent + 1)

        if self.else_statement is not None:
            print('|' * indent + "ELSE")
            self.else_statement.printTree(indent + 1)

    @addToClass(AST.WhileStatement)
    def printTree(self, indent=0):
        print('|' * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.code_block.printTree(indent + 1)

    @addToClass(AST.RangeExpression)
    def printTree(self, indent=0):
        print('|' * indent + "RANGE")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ForStatement)
    def printTree(self, indent=0):
        print('|' * indent + "FOR")
        self.iteration_variable_range.printTree(indent + 1)
        self.code_block.printTree(indent + 1)

    @addToClass(AST.TransposeStatement)
    def printTree(self, indent=0):
        print('|' * indent + "TRANSPOSE")
        self.value.printTree(indent + 1)

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        print('|' * indent + "PRINT")
        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.ZerosStatement)
    def printTree(self, indent=0):
        print('|' * indent + "ZEROS")
        print('|' * (indent + 1) + str(self.value))

    @addToClass(AST.OnesStatement)
    def printTree(self, indent=0):
        print('|' * indent + "ONES")
        print('|' * (indent + 1) + str(self.value))

    @addToClass(AST.EyeStatement)
    def printTree(self, indent=0):
        print('|' * indent + "EYE")
        print('|' * (indent + 1) + str(self.value))

    @addToClass(AST.ListOfIntegers)
    def printTree(self, indent=0):
        for v in self.value:
            print('|' * indent + str(v))

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
