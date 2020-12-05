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

var buffer = new Uint8Array(1);

function readBit(buffer, i, bit){
  return (buffer[i] >> bit) % 2;
}

function setBit(buffer, i, bit, value){
  if(value == 0){
    buffer[i] &= ~(1 << bit);
  }else{
    buffer[i] |= (1 << bit);
  }
}

// write bit 0 of buffer[0]
setBit(buffer, 0, 0, 1)

export const encode = (inputPath, outputPath) => {
    const data = fs.readFileSync(inputPath, { encoding: 'ascii' }).toString()
    const charCountsPriorityQueue = getCharacterCount(data)
    const root = buildTree(charCountsPriorityQueue)
    const table = buildCharacterTranslation(root)
    const translate = datum => table[datum]
    const serialisedTable = JSON.stringify(table)
    // const buff = Buffer.from()
    const encoded = [...data].map(translate).flat().join('')
    // const output = serialisedTable.concat(encoded)
    console.log({ table, encoded, serialisedTable })
    // fs.writeFileSync(output)
    // 0000000000
}

const decode = () => {
    //decode translation table
    //run data back through translation table
    //output text to file
}

encode('test.txt', '')