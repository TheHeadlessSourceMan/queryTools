"""
A simple query that uses paths and * character.  That's it.
"""
import typing
import queryTools


class SimpleQuery(queryTools.Query):
    """
    A simple query that uses paths and * character.  That's it.

    supports /foo/*/bar but not /foo/item*/bar
    """

    def __init__(self,
        queryString:str,
        ignoreCase:bool=False):
        """ """
        self._ignoreCase=ignoreCase
        queryTools.Query.__init__(self,queryString,ignoreCase)

    def assign(self,
        queryString:str,
        ignoreCase:bool=False)->None:
        """
        Parse the query string into a searchable expression
        """
        self._ignoreCase=ignoreCase
        if ignoreCase:
            queryString=queryString.lower()
        self._querySteps=queryString.split('/')

    def paths(self,db)->typing.List[str]:
        """
        get all paths that match this query
        """
        ret=[]
        def _paths(steps:typing.List[str],path:str='')->None:
            if '*' not in steps:
                # no wildcards so we could have only the one
                if db.exists(self._queryString):
                    ret.append(self._queryString)
            else:
                for i,step in enumerate(steps):
                    if step.find('*')>=0:
                        for subpath in db.dir(path):
                            _paths(steps[i:],subpath)
                        break
                    else:
                        path='%s/%s'%(path,step)
        _paths(self._queryString)
        return ret

    def matches(self,
        path:typing.Union[str,typing.List[str]]
        )->bool:
        """
        check to see if a path matches this query
        """
        if isinstance(path,str):
            if self._ignoreCase:
                path=path.lower()
            path=path.split('/')
        else:
            if self._ignoreCase:
                path=[p.lower() for p in path]
        if len(path)!=len(self._querySteps):
            return False
        for i,step in enumerate(self._querySteps):
            if step not in ('*',path[i]):
                return False
        return True

    def find(self,
        tree:queryTools.TreeLike,
        _tape:typing.Optional[queryTools.Tape[queryTools.TreeLike]]=None
        )->typing.Generator[queryTools.TreeLike,None,None]:
        """
        Finds items in the tree using a breadth-first search

        :tree: starting location of the tree.  Usually you'd pass root.
        """
        return # TODO: need to implement find
