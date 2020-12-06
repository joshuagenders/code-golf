
import heapq

def lz(data):
    d = {chr(i):i for i in range(255)}
    output = []
    byte_data = bytes(data, 'utf-8')
    counter = 256
    i = 0
    current_window = 1
    for i in range(0, len(byte_data), current_window):
        current = byte_data[i:i + current_window]
        nxt = current = byte_data[i:i + current_window + 1]
        if (nxt in d):
            output.append(d[nxt] ^ 65280)
            output.append(d[nxt] & 255)
        else:
            d[nxt] = counter
            counter += 1
            output.append(current[0])
            output.append(0)
    return output

def encode(input_file, output_file):
    data = open(input_file, encoding='utf-8').read()
    print(f'File: {input_file}')
    print(f'File size: {len(data)}')
    zipped = lz(data)
    print(f'Zipped size: {len(zipped)}')

    q = []
    for i in range(256):
        value = chr(i)
        count = data.count(chr(i))
        left = None
        right = None
        heapq.heappush(q, (count, { value, count, left, right }))
    while len(q) > 1:
        right = heapq.heappop(q)
        left = heapq.heappop(q)
        count = left[0]+right[0]
        value = None
        heapq.heappush(q, (count, { value, count, left, right }))
    translation = build_character_translation(q[0])
    translated = map(lambda x: translation[x], zipped)
    print(translated)
    # lz then huffman tree
    # print(character_list)
def build_character_translation(start_node, current_path=[]):
    if start_node.value:
        return current_path
    paths = []
    if start_node.left:
        paths.extend(build_character_translation(start_node.left, current_path[:].append(0)))
    if start_node.right:
        paths.extend(build_character_translation(start_node.right, current_path[:].append(1)))
    return paths

def decode(input_file, output_file):
    pass

if __name__ == "__main__":
    encode('./testfiles/test.txt', 'output.bin')
    decode('output.bin', 'decoded.txt')