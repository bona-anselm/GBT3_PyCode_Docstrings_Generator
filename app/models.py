import ast


class ExtractFunctionNames(ast.NodeVisitor):
    """AST visitor to extract function names from the code."""
    def __init__(self):
        self.function_names = []
    
    def visit_FunctionDef(self, node):
        """Visit FunctionDef nodes and extract the function name."""
        self.function_names.append(node.name)
    

class ExtractClassNames(ast.NodeVisitor):
    """AST visitor to extract class names from the code."""
    def __init__(self):
        self.class_names = []
    
    def visit_ClassDef(self, node):
        """Visit ClassDef nodes and extract the class name."""
        self.class_names.append(node.name)
