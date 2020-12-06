
def lz(data):
    d = {i:chr(i) for i in range(255)}
    output = []
    ascii_bytes = bytes(data, 'utf-8')
    counter = 256
    i = 0
    while(i < len(ascii_bytes)):
        current_window = 1
        current = ascii_bytes[i:i+current_window]
        nxt = ascii_bytes[i:i+current_window+1]
        while(nxt in d.values()):
            current_window += 1
            current = ascii_bytes[i:i+current_window]
            nxt = ascii_bytes[i:i+current_window+1]
        if nxt not in d:
            d[counter] = nxt
            counter += 1
        if current_window == 1:
            output.append(current[0])
            output.append(0)
        else:
            output.append(counter >> 8)
            output.append(counter ^ (2**8))
        i += current_window

    return output

def encode(input_file, output_file):
    data = open(input_file, encoding='utf-8').read()
    print(f'File: {input_file}')
    print(f'File size: {len(data)}')
    zipped = lz(data)
    print(f'Zipped size: {len(zipped)}')

    # character_list = [{chr(i): data.count(chr(i))} for i in range(256)]
    # lz then huffman tree
    # print(character_list)

def decode(input_file, output_file):
    pass

if __name__ == "__main__":
    encode('./testfiles/test.txt', 'output.bin')
    decode('output.bin', 'decoded.txt')