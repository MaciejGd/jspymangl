from words_test import words_list

CHARS='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class NameMangler():
    def __init__(self):
        self.index_stack = [-1]
        self.length = 0
        self.skip_name = []

    def generate_mangle(self):
        i = self.length
        while (self.index_stack[i] == len(CHARS)-1):
            self.index_stack[i] = 0
            i-=1
        # if we want out of stack we need to add another letter
        if i == -1:
            self.index_stack.append(0)
            self.length+=1
        else:
            self.index_stack[i]+=1
        result=""
        for el in self.index_stack:
            result += CHARS[el]
        return result

    def save_state(self):
        return "".join(str(x)+'.' for x in self.index_stack)
    
    def restore_state(self, save):
        self.index_stack.clear()
        self.length = -1
        current_num=""
        for i in save:
            if i == '.':
                self.index_stack.append(int(current_num))
                current_num=""
                self.length += 1
                continue
            current_num+=i



"""mangle test set on set consisting of ~10k words"""
def test_on_big_set():
    mangler = NameMangler()
    for i in words_list:
        line_len = 25
        padding = line_len - len(i)
        print("og_word: " + i, end="")
        print(padding * " ", end="")
        print("magled: " + mangler.generate_mangle())

"""for such data set only 3 letters for mangled name has been used!!!"""

"""we want to skip mangling if mangled name is keyword or original id"""
def test_on_skipping(skip_set):
    mangler = NameMangler()
    input_set = ["werowero", "peorwoepr", "qweqsdw", "peroweer"]
    mangler.restore_state("0.3.")
    for i in input_set:
        mangle = mangler.generate_mangle()
        while mangle in skip_set: # use set in here for fast lookups
            mangle = mangler.generate_mangle()
        print(mangle)

#test_on_big_set()
skip_set = {"aaa", "b", "d"}
test_on_skipping(skip_set)