r"""
A regular expression based query.

Details:
    each path section /xyz/ is treated as its own standalone regular expression
    leading * is treated more like a path operator since it makes no sense as a regex
        /location/*.exe
    . prefers to refer to a literal . over a regex .
        a.exe would match "a.exe", but not "aZexe" as it would in a pure regex
        rather, you would have to use a[.]exe
    if the entire path step is . or .. they do not match, but traverse
        /../sibling
        if you want any one or two characters do [.] or [.]{2}
    / is the always path separator
        never \ even on windows
        / is not matched, but splits which match
    "*" alone means "any child of"
        windows/*/*.exe
    "**" alone means "any descendent of"
        windows/**/*.exe
"""
import typing
import re
import queryTools


class ReQuery(queryTools.Query):
    r"""
    A regular expression based query.

    Details:
        each path section /xyz/ is treated as its own standalone regular expression
        leading * is treated more like a path operator since it makes no sense as a regex
            /location/*.exe
        . prefers to refer to a literal . over a regex .
            a.exe would match "a.exe", but not "aZexe" as it would in a pure regex
            rather, you would have to use a[.]exe
        if the entire path step is . or .. they do not match, but traverse
            /../sibling
            if you want any one or two characters do [.] or [.]{2}
        / is the always path separator
            never \ even on windows
            / is not matched, but splits which match
        "*" alone means "any child of"
            windows/*/*.exe
        "**" alone means "any descendent of"
            windows/**/*.exe
    """

    def __init__(self,
        queryString:str,
        ignoreCase:bool=False):
        """ """
        queryTools.Query.__init__(self,queryString,ignoreCase)

    def assign(self,
        queryString:str,
        ignoreCase:bool=False)->None:
        """
        Parse the query string into a searchable expression
        """
        reFlags=0
        if ignoreCase:
            reFlags=re.IGNORECASE
        self._querySteps=[]
        currentStep:typing.List[str]=[]
        for c in queryString:
            if c=='/':
                current=''.join(currentStep)
                if not current or current=='.':
                    # could just as easily not add it instead
                    self._querySteps.append(self.__SAMEDIR_STEP__)
                elif current=='..':
                    self._querySteps.append(self.__PARENTDIR_STEP__)
                elif current=='*':
                    self._querySteps.append(self.__CHILDOF_STEP__)
                elif current=='**':
                    self._querySteps.append(self.__DESCENDENTOF_STEP__)
                else:
                    self._querySteps.append(re.compile(current,reFlags))
                currentStep=[]
            else:
                currentStep.append(c)
        if currentStep:
            current=''.join(currentStep)
            if not current or current=='.':
                # could just as easily not add it instead
                self._querySteps.append(self.__SAMEDIR_STEP__)
            elif current=='..':
                self._querySteps.append(self.__PARENTDIR_STEP__)
            elif current=='*':
                self._querySteps.append(self.__CHILDOF_STEP__)
            elif current=='**':
                self._querySteps.append(self.__DESCENDENTOF_STEP__)
            else:
                self._querySteps.append(re.compile(current,reFlags))
        self._queryString=queryString

    def _iterChildren(self,
        tree:queryTools.TreeLike,
        _tape:typing.Optional[queryTools.Tape[queryTools.TreeLike]]
        )->typing.Generator[queryTools.TreeLike,None,None]:
        """
        Iterates over all children items

        :tree: starting location of the tree.
        """
        for c in tree.children:
            if c not in _tape.visited:
                yield c

    def _iterDescendents(self,
        tree:queryTools.TreeLike,
        _tape:typing.Optional[queryTools.Tape[queryTools.TreeLike]]
        )->typing.Generator[queryTools.TreeLike,None,None]:
        """
        Iterates over items in the tree using a breadth-first search

        :tree: starting location of the tree.
        """
        _tape.push(tree)
        while not _tape.isDone:
            tree=_tape.pop()
            if tree not in _tape.visited:
                yield tree
                for c in tree.children:
                    _tape.push(c)

    def matches(self, # pylint: disable=arguments-differ
        path:typing.Union[str,typing.List[str],queryTools.TreeLike],
        _startingAt:int=0
        )->bool:
        """
        check to see if a path matches this query
        """
        if isinstance(path,str):
            path=path.split('/')
        if isinstance(path,(list,tuple,dict)):
            path=queryTools.primativeAsTree(path)
        path=typing.cast(queryTools.TreeLike,path)
        _tape=queryTools.Tape()
        pathIdx=0
        for step in enumerate(self._querySteps):
            c=path[pathIdx]
            if isinstance(step,int):
                if step==self.__SAMEDIR_STEP__:
                    pathIdx-=1
                elif step==self.__PARENTDIR_STEP__:
                    pathIdx-=2
                elif step==self.__CHILDOF_STEP__:
                    pass # always true
                elif step==self.__DESCENDENTOF_STEP__:
                    for desc in self._iterDescendents(path,_tape):
                        if self.matches(desc,_startingAt+1):
                            return True
                    return False
            elif not self._matchesStep(c,_startingAt):
                return False
            pathIdx+=1
            _startingAt+=1
        return True

    def _matchesStep(self,item:queryTools.TreeLike,stepIdx:int)->bool:
        """
        check to see if the item matches the given step

        mostly a separate function to make it easy to override
        for derived classes
        """
        step=self._querySteps[stepIdx]
        if isinstance(step,int):
            raise Exception('Tape has been scrambled')
        return step.match(item.name) is not None

    def find(self,
        tree:queryTools.TreeLike,
        _tape:typing.Optional[queryTools.Tape[queryTools.TreeLike]]=None
        )->typing.Generator[queryTools.TreeLike,None,None]:
        """
        Finds items in the tree using a breadth-first search

        :tree: starting location of the tree.  Usually you'd pass root.
        """
        if _tape is None:
            _tape=typing.cast(queryTools.Tape[queryTools.TreeLike],queryTools.Tape())
        if self._querySteps:
            if tree not in _tape.visited:
                yield tree
            return
        _tape.visited.add(tree)
        while not _tape.isDone:
            c=_tape.pop()
            if c in _tape.visited:
                continue
            _tape.push(c)
            for stepIdx,step in enumerate(self._querySteps):
                if isinstance(step,int):
                    if step==self.__SAMEDIR_STEP__:
                        continue
                    elif step==self.__PARENTDIR_STEP__:
                        pass
                    elif step==self.__CHILDOF_STEP__:
                        pass
                    elif step==self.__DESCENDENTOF_STEP__:
                        pass
                elif self._matchesStep(c,stepIdx):
                    _tape.push(c)
