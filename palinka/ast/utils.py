from __future__ import annotations

from palinka.model.ast.statement import Statement
from palinka.model.ast.unary_expression import UnaryExpression
from palinka.model.ast.cast_expression import CastExpression
from ..model import ast
from typing import Union, Optional

def function_call_expr(function_id, *args) -> ast.PostfixExpression:
    pargs = []
    for arg in args:
        if isinstance(arg, str):
            pargs.append(id_expr(arg))
        else:
            pargs.append(arg)

    return ast.PostfixExpression.call(
        ast.PrimaryExpression.identifier(ast.Identifier(function_id)).as_(ast.PostfixExpression),
        [
            arg.as_(ast.AssignmentExpression) for arg in pargs
        ]
    )

def sizeof(n: ast.TypeName) -> ast.UnaryExpression:
    return ast.UnaryExpression.sizeof_typename(n)

def function_call_stmt(function_id, *args) -> ast.Statement:
    return ast.Statement(ast.ExpressionStatement(function_call_expr(function_id, *args).as_expression()))

def return_stmt(n) -> ast.Statement:
    if isinstance(n, str):
        n = id_expr(n)
    return ast.Statement(ast.JumpStatement.return_(n.as_expression()))

def constant_expr(constant) -> ast.PrimaryExpression:
    return ast.PrimaryExpression(ast.Constant(constant))

def id_expr(name: str) -> ast.PrimaryExpression:
    return ast.PrimaryExpression(ast.Identifier(name))

def assign_expr(lh, rh, op = '=') -> ast.AssignmentExpression:
    if isinstance(lh, str):
        lh = id_expr(lh)
    
    if isinstance(rh, str):
        rh = id_expr(rh)

    # idb = open_data_block(sys, $DataBlock:@segment.seg_name);  
    return  ast.AssignmentExpression.expr(
        lh.as_(ast.ConditionalExpression), 
        '=', 
        rh.as_(ast.AssignmentExpression))

def assign_stmt(lh, rh) -> ast.Statement:
    return ast.Statement(ast.ExpressionStatement(assign_expr(lh, rh).as_expression()))

def typename(specs: str, as_ptr: bool):
    if not isinstance(specs, list):
        specs = [specs]

    pspecs = []

    for spec in specs:
        if isinstance(spec, str):
            spec = id_expr(spec)
        
        if isinstance(spec, ast.TypeSpecifier):
            spec = spec.as_specifier_qualifier()
        
        pspecs.append(spec)
    
    return ast.TypeName.create(
        pspecs,
        ast.AbstractDeclarator.basic_ptr() if as_ptr else None
    )    

def cast_expr(type_name: ast.TypeName, n: ast.CastExpression) -> ast.CastExpression:
    if not isinstance(type_name, ast.TypeName):
        type_name = typename(type_name)
    
    return ast.CastExpression.expr(type_name, n.as_(ast.CastExpression))

def mult_expr(lh: ast.MultiplicativeExpression, rh: ast.CastExpression, op="*") -> ast.MultiplicativeExpression:
    return ast.MultiplicativeExpression.expr(lh.as_(ast.MultiplicativeExpression), ast.MultiplicativeExpressionBinop(op), rh.as_(ast.CastExpression))

def deref_expr(n: Union[str, CastExpression]) -> UnaryExpression:
    if isinstance(n, str):
        n = id_expr(n).as_(ast.CastExpression)
    else:
        n = n.as_(ast.CastExpression)

    return ast.UnaryExpression.unary(
        ast.UnaryOperator('*'), 
        n
    )

def ref_expr(n: Union[str, CastExpression]) -> UnaryExpression:
    if isinstance(n, str):
        n = id_expr(n).as_(ast.CastExpression)
    else:
        n = n.as_(ast.CastExpression)

    return ast.UnaryExpression.unary(
        ast.UnaryOperator('&'), 
        n
    )

def getitem_expr(lh: Union[str, ast.PostfixExpression], rh: Union[str, ast.Expression], arrow: bool = True) -> ast.PostfixExpression:
    """
        lh[rh]
    """
    if isinstance(lh, str):
        lh = id_expr(lh).as_(ast.PostfixExpression)
    else:
        lh = lh.as_(ast.PostfixExpression)

    if isinstance(rh, str):
        rh = id_expr(rh).as_expression()
    else:
        rh = rh.as_(ast.Expression)
    
    if arrow:
        return ast.PostfixExpression.second_case(
            lh,
            rh
        )
    
def attr_access_expr(lh: Union[str, ast.PostfixExpression], attr_id: str, arrow=True) -> ast.PostfixExpression:
    """
        lh->attr_id
    """
    if isinstance(lh, str):
        lh = id_expr(lh).as_(ast.PostfixExpression)
    else:
        lh = lh.as_(ast.PostfixExpression)

    if arrow:
        return ast.PostfixExpression.fifth_case(
            lh,
            ast.Identifier(attr_id)
        )
    else:
        return ast.PostfixExpression.fourth_case(
            lh,
            ast.Identifier(attr_id)
        )     

def func_decl(decl_specs: list[ast.DeclarationSpecifier], declarator: ast.Declarator, decls: list[ast.Declaration], stmts: ast.CompoundStatement) -> ast.FunctionDefinition:
    return ast.FunctionDefinition.create(decl_specs, declarator, decls, stmts)

def func_declarator(id: str, params: Optional[ast.ParameterList], as_ptr=False):
   return ast.Declarator.create(
        ast.Pointer.basic() if as_ptr else None,
        ast.DirectDeclarator.call(
            ast.DirectDeclarator.identifier(ast.Identifier(id)),
            # System_t* sys
            params
        )
    )

def id_declarator(id: str, as_ptr: bool = False) -> ast.Declarator:
    return ast.Declarator.create(
        ast.Pointer.basic() if as_ptr else None,
        ast.DirectDeclarator.identifier(
            ast.Identifier(id)
        )
    )

def param_decl(decl_specs: list[ast.DeclarationSpecifier], declarator: ast.Declarator) -> ast.ParameterDeclaration:
    if not isinstance(decl_specs, list):
        decl_specs = [decl_specs]
    return ast.ParameterDeclaration.create(decl_specs, declarator)

def param_list(*param_decls) -> ast.ParameterList:
    param_decls = list(param_decls)
    ls = ast.ParameterList.create(param_decls.pop(0))
    
    while param_decls:
        ls = ast.ParameterList.concat(ls, param_decls.pop(0))
    
    return ls

def struct_specifier(id: str) -> ast.StructOrUnionSpecifier:
    return ast.StructOrUnionSpecifier.struct_identifier(ast.Identifier(id))

def struct_var_decl(struct_id: str, var_id: str, as_ptr: bool) -> ast.Declaration:
    return ast.Declaration.create([  # DataBlock_t* idb;
            ast.DeclarationSpecifier.create(
                ast.TypeSpecifier.create(
                        ast.StructOrUnionSpecifier.struct_identifier(ast.Identifier(struct_id))
                    )
                )
        ], [
            ast.InitDeclarator.create(
                ast.Declarator.create(
                    ast.Pointer.basic() if as_ptr else None,
                    ast.DirectDeclarator.identifier(ast.Identifier(var_id))
                )
            )
    ])