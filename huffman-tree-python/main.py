
import heapq, json
import itertools

def lz(data):
    d = {chr(i):i for i in range(255)}
    output = []
    byte_data = bytes(data, 'utf-8')
    counter = 256
    current_window = 1
    for i in range(0, len(byte_data), current_window):
        current = byte_data[i:i + current_window]
        nxt = current = byte_data[i:i + current_window + 1]
        if (nxt in d):
            output.append(d[nxt] % 255)
            output.append(d[nxt] & 0x000000FF)
        else:
            d[nxt] = counter
            counter += 1
            output.append(current[0])
            output.append(0)
    return output

class Node:
    def __init__(self, left, right, count, value):
        self.left = left
        self.right = right
        self.count = count
        self.value = value
    def __lt__(self, other):
        return self.count < other.count
    # def __str__(self):
    #     return (f'Node: {self.value} count {self.count} \n  left: {self.left is not None}\n right: {self.right is not None}\n')

def encode(input_file, output_file):
    data = open(input_file, encoding='utf-8').read()
    print(f'File: {input_file}')
    print(f'File size: {len(data)}')
    zipped = lz(data)
    print(f'Zipped size: {len(zipped)}')
    print(zipped)
    q = []
    for i in range(256):
        count = bytes(zipped).count(i)
        if (count):
            value = i
            n = Node(None, None, count, value)
            heapq.heappush(q, (count, n))
    while len(q) > 1:
        right = heapq.heappop(q)[1]
        left = heapq.heappop(q)[1]
        count = left.count + right.count
        heapq.heappush(q, (count, Node(left, right, count, None)))
    translation_list = build_character_translation(q[0][1], [])
    translation = {k:v for list_item in translation_list for (k,v) in list_item.items()}
    encoded = list(itertools.chain(*[translation.get(n) for n in zipped]))
    print(*encoded)

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

def decode(input_file, output_file):
    pass

if __name__ == "__main__":
    encode('./testfiles/test.txt', 'output.bin')
    decode('output.bin', 'decoded.txt')