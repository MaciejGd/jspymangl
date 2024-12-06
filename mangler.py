import esprima.visitor as vis

# class responsible for switching names in identifiers
class ManglerVisitor(vis.NodeVisitor):
    def __init__(self, tokens):
        self.tokens = tokens
    
    # vist identifier and take certain actions
    def visit_Identifier(obj):
        print(obj.name)
        return obj