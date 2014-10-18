class heapList(list):
    def __init__(self, *newList):
        self.newList = list(newList)
        self._makeMinHeap()

    def minHeapAdd(self, value):
        pass


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

            print self.newList
    
    
    def _makeMinHeap(self):
    
        p = len(self.newList) / 2 - 1
        while p >= 0:
            self._minHeapDown(p)
            p -= 1
