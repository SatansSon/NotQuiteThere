import functools
import math
import operator
import sys

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
            
        x += 1

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
        if all(i in '1234567890-.' for i in char) and char not in '-.':
            if '.' in char:
                parsed.append(float(char))
            else:
                parsed.append(int(char))
        elif char != ' ':
            parsed.append(char)
                
    return parsed

def lastNindex(string, char, N):
    if string.count(char) < N:
        return -1
    found = 0
    for i, c in enumerate(string[::-1], 1):
        if c == char:
            found += 1
        if found == N:
            return len(string) - i
    return -1

def firstNindex(string, char, N):
    if string.count(char) < N:
        return -1
    found = 0
    for i, c in enumerate(string):
        if c == char:
            found += 1
        if found == N:
            return i
    return -1

def run(program, inputs=()):
    stack = Stack()
    program = parse(program)
    popmath = True
    mapcmd = False
    printed = False
    loop_depth = 0
    index = 0
    register = 0
    
    stack.push(*inputs)
    
    while index < len(program):

        char = program[index]
        
        if isinstance(char, (int,float)):
            stack.push(char)
            index += 1
            continue

        if len(char) > 1:
            stack.push(char)
            index += 1
            continue

        if char in '-*%/^':
            if popmath:
                if mapcmd:
                    element = stack.pop()
                    for i in range(len(stack)):
                        stack[i] = eval('element {} stack[i]'.format(char.replace('^','**')))
                else:
                    stack.push(eval('stack.pop() {} stack.pop()'.format(char.replace('^','**'))))
            else:
                if mapcmd:
                    for i in range(len(stack)):
                        stack[i] = eval('stack[-1] {} stack[i]'.format(char.replace('^','**')))
                else:
                    stack.push(eval('stack[-1] {} stack[-2]'.format(char.replace('^','**'))))

        if char == '[':
            loop_depth += 1
            if not stack[-1]:
                index = lastNindex(program, ']', loop_depth)

        if char == ']':
            if stack[-1]:
                index = firstNindex(program, '[', loop_depth)
            else:
                loop_depth -= 1

        if mapcmd:
            for i in range(len(stack)):
                if char == 'n':
                    stack[i] = not stack[i]
                if char == 'i':
                    stack[i] = int(stack[i])
                if char == '|':
                    stack[i] = abs(stack[i])
                if char == 'f':
                    stack[i] = math.factorial(stack[i])
                if char == '\\':
                    stack[i] = 1.0 / stack[i]
                if char == 'I':
                    stack[i] = isinstance(stack[i], int) or stack[i].is_integer()

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
            stack.push(*range(1,stack.pop()+1))
        if char == 'y':
            stack.push(*range(stack.pop(),stack.pop()+1))
        if char == 'S':
            stack.push(sum(stack))
        if char == 'P':
            stack.push(functools.reduce(operator.mul, stack))
        if char == '|':
            stack.push(abs(stack.pop()))
        if char == 'f':
            stack.push(math.factorial(stack.pop()))
        if char == '\\':
            stack.push(1.0 / stack.pop())
        if char == 'l':
            stack.push(len(stack))
        if char == 'o':
            print(end=str(stack.pop()))
            printed = True
        if char == 'O':
            print(stack)
            printed = True
        if char == 'w':
            print(end=chr(stack.pop()))
            printed = True
        if char == 'm':
            stack.push(min(stack.pop()))
        if char == 'M':
            stack.push(max(stack.pop()))
        if char == 'x':
            popmath = not popmath
        if char == 'X':
            mapcmd = not mapcmd
        if char == '?':
            return
        if char == ':':
            stack.push(stack[-1])
        if char == 'I':
            stack.push(isinstance(stack.pop(), int) or stack[i].is_integer())
        if char == 'Z':
            register = stack.pop()
        if char == 'z':
            stack.push(register)

        index += 1

    if printed:
        return

    char = stack.pop()
    if char == 0:
        char == ''
    elif char < -1:
        char = chr(abs(char))
        print(char.join(map(str, stack[::-1])))
        return
    else:
        try:
            char = chr(char)
        except:
            print(char)
            return
    print(char.join(map(chr, map(abs, stack))))
    
if __name__ == '__main__':
    prog = sys.argv[1]
    inputs = list(map(eval, sys.stdin.read().splitlines()))
    run(prog, inputs)
