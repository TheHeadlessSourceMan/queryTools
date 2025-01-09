"""
A parsing tape used for tree traversal.

It has two purposes:
1) keep track of known nodes that still need to be searched
    tape.push()
    to add and to process use
    while not tape.isDone:
        tape.pop()
2) keep track of visited nodes to prevent infinite loops
    if item not in tape:
"""
import typing


TapeT=typing.TypeVar('TapeT')
class Tape(typing.Generic[TapeT]):
    """
    A parsing tape used for tree traversal.

    It has two purposes:
    1) keep track of known nodes that still need to be searched
        tape.push()
        to add and to process use
        while not tape.isDone:
            tape.pop()
    2) keep track of visited nodes to prevent infinite loops
        if item not in tape.visited:

    (NOTE: they work together so
        calling pop() automatically adds to visited
        you cannot push() something that is already in visited)
    """
    def __init__(self,initial:typing.Optional["Tape[TapeT]"]=None):
        self.visited:typing.Set[TapeT]=set()
        self._list:typing.List[TapeT]=[]
        if initial is not None:
            self.visited=initial.visited.copy()
            self._list=[]

    def copy(self)->"Tape":
        """
        create a copy at the current point for forked searching
        """
        return Tape(self)

    def push(self,item:TapeT)->None:
        """
        add a new item to the end of the tape
        """
        if item not in self.visited:
            self._list.append(item)

    def pop(self)->TapeT:
        """
        pop the next item from the tape
        """
        ret=self._list.pop(0)
        self.visited.add(ret)
        return ret

    @property
    def isDone(self):
        """
        is the tape done?
        """
        return len(self._list)==0
