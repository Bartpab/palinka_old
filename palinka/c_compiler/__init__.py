from palinka.model.ast.translation_unit import TranslationUnit
from . import automation
from .dispatch import compiler_dispatch
import palinka.model.ast as ast

def compile(root: ast.TranslationUnit) -> str:
    """
        Compile the translation unit
    """
    return compiler_dispatch(root, dispatcher=compiler_dispatch)