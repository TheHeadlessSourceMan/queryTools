"""
A query to match grep-style regular expressions
"""
import typing
import re
import queryTools


class GrepQuery(queryTools.ReQuery):
    r"""
    A query to match grep-style regular expressions
    """
    def __init__(self,queryString:str,ignoreCase:bool=False):
        queryTools.ReQuery.__init__(self,queryString,ignoreCase)

    def assign(self,queryString:str,ignoreCase:bool=False)->None:
        """
        Parse the query string into a searchable expression
        """
        self.re=grepToRegex(queryString,ignoreCase)


def grepToRegex(pattern:str,ignoreCase:bool=False)->typing.Pattern:
    """
    Translate a grep BRE to a Python ERE.
    """
    flags=0
    if ignoreCase:
        flags|=re.IGNORECASE
    # Replace \< and \> with \b
    pattern=pattern.replace(r"\<",r"\b").replace(r"\>",r"\b")
    # Replace \{ and \} with { and }
    pattern=pattern.replace(r"\{","{").replace(r"\}","}")
    # Replace \+ with +
    pattern=pattern.replace(r"\+","+")
    # Replace \| with |
    pattern=pattern.replace(r"\|","|")
    # Replace \( and \) with ( and )
    pattern=pattern.replace(r"\(","(").replace(r"\)",")")
    # Replace \? with ?
    pattern=pattern.replace(r"\?","?")
    # Replace \. with .
    pattern=pattern.replace(r"\.",".")
    # Replace \* with *
    pattern=pattern.replace(r"\*","*")
    # Replace \[ and \] with [ and ]
    pattern=pattern.replace(r"\[","[").replace(r"\]","]")
    # Replace ^ with \A
    pattern=pattern.replace("^",r"\A")
    # Replace $ with \Z
    pattern=pattern.replace("$",r"\Z")
    return re.compile(pattern,flags)
