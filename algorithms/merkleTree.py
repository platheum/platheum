from typing import List
import typing
import hashlib



class Node:
    def __init__(self, left, right)-> None:
        self.left: Node = left
        self.right: Node = right

    
    @staticmethod
    def hash(val: str)-> str:
        return hashlib.sha256(val.encode("utf-8")).hexdigest()
    def __str__(self):
        return(str(self.value))


class Pair:
    def __init__(self, left: Node, right: Node) -> None:
         self.left: Node = left
         self.right: Node = right

class MerkleTree:
    def __init__(self, values: List[str])-> None:
        self.__buildTree(values)
    
    def __buildTree(self, values: List[str])-> None:
        if len(values)%2 != 0: #if odd
            print('is odd height')
            values.append(values[-1])

        
        nodes = []
        for index in range(1, len(values)):
            if index == 1:
                nodes.append(Node(values[index-1], values[index]))

        print(nodes)

 
    def getRootHash(self)-> str:
         return self.root.value

def mixmerkletree()-> None:
    elems = ["Mix","ss",'grgr']
  
    mtree = MerkleTree(elems)

mixmerkletree()