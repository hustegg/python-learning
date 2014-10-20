def swap(inList, idx1, idx2):
    temp = inList[idx1]
    inList[idx1] = inList[idx2]
    inList[idx2] = temp

def bubbleSort1(*inList):
    newList = list(inList)
    l = len(newList)
    i = 1
    while i <= l:
        j = 0
        while j < l - i:
            if newList[j] > newList[j + 1]:
                swap(newList, j, j + 1)
            j += 1
        i += 1
    return newList
            
def bubbleSort2(*inList):
    newList = list(inList)
    l = len(newList)
    i = 1
    flag = True  # swappiness never happened && finish sorting
    while flag:
        j = 0
        flag = False
        while j < l - i:
            if newList[j] > newList[j + 1]:
                swap(newList, j, j + 1)
                flag = True
            j += 1
        i += 1
    return newList

def bubbleSort3(*inList):
    newList = list(inList)
    l = len(newList)
    i = 1
    flag = l - 2
    while flag > 0:
        j = 0
        k = flag
        flag = 0
        while j <= k:
            if newList[j] > newList[j + 1]:
                swap(newList, j, j + 1)
                flag = j
            j += 1
    return newList

def insertSort(*inList):
    newList = list(inList)
    l = len(newList)
    i = 1
    while i < l:
        j = i
        temp = newList[j]
        while j > 0:
            if temp > newList[j - 1]:
                break
            newList[j] = newList[j - 1]
            j -= 1
        newList[j] = temp
        i += 1
    return newList

if __name__ == '__main__':
    print insertSort(314,15,926,53,5897,9323,84626,43383,279,502,88,41,97,16939,93,75,1058,209,74,9,445,9,23,07,8,16,40,62,862,0,8,99,8628,0,34,8,2,53)



