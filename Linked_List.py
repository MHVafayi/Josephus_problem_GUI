class Node:
    def __init__(self, value, next=None, pre=None):
        self.next = next
        self.value = value
        self.pre = pre


class Linked_List:
    def __init__(self, head=None):
        self.head = head

    def create(self, n: int):
        self.head = Node(1)
        temp = self.head
        for i in range(1, n):
            temp.next = Node(i + 1)
            temp = temp.next
        temp.next = self.head

    def get_head(self):
        return self.head

    def __len__(self):
        length = 1
        temp = self.head
        while temp.next != self.head:
            length += 1
            temp = temp.next
        return length

    def __getitem__(self, index: int):
        temp = self.head
        if index >= 0:
            for i in range(0, index):
                temp = temp.next
        else:
            size = self.__len__()
            for i in range(0, size + (index % size)):
                temp = temp.next
        return temp
