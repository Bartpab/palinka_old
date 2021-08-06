from palinka.model.ast import plant
from pycparser.c_ast import FileAST
import palinka.model.automation as model
import palinka.model.ast as ast


class CParser:
    """
        \brief Parser of the Plant Model
        \return The related AST
    """
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)
    
    def generic_visit(self, node):
        if node is None:
            return None

    def visit_Plant(self, node: model.Plant) -> ast.Plant:
        plant_memory_size = sum([sys.memory_size for sys in node.get_systems()])
        return ast.Plant(
            [
                ast.File("plant.h", 
                    [
                        ast.Include("stddef.h", True)
                    ], 
                    ast.FileAST([
                        # Plant Memory Size
                        ast.Decl(None, None, None, None, ast.TypeDecl("PLANT_MEMORY", ["const"], ast.ID("size_t")), ast.Constant("size_t", str(plant_memory_size)), None)
                    ])
                )
            ], [
                
            ]
        )
