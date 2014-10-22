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

def shellSort(*inList):
    newList = list(inList)
    l = len(newList)
    gap = l / 2
    while gap > 0:
        i = gap
        while i < l:
            temp = newList[i]
            j = i
            while j >= gap:
                if temp > newList[j - gap]:
                    break
                newList[j] = newList[j - gap]
                j -= gap
            newList[j] = temp
            i += 1
        gap /= 2
    
    return newList     

def selectSort(*inList):
    newList = list(inList)
    l = len(newList)
    i = 0
    while i < l:
        j = i + 1
        minI = i
        while j < l:
            if newList[j] < newList[minI]:
                minI = j
            j += 1
        swap(newList, i, minI)
        i += 1

    return newList

def _mergeSortCom(inList1, inList2):
    newList = []
    len1 = len(inList1)
    len2 = len(inList2)
    i = j = 0
    while i < len1 and j < len2:
        if inList1[i] < inList2[j]:
            newList.append(inList1[i])
            i += 1
        else:
            newList.append(inList2[j])
            j += 1
    if i == len1:
        newList.extend(inList2[j:])
    else:
        newList.extend(inList1[i:])

    return newList

def mergeSort(inList):
    l = len(inList)
    listL = inList[: l / 2]
    listR = inList[l / 2 :]
    if len(listL) > 1:
        listL = mergeSort(listL)
    if len(listR) > 1:
        listR = mergeSort(listR)
    inList = _mergeSortCom(listL, listR)
    return inList



if __name__ == '__main__':
    print shellSort(314,15,926,53,5897,9323,84626,43383,279,502,88,41,97,16939,93,75,1058,209,74,9,445,9,23,07,8,16,40,62,862,0,8,99,8628,0,34,8,2,53)
    a = [314,15,926,53,5897,9323,84626,43383,279,502,88,41,97,16939,93,75,1058,209,74,9,445,9,23,07,8,16,40,62,862,0,8,99,8628,0,34,8,2,53]
    print mergeSort(a)



