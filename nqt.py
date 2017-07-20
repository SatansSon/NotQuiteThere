import sys
import itertools
import math

class Stack(list):
    def push(self,*values):
        for i in values:
            if isinstance(i,str):
                for c in i:
                    self.append(ord(c))
            elif isinstance(i,(int,float,bool)):
                self.append(i)
    def pop(self):
        try:
            return super().pop(-1)
        except:
            return 0

def parse(code):

    temp = comp = ''
    final = []
    nums = []
    parsed = []
    instring = incomp = False

    x = 0

    for char in code:
        
        if char == '-':
            try:
                if code[x+1].isdigit():
                    temp += char
                    continue
            except:
                pass

        if char == '.':
            try:
                if code[x+1].isdigit() and code[x-1].isdigit():
                    temp += char
                    continue
            except:
                pass

        if char.isdigit():
            temp += char
        else:			
            if temp:
                nums.append(temp)
                temp = ''
            nums.append(char)

    if temp:
        nums.append(temp)
        temp = ''

    for c in nums:
        if c == "'":
            instring = not instring
        if instring:
            temp += c*(c!="'")
        else:
            if temp:
                final.append(temp)
                temp = ''
            else:
                final.append(c)

    for char in final:
        if all(i in '1234567890-.' for i in char):
            if '.' in char:
                parsed.append(float(char))
            else:
                parsed.append(int(char))
        elif char != ' ':
            parsed.append(char)
                
    return parsed

def run(program,inputs=[]):
    stack = Stack()
    stack.push(*inputs)
    if_ = True
    popmath = True
    for char in parse(program):
        
        if not if_:
            if char == '+':
                if_ = True
            continue
        
        if isinstance(char, (int,float)):
            stack.push(char)
            continue

        if len(char) > 1:
            stack.push(char)
            continue

        if char in '-*%/^':
            if popmath:
                stack.push(eval('stack.pop() {} stack.pop()'.format(char.replace('^','**'))))
            else:
                stack.push(eval('stack[-1] {} stack[-2]'.format(char.replace('^','**'))))

        if char == 's':
            stack.sort()
        if char == 'c':
            stack.clear()
        if char == 'r':
            stack.reverse()
        if char == 'p':
            stack.pop()
        if char == '=':
            stack.push(stack.pop() == stack.pop())
        if char == 'n':
            stack.push(not stack.pop())
        if char == 'i':
            stack.push(int(stack.pop()))
        if char == 'R':
            stack.push(range(1,stack.pop()+1))
        if char == 'S':
            stack.push(sum(stack))
        if char == 'P':
            stack.push(itertools.product(stack))
        if char == '|':
            stack.push(abs(stack.pop()))
        if char == 'f':
            stack.push(math.factorial(stack.pop()))
        if char == '\\':
            stack.push(1.0 / stack.pop())
        if char == 'l':
            stack.push(len(stack))
        if char == 'o':
            print(stack.pop())
        if char == 'w':
            print(chr(stack.pop()))
        if char == 'm':
            stack.push(min(stack.pop()))
        if char == 'M':
            stack.push(max(stack.pop()))
        if char == 'x':
            popmath = True
        if char == 'X':
            popmath = False
        if char == '?':
            return

    char = stack.pop()
    if char == 0:
        char = ''
    elif char == -1:
        char = abs(stack.pop())
        if char == 0:
            char = ''
        else:
            char = chr(char)
        print(char.join(map(str, stack)))
        return
    else:
        try:
            char = chr(char)
        except:
            print(char)
            return
    print(char.join(map(chr, map(abs, stack))))

prog = sys.argv[1]
inputs = map(eval, sys.argv[2:])
if prog.endswith('.txt'):
    prog = open(prog).read()

run(prog,inputs)
