
import heapq
import itertools
import json
from functools import reduce
from json import JSONEncoder

class DefaultEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__  

class Node:
    def __init__(self, left, right, count, value):
        self.left = left
        self.right = right
        self.count = count
        self.value = value
    def __lt__(self, other):
        return self.count < other.count

def chunk_to_byte(b):
    return 1 * b[0] + 2 * b[1] + 4 * b[2] + 8 * b[3] + 16 * b[4] + 32 * b[5] + 64 * b[6] + 128 * b[7]

def byte_chunks(arr):
    for i in range(0, len(arr), 8):
        if (i + 8 > len(arr)):
            x = arr[i:len(arr)]
            x.extend([0] * (8 - (len(arr)-i)))
            yield x 
        else:
            yield arr[i:i + 8]

def encode(input_file, output_file):
    with open(input_file, encoding='utf-8') as f:
        data = f.read()
    print(f'File: {input_file}')
    print(f'File size: {len(data)}')
    
    q = []
    for i in range(256):
        count = bytes(data, 'utf-8').count(i)
        if (count):
            value = i
            n = Node(None, None, count, value)
            heapq.heappush(q, (count, n))
    while len(q) > 1:
        right = heapq.heappop(q)[1]
        left = heapq.heappop(q)[1]
        count = left.count + right.count
        heapq.heappush(q, (count, Node(left, right, count, None)))
    root = q[0][1]
    translation_list = build_character_translation(root, [])
    translation = {k:v for list_item in translation_list for (k,v) in list_item.items()}
    encoded = list(itertools.chain(*[translation.get(n) for n in bytes(data, 'utf-8')]))
    
    encoded_bytes = bytes(chunk_to_byte(b) for b in byte_chunks(encoded))
    serialisedTree = DefaultEncoder().encode(root)
    output = bytes(serialisedTree, 'utf-8') + encoded_bytes
    print(f'Encoded size: {len(output)}')
    print(f'Ratio: {len(output) / len(data)}')
    with open(output_file, 'wb') as f:
        f.write(output)

def build_character_translation(start_node, current_path=[]):
    if start_node.value is not None:
        return [{start_node.value: current_path}]
    paths = []
    if start_node.left:
        new_path = current_path[:]
        new_path.append(0)
        paths.extend(build_character_translation(start_node.left, new_path))
    if start_node.right:
        new_path = current_path[:]
        new_path.append(1)
        paths.extend(build_character_translation(start_node.right, new_path))
    return paths

def decode_data(input_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    opening = ord('{')
    closing = ord('}')
    openingCount = 0
    start = data.index(opening)
    for i in range(start, len(data)):
        val = data[i]
        if (opening == val):
            openingCount += 1
        if (closing == val):
            openingCount -= 1
        if (openingCount == 0):
            data_start = i + 1
            break
    tree_data = data[:data_start]
    encoded_data = data[data_start:]
    tree = json.loads(tree_data)
    read_bit = lambda i, bit: (encoded_data[i] >> bit) % 2
    current_node = tree
    output = ''
    for i in range(len(encoded_data)):
        bit = read_bit(i // 8, i % 8)
        if bit:
            if current_node['right']:
                current_node = current_node['right']
        else:
            if current_node['left']:
                current_node = current_node['left']
        if current_node['value']:
            output += chr(current_node['value'])
            current_node = tree
    return output

def decode(input_file, output_file):
    data = decode_data(input_file)
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(data)

if __name__ == "__main__":
    encode('./testfiles/tale.txt', 'output.bin')
    decode('output.bin', 'decoded.txt')