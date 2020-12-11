from bitstring import BitArray

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
    
    print (f'byte count {byte_count}')
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
            print (f'add to dict: {current_bytes}:{byte_val}')
            dictionary[next_bytes.bin] = byte_val
            counter += 1

        to_output = dictionary[current_bytes.bin]
        output.prepend(to_output)
        byte_index += current_window // 8 - 1 or 1
    print (f'uncompressed  : {data.bin}')
    print (f'compressed    : {output.bin}')
    

def decompress(data):
    compressed_int = lambda x: BitArray(x.to_bytes(2, 'big'))[16 - bit_count:]
    int_to_8bits = lambda x: BitArray(x.to_bytes(1, 'big'))
    dictionary = {compressed_int(i):int_to_8bits(i).bin for i in range(255)}

    output = bytearray()
    bit_count = 10
    for index in range(0, len(output), bit_count):
        # take val
        window = bit_count
        current = bytes(data[index:index + bit_count])
        nxt = bytes(data[index:index + bit_count + window])

        # decode
        while nxt in dictionary:
            index += bit_count
            current = bytes(data[index:index+bit_count])    

def main():
    # compress(b'thisissthe')
    compress(b'???')

if __name__ == "__main__":
    main()
