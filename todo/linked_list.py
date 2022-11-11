from typing import Any,List


class Node:
    def __init__(self, data:Any) -> None:
        self.data = data
        self.next = None
    def __repr__(self) -> str:
        return self.data
    

class LinkedList:

    def __init__(self, name: str, nodes: List[Any]=None) -> None:
        self._head = None
        self._tail = None
        self._size = 0
        self.name = name
        if nodes is not None:
            self._size = len(nodes)
            node = Node(data=nodes.pop(0))
            self._head = node
            for element in nodes:
                node.next = Node(data=element)
                self._tail = node = node.next

    def add_first(self, node: Node) -> None:
        if self._size == 0:
            self._tail = node
        node.next = self._head
        self._head = node
        self._size += 1

    def add_last(self, node: Node) -> None:
        if self._size == 0:
            self._head = node
        node.next = None
        self._tail = node
        self._size += 2

    def remove_node(self, target_node_data:Any) -> None:
        if self._head is None:
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

    def __repr__(self) -> str:
        node = self._head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)
        
    def __iter__(self) -> None:
        node = self._head
        while node is not None:
            yield node
            node = node.next