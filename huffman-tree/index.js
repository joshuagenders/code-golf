import fs from 'fs'

const priorityQueue = (items=[]) => ({
    push(item){
        for (const [i, x] of items.entries()){
            if (item.count > x.count){
                items.splice(i, 0, item)
                return
            }
        }
        items.push(item)
    },
    pop: () => items.pop(),
    items
})

const getCharacterCount = (chars) => {
    let counts = {}
    for (let i = 0; i < 256; i++){
        counts[String.fromCharCode(i)] = 0
    }
    for (const char of chars){
        counts[char]++
    }
    const pq = priorityQueue()
    for (const [char, count] of Object.entries(counts)) {
        if (count > 0)
            pq.push(treeNode(undefined, undefined, count, char), count)
    }
    return pq
}

const buildTree = (charPq) => {
    while (charPq.items.length > 1) {
        let r = charPq.pop()
        let l = charPq.pop()
        let newNode = treeNode(l, r, l.count + r.count, undefined)
        charPq.push(newNode, newNode.count)
    }
    return charPq.items[0]
}

const treeNode = (left, right, count, value) => ({
    left,
    right,
    count,
    value,
})

const buildCharacterTranslation = (currentNode, currentPath=[]) => {
    const map = {}
    if (currentNode.value) {
        map[currentNode.value] = currentPath
        return map
    }
    if (currentNode.left){
        Object.assign(map, buildCharacterTranslation(currentNode.left, [...currentPath, 0]))
    }
    if (currentNode.right){
        Object.assign(map, buildCharacterTranslation(currentNode.right, [...currentPath, 1]))
    }
    return map
}

export const encode = (inputPath, outputPath) => {
    const data = fs.readFileSync(inputPath, { encoding: 'ascii' }).toString()
    const charCountsPriorityQueue = getCharacterCount(data)
    const root = buildTree(charCountsPriorityQueue)
    const table = buildCharacterTranslation(root)
    const translate = datum => table[datum]
    //todo write bytes at this map stage
    const encoded = [...data].map(translate).flat()
    const additionalBits = encoded.length % 8
    const numBytes = additionalBits 
        ? ~~(encoded.length / 8) + 1
        : ~~(encoded.length / 8)

    const buffer = new Uint8Array(numBytes)
    // const readBit = (i, bit) => (buffer[i] >> bit) % 2
    const setBit = (i, bit, value) => {
        if (value == 0) {
          buffer[i] &= ~(1 << bit)
        } else {
          buffer[i] |= (1 << bit)
        }
    }
    for (const [index, bit] of encoded.entries()){
        setBit(~~(index / 8), index % 8, bit)
    }
    fs.writeFileSync(`${outputPath}.bin`, Buffer.from(buffer))

    //todo - put in same file
    const serialisedTree = JSON.stringify(Object.assign(root, { additionalBits }))
    fs.writeFileSync(`${outputPath}.tree`, Buffer.from(serialisedTree))
}


const decode = (inputPath, outputPath) => {
    const tree = JSON.parse(fs.readFileSync(`${inputPath}.tree`).toString())
    const buffer = fs.readFileSync(`${inputPath}.bin`)
    const readBit = (i, bit) => (buffer[i] >> bit) % 2
    let currentNode = tree
    let output = ''
    const bitCount = tree.additionalBits
        ? (buffer.length * 8) - (8 - tree.additionalBits)
        : (buffer.length * 8)

    for (let i = 0; i < bitCount; i++){
        const bit = readBit(~~(i / 8), i % 8)
        if (bit){
            if (currentNode.right){
                currentNode = currentNode.right
            }
        }else{
            if (currentNode.left){
                currentNode = currentNode.left
            }
        }
        if (currentNode.value){
            output += currentNode.value
            currentNode = tree
        }
    }
    console.log(output)
    fs.writeFileSync(outputPath, Buffer.from(output))
}

encode('test.txt', 'out')
decode('out', 'decoded.txt')