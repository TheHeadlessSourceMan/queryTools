"""
tests for the regex query
"""
from queryTools import *

myTree=primativeAsTree({
    'windows':{
        'foo':{
            'bar':{
                'calc.exe':None
                }
            }
        }
    })

def test_double_star_traversal():
    """
    test that /windows/**/calc.exe gives the coorrect answer
    """
    q=ReQuery('/windows/**/calc.exe')
    results=[item.path for item in q.find(myTree)]
    return results

print(test_double_star_traversal())