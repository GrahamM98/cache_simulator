import sys
import math

#cache size in kilobytes
cacheSize = 1024
#cache line size in bytes
cacheLineSize = 256
#number of ways per set
ways = 16

#calculates number of bits for offset
offsetN = int(math.log(cacheLineSize, 2))
#calculate number of bits for an address, add ten because cache size is in kilobytes
addrSize = int(math.log(cacheSize, 2)) + 10
#calculate number of sets, multiply by 2^10 to get cache size in bytes
sets = int((1024*cacheSize)/(cacheLineSize*ways))
#calculate number of bits for set index
indexN = int(math.log(sets, 2))

def assign(addr):
    print(addr, end=', ')
    binAddr = bin(int(addr, 0))
    print(binAddr)
    binAddr = binAddr[2:]

    #find offset of 
    offset = '0b' + binAddr[-offsetN:]
    if offset == '0b': offset = '0b0'
    print("offset: {0}".format(offset))

    #find set index of current address
    index = '0b' + binAddr[-(offsetN+indexN):-offsetN]
    if index == '0b': index = '0b0'
    print("set index: {0}".format(index))

    #find tag of current address
    tag = '0b' + binAddr[:-(offsetN+indexN)]
    if tag == '0b': tag = '0b0'
    print("tag: {0}".format(tag))

    print()
    return

file = open(sys.argv[1])

print("address space: {0}, sets: {1}, set index: {2}, offset: {3}".format(addrSize, sets, indexN, offsetN))

for line in file:
    addr = line.split()[-1]
    assign(addr)
    