from __future__ import annotations

from abc import ABC, abstractmethod


#Inicialização Classe Node (Retirado do material do Prof Gilberto)

class Node():
    def __init__(self, key: object, value: object) -> None:
        self.key = key
        self.value = value
        self.left: Node = None
        self.right: Node = None

    def __str__(self) -> str:
        return str(self.key)
    
    def next(self, other_key: object) -> Node:
       return self.left if other_key < self.key else self.right

#Inicialização Classe BinarySearchTree (Retirado do material do Prof Gilberto)
class BinarySearchTreeADT(ABC):
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def is_empty(self) -> bool: ...
    @abstractmethod
    def search(self, key: object) -> object: ...
    @abstractmethod
    def insert(self, key: object, value: object) -> None: ...
    @abstractmethod
    def delete(self, key: object) -> bool: ...
    @abstractmethod
    def pre_order_traversal(self) -> None: ...
    @abstractmethod
    def in_order_traversal(self) -> None: ...
    @abstractmethod
    def post_order_traversal(self) -> None: ...
    @abstractmethod
    def level_order_traversal(self) -> None: ...

    # Métodos Que foram desenvolvidos na atividade
    @abstractmethod
    def size(self) -> int: ...
    @abstractmethod
    def degree(self, key: object) -> int: ...
    @abstractmethod
    def height(self, key: object) -> int: ...
    @abstractmethod
    def depth(self, key: object) -> int: ...
    @abstractmethod
    def descendent(self, key: object) -> str: ...


class BinarySearchTree(BinarySearchTreeADT):  # Métodos da Classe BinarySearchTree (Retirado do material do Prof Gilberto)
    def __init__(self) -> None:
        self._root: Node = None

    def clear(self) -> None:
        self._root = None

    def is_empty(self) -> bool:
        return self._root is None
    
    def _get_parent(self, key: object) -> Node:
        parent: Node = None
        current: Node = self._root
        while current and key != current.key:
            if key != current.key:
                parent = current
                current = current.next(key)
        return parent, current

    def search(self, key: object) -> object:
        def search(current: Node, key: object) -> object:
            if current is None:
                return None
            elif key == current.key:
                return current.value
            return search(current.next(key), key)
        return search(self._root, key)
    
    def insert(self, key: object, value: object) -> None:
        def insert(current: Node, key: object, value: object) -> Node:
            if current is None:
                return Node(key, value)
            elif key > current.key:
                current.right = insert(current.right, key, value)
            elif key < current.key:
                current.left = insert(current.left, key, value)
            return current
        self._root = insert(self._root, key, value)

    def __str__(self) -> str:
        return '[empty]' if self.is_empty() else self._str_tree()
    
    def _str_tree(self) -> str:
        def _str_tree(current: Node, is_right: bool, tree: str, ident: str) -> str:
            if current.right:
                tree = _str_tree(current.right, True, tree, ident + (' ' * 8 if is_right else ' |' + ' ' * 6))
            tree += ident + (' /' if is_right else ' \\') + "----- " + str(current) +'\n'
            if current.left:
                tree = _str_tree(current.left, False, tree, ident + (' |' + ' ' * 6
            if is_right else ' ' * 8))
            return tree
        tree: str = ''
        if self._root.right:
            tree = _str_tree(self._root.right, True, tree, '')
        tree += str(self._root) + '\n'
        if self._root.left:
            tree = _str_tree(self._root.left, False, tree, '')
        return tree

    def _delete_by_copying(self, key: object) -> bool:
        parent: Node; current: Node
        parent, current = self._get_parent(key)
        if current is None:
            return False
        # Caso 3
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            self._delete_by_copying(at_the_right.key)
            current.key, current.value = at_the_right.key, at_the_right.value
        # Caso 1/2
        else:
            next_node: Node = current.left or current.right
            if current == self._root:
                self._root = next_node
            elif current == parent.left:
                parent.left = next_node
            else:
                parent.right = next_node
        return True

    def delete(self, key: object) -> bool:
        return self._delete_by_copying(key)
    
    def _delete_by_merging(self, key: object) -> bool:
        parent: Node; current: Node
        parent, current = self._get_parent(key)
        if current is None:
            return False
        # Caso 3
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            at_the_right.right = current.right
            if current == self._root:
                self._root = current.left
            elif parent.left == current:
                parent.left = current.left
            else:
                parent.right = current.left
        # Caso 1/2
        else:
                next_node: Node = current.left or current.right
                if current == self._root:
                    self._root = next_node
                elif current == parent.left:
                    parent.left = next_node
                else:
                    parent.right = next_node
        return True
    
    def delete(self, key: object) -> bool:
        return self._delete_by_merging(key)
    
    def pre_order_traversal(self) -> None:
        def pre_order_traversal(current: Node) -> None:
            if current:
                print(current.key, end=' ')
                pre_order_traversal(current.left)
                pre_order_traversal(current.right)
        pre_order_traversal(self._root)
    
    def in_order_traversal(self) -> None:
        def in_order_traversal(current: Node) -> None:
            if current:
                in_order_traversal(current.left)
                print(current.key, end=' ')
                in_order_traversal(current.right)
        in_order_traversal(self._root)
    
    def post_order_traversal(self) -> None:
        def post_order_traversal(current: Node) -> None:
            if current:
                post_order_traversal(current.left)
                post_order_traversal(current.right)
                print(current.key, end=' ')
        post_order_traversal(self._root)

    def level_order_traversal(self) -> None:
        if self._root:
            queue = [self._root]
            while queue:
                current: Node = queue.pop(0)
                print(current.key, end=' ')
                if current.left: queue.append(current.left)
                if current.right: queue.append(current.right)

    # Metodos adicionais desenvolvidos 
    def size(self)-> int: 
        def size(current: Node) -> int:
            if current is None:
                return 0
            else:
                return 1 + size(current.left) + size(current.right)
        return size(self._root)
    
    def degree(self, key: object) -> int:
        def degree(current: Node, key: object) -> int:
            if current is None:
                return -1
            elif key == current.key:
                count = 0
                if current.left:
                    count += 1
                if current.right:
                    count += 1
                return count
            return degree(current.next(key), key)
        return degree(self._root, key)
    
    def height(self, key: object) -> int:
        def height(current: Node) -> int:
            if current is None:
                return -1
            else:
                left_height = height(current.left)
                right_height = height(current.right)
                return max(left_height, right_height) + 1
        parent, key_node = self._get_parent(key)
        if key_node is None:
            return -1
        else:
            return height(key_node)
        
    def depth(self, key: object) -> int:
        contador = 0

        def depth(current: Node, key: object) -> int:
            if current is None:
                return -1
            elif key == current.key:
                return contador
            else:
                return 1 + depth(current.next(key), key)
        return depth(self._root, key)
    
    def descendent(self, key: object) -> str:
        descendents = ''
        key_found = False
        def descendent(current: Node, key: object) -> None:
            nonlocal descendents
            nonlocal key_found
            if current is None:
                return 
            if descendents:
                descendents += ' ' + str(current.key)
            elif key == current.key:
                descendents += str(current.key)
                descendent(current.left, key)
                descendent(current.right, key)
                key_found = True
                return
            if key_found == False:
                descendent(current.left, key)
            if key_found == False:
                descendent(current.right, key)
        descendent(self._root, key)
        if descendents == '':
            descendents += 'None'
        return descendents
    
if __name__ == "__main__":
    
    #Inicializando e criando a árvore binária
    arvore = BinarySearchTree()
    arvore.insert(4,"A")
    arvore.insert(2,'B')
    arvore.insert(6,'C')
    arvore.insert(1,'D')
    arvore.insert(3,'E')
    arvore.insert(5,'F')
    arvore.insert(7,'G')

    #Mostrando na tela as arvores e as informacoes dos métodos criados
    print(arvore)
    print("Quantidade de nós da árvore: ", arvore.size())
    print("Grau do nó 2: ", arvore.degree(2))
    print("Altura do nó 3: ",arvore.height(3))
    print("Profundidade do nó 6: ", arvore.depth(6))
    print("Descendentes do nó 2: ", arvore.descendent(2))