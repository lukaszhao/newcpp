#!python

import unittest
from unittest.case import expectedFailure
import newcpp

"""
class TestGenerateFunctions(unittest.TestCase):
    def test_generateHeaderFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        classbrief = "A dog that barks"
        authorinfo = "Mariah Carey <mariahcarey@gmail.com>"
        date = "May 1st, 2021"
        needInterface = True
        needPimpl = True
        content = newcpp.generateHeaderFile(namespace, classname, classbrief, authorinfo, date, needInterface, needPimpl)
        print(content)

class TestGenerateCppFile(unittest.TestCase):
    def test_generateCppFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        classbrief = "A dog that barks"
        authorinfo = "Mariah Carey <mariahcarey@gmail.com>"
        date = "May 1st, 2021"
        needPimpl = True
        content = newcpp.generateCppFile(namespace, classname, classbrief, authorinfo, date, needPimpl)
        print(content)

class TestGenerateUnitTest(unittest.TestCase):
    def test_generateUnitTest(self):
        namespace = "rollingstone"
        classname = "Dog"
        needPimpl = True
        content = newcpp.generateUnitTest(namespace, classname, needPimpl)
        print(content)

class TestGenerateImpHeaderFile(unittest.TestCase):
    def test_generateImpHeaderFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        classbrief = "A dog that barks"
        authorinfo = "Mariah Carey <mariahcarey@gmail.com>"
        date = "May 1st, 2021"
        content = newcpp.generateImpHeaderFile(namespace, classname, authorinfo, date)
        print(content)

class TestGenerateImpCppFile(unittest.TestCase):
    def test_generateImpCppFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        classbrief = "A dog that barks"
        authorinfo = "Mariah Carey <mariahcarey@gmail.com>"
        date = "May 1st, 2021"
        content = newcpp.generateImpCppFile(namespace, classname, authorinfo, date)
        print(content)
"""

class TestGenerateMockHeaderFile(unittest.TestCase):
    def test_generateMockHeaderFile(self):
        namespace = "rollingstone"
        classname = "Dog"
        content = newcpp.generateMockHeaderFile(namespace, classname)
        print(content)

if __name__ == '__main__':
    unittest.main()