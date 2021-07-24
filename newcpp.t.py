#!python

import unittest
from unittest.case import expectedFailure
import newcpp

class TestGenerateFunctions(unittest.TestCase):
    def test_generateHeaderFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        classbrief = "A dog that barks"
        authorinfo = "Mariah Carey <mariahcarey@gmail.com>"
        date = "May 1st, 2021"
        needInterface = False
        needPimpl = True
        content = newcpp.generateHeaderFile(namespace, classname, classbrief, authorinfo, date, needInterface, needPimpl)
        print(content)
    

if __name__ == '__main__':
    unittest.main()