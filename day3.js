const input = `00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010`

const parsedInput = input.split('\n').map((s) => s.split('').map(Number));

function toDec(bin) {
    return parseInt(bin.join(''), 2);
}

function getMLBits(input, pos) {
    const hash = {0: 0, 1: 0};
    input.forEach((i) => hash[i[pos]]++);
    if (hash[1] >= hash[0]) {
        return [1, 0];
    }
    return [0, 1];
}

function filterCollectionByMLIndex(input, idx) {
    let collection = input;
    let bitPos = 0;
    while (collection.length > 1) {
        const mlBits = getMLBits(collection, bitPos);
        collection = collection.filter((i) => i[bitPos] === mlBits[idx])
        bitPos++;
    }
    return collection[0];
}

const oxy = filterCollectionByMLIndex(parsedInput, 0);
const co2 = filterCollectionByMLIndex(parsedInput, 1);
console.log(toDec(oxy) * toDec(co2));


