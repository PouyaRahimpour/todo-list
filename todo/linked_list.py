from typing import Any, List


class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.next = None

    def __repr__(self) -> str:
        return self.data


class LinkedList:

    def __init__(self, nodes: list[Any] = []) -> None:
        self._head = None
        self._tail = None
        self._size = 0

        if nodes != []:
            self._size = len(nodes)
            node = Node(data=nodes.pop(0))
            self._head = self._tail = node
            for element in nodes:
                node.next = Node(data=element)
                node = node.next
                self._tail = node

    def add_first(self, data: Any) -> None:
        node = Node(data)
        if self._size == 0:
            self._tail = node
        node.next = self._head
        self._head = node
        self._size += 1

    def add_last(self, data: Any) -> None:
        node = Node(data)
        node.next = None
        if self._size == 0:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def is_empty(self) -> bool:
        return self._head is None

    def remove_first(self) -> None:
        if self.is_empty():
            raise Exception("List is empty")
        self._head = self._head.next
        self._size -= 1

    def remove_node_with_data(self, target_node_data: Any) -> None:
        if self.is_empty():
            raise Exception("List is empty")

        if self._head.data == target_node_data:
            self._head = self._head.next
            self._size -= 1
            return

        previous_node = self._head
        for node in self:
            if node.data == target_node_data:
                if node is self._tail:
                    self._tail = previous_node
                previous_node.next = node.next
                self._size -= 1
                return
            previous_node = node
        raise Exception(f'Node with data "{target_node_data}" not found')

    def remove_node(self, index: int) -> None:
        if self.is_empty():
            raise Exception("List is empty")

        if index < 0 or index > self._size:
            raise IndexError

        if index == 0:
            node = self._head
            self.remove_first()
            return node.data

        previous_node = self._head
        node = previous_node.next
        for i in range(index-1):
            previous_node = node
            node = node.next
        if node is self._tail:
            self._tail = previous_node
        previous_node.next = node.next

        self._size -= 1
        return node.data

    # def list_of(self) -> list:
    #     node = self._head
    #     nodes = []
    #     while node is not None:
    #         nodes.append(node.data)
    #         node = node.next
    #     return nodes

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index > self._size:
            raise IndexError
        tmp = self._head
        for i in range(index):
            tmp = tmp.next
        if tmp is None:
            raise IndexError
        return tmp.data

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        node = self._head
        nodes = []
        while node is not None:
            nodes.append(str(node.data))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self) -> None:
        node = self._head
        while node is not None:
            yield node.data
            node = node.next
        # return LinkedListIterator(self)
# class LinkedListIterator:
#     def __init__(self, linked_list) -> None:
#         self._index = 0
#         self._linked_list = linked_list

#     def __next__(self):
#         if self._index < self._linked_list._size:
#             node = self._linked_list._head
#             for i in range(self._index):
#                 node = node.next
#                 self._index += 1
#             return node.data
#         raise StopIteration
