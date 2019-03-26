#!/usr/bin/python

# from scanner import scanner
import ply.yacc as yacc


class Parser:
    precedence = (
        ('nonassoc', 'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN',
         'MULTIPLIES_ASSIGN', 'DIVIDES_ASSIGN'),

        ('nonassoc', 'EQUAL', 'INEQUAL'),

        ('nonassoc', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'),

        ('left', 'PLUS', 'MINUS', 'DOT_PLUS', 'DOT_MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'DOT_TIMES', 'DOT_DIVIDE'),

        ('right', 'MINUS'),

        ('left', 'APOSTROPHE'),

        ('nonassoc', 'COLON')
    )

    def __init__(self, lexer, **kwargs):
        self.tokens = lexer.tokens
        self.lexer = lexer
        self.parser = yacc.yacc(module=self, start='program', **kwargs)

    def p_program(self, p):
        """program : multiline_statement"""

        p[0] = ('program', p[1])

    def p_error(self, p):
        if p:
            raise SyntaxError("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                                  self.lexer.find_column(
                                                                                                      self.lexer.get_data(),
                                                                                                      p),
                                                                                                  p.type, p.value))
            # self.parser.errok()
        else:
            print("Unexpected end of input")

    def p_multiline_statement_1(self, p):
        """multiline_statement : code_block"""
        p[0] = p[1]

    def p_multiline_statement_2(self, p):
        """multiline_statement :  multiline_statement code_block"""
        p[0] = p[1] + p[2]

    def p_code_block_1(self, p):
        """code_block : statement"""

        p[0] = p[1]

    def p_code_block_2(self, p):
        """code_block : LCURLY_BRACKET multiline_statement RCURLY_BRACKET"""

        p[0] = p[2]

    def p_statement_1(self, p):
        """statement : SEMICOLON"""

        p[0] = []

    def p_statement_2(self, p):
        """statement : statement SEMICOLON"""

        p[0] = p[1]

    def p_statement_3(self, p):
        """statement : expression_statement SEMICOLON"""

        p[0] = [p[1]]

    def p_statement_4(self, p):
        """statement : if_statement
                     | while_statement
                     | for_statement
                     | print_statement
                     | return_statement
                     | break_statement
                     | continue_statement"""
        p[0] = [p[1]]

    def p_expression_statement(self, p):
        """expression_statement : expression
                                | assignment_expression"""

        p[0] = p[1]

    def p_expression_1(self, p):
        """expression : math_expression
                      | conditional_expression"""

        p[0] = p[1]

    def p_expression_2(self, p):
        """expression : LPAREN expression RPAREN"""

        p[0] = p[2]

    def p_assignment_expression(self, p):
        """assignment_expression : variable_access_expression ASSIGN expression
                  | variable_access_expression ADD_ASSIGN expression
                  | variable_access_expression SUB_ASSIGN expression
                  | variable_access_expression MULTIPLIES_ASSIGN expression
                  | variable_access_expression DIVIDES_ASSIGN expression"""

        p[0] = ('assignment', p[2], p[1], p[3])

    def p_math_expression_1(self, p):
        """math_expression : math_expression PLUS math_expression
                           | math_expression MINUS math_expression
                           | math_expression DOT_PLUS math_expression
                           | math_expression DOT_MINUS math_expression
                           | math_expression TIMES math_expression
                           | math_expression DIVIDE math_expression
                           | math_expression DOT_TIMES math_expression
                           | math_expression DOT_DIVIDE math_expression
                           """

        p[0] = ('math-expression', p[2], p[1], p[3])

    def p_math_expression_2(self, p):
        """math_expression : LPAREN math_expression RPAREN"""

        p[0] = p[2]

    def p_math_expression_3(self, p):
        """math_expression : transpose_matrix
                           | single_matrix_operation_function
                           | variable_access_expression
                           | matrix
                           | value"""

        p[0] = p[1]

    def p_math_expression_4(self, p):
        """math_expression : MINUS variable_access_expression"""

        p[0] = ('uminus', p[2])

    def p_matrix_1(self, p):
        """matrix : LSQUARE_BRACKET RSQUARE_BRACKET"""

        p[0] = []

    def p_matrix_2(self, p):
        """matrix : LSQUARE_BRACKET matrix_content RSQUARE_BRACKET"""

        p[0] = p[2]

    def p_matrix_row_1(self, p):
        """matrix_row : value"""

        p[0] = [p[1]]

    def p_matrix_row_2(self, p):
        """matrix_row : matrix_row COMA value"""

        p[0] = p[1] + [p[3]]

    def p_matrix_content_1(self, p):
        """matrix_content : matrix_row"""

        p[0] = p[1]

    def p_matrix_content_2(self, p):
        """matrix_content : matrix_content SEMICOLON matrix_row"""

        matrix_content = p[1]
        matrix_row = p[3]

        if type(matrix_content[0]) == list:
            matrix_content += [matrix_row]

        else:
            matrix_content = [matrix_content, matrix_row]

        p[0] = matrix_content

    def p_variable_access_expression_1(self, p):
        """variable_access_expression : ID"""

        p[0] = ('id', p[1])

    def p_variable_access_expression_2(self, p):
        """variable_access_expression : ID LSQUARE_BRACKET list_of_integers RSQUARE_BRACKET"""

        p[0] = ('index', ('id', p[1]), p[3])

    def p_list_of_integers_1(self, p):
        """list_of_integers : INT_NUM"""

        p[0] = [p[1]]

    def p_list_of_integers_2(self, p):
        """list_of_integers : list_of_integers COMA INT_NUM"""

        p[0] = p[1] + [p[3]]

    def p_contitional_expression(self, p):
        """conditional_expression : expression EQUAL expression
                                  | expression INEQUAL expression
                                  | expression LESS expression
                                  | expression GREATER expression
                                  | expression LESS_EQUAL expression
                                  | expression GREATER_EQUAL expression"""

        p[0] = ('condition', p[2], p[1], p[3])

    def p_if_statement_2(self, p):
        """if_statement : IF expression code_block"""

        p[0] = ('if', p[2], p[3], None)

    def p_if_statement_1(self, p):
        """if_statement : IF expression code_block ELSE code_block
                        | IF expression code_block ELSE if_statement"""

        p[0] = ('if', p[2], p[3], ('else', p[5]))

    def p_coma_separated_expressions_1(self, p):
        """coma_separated_expressions : expression"""
        p[0] = [p[1]]

    def p_coma_separated_expressions_2(self, p):
        """coma_separated_expressions : coma_separated_expressions COMA expression"""
        p[0] = p[1] + [p[3]]

    def p_print_statement(self, p):
        """print_statement : PRINT coma_separated_expressions"""

        p[0] = ('print', p[2])

    def p_while_statement(self, p):
        """while_statement : WHILE expression code_block"""
        p[0] = ('while', p[2], p[3])

    def p_range_statement(self, p):
        """range_statement : math_expression COLON math_expression"""

        p[0] = ('range', p[1], p[3])

    def p_for_statement(self, p):
        """for_statement : FOR ID ASSIGN range_statement code_block"""

        p[0] = ('for', ('id-range', p[2], p[4]), p[5])

    def p_return_statement(self, p):
        """return_statement : RETURN expression"""

        p[0] = ('return', p[2])

    def p_break_statement(self, p):
        """break_statement : BREAK"""

        p[0] = ('break',)

    def p_continue_statement(self, p):
        """continue_statement : CONTINUE"""

        p[0] = ('continue',)

    def p_transpose_matrix(self, p):
        """transpose_matrix : variable_access_expression APOSTROPHE"""

        p[0] = ('transpose', p[1])

    def p_single_matrix_operation_function(self, p):
        """single_matrix_operation_function : EYE LPAREN INT_NUM RPAREN
                                            | ZEROS LPAREN INT_NUM RPAREN
                                            | ONES LPAREN INT_NUM RPAREN"""

        p[0] = (p[1], int(p[3]))

    def p_value_1(self, p):
        """value : INT_NUM"""

        p[0] = ('integer', int(p[1]))

    def p_value_2(self, p):
        """value : FLOATING_POINT_NUM"""

        p[0] = ('float', float(p[1]))

    def p_value_3(self, p):
        """value : STRING"""

        p[0] = ('string', p[1])

    def parse(self, text, lexer, **kwargs):
        return self.parser.parse(text, lexer=lexer, **kwargs)
