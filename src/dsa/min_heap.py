class OverdueMinHeap:
    def __init__(self, items=None, key=lambda x: x["due_at"]):
        self.key = key
        self.heap = []
        if items is not None:
            self.heaped(items)

    def _less(self, a, b):
        return self.key(a) < self.key(b)

    def _sift_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self._less(self.heap[i], self.heap[p]):
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and self._less(self.heap[c], self.heap[smallest]):
                    smallest = c
            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top

    def heaped(self, items):
        self.heap = list(items)
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)