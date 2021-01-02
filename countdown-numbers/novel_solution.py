import time

large_set = (25 , 50 , 75 , 100)
small_set = (1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10)
unique_set = (25 , 50 , 75 , 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

target_min = 100
target_max = 999
num_choices = 4 # 5 

nodes = {}

OPERATORS = set(['+', '-', '*', '/', '(', ')'])  # set of operators
PRIORITY = {'+':1, '-':1, '*':2, '/':2} # dictionary having priorities 

def infix_to_postfix(expression): #input expression
    stack = [] # initially stack empty
    output = '' # initially output empty

    for ch in expression:
        if ch not in OPERATORS:  # if an operand then put it directly in postfix expression
            output+= ch
        elif ch=='(':  # else operators should be put in stack
            stack.append('(')
        elif ch==')':
            while stack and stack[-1]!= '(':
                output+=stack.pop()
            stack.pop()
        else:
            # lesser priority can't be on top on higher or equal priority    
             # so pop and put in output   
            while stack and stack[-1]!='(' and PRIORITY[ch]<=PRIORITY[stack[-1]]:
                output+=stack.pop()
            stack.append(ch)

    while stack:
        output+=stack.pop()
    return output

def get_or_create_node(number):
    if number not in nodes:
        # print (f'creating node for {number}')
        nodes[number] = Node(number)
    return nodes[number]

class Equation:
    def __init__(self, operations = []):
        self.operations = operations

    def __eq__(self, other):
        if len(self.operations) != len(other.operations):
            return False
        for op in range(len(self.operations)):
            if self.operations[op][0] != other.operations[op][0]:
                return False
            if self.operations[op][1] != other.operations[op][1]:
                return False
        return True

    def append(self, op):
        self.operations.append(op)

    def __str__(self):
        output = ''
        for op, n in self.operations:
            if output == '':
                output = f'{n}'
                continue
            if op == '*' or op =='/':
                output = f'({output})'
            output += f' {op} {n}'
        return output

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.operations)

class Node:
    def __init__(self, number):
        self.number = number
        self.equations = set()

    def __str__(self):
        output = f'target number: {self.number} \n'
        for eq in self.equations:
            output += f'{eq}\n'
            # output += f'{eq}\n'
        return output

    def operate_with_all(self):
        if self.number == 0:
            return
        results = []
        for x in unique_set:
            results.append((self.number + x, ('+', x)))
            results.append((self.number - x, ('-', x)))
            if x != 1 and x != 0:
                results.append((self.number / x, ('/', x)))
                results.append((self.number * x, ('*', x)))
        valid_results = [result for result in results if float(result[0]).is_integer() and result[0] > 0]

        # print(f'valid results {valid_results}')
        # # all of this nodes equations, combined with the equations to the new nodes
        for result in valid_results:
            node = get_or_create_node(result[0])
            # print(f'target: {result[0]}')
            for equation in self.equations:
                # print(f'equation: {equation}')
                if len(equation) >= num_choices:
                    continue
                new_number = result[1][1]
                count = sum(1 for x in equation.operations if x[1] == new_number)
                new_equation = Equation(equation.operations[::])
                new_equation.append(result[1])

                # print(f'new_number {new_number}')
                if new_number in large_set and count < 2:
                    node.equations.add(new_equation)
                    # print(f'{self.number}->{node.number},{result[0]},{new_equation}')
                    # print(f'{new_equation}')
                if new_number in small_set and count == 0:
                    node.equations.add(new_equation)
                    # print(f'{new_equation}')
                    # print(f'{self.number}->{node.number},{result[0]},{new_equation}')

            # break

def print_results():
    result_nodes = [ node for k,node in nodes.items() if node.number >= target_min and node.number <= target_max and len(node.equations) > 0]
    # print(*result_nodes)
    # todo: group by length and print count
    total = 0
    for n in result_nodes:

        x = len(n.equations)
        print(f'{n.number}: {x}')
        total += len(n.equations)
    print(total)

if __name__ == '__main__':
    begin = time.time() 
    initial_nodes = [Node(node) for node in unique_set]

    # initial nodes should contain a single equation, + n
    for node in initial_nodes:
        node.equations.add(Equation([('+', node.number)]))
        nodes[node.number] = node

    rounds = num_choices
    for r in range(1, rounds):
        # take a copy of the list as it will be modified
        print(f'Processing round {r}')
        n = dict(nodes)
        for k,node in n.items():
            node.operate_with_all()
        print_results()

    # final round nodes
    # print(f'Processing round {rounds}')
    # result_nodes = [ node for k,node in nodes.items() if node.number >= target_min and node.number <= target_max ]
    # for result in result_nodes:
    #     result.operate_with_all()
    end = time.time()
    
    print_results()    
    print('done')

    elapsed = end - begin
    print(f'{elapsed} seconds')

# todo validator
# 1 digit  has 4 combinations          4
# 2 digits has 36 combinations         40
# 3 digits has 420 combinations        460
# 4 digits has 6564 combinations       7024
# 5 digits has 129444 combinations     136468
# 6 digits has 3078564 combinations    3215032





