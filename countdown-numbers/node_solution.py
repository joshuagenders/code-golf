from itertools import permutations, combinations, chain
import time
 
large_set = (25 , 50 , 75 , 100)
small_set = (1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10)
operators = ['+', '-', '/', '*']

operator_table = {
    '+': lambda x, y: y + x,
    '-': lambda x, y: y - x, 
    '/': lambda x, y: y / x,
    '*': lambda x, y: y * x
}

full_set = large_set + small_set + operators
target_min = 100
target_max = 999
num_choices = 6
solutions = {}
class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.valence = 2 if value in operators else 0
        self.children = children

    def is_operator(self):
        return self.value in operators # valence > 0?

nodes = [Node(n) for n in full_set]
for node in nodes:
    if node.value in operators:
        node.children = nodes
    else:
        node.children.append([n for n in nodes if n != node])

def can_move(source, target, visited, stack_size, number_count, operator_count):
    if target in visited:
        return False
    # if operator and not enough operands on stack then can't move
    if stack_size + 1 - target.valence <= 0:
        return False
    if number_count > num_choices:
        return False
    if operator_count > num_choices - 1:
        return False

def all_solutions_from_node(node, visited, stack = [], number_count = 0, operator_count = 0):
    op_count = operator_count + 1 if node.is_operator() else operator_count
    num_count = number_count + 1 if not node.is_operator() else number_count
    
    if node.is_operator():
        # perform operation
        result = operator_table[node.value](stack.pop(), stack.pop())
        if result < 0 or not float(result).is_integer():
            return
        else:
            stack.push(result)

    # store result of operation(s) if only 1 item on the stack
    if (len(stack) == 1):
        key = ''.join([v.value for v in visited])
        if (key in solutions):
            # already processed this path, should at least halve the number of calculations required, as the small set includes doubles
            return
        else:
            solutions[key] = stack[0]

    for child in node.children():
        if can_move(node, child, visited, len(stack), num_count, op_count):
            all_solutions_from_node(node, visited + node, stack + node.value, num_count, op_count)
    

def traverse_possible_outcomes():
    for node in nodes:
        starting_values.append(node.value)
        all_solutions_from_node(node, [])
    print(len(solutions))
    # create nodes for each operator and set
    # movement through nodes simulates processing reverse polish notation

    # for each node, recursively move through children based on rules
    # cannot move if results in negative value
    # output solution each time stack reaches 0, as there are repeats of numbers, store in map of string(rpn) -> solution
    # cannot visit a number node you've already visited (operator nodes can be revisited and are their own children)

    

if __name__ == "__main__":
    begin = time.time() 
    result = traverse_possible_outcomes()
    end = time.time()
    elapsed = end - begin
    print(f'{elapsed} seconds')