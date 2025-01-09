"""
Tools to attempt to abstract queries
    (eg: sql, glob expressions, regular expression, sparql, xpath, graphql, etc)
away from the systems they represent
"""
from .treeInterface import *
from .tape import *
from .query import *
from .reQuery import *
from .globQuery import *