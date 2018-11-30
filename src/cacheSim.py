import sys
import math

#cache size in kilobytes
cacheSize = 4096
#cache line size in bytes
cacheLineSize = 4
#number of ways per set
ways = 16

missTotal = 0

requestTotal = 0

#calculates number of bits for offset
offsetN = int(math.log(cacheLineSize, 2))
#calculate number of bits for an address, add ten because cache size is in kilobytes
addrSize = int(math.log(cacheSize, 2)) + 10
#calculate number of sets, multiply by 2^10 to get cache size in bytes
sets = int((1024*cacheSize)/(cacheLineSize*ways))
#calculate number of bits for set index
indexN = int(math.log(sets, 2))

#set up cache structure
cache = [None]*sets
for i in range(sets):
    cache[i] = [None]*ways
    for j in range(ways):
        cache[i][j] = {"tag": None, "val": 0, "data": None, "history": 0}

def updateHistory():
    for i in range(sets):
        for j in range(ways):
            cache[i][j]["history"] += 1

def assign(addr):
    global missTotal
    global requestTotal

    print(addr, end=', ')
    binAddr = bin(int(addr, 0))
    print(binAddr)

    # goes to second character in input line of address
    binAddr = binAddr[2:]

    # find offset of address
    offset = '0b' + binAddr[-offsetN:]
    if offset == '0b': offset = '0b0'
    print("offset: {0}".format(int(offset, 0)))

    # find set index of current address
    index = '0b' + binAddr[-(offsetN+indexN):-offsetN]
    if index == '0b': index = '0b0'
    print("set index: {0}".format(int(index, 0)))

    #find tag of current address
    tag = '0b' + binAddr[:-(offsetN+indexN)]
    if tag == '0b': tag = '0b0'
    print("tag: {0}".format(int(tag, 0)))

    cacheMiss = 1
    replace = 1

    for j in range(ways):
        if cache[int(index, 0)][j]["tag"] == hex(int(tag, 0)):
            cacheMiss = 0
            break

 # checks if miss due to empty way
    if cacheMiss == 1:
        for j in range(ways):
            if cache[int(index, 0)][j]["val"] == 0:
                cache[int(index, 0)][j]["tag"] = hex(int(tag, 0))
                cache[int(index, 0)][j]["val"] = 1
                cache[int(index, 0)][j]["data"] = str(cacheLineSize) + "b@" +addr
                cache[int(index, 0)][j]["history"] = 0
                replace = 0
                break

    if cacheMiss == 1:
        missTotal += 1
    requestTotal += 1



    # for loop for replacement policy LRU
    if cacheMiss == 1 and replace == 1:
        target = 0
        maxHist = 0
        for j in range(ways):
            # gets max history reference in memory
            if cache[int(index, 0)][j]["history"] >= maxHist:
                maxHist = cache[int(index, 0)][j]["history"]
                target = j
        cache[int(index, 0)][target]["tag"] = hex(int(tag, 0))
        cache[int(index, 0)][target]["val"] = 1
        cache[int(index, 0)][target]["data"] = str(cacheLineSize) + "b@" +addr
        cache[int(index, 0)][target]["history"] = 0

    updateHistory()

    print()
    return

file = open(sys.argv[1])

print("address space: {0}, sets: {1}, set index: {2}, offset: {3}".format(addrSize, sets, indexN, offsetN))

for line in file:
    addr = line.split()[-1]
    assign(addr)
for i in range(sets):
    print("set: {0}".format(i))
    for j in range(ways):
        print("{0}, {1}, {2}, {3}".format(cache[i][j]["tag"], cache[i][j]["val"], cache[i][j]["data"], cache[i][j]["history"]))
    print()
print("Miss Rate: {0}%".format((float(missTotal)/float(requestTotal))*100))
