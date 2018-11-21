import sys
import math

#cache size in kilobytes
cacheSize = 1024
#cache line size in bytes
cacheLineSize = 256
#number of ways per set
ways = 16

offset = int(math.log(cacheLineSize, 2))
addrSize = int(math.log(cacheSize, 2)) + 10
sets = int((1024*cacheSize)/(cacheLineSize*ways))
index = int(math.log(sets, 2))

def assign(addr):

    print(addr, end=', ')
    print(bin(int(addr, 0)))
    return

file = open(sys.argv[1])

print("address space: {0}, sets: {1}, set index: {2}, offset: {3}".format(addrSize, sets, index, offset))

for line in file:
    addr = line.split()[-1]
    assign(addr)
    