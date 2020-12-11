from bitstring import BitArray

# todo : variable length
def compress(d: bytes):
    bit_count = 10
    compressed_int = lambda x: BitArray(x.to_bytes(2, 'big'))[16 - bit_count:]
    int_to_8bits = lambda x: BitArray(x.to_bytes(1, 'big'))
    dictionary = {int_to_8bits(i).bin:compressed_int(i) for i in range(255)}
    data = BitArray(d)
    output = BitArray()
    byte_count = len(data) // 8
    byte_index = 0
    counter = 256
    
    while byte_index < byte_count:
        current_window = 8
        current_bytes = data[byte_index*8:byte_index*8 + current_window]
        next_bytes = data[byte_index*8:byte_index*8 + current_window]
        while next_bytes.bin in dictionary:
            current_bytes = next_bytes
            if byte_index + current_window // 8 > byte_count:
                break
            else:
                current_window += 8
                next_bytes = data[byte_index*8:byte_index*8 + current_window]

        # if there is a next byte and there is room in the dictionary then add to dictionary
        if byte_index + current_window // 8 < byte_count and counter < 2 ** bit_count:
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

if __name__ == "__main__":
    val = b'?? ?? abc abcabcabc ab??c'
    # val = b'ababc'
    # val = b'???'
    # val = b'thisisthe'
    # val = b'ababcabca'
    compressed = compress(val)
    decompressed = decompress(compressed)
    print (f'compressed: {compressed}')
    print (f'val         : {bytes(val)}')
    print (f'decompressed: {bytes(decompressed)}')
    assert bytes(decompressed) == val
