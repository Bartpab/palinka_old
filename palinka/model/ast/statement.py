from __future__ import annotations
from os import stat
from typing import Union, Tuple, Optional

from .identifier import Identifier

import palinka.model.ast.constant_expression as constant_expression
import palinka.model.ast.expression as expression

class LabeledStatement:
    """
        Represents a labeled statement.

        <labeled-statement> ::= <identifier> : <statement>
                            |   case <constant-expression> : <statement>
                            |   default: <statement> 
    """
    def __init__(self, nodes: Union[
        Tuple[Identifier, Statement],               # ::= <identifier> : <statement>
        Tuple[constant_expression.ConstantExpression, Statement],       # ::= case <constant-expression> : <statement>
        Tuple[Statement]                            # ::= default: <statement
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    @staticmethod
    def first_case(n1: Identifier, n2: Statement):
        return LabeledStatement((n1, n2), 1)

    @staticmethod
    def second_case(n1: constant_expression.ConstantExpression, n2: Statement):
        return LabeledStatement((n1, n2), 2)

    @staticmethod
    def third_case(n1: Statement):
        return LabeledStatement((n1,), 3)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)

class ExpressionStatement:
    """
        Represents an expression statement.

        <expression-statement> ::= <expression>?;

    """
    def __init__(self, node: Optional[expression.Expression]):
        self.nodes = [node] if node else []
    
    def __iter__(self):
        return iter(self.nodes)
    
    def as_statement(self):
        return Statement(self)

class If:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)    

class Switch:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class SelectionStatement:
    """
        Represents a selection statement.

        <selection-statement> ::= if ( <expression> ) <statement>
                               | if ( <expression> ) <statement> else <statement>
                               | switch ( <expression> ) <statement>
    """
    def __init__(self, nodes: Union[
            Tuple[If, expression.Expression, Statement], # if (<expression>) <statement>
            Tuple[If, expression.Expression, Statement, Statement], # if ( <expression> ) <statement> else <statement>
            Tuple[Switch, expression.Expression, Statement] # switch (<expression>) <statement>
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = nodes
    
    @staticmethod
    def if_(n1: expression.Expression, n2: Statement):
        return SelectionStatement((If(), n1, n2), 1)
    
    @staticmethod
    def if_else(n1: expression.Expression, n2: Statement, n3: Statement):
        return SelectionStatement((If(), n1, n2, n3), 2)

    @staticmethod
    def switch(n1: expression.Expression, n2: Statement):
        return SelectionStatement((Switch(), n1, n2), 3)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)

class IterationStatement:
    """
        Represents an iteraton statement.

        <iteration-statement> ::= while (<expression>) <statement>
                                | do <statement> while (<expression>)
                                | for ( <expression>?; <expression>?; <expression>? ) <statement>
    """
    def __init__(self, nodes: Union[
        Tuple[expression.Expression, Statement], # while (<expression>) <statement>
        Tuple[Statement, expression.Expression], # do <statement> while <expression>
        Tuple[Optional[expression.Expression], Optional[expression.Expression], Optional[expression.Expression], Statement] # for ( <expression>; <expression>; <expression> ) <statement>
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(filter(lambda n: n is not None, nodes))
    
    @staticmethod
    def first_case(n1: expression.Expression, n2: Statement):
        """
            <iteration-statement> ::= while (<expression>) <statement>
        """
        return IterationStatement((n1, n2), 1)
    
    @staticmethod
    def second_case(n1: Statement, n2: expression.Expression):
        """
            <iteration-statement> ::= do <statement> while (<expression>)
        """
        return IterationStatement((n1, n2), 2)

    @staticmethod
    def third_case(n1: Optional[expression.Expression], n2: Optional[expression.Expression], n3: Optional[expression.Expression], n4: Statement):
        """
            <iteration-statement> ::= for ( <expression>?; <expression>?; <expression>? ) <statement>
        """
        return IterationStatement((n1, n2, n3, n4), 3)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)

class Goto:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Continue:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Break:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Return:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class JumpStatement:
    def __init__(self, nodes: Union[
            Tuple[Goto, Identifier], 
            Tuple[Continue], 
            Tuple[Break], 
            tuple[Return, expression.Expression]
        ], discr):
        self.discr = discr
        self.nodes = list(nodes)
        self.case = nodes
    
    @staticmethod
    def goto(n1: Identifier) -> JumpStatement:
        return JumpStatement((Goto(), n1), 1)
    
    @staticmethod
    def continue_() -> JumpStatement:
        return JumpStatement((Continue(),), 2)
    
    @staticmethod
    def break_() -> JumpStatement:
        return JumpStatement((Break(),), 3)

    @staticmethod
    def return_(n1: expression.Expression) -> JumpStatement:
        return JumpStatement((Return(), n1), 4)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def is_fourth_case(self):
        return self.discr == 4

    def __iter__(self):
        return iter(self.nodes)

class Statement:
    """
        <statement> ::= <labeled-statement>
              | <expression-statement>
              | <compound-statement>
              | <selection-statement>
              | <iteration-statement>
              | <jump-statement>
    """
    def __init__(self, node: Union[LabeledStatement, ExpressionStatement, SelectionStatement, IterationStatement, JumpStatement]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)

