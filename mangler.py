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
    
    def visit_FunctionDeclaration(self, obj):
        keys = obj.__dir__()
        values = obj.items()
        for i, j in zip(keys,values):
            print("next_item")
            print("Key " + i)
            print("value: ")
            print(j)
        # we can use such behaviour to properly visit every scope and add mangling accordingly