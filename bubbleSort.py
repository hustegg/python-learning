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




if __name__ == '__main__':
    print bubbleSort1(3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,)
    print bubbleSort2(3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,)
    print bubbleSort3(3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,)
