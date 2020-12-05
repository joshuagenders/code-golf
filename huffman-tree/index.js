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
    const encoded = []
    for (let i = 0; i < data.length; i++){
        encoded.push(...table[data[i]])
    }
    const additionalBits = encoded.length % 8
    if (additionalBits){
        for (let i = 8 - additionalBits; i > 0; i--){
            encoded.push(0)
        }
    }
    const bytes = []
    for (let i = 0; i < encoded.length; i += 8) {
        bytes.push(
            encoded[i] +
            encoded[i+1] * 2 +
            encoded[i+2] * 4 +
            encoded[i+3] * 8 +
            encoded[i+4] * 16 +
            encoded[i+5] * 32 +
            encoded[i+6] * 64 +
            encoded[i+7] * 128)            
    }

    const serialisedTree = JSON.stringify(Object.assign(root, { additionalBits }))
    fs.writeFileSync(outputPath, Buffer.from(serialisedTree))

    const buffer = new Uint8Array(bytes)
    fs.appendFileSync(outputPath, Buffer.from(buffer))
}


export const decode = (inputPath, outputPath) => {
    const data = fs.readFileSync(`${inputPath}`)
    const opening = '{'.charCodeAt(0)
    const closing = '}'.charCodeAt(0)

    let dataStart
    let openingCount = 0
    for (dataStart = 0; dataStart < data.length; dataStart++){
        if (opening === data[dataStart])
            openingCount++
        if (closing === data[dataStart])
            openingCount--
        if (openingCount === 0)
            break
    }
    const tableString = data.slice(0, dataStart + 1)
    const tree = JSON.parse(Buffer.from(tableString).toString())
    const buffer = data.slice(dataStart + 1)

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
    // console.log(output)
    fs.writeFileSync(outputPath, Buffer.from(output))
}

encode('test.txt', 'out.bin')
decode('out.bin', 'decoded.txt')