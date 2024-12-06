import esprima.visitor as vis

# class responsible for switching names in identifiers
class ManglerVisitor(vis.NodeVisitor):
    def __init__(self, tokens):
        self.tokens = tokens
    
    # vist identifier and take certain actions
    def visit_Identifier(self, obj):
        #print("Token value " + obj.name + " | Token index: " + obj.idx)
        if (obj.name == "i"):
            #print("value of node is equal to i, obj index: " + obj.idx)
            self.tokens[obj.idx].value = "TEST_1"
        return obj