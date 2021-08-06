from pycparser.c_generator import CGenerator as BaseCGenerator

import palinka.model.ast as ast 

class CGenerator(BaseCGenerator):
    def visit_Plant(self, node: ast.Plant):
        return "\n".join([self.visit(file) for file in node.files] + [self.visit(sys) for sys in node.systems])

    def visit_System(self, node: ast.System):
        return "\n".join([self.visit(file) for file in node.files])

    def visit_File(self, node: ast.File):
        include_str = "\n".join([self.visit(incl) for incl in node.includes])

        if len(include_str) > 0:
            include_str += "\n\n"
        
        translation_unit_str = self.visit(node.translation_unit)

        return """%s\n%s%s\n%s""" % ("/// BEGIN FILE %s ///" % node.id, include_str, translation_unit_str, "/// END FILE ///")

    def visit_Include(self, node: ast.Include):
        if node.is_global:
            return "#include <%s>" % node.id
        else:
            return "#include \"%s\"" % node.id