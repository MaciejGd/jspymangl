import esprima.visitor as vis
from esprima import nodes as Node
from esprima.syntax import Syntax

class ManglingCandidates():
    def __init__(self):
        self.mangle_vars = {}
        self.mangle_funcs = {}
        self.mangle_objs = {}
    def clone(self):
        cpy_mang_cand = ManglingCandidates()
        for i in self.mangle_vars:
            cpy_mang_cand.mangle_vars[i] = self.mangle_vars[i]
        for i in self.mangle_vars:
            cpy_mang_cand.mangle_funcs[i] = self.mangle_funcs[i]
        for i in self.mangle_objs:
            cpy_mang_cand.mangle_objs[i] = self.mangle_objs[i]
        return cpy_mang_cand


class ScopeVisitor(vis.Visitor):
    def __init__(self, mangle_candidates, is_global_scope=True, is_function_scope=False):
        self.child_scopes = []
        self.ids = []
        self.mang_cand = mangle_candidates.clone() # unfortunately we need to pass as a copy in here [possible refactoring needed]
        print("Scope visitor constructor")

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
                            self.child_scopes.append(last)
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
        func_id = obj.id
        if func_id.name in self.mang_cand.mangle_funcs:
            self.mang_cand.mangle_funcs[func_id.name].append(func_id)
        else:
            self.mang_cand.mangle_funcs[func_id.name] = [func_id]

    def visit_VariableDeclarator(self, obj):
        id_name = obj.id.name
        if id_name in self.mang_cand.mangle_vars: # if it already exists in map then append
            self.mang_cand.mangle_vars[id_name].append(obj.id)
        else: # if it not exist in map then add it
            self.mang_cand.mangle_vars[id_name] = [obj.id]
        # parse init part further, do not parse id again
        yield obj.init

    # parse call expression e.x. func(nameOne, nameTwo, etc.)
    def visit_CallExpression(self, obj):
        caller_id = obj.callee
        if caller_id.name in self.mang_cand.mangle_funcs:
            self.mang_cand.mangle_funcs[caller_id.name].append(caller_id)
        return obj.arguments

    def visit_Identifier(self, obj):
        print(obj.name, end=" : ")
        print(obj.idx)
        id_name = obj.name
        if id_name in self.mang_cand.mangle_vars:
            self.mang_cand.mangle_vars[id_name].append(obj)


def ScopeVisitorTest(ast):
    mang_cand = ManglingCandidates()
    scopeVis = ScopeVisitor(mang_cand)
    scopeVis.visit(ast)
    #print(scopeVis.child_scopes)
    #print("mangle candidates variables: ")
    print(scopeVis.mang_cand.mangle_vars)
    print("function mangle candidates variables: ")
    print(scopeVis.mang_cand.mangle_funcs)
