class _Node:
    def __init__(self, loan):
        self.loan = loan
        self.prev = None
        self.next = None


class ActiveLoansLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, loan):
        node = _Node(loan)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def remove(self, loan_id):
        cur = self.head
        while cur:
            if cur.loan["loan_id"] == loan_id:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                return cur.loan
            cur = cur.next
        return None

    def traverse(self, visit=None):
        items = []
        cur = self.head
        while cur:
            items.append(cur.loan)
            if visit:
                visit(cur.loan)
            cur = cur.next
        return items