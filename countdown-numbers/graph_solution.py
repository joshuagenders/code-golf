
# Rules of the countdown numbers game:
# ------------------------------------
# * Six, face-down, numbered tiles are selected from twenty-four shuffled tiles.
# * The tiles are arranged into two groups: Large Numbers and Small Numbers.
# * There are four numbers in the large set { 25 , 50 , 75 , 100 }
# * There are twenty numbers in the small set, two each of the numbers 1-10
# * { 1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10 }
# * One contestant selects as many numbers as desired (unseen) from the large set (between none and all four), and the balance are pulled from the small set to make six numbers in total.
# * A random three-digit target number is then chosen by a computer*.
# * The contestants are given 30 seconds to get as close as possible to the chosen target by using just the four basic arithmetic operators + - × ÷
# * Not all the digits need to be used.
# * Concatenation of the digits is not allowed (You can’t use a “2” and “2” to make “22”).
# * At no intermediate step in the process can the current running total become negative or involve a fraction.
# * Each numbered tile can only be used once in the calculation.
# * 10 points are awarded for correctly getting the exact solution.
# * 7 points are awarded for getting within 5 of the required solution.
# * 5 points are awarded for getting within 10 points of the required solution.
# * There is some speculation as to whether 100 is a possible target number generated by the computer. Some say that only numbers range 101-999 are generated (which are the rules in the French variant), and other say that any three digit numbers is possible.

# TODO
# at depth 5, don't bother moving to 6 if there's no way 6 results in 100-999 (too large etc.)
import time

large_set = (25 , 50 , 75 , 100)
small_set = (1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10)
operators = ('+', '-', '/', '*')

operator_table = {
    '+': lambda x, y: y + x,
    '-': lambda x, y: y - x, 
    '/': lambda x, y: y / x,
    '*': lambda x, y: y * x
}

full_set = large_set + small_set + operators
target_min = 100
target_max = 999
num_choices = 4
equation_length = num_choices * 2 - 1
solutions = {}

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children
        self.is_operator = self.value in operators

    def __str__(self):
        return f'{self.value}'


nodes = [Node(n) for n in full_set]
for node in nodes:
    if node.is_operator:
        # can move from an operator to any node including self
        node.children = nodes
    elif node.value == 1:
        # don't include useless relationships like 1->/ and 1->* (divide/multiply by 1)
        node.children = [n for n in nodes if n != node and n.value not in ['/', '*']]
    else:
        # can move from a number to any node but itself
        node.children = [n for n in nodes if n != node]


def can_move(source, target, visited, stack_size, number_count, operator_count):
    if target.is_operator:
        # if operator and not enough operands on stack then can't move
        if stack_size - 1 <= 0:
            # print('not enough operands')
            return False
        if operator_count + 1 > num_choices - 1:
            # print('op lim')
            return False
    else:
        if target in visited:
            # print('target in visited')
            return False
        if number_count + 1 > num_choices:
            # print('num lim')
            return False
    
    return True

def all_solutions_from_node(node, visited, stack = [], number_count = 0, operator_count = 0):
    op_count = operator_count + 1 if node.is_operator else operator_count
    num_count = number_count + 1 if not node.is_operator else number_count
    now_visited = visited + [node]
    # print(node)
    key = ' '.join([str(v.value) for v in now_visited])
    new_stack = stack[::]

    if node.is_operator:
        if len(new_stack) < 2:
            # not enough operands
            return
        # perform operation
        try:
            result = operator_table[node.value](new_stack.pop(), new_stack.pop())
            if result < 0 or not float(result).is_integer():
                return
            else:
                new_stack.append(result)
        except:
            return
    else:
        new_stack.append(node.value)

    # store result of operation(s) if only 1 item on the stack
    if len(new_stack) == 1:
        # key = ''.join([str(v.value) for v in now_visited])
        # print(key)
        if key in solutions:
            # print('processed this path')
            return
        else:
            solution = new_stack[0]
            if (solution > target_min and solution < target_max):
                # print(f'found solution {key} = {new_stack[0]}')
                solutions[key] = solution
    if len(visited) < equation_length:
        for child in node.children:
            # print(f'prospective child: {child}')
            if can_move(node, child, visited + [node], len(new_stack), num_count, op_count):
                # print('can move')
                all_solutions_from_node(child, now_visited, new_stack, num_count, op_count)


def traverse_possible_outcomes():
    viewed_starting_values = []
    for node in nodes:
        if node.value in viewed_starting_values:
            continue
        # print(f'calculating all equations starting with {node}')
        viewed_starting_values.append(node.value)
        begin = time.time() 
        all_solutions_from_node(node, [])
        end = time.time()
        elapsed = end - begin
        # print(f'{node}: {elapsed} seconds')
        
if __name__ == "__main__":
    begin = time.time() 
    result = traverse_possible_outcomes()
    end = time.time()
    elapsed = end - begin

    # print(*solutions, sep='\n')
    print(f'{elapsed} seconds')
    solution_count = sum([1 for s in solutions])
    print(f'found {solution_count} solutions')
