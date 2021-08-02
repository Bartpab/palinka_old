from ..model import ast

from . import abstract_declarator
from . import direct_abstract_declarator
from . import additive_expression
from . import additive_expression_binop
from . import and_expression
from . import assignment_expression
from . import assignment_expression_op
from . import constant
from . import cast_expression
from . import compound_statement
from . import conditional_expression
from . import constant_expression
from . import char
from . import declaration_specifier
from . import declaration
from . import declarator
from . import direct_declarator
from . import enum_specifier
from . import enumerator
from . import equality_expression
from . import equality_expression_binop
from . import exclusive_or_expression
from . import expression
from . import external_declaration
from . import function_definition
from . import identifier
from . import inclusive_or_expression
from . import init_declarator
from . import initializer
from . import initializer_list
from . import logical_and_expression
from . import logical_or_expression
from . import multiplicative_expression
from . import multiplicative_expression_binop
from . import parameter_declaration
from . import parameter_list
from . import pointer
from . import postfix_expression
from . import postfix_expression_binop
from . import postfix_expression_single_op
from . import primary_expression
from . import preprocessor
from . import relational_expression
from . import relational_expression_binop
from . import shift_expression
from . import shift_expression_binop
from . import specifier_qualifier
from . import statement
from . import labeled_statement
from . import expression_statement
from . import if_
from . import include
from . import switch
from . import selection_statement
from . import iteration_statement
from . import goto
from . import continue_
from . import break_
from . import return_
from . import jump_statement
from . import storage_class_specifier
from . import string
from . import struct_declaration
from . import struct_declarator
from . import struct_or_union_specifier
from . import struct
from . import sizeof
from . import union
from . import translation_unit
from . import typedef_name
from . import type_name
from . import type_qualifier
from . import type_specifier
from . import const
from . import volatile
from . import unary_expression
from . import unary_operator
from . import void

MODULE_DISPATCHER_MAP = [
    (ast.AbstractDeclarator,        abstract_declarator),
    (ast.DirectAbstractDeclarator,  direct_abstract_declarator),
    (ast.AdditiveExpression,        additive_expression),
    (ast.AdditiveExpressionBinop,   additive_expression_binop),
    (ast.AndExpression,             and_expression),
    (ast.AssignmentExpression,      assignment_expression),
    (ast.AssignmentExpressionOp,    assignment_expression_op),
    (ast.CastExpression,            cast_expression),
    (ast.CompoundStatement,         compound_statement),
    (ast.Constant,                  constant),
    (ast.ConditionalExpression,     conditional_expression),
    (ast.ConstantExpression,        constant_expression),
    (ast.Char,                      char),
    (ast.DeclarationSpecifier,      declaration_specifier),
    (ast.Declaration,               declaration),
    (ast.Declarator,                declarator),
    (ast.DirectDeclarator,          direct_declarator),
    (ast.EnumSpecifier,             enum_specifier),
    (ast.Enumerator,                enumerator),
    (ast.EqualityExpression,        equality_expression),
    (ast.EqualityExpressionBinop,   equality_expression_binop),
    (ast.ExclusiveOrExpression,     exclusive_or_expression),
    (ast.Expression,                expression),
    (ast.ExternalDeclaration,       external_declaration),
    (ast.FunctionDefinition,        function_definition),
    (ast.Identifier,                identifier),
    (ast.InclusiveOrExpression,     inclusive_or_expression),
    (ast.InitDeclarator,            init_declarator),
    (ast.Initializer,               initializer),
    (ast.InitializerList,           initializer_list),
    (ast.LogicalAndExpression,      logical_and_expression),
    (ast.LogicalOrExpression,       logical_or_expression),
    (ast.MultiplicativeExpression,  multiplicative_expression),
    (ast.MultiplicativeExpressionBinop, multiplicative_expression_binop),
    (ast.ParameterDeclaration,      parameter_declaration),
    (ast.ParameterList,             parameter_list),
    (ast.Pointer,                   pointer),
    (ast.PostfixExpression,         postfix_expression),
    (ast.PostfixExpressionBinaryOp, postfix_expression_binop),
    (ast.PostfixExpressionSingleOp, postfix_expression_single_op),
    (ast.PrimaryExpression,         primary_expression),
    (ast.Preprocessor,              preprocessor),
    (ast.RelationalExpression,      relational_expression),
    (ast.RelationalExpressionBinop, relational_expression_binop),
    (ast.ShiftExpression,           shift_expression),
    (ast.ShiftExpressionBinop,      shift_expression_binop),
    (ast.SpecifierQualifier,        specifier_qualifier),
    (ast.Statement,                 statement),
    (ast.LabeledStatement,          labeled_statement),
    (ast.ExpressionStatement,       expression_statement),
    (ast.If,                        if_),
    (ast.Include,                   include),
    (ast.Switch,                    switch),
    (ast.SelectionStatement,        selection_statement),
    (ast.IterationStatement,        iteration_statement),
    (ast.Goto,                      goto),
    (ast.Continue,                  continue_),
    (ast.Break,                     break_),
    (ast.Return,                    return_),
    (ast.JumpStatement,             jump_statement),
    (ast.StorageClassSpecifier,     storage_class_specifier),
    (ast.String,                    string),
    (ast.StructDeclaration,         struct_declaration),
    (ast.StructDeclarator,          struct_declarator),
    (ast.StructOrUnionSpecifier,    struct_or_union_specifier),
    (ast.Struct,                    struct),
    (ast.SizeOf,                    sizeof),
    (ast.Union,                     union),
    (ast.TranslationUnit,           translation_unit),
    (ast.TypedefName,               typedef_name),
    (ast.TypeName,                  type_name),
    (ast.TypeQualifier,             type_qualifier),
    (ast.TypeSpecifier,             type_specifier),
    (ast.Const,                     const),
    (ast.Volatile,                  volatile),
    (ast.UnaryExpression,           unary_expression),
    (ast.UnaryOperator,             unary_operator),
    (ast.Void,                      void)
]

def build_dispatcher_map(module_dispatcher, function: str):
    """
        Build a dispatcher map in the form of [(ast_type, module.function), ...]
    """
    dispatcher_map = []
    for k, m in module_dispatcher:
        dispatcher_map.append((k, getattr(m, function)))
    
    return dispatcher_map

COMPILER_DISPATCHER_MAP = build_dispatcher_map(MODULE_DISPATCHER_MAP, 'compile')

def build_dispatcher(dispatcher_map, fallback=None):
    """
        Build a dispatcher based on the dispatcher map
    """
    def func(node, *args, **kwargs):
        for kt, f in dispatcher_map:
            if isinstance(node, kt):
                return f(node, *args, **kwargs)

        if not fallback:
            raise Exception(f"Unknown type {node.__class__.__module__}.{node.__class__.__name__} cannot dispatch.")
        
        return fallback(node, *args, **kwargs)
        
    return func

compiler_dispatch = build_dispatcher(COMPILER_DISPATCHER_MAP)
