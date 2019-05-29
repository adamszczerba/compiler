
class Type:
    pass


class CodeBlockType(Type):
    pass


class IntegerType(Type):
    pass


class FloatType(Type):
    pass


class StringType(Type):
    pass


class MatrixType(Type):
    def __init__(self, dimensions, lengths, value_type):
        self.dimensions = dimensions
        self.lengths = lengths
        self.value_type = value_type


class ErrorType(Type):
    pass


class VariableSymbol:
    def __init__(self, name, value_type):
        self.name = name
        self.value_type = value_type
