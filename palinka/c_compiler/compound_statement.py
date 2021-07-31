from typing import Text
from ..model import ast
from ..utils import TextBuilder as TB

def compile(node: ast.CastExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    tb = TB()
    tb.add("{")
    tb.push(" " * 4)
    tb.add("\n".join([dispatch(cnode, *args, **kwargs) for cnode in node]))
    tb.pop()
    tb.add("}")

    return str(tb)