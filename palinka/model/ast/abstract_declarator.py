from __future__ import annotations
from typing import Union, Tuple, Optional

from .pointer               import Pointer
from .parameter_list        import ParameterList
from .constant_expression   import ConstantExpression

class AbstractDeclarator:
    """
        Represents an abstract declarator.

        <abstract-declarator> ::= <pointer>
                              | <pointer> <direct-abstract-declarator>
                              | <direct-abstract-declarator>
    """
    def __init__(self, nodes: Union[
            Tuple[Pointer], 
            Tuple[Pointer, DirectAbstractDeclarator], 
            Tuple[DirectAbstractDeclarator]
        ]):

        self.nodes = list(nodes)
    
    @staticmethod
    def basic_ptr():
        nodes = (Pointer.basic(),)
        return AbstractDeclarator(nodes)

    def __iter__(self):
        return iter(self.nodes)

class DirectAbstractDeclarator:
    """
        Represents a direct abstract declarator.

        <direct-abstract-declarator> ::= ( <abstract-declarator> )
                                     | <direct-abstract-declarator>? [<constant-expression>?]
                                     | <direct-abstract-declarator>? (<parameter-list>?)
    """
    def __init__(self, nodes: Union[
            Tuple[AbstractDeclarator], 
            Tuple[Optional[DirectAbstractDeclarator], Optional[ConstantExpression]], 
            Tuple[Optional[DirectAbstractDeclarator], Optional[ParameterList]]],
            discr=None
    ):
        self.discr = discr
        self.case = nodes
        self.nodes = list(filter(lambda n: n is not None, nodes))

    @staticmethod
    def create(n1: AbstractDeclarator):
        return DirectAbstractDeclarator((n1,), None)

    @staticmethod
    def bracket(n1: Optional[DirectAbstractDeclarator], n2: Optional[ConstantExpression]):
        return DirectAbstractDeclarator((n1, n2), "bracket")

    @staticmethod
    def par(n1: Optional[DirectAbstractDeclarator], n2: Optional[ParameterList]):
        return DirectAbstractDeclarator((n1, n2), "par")

    def is_first_case(self):
        return len(self.case) == 1
    
    def is_second_case(self):
        return len(self.case) == 2 and \
            ( \
                isinstance(self.case[1], ConstantExpression) or \
                self.discr == 'bracket'
            )

    def is_third_case(self):
        return len(self.case) == 2 and \
            ( \
                isinstance(self.case[1], ParameterList) or \
                self.discr == 'par'
            )


    def __iter__(self):
        return iter(self.nodes)