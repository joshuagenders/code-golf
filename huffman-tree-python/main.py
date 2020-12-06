
import heapq
import json
import itertools
from functools import reduce

def lz(data):
    d = {i:chr(i) for i in range(255)}
    output = []
    int_data = [int(b) for b in bytes(data, 'utf-8')]
    counter = 256
    current_window = 1
    
    for i in range(0, len(int_data), current_window):
        current = chr(int_data[i:i + current_window][0])
        x = list(map(chr, int_data[i:i + current_window + 1]))
        nxt = ''.join([current] + x)
        if (nxt in d.values()):
            for k, v in d.items():
                if v == nxt:
                    output.append((int(k) & 0x0000FF00) >> 8)
                    output.append(int(k) & 0x000000FF)
                    break
        else:
            d[counter] = nxt
            counter += 1
            output.append(ord(current))
            output.append(0)

    byte_output = []
    half_remaining = False
    for i in range(len(output)):
        is_dict_bits = i % 2 == 1
        if not half_remaining:
            if is_dict_bits:
                byte_output.append(output[i] << 4 & 0x00000010)
                half_remaining = True
            else:
                byte_output.append(output[i])
        else:
            if is_dict_bits:
                byte_output[-1:] = [byte_output[-1:][0] ^ output[i]]
                half_remaining = False
            else:
                byte_output[-1:] = [byte_output[-1:][0] ^ (output[i] >> 4)]
                byte_output.append((output[i] << 4) & 0x00000010)
                half_remaining = True
    # print(byte_output)
    return bytes(byte_output)

def unlz(data):
    # construct d (table) - lookups for 0-255
    # for int in byte pairs
    #   if val in table
    #     add to table
    #   perform lookup
    #   write output

    pass

def decode_data():
    # parse tree from file
    # parse data into byte array
    # unzip byte array
    pass

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
    zipped = lz(data)
    # print(zipped)

    print(f'Zipped size: {len(zipped)}')
    # print(zipped)
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
    root = q[0][1]
    translation_list = build_character_translation(root, [])
    translation = {k:v for list_item in translation_list for (k,v) in list_item.items()}
    encoded = list(itertools.chain(*[translation.get(n) for n in zipped]))
    # print(*encoded)
   
    encoded_bytes = bytes(chunk_to_byte(b) for b in byte_chunks(encoded))
    # serialisedTree = json.dumps(root)
    # print(serialisedTree)
    print(f'Encoded size: {len(encoded_bytes)}')
    with open(output_file, 'wb') as f:
        f.write(encoded_bytes)

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
    encode('./testfiles/tale.txt', 'output.bin')
    decode('output.bin', 'decoded.txt')