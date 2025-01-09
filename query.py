#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
This adds support for finding things by query
"""
import typing
from abc import abstractmethod
import queryTools


class Query:
    """
    This adds support for finding things by query
    """

    __SAMEDIR_STEP__=0
    __PARENTDIR_STEP__=1
    __CHILDOF_STEP__=2
    __DESCENDENTOF_STEP__=3

    def __init__(self,
        queryString:str,
        ignoreCase:bool=False):
        """ """
        self._queryString:str=''
        self._querySteps:typing.List[typing.Union[typing.Pattern,int]]=[]
        self.assign(queryString,ignoreCase)

    @property
    def queryString(self)->str:
        """
        the query as a string value
        """
        return self._queryString
    @queryString.setter
    def queryString(self,queryString:str):
        self.assign(queryString)

    @abstractmethod
    def assign(self,
        queryString:str,
        ignoreCase:bool=False
        )->None:
        """
        child classes must implement
        """

    @abstractmethod
    def matches(self,
        path:typing.Union[str,typing.List[str]]
        )->bool:
        """
        Child classes must implement
        """

    @abstractmethod
    def find(self,
        tree:queryTools.TreeLike,
        _tape:typing.Optional[queryTools.Tape[queryTools.TreeLike]]=None
        )->typing.Generator[queryTools.TreeLike,None,None]:
        """
        Finds items in the tree using a breadth-first search

        :tree: starting location of the tree.  Usually you'd pass root.
        """

    def __repr__(self)->str:
        return str(self.queryString)


def cmdline(args:typing.Iterable[str]):
    """
    Run the command line

    :param args: command line arguments (WITHOUT the filename)
    """
    printhelp=False
    if not args:
        printhelp=True
    else:
        for arg in args:
            if arg.startswith('-'):
                av=[a.strip() for a in arg.split('=',1)]
                if av[0] in ['-h','--help']:
                    printhelp=True
                else:
                    print('ERR: unknown argument "'+av[0]+'"')
            else:
                print('ERR: unknown argument "'+arg+'"')
    if printhelp:
        print('Usage:')
        print('  query.py [options]')
        print('Options:')
        print('   NONE')
        return -1
    return 0


if __name__=='__main__':
    import sys
    sys.exit(cmdline(sys.argv[1:]))
