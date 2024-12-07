# -*- coding: utf-8 -*-
# Copyright JS Foundation and other contributors, https://js.foundation/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import esprima.esprima as _es
import sys
from mangler import ManglerVisitor as mangVis
from scope import ScopeVisitorTest as scpVisTest

# load input file 
def load(input_file):
    return open(input_file, "r").read()

# save output to a file 
def save(output_file, file_content):
    with open(output_file, "w") as fp:
        fp.write(file_content)

# wrapper to the mangler
class ManglerWrapper():
    def __init__(self, input_file):
        self.input_file = input_file
        self.js_code = load(input_file)
        self.ast = _es.parse(self.js_code)
        self.tokens = _es.tokenize(self.js_code)
        self.visitor = mangVis(self.tokens)
        self.output_file = self.prepareOutputFile()

    ### DEBUG PRINT
    def printAst(self):
        print("abstract syntax tree")
        print(self.ast)
    
    def printTokens(self):
        print("tokenized data")
        print(self.tokens)

    ### OUTPUT FILE
    # prepare output filename
    def prepareOutputFile(self):
        file_no_ext=self.input_file[0:len(self.input_file)-3]
        return file_no_ext + ".out.js"
    # combine file from tokens array
    def combineFile(self):
        output_file=""
        for i in self.tokens:
            output_file += " "
            output_file += i.value
        print("output content:")
        print(output_file)
        return output_file
    
    # save combined array to file
    def createOutputFile(self):
        file_content = self.combineFile()
        save(self.output_file, file_content)

    ### MANGLING
    def runVisitor(self):
        self.visitor.visit(self.ast)

# first check how combined file look alike, then run visitor and check again
def indexTest(mangler):
    print("COMBINING OG FILE")
    mangler.combineFile()
    mangler.runVisitor()
    print("COMBINING VISITED FILE")
    mangler.combineFile()
    mangler.createOutputFile()

def main():
    # handle input
    file_name=""
    sys.argv.pop(0)
    if len(sys.argv) == 0:
        file_name="./js_test/scope_test/test1.js"
    else:
        file_name=load(sys.argv[0])
    # create wrapper instance
    mangler = ManglerWrapper(file_name)
    scpVisTest(mangler.ast)
    #print("PRINTING TOKENS")
    #mangler.printAst()
    #mangler.printTokens()
    #mangler.runVisitor()
    
    

if __name__=="__main__":
    main()