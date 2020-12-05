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
    if (currentNode.value) {
        return [{char: currentNode.value, charPath: currentPath}]
    }
    const paths = []
    if (currentNode.left){
        paths.push(...buildCharacterTranslation(currentNode.left, [...currentPath, 0]))
    }
    if (currentNode.right){
        paths.push(...buildCharacterTranslation(currentNode.right, [...currentPath, 1]))
    }
    return paths
}

const characterTranslationTable = (rootNode) => {
    const translations = buildCharacterTranslation(rootNode)
    const t = new Map()
    for (const translation of translations){
        t.set(translation.char, translation.charPath.join(''))
    }
    return t
}

export const encode = (inputPath, outputPath) => {
    const data = fs.readFileSync(inputPath, { encoding: 'ascii' }).toString()
    const charCountsPriorityQueue = getCharacterCount(data)
    const root = buildTree(charCountsPriorityQueue)
    const table = characterTranslationTable(root)
    const throughTranslationTable = datum => table.get(datum)
        
    const serialisedTable = [...table.keys()].map(k => `${k}:${table.get(k)}`).join(',').concat(';')
    const encoded = [...data].map(throughTranslationTable).join('')
    const output = serialisedTable.concat(encoded)
    console.log({ output })
    // fs.writeFileSync(output)
}

const decode = () => {
    //decode translation table
    //run data back through translation table
    //output text to file
}

encode('test.txt', '')