import esprima.visitor as vis
from esprima import nodes as Node
from esprima.syntax import Syntax

class ScopeVisitor(vis.Visitor):
    def __init__(self, mangle_candidates, is_global_scope=True, is_function_scope=False):
        self.child_scopes = []
        self.ids = []
        self.mang_cand = {} # unfortunately we need to pass as a copy in here [possible refactoring needed]
        self.copy_mangle_candidates(mangle_candidates)
        print("Scope visitor constructor")

    def copy_mangle_candidates(self, mangle_candidates):
        for i in mangle_candidates:
            self.mang_cand[i] = mangle_candidates[i]

        # create instance of object if it does not already exists
    def force_push_mangle(self, obj):
        if getattr(obj, "name", None) == None:
            print("Error during pushing mangle candidate in obj")
            print(obj)
            return 
        if obj.name in self.mang_cand:
            self.mang_cand[obj.name].append(obj)
        else:
            self.mang_cand[obj.name] = [obj]
    # push object to list if its instance already exists
    def push_mangle(self, obj):
        if getattr(obj, "name", None) == None:
            print("Error in visiting node: ")
            print(obj)
            return
        if obj.name in self.mang_cand:
            self.mang_cand[obj.name].append(obj)


    def visit(self, obj):
        """we override this function as we do not want to enter inner scopes, and first just parse global scope"""
        if not hasattr(self, 'visitors'):
            self._visit_context = {}
            self._visit_count = 0
        try:
            self._visit_count += 1
            stack = vis.deque()
            stack.append((obj, None))
            last_result = None
            while stack:
                try:
                    last, visited = stack[-1]
                    if isinstance(last, vis.types.GeneratorType):
                        stack.append((last.send(last_result), None))
                        last_result = None
                    elif isinstance(last, vis.Visited):
                        stack.pop()
                        last_result = last.result
                    elif isinstance(last, vis.Object):
                        if last in self._visit_context:
                            if self._visit_context[last] == self.visit_Object:
                                visitor = self.visit_RecursionError
                            else:
                                visitor = self.visit_Object
                        else:
                            method = 'visit_' + last.__class__.__name__
                            visitor = getattr(self, method, self.visit_Object)
                        self._visit_context[last] = visitor
                        stack.pop()
                        if (isinstance(last, Node.FunctionDeclaration)): # do not add function declaration to a stack as we will parse it later
                            self.handleFunctionDeclaration(last)
                            self.child_scopes.append(last.body)
                        elif isinstance(last, Node.FunctionExpression):
                            self.child_scopes.append(last.body)
                        else: # here append new scopes symbols
                            stack.append((visitor(last), last))
                    else:
                        method = 'visit_' + last.__class__.__name__
                        visitor = getattr(self, method, self.visit_Generic)
                        stack.pop()
                        stack.append((visitor(last), None))
                except StopIteration:
                    stack.pop()
                    if visited and visited in self._visit_context:
                        del self._visit_context[visited]
            return last_result
        finally:
            self._visit_count -= 1
            if self._visit_count <= 0:
                self._visit_context = {}
    
    # add function id to scope mangle but do not parse it yet
    def handleFunctionDeclaration(self, obj):
        self.force_push_mangle(obj.id)

    def visit_VariableDeclarator(self, obj):
        self.force_push_mangle(obj.id)
        # parse init part further, do not parse id again
        yield obj.init

    # parse call expression e.x. func(nameOne, nameTwo, etc.)
    def visit_CallExpression(self, obj):
        caller_id = obj.callee
        if (obj.callee.type == "MemberExpression"):
            return vis.Visited(obj) # skip mangling object members for now
        self.push_mangle(obj.callee)
        return obj.arguments

    def visit_Identifier(self, obj):
        self.push_mangle(obj)


        



def ScopeVisitorTest(ast):
    mang_cand = {}
    scopeVis = ScopeVisitor(mang_cand)
    scopeVis.visit(ast)
    #print(scopeVis.child_scopes)
    print("mangle candidates: ")
    idx = 0
    for i in scopeVis.child_scopes:
        new_scopeVis = ScopeVisitor(scopeVis.mang_cand)
        new_scopeVis.visit(i)
        print("NEW INNER AST: ", idx)
        print(new_scopeVis.mang_cand)
        idx+=1
    #print(scopeVis.mang_cand)
    
