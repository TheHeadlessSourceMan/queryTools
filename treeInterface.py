"""
This is a general prototype for how trees look,
which is necessary for queries to work.

Usually you would want to use something powerful
for your tree like an xml structure, a EzFs directory,
a bigBallOfMud, or a general pynode.
"""
from dataclasses import dataclass, field
import typing


class TreeLike(typing.Protocol):
    """
    This is a general prototype for how trees look,
    which is necessary for queries to work.

    Usually you would want to use something powerful
    for your tree like an xml structure, a EzFs directory,
    a bigBallOfMud, or a general pynode.
    """
    name:str
    parent:"TreeLike"
    children:typing.Iterable["TreeLike"]


@dataclass
class Tree(TreeLike):
    """
    A simple instaciable tree
    """
    name:str=''
    parent:typing.Optional[TreeLike]=None
    children:typing.List[TreeLike]=field(default_factory=lambda: [])

    @property
    def path(self)->str:
        """
        get the path to this item
        """
        return '/'+('/'.join(self.pathSegments))
    @property
    def pathSegments(self)->typing.Iterable[str]:
        """
        get the path to this item
        """
        ret=[]
        item=self
        while item is not None:
            ret.append(item.name)
            item=item.parent
        ret.reverse()
        return ret

    def __hash__(self) -> int:
        return self.path.__hash__()


def primativeAsTree(
    prim:typing.Union[
        typing.Iterable[typing.Union[str,typing.Iterable]], # list-of-lists style tree
        typing.Dict[str,typing.Any]
    ],
    parent:typing.Optional[TreeLike]=None
    )->TreeLike:
    """
    Turns a python primative type into a tree.
        a) list of strings into a tree of strings/lists
        b) a dict of dicts into a tree
        c) mix of those
    """
    ret=Tree(parent=parent)
    if prim is None:
        pass
    elif hasattr(prim,'items'):
        # dict of dicts
        for k,v in prim.items():
            if isinstance(v,(str,int,float,bool)):
                v=str(v)
            else:
                v=primativeAsTree(v,ret)
                v.name=k
            ret.children.append(v)
    else:
        # list of strings/lists
        for item in prim:
            if isinstance(item,str):
                t=Tree(name=item)
            else:
                t=primativeAsTree(item,ret)
            ret.children.append(t)
    return ret
