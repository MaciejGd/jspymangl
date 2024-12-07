import esprima.visitor as vis
from esprima import nodes as Node
from esprima.syntax import Syntax

class ScopeVisitor(vis.Visitor):
    def __init__(self, is_global_scope=True, is_function_scope=False):
        self.child_scopes = []
        self.ids = []
        self.mangle_vars = {}
        self.mangle_funcs = {}
        print("Scope visitor constructor")
    
    #def init_visit(self, obj): # function will vary depending on type of scope


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
                            print("In function instance")
                            self.HandleFunctionDeclaration(last)
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
    def HandleFunctionDeclaration(self, obj):
        func_id = obj.id
        if func_id.name in self.mangle_funcs:
            self.mangle_funcs.append(func_id)
        else:
            self.mangle_funcs[func_id.name] = [func_id]

    def visit_VariableDeclarator(self, obj):
        print("in variable declarator visitor")
        id_name = obj.id.name
        if id_name in self.mangle_vars: # if it already exists in map then append
            self.mangle_vars[id_name].append(obj.id)
        else: # if it not exist in map then add it
            self.mangle_vars[id_name] = [obj.id]
        # parse init part further, do not parse id again
        yield obj.init

    def handleVariableDeclarator(self, obj):
        print("in variable declarator visitor")
        id_name = obj.id.name
        if id_name in self.mangle_vars: # if it already exists in map then append
            self.mangle_vars[id_name].append(obj.id)
        else: # if it not exist in map then add it
            self.mangle_vars[id_name] = [obj.id]
        # also if we can mangle the identifier after assignement operator we should also do it
        # handle var num = num1;
        # if obj.init.type == "Identifier":
        #     if obj.init.name in self.mangle_vars:
        #         self.mangle_vars[obj.init.name].append(obj.init)
        # # handle var num = func2(num1, num2, num3);
        # if obj.init.type == "CallExpression":

    def visit_Identifier(self, obj):
        print("in identifier: ")
        print(obj.name)
        id_name = obj.name
        if id_name in self.mangle_vars:
            self.mangle_vars[id_name].append(obj)


def ScopeVisitorTest(ast):
    scopeVis = ScopeVisitor()
    print(ast)
    scopeVis.visit(ast)
    #print(scopeVis.child_scopes)
    print("mangle candidates variables: ")
    print(scopeVis.mangle_vars)
    print("function mangle candidates variables: ")
    print(scopeVis.mangle_funcs)
