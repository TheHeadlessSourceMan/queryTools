r"""
A query based upon glob expressions.

Details:
    each path section /xyz/ is treated as its own standalone expression
    supports * and ? glob expressions
    if the entire path step is . or .. they do not match, but traverse
        /../sibling
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


class GlobQuery(queryTools.ReQuery):
    r"""
    A query based upon glob expressions.

    Details:
        each path section /xyz/ is treated as its own standalone expression
        supports * and ? glob expressions
        if the entire path step is . or .. they do not match, but traverse
            /../sibling
        / is the always path separator
            never \ even on windows
            / is not matched, but splits which match
        "*" alone means "any child of"
            windows/*/*.exe
        "**" alone means "any descendent of"
            windows/**/*.exe
    """
    def __init__(self,queryString:str,ignoreCase:bool=False):
        queryTools.ReQuery.__init__(self,queryString,ignoreCase)

    def assign(self,queryString:str,ignoreCase:bool=False)->None:
        """
        Parse the query string into a searchable expression
        """
        self._querySteps=[]
        if ignoreCase:
            reFlags=re.IGNORECASE
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
                    current=re.escape(current).replace('\\*','.*').replace('\\?','.')
                    self._querySteps.append(re.compile(currentStep,reFlags))
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
                self._querySteps.append(re.compile(currentStep,reFlags))
        self._queryString=queryString