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

def run(program,inputs=[]):
    stack = Stack()
    stack.push(*inputs)
    popmath = True
    printed = False
    loop_depth = 0
    program = parse(program)
    index = 0
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
                stack.push(eval('stack.pop() {} stack.pop()'.format(char.replace('^','**'))))
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
            printed = True
        if char == 'O':
            print(stack)
            printed = True
        if char == 'w':
            print(chr(stack.pop()))
            printed = True
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

        index += 1

    if printed:
        return

    char = stack.pop()
    if char == 0:
        char = ''
    elif char < 0:
        char = chr(abs(char))
        print(char.join(map(str, stack)))
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
