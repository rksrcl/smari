import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.defined_vars = set()
        self.used_vars = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_vars.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)

    def analyze_code(self, code):
        self.defined_vars = set()
        self.used_vars = set()
        tree = ast.parse(code)
        self.visit(tree)
        return self.defined_vars, self.used_vars
