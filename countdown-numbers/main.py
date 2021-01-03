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

full_set = large_set + small_set
target_min = 100
target_max = 999

# generate each solution, store in a map from solution -> equation
def traverse_possible_outcomes(index_count = 6):
    solutions = {}
    for indexes_in_use in range(2, index_count + 1):
        for c in combinations(full_set, indexes_in_use):
            possible_equations = generate_rpn_for_set(c)
            for p in possible_equations:
                try:
                    solution = solve_rpn(p)
                    if solution >= target_min and solution <= target_max and float(solution).is_integer(): 
                        if not solution in solutions:
                            solutions[solution] = {p}
                        else:
                            solutions[solution].add(p)
                except:
                    pass
    return solutions

def generate_rpn_for_set(numbers):
    number_permutations = permutations(numbers)
    operator_combinations = combinations(operators, len(numbers) - 1)
    equations = list(set(chain(*[permutations(x + y) for x in number_permutations for y in operator_combinations])))
    valid_equations = filter(is_valid_rpn, equations)
    # print (f'{list(valid_equations)} valid equations for set {numbers}')
    return valid_equations

def is_valid_rpn(tokens):
    stack_size = 0
    for token in tokens:
        if (type(token) != int):
            stack_size -= 1
        else:
            stack_size += 1
        if stack_size <= 0:
            return False
    return stack_size == 1

def solve_rpn(tokens):
    stack = []
    for token in tokens:
        if (type(token) != int):
            stack.append(operator_table[token](stack.pop(), stack.pop()))
        else:
            stack.append(token)
    return stack[0]

if __name__ == "__main__":
    numbers_used = 2 # anything larger than 3 won't run, O(((2n-1)!)^2) ?
    begin = time.time() 
    result = traverse_possible_outcomes(numbers_used)
    end = time.time()
    elapsed = end - begin
    # solutions = [strl for k,v in result.items() for l in v]
    solutions = [' '.join(map(str, l)) for k,v in result.items() for l in v]
    print(*solutions, sep='\n')
    print(f'{elapsed} seconds')
