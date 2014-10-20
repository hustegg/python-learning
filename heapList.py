class heapList(list):
    def __init__(self, *newList):
        self.newList = list(newList)
        self._makeMinHeap()

    def minHeapAdd(self, value):
        self.newList.append(value)
        self._minHeapUp(len(self.newList) - 1)

    def minHeapDel(self, idx):
        self.newList._swap(idx, len(self.newList) - 1)
        self.newList.pop()
        self.newList._minHeapDown(idx)

    def __getitem__(self, key):
        return self.newList[key]

    def __iter__(self):
        return iter(self.newList)

    def _swap(self, idx1, idx2):
        _temp = self.newList[idx1]
        self.newList[idx1] = self.newList[idx2]
        self.newList[idx2] = _temp
    
    def _minHeapUp(self, idx):
        c = idx
        p = (c - 1) / 2
    
        while p >= 0:
            if self.newList[p] <= self.newList[c]:
                break
            self._swap(p, c)
            c = p
            p = (c - 1) / 2

            print self.newList
    
    def _minHeapDown(self, idx):
        p = idx
    
        while 2 * p + 1 <= len(self.newList) - 1:
            if 2 * p + 2 <= len(self.newList) - 1 and self.newList[2 * p + 2] < min(self.newList[2 * p + 1], self.newList[p]):
                    c = 2 * p + 2
            elif self.newList[2 * p + 1] < self.newList[p]:
                c = 2 * p + 1
            else:
                break
    
            self._swap(p, c)
            p = c

    def _makeMinHeap(self):
    
        p = len(self.newList) / 2 - 1
        while p >= 0:
            self._minHeapDown(p)
            p -= 1

if __name__ == '__main__':
    a = heapList(9,8,7,6,5,4,3,2,1)
    a.minHeapAdd(0)


