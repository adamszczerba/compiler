import sys

from parser import Mparser
from scanner import scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = scanner.Scanner()
    lexer.build()

    parser = Mparser.Parser(lexer)

    try:
       ast = parser.parse(text, lexer=lexer)
       ast.printTree()
    except SyntaxError as e:
        print(e)
