# max number for 6 is 100 * 75 * 50 * 25 = 9,375,000
# largest number you can get to and still divide/minus to get to the answer is 999 * 100 = 99900
# any even number / odd number results in decimal
# any odd number / even number results in decimal

# calculate the result of every 'single' operation on numbers up to 64800. +/-* for 1-10, 25, 50, 75, 100
# 1+100, 1+75, 
# essentially creating a graph between numbers where the operation with another number is the edge
# find single ways to get to numbers from numbers within valid space
# all valid operations are some combination of these single operations

# so once you combine all the ways to get to a number from a number with a single operation, you can then use the results as indexes in a map
# i.e. if you can get to number x, here are all the valid numbers you could have come from, and all the valid ones you could go to
# then traverse from each node finding all <=6 length chains resulting in numbers between 100 and 999
# certain shortcuts can be made, i.e. once chain is length 5,  numbers over 9990 cannot result in an answer
# any valid answer at chain
# 1: {
#     2: '- 1',
#     1: '* 1',
#     10: '/ 10'
#     # would have 2-11 -
# }
# take each number, create a node
# take each node, combine with each possble operation + number (small +big set with each operator = 56 operations)
#   get or create node as a result
#   add the operation to the node, (could we optimise by adding the reverse operation?)
# do not create nodes for invalid operations, e.g. negative, non-integer,
# repeat for total of 6 times
# ...
# two ways to maybe combine:
# the last round is looping through 1-999, and performing the same loop, except now instead of adding to the node's paths, we combine that operation with every path in that node, and output
# loop through all nodes from 1-999 and construct valid 6 length paths

large_set = (25 , 50 , 75 , 100)
small_set = (1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10)
unique_set = (25 , 50 , 75 , 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
operators = ('+', '-', '/', '*')

target_min = 100
target_max = 999
num_choices = 3 # 6


operator_table = {
    '+': lambda x, y: y + x,
    '-': lambda x, y: y - x, 
    '/': lambda x, y: y / x,
    '*': lambda x, y: y * x
}

nodes = {}

def get_or_create_node(number):
    if number not in nodes:
        print (f'creating node for {number}')
        nodes[number] = Node(number)
    return nodes[number]

### a sequence of operations
## the operator and number at each step
# class Equation:
#     def __init__(self, current_value, operations = []):
#         # [[number, operation]]
#         self.operations = operations
#         self.initial_value = current_value
#         self.current_value = current_value

#     def append(self, operation, number):
#         new_value = operator_table[operation](number, self.current_value)
#         if not float(new_value).is_integer() or new_value < 0:
#             return False
#         # ensure doesn't include more than one of large set, or two of small set
#         count = sum([o for o in self.operations if o[0] == number])
#         if number in large_set and count < 2:
#             return Equation(new_value, [self.operations, [number, operation]])
#         elif number in small and count == 0:
#             return Equation(new_value, [self.operations, [number, operation]])
#         return False

class Node:
    def __init__(self, number):
        self.number = number
        self.equations = []

    def __str__(self):
        return f'{self.number} : {self.equations}'
    def operate_with_all(self):
        if self.number == 0:
            return
        # combinations = []
        # for num in unique_set:
        #     for op in operators:
        #         combinations.append([op, num])
        
        # for equation in self.equations:
        #     pass


        # perform operations with number
        # store valid equations 
        results = []
        for x in unique_set:
            # result, operator, 
            results.append((x + self.number, ('+', x)))
            results.append((x - self.number, ('-', x)))
            if x != 1 and x != 0:
                results.append((x / self.number, ('/', x)))
                results.append((x * self.number, ('*', x)))
        valid_results = [result for result in results if float(result[0]).is_integer() and result[0] >= 0]

        # print(f'valid results {valid_results}')
        # # all of this nodes equations, combined with the equations to the new nodes
        for result in valid_results:
            node = get_or_create_node(result[0])
            for equation in self.equations:
                # print(f'equation: {equation}')
                if len(equation) > num_choices - 1:
                    continue
                new_number = result[1][1]
                count = sum(1 for x in equation if x[1] == new_number)
                new_equation = equation[::]
                new_equation.append(result[1])

                if new_number in large_set and count < 2:
                    node.equations.append(new_equation)
                    # print(f'{self.number},{result[0]},{new_equation}')
                if new_number in small_set and count == 0:
                    new_equation.append(result[1])
                    node.equations.append(new_equation)
                    # print(f'{self.number},{result[0]},{new_equation}')

            # break

if __name__ == '__main__':
    initial_nodes = [Node(node) for node in unique_set]
#
    # initial nodes should contain a single equation, + n
    for node in initial_nodes:
        node.equations = [[('+', node.number)]]
        nodes[node.number] = node

    rounds = num_choices
    for r in range(rounds - 1):
        # take a copy of the list as it will be modified
        n = dict(nodes)
        for k,node in n.items():
            node.operate_with_all()
        # break    

    # final round nodes
    result_nodes = [ node for k,node in nodes.items() if node.number >= target_min and node.number <= target_max ]
    for result in result_nodes:
        result.operate_with_all()

    results = [ result for sublist in result_nodes for sublist in result.equations ]
    # [item for sublist in regular_list for item in sublist]
    print(*results)
    print('done')






