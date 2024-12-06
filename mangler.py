import esprima.visitor as vis

# class responsible for switching names in identifiers
class ManglerVisitor(vis.Visitor):
    def __init__(self, tokens):
        self.tokens = tokens
    
    # vist identifier and take certain actions
    def visit_Identifier(self, obj):
        print("Identifier, value: " + obj.name + " is_mangle_candidate: " + str(obj.mangle_candidate))
        if (obj.name == "i"):
            #print("value of node is equal to i, obj index: " + obj.idx)
            self.tokens[obj.idx].value = "TEST_1"
        return obj