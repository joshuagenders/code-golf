
import heapq
import itertools
import json
from functools import reduce
from json import JSONEncoder
from bitstring import BitArray

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

def build_tree(data):
    q = []
    for i in range(256):
        count = data.count(i)
        if (count):
            value = i
            n = Node(None, None, count, value)
            heapq.heappush(q, (count, n))
    while len(q) > 1:
        right = heapq.heappop(q)[1]
        left = heapq.heappop(q)[1]
        count = left.count + right.count
        heapq.heappush(q, (count, Node(left, right, count, None)))
    return q[0][1]

def merge_dictionaries(items):
    return {k:v for list_item in items for (k,v) in list_item.items()}

def encode(data: bytes):
    root = build_tree(data)

    translation_list = build_character_translation(root, [])
    # print(f'translation list {translation_list}')
    translation = merge_dictionaries(translation_list)
    # print(f'translation {translation}')
    translated = list(itertools.chain(*[translation.get(byte) for byte in data]))
    # print(f'l translated {len(translated)}')
    additional_bytes = len(translated) % 8
    # print(f'additional bytes {additional_bytes}')
    x = BitArray(translated) + BitArray([0] * (8 - additional_bytes))
    x.reverse()
    x.byteswap()
    # print (f'x {x.bin}')
    encoded_bytes = x.tobytes()
    # print(f'encoded bytes: {encoded_bytes}')
    root.additional_bytes = additional_bytes
    
    serialised_tree = DefaultEncoder().encode(root)
    output = bytes(serialised_tree, 'ascii') + encoded_bytes
    return output

def build_character_translation(start_node, current_path=BitArray()):
    if start_node.value is not None:
        return [{start_node.value: current_path}]
    paths = []
    if start_node.left:
        new_path = current_path + BitArray([False])
        paths.extend(build_character_translation(start_node.left, new_path))
    if start_node.right:
        new_path = current_path + BitArray([True])
        paths.extend(build_character_translation(start_node.right, new_path))
    return paths

def decode(data:bytes):
    opening = ord('{')
    closing = ord('}')
    opening_count = 0
    start = data.index(opening)
    for i in range(start, len(data)):
        val = data[i]
        if (opening == val):
            opening_count += 1
        if (closing == val):
            opening_count -= 1
        if (opening_count == 0):
            data_start = i + 1
            break
    tree_data = data[0:data_start]
    encoded_data = data[data_start:]
    tree = json.loads(tree_data)
    read_bit = lambda i, bit: (encoded_data[i] >> bit) % 2
    current_node = tree
    output = bytearray()

    bit_count = (len(encoded_data) * 8) - (8 - tree['additional_bytes'])
    for i in range(bit_count):
        bit = read_bit(i // 8, i % 8)
        if bit:
            if current_node['right']:
                current_node = current_node['right']
        else:
            if current_node['left']:
                current_node = current_node['left']
        if current_node['value']:
            output.append(current_node['value'])
            current_node = tree
    return output

# todo : variable length
def compress(d: bytes):
    bit_count = 10
    compressed_int = lambda x: BitArray(x.to_bytes(2, 'big'))[16 - bit_count:]
    int_to_8bits = lambda x: BitArray(x.to_bytes(1, 'big'))
    bit_index = lambda byte_index: byte_index * 8

    dictionary = {int_to_8bits(i).bin:compressed_int(i) for i in range(255)}
    counter = 256
    data = BitArray(d)
    output = BitArray()
    data_bit_count = len(data)
    data_byte_count = data_bit_count // 8
    byte_index = 0

    while byte_index < data_byte_count:
        current_window = 8
        index = bit_index(byte_index)
        current_bytes = data[index:index + current_window]
        next_bytes = data[index:index + current_window]
        while next_bytes.bin in dictionary:
            if index + current_window > data_bit_count:
                break
            current_bytes = next_bytes
            current_window += 8
            next_bytes = data[index:index + current_window]

        # if there is a next byte and there is room in the dictionary then add to dictionary
        if index + current_window < data_bit_count and counter < 2 ** bit_count:
            byte_val = BitArray(counter.to_bytes(2, 'big'))[16 - bit_count:]
            dictionary[next_bytes.bin] = byte_val
            counter += 1

        to_output = dictionary[current_bytes.bin]
        output.append(to_output)
        byte_index += current_window // 8 - 1 or 1
    return output
    

def decompress(data: BitArray):
    bit_count = 10
    compressed_int = lambda x: BitArray(x.to_bytes(2, 'big'))[16 - bit_count:]
    dictionary = {compressed_int(i).bin:i.to_bytes(1, 'big') for i in range(255)}
    counter = 256
    output = bytearray()
    for i in range(0, len(data) // bit_count):
        index = i * bit_count
        current = data[index:index + bit_count]
        key = compressed_int(counter).bin
        if i + 1 < len(data) // bit_count:
            nxt = data[index+bit_count:index+bit_count+bit_count]
            counter += 1
            dictionary[key] = dictionary[current.bin] + bytes([dictionary[nxt.bin][0]])
        
        to_output = dictionary[current.bin]
        output.extend(to_output)
    return output

def run_example(input_file):
    print(f'File: {input_file}')    

    with open(f'./testfiles/{input_file}.txt', 'rb') as f:
        data = f.read()
    print(f'File size: {len(data)}')

    encoded = encode(data)
    print(f'Encoded size: {len(encoded)}')
    print(f'Ratio: {len(encoded) / len(data)}')

    with open('./testfiles/output.bin', 'wb') as f:
        f.write(encoded)

    decoded = decode(encoded)

    # print(f'decoded {decoded}')
    assert data == bytes(decoded)

    compressed = compress(data)
    decompressed = decompress(compressed)

    print(f'Compressed size: {len(compressed)}')
    print(f'Ratio: {len(compressed) / len(data)}')

    assert decompressed == data

    compressed_encoded = compress(encoded)
    decompressed_encoded = decompress(compressed_encoded)

    print(f'Encoded + compressed size: {len(compressed_encoded)}')
    print(f'Ratio: {len(compressed_encoded) / len(data)}')

    assert decompressed_encoded == encoded

    encoded_compressed = encode(compressed.tobytes())
    decoded_compressed = decode(encoded_compressed)

    print(f'Comprssed + encoded size: {len(encoded_compressed)}')
    print(f'Ratio: {len(encoded_compressed) / len(data)}')

    assert decoded_compressed == compressed.tobytes()


if __name__ == "__main__":
    run_example('tale')
