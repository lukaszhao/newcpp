#!python


from os import name
from typing import ForwardRef


def generateMemberVar(classname):
    memberVar = "m_"
    if len(classname) > 0:
        memberVar = memberVar + classname[0].lower()
    if len(classname) > 1:
        memberVar = memberVar + classname[1:]
    return memberVar


def generateOnTheFlyVar(classname):
    onTheFlyVar = ""
    if len(classname) > 0:
        onTheFlyVar = onTheFlyVar + classname[0].lower()
    if len(classname) > 1:
        onTheFlyVar = onTheFlyVar + classname[1:]
    return onTheFlyVar


FILEDOXYGEN = """/**
 * @file $$filename$$
 * @brief $$classbrief$$
 * @author $$authorinfo$$
 * @date $$date$$
 */

"""

def generateFileDoxygen(filename, classbrief, authorinfo, date):
    filedoxygen = FILEDOXYGEN
    filedoxygen = filedoxygen.replace("$$filename$$", filename)
    filedoxygen = filedoxygen.replace("$$classbrief$$", classbrief)
    filedoxygen = filedoxygen.replace("$$authorinfo$$", authorinfo)
    filedoxygen = filedoxygen.replace("$$date$$", date)
    return filedoxygen


def generateClassHeadCommentBlock(classname, isHeader):
    blockChar = "="
    if not isHeader:
        blockChar = "-"
    blockLen = 9 + len(classname)
    paddinglen = int((80 - blockLen) / 2)
    if paddinglen < 0:
        paddinglen = 0
    padding = " " * paddinglen
    line0 = padding + "// " + blockChar * (6 + len(classname))
    line1 = padding + "// class " + classname
    block = line0 + "\n" + line1 + "\n" + line0 + "\n\n"
    return block


CLASSDOXYGEN = """/**
 * @brief $$classbrief$$
 */
"""

def generateClassDoxygen(classbrief):
    classdoxygen = CLASSDOXYGEN.replace("$$classbrief$$", classbrief)
    return classdoxygen


def includeGuard(filenamepre):
    return "INCLUDED_" + filenamepre.upper()


INCLUDE_GUARD_BEGIN = """#ifndef $$includeguard$$
#define $$includeguard$$

"""

def generateIncludeGuardBegin(filenamepre):
    return INCLUDE_GUARD_BEGIN.replace("$$includeguard$$", includeGuard(filenamepre))


INCLUDE_GUARD_END = """#endif  /* $$includeguard$$ */
"""

def generateIncludeGuardEnd(filenamepre):
    return INCLUDE_GUARD_END.replace("$$includeguard$$", includeGuard(filenamepre))


def generateFilenamePre(namespace, classname):
    return namespace.lower() + "_" + classname.lower()


def generateInterfaceClassname(classname):
    return classname + "I"


def includeInterfaceHeader(namespace, classname):
    interfaceclassname = generateInterfaceClassname(classname)
    filenamepre = generateFilenamePre(namespace, interfaceclassname)
    return "#include <" + filenamepre + ".h>\n\n"

def generateIncludeFiles(namespace, classname, needInterface, needPimpl):
    includeBlock = ""
    if needInterface:
        includeBlock = includeBlock + includeInterfaceHeader(namespace, classname)
    else:
        includeBlock = includeBlock + "#include <string>\n\n"
    if needPimpl:
        includeBlock = includeBlock + "#include <memory>\n\n"
    return includeBlock

def generateNamespaceBegin(namespace):
    return "namespace " + namespace + " {\n\n"

def generateNamespaceEnd(namespace):
    return "}  /* namespace " + namespace + " */\n\n"

def generateDeclareClass(classname, needInterface):
    interfaceClassname = generateInterfaceClassname(classname)
    if needInterface:
        return "class " + classname + " : public " + interfaceClassname + " {\n"
    else:
        return "class " + classname + " {\n"

def generateCloseDeclareClass():
    return "};\n\n"


def generateImpClassname(classname):
    return classname + "Imp"


DECLARE_IMP = """private:
    std::unique_ptr<$$impclassname$$> $$impMemberVar$$;

"""

def generateDeclareImp(classname, needPimpl):
    declareImp = ""
    if needPimpl:
        impClassname = generateImpClassname(classname)
        impMemberVar = generateMemberVar(impClassname)
        declareImp = DECLARE_IMP.replace("$$impclassname$$", impClassname).replace("$$impMemberVar$$", impMemberVar)
    return declareImp


FORWARD_DECLARE_IMP = """class $$impClassname$$;  // forward declaration

"""

def generateForwardDeclareImp(classname, needPimpl):
    forwardDeclareImp = ""
    if needPimpl:
        impClassname = generateImpClassname(classname)
        forwardDeclareImp = FORWARD_DECLARE_IMP.replace("$$impClassname$$", impClassname)
    return forwardDeclareImp


DECLARE_CTOR_DTOR = """public:
    /**
     * @brief ctor
     */
    $$classname$$();

    /**
     * @brief dtor
     */
    ~$$classname$$();

"""

def generateDeclareCtorDtor(classname):
    return DECLARE_CTOR_DTOR.replace("$$classname$$", classname)

DUMMY_FUNCTION_VERSION_DOXYGEN = """    /**
     * @brief get the version of this class
     * @return function returns a string representing the version
     */
"""

def generateDummyFunctionVersion(needInterface):
    dummyFuncDeclare = DUMMY_FUNCTION_VERSION_DOXYGEN
    dummyFuncDeclare = dummyFuncDeclare + "    std::string version() const"
    if needInterface:
        dummyFuncDeclare = dummyFuncDeclare + " override final;\n"
    else:
        dummyFuncDeclare = dummyFuncDeclare + ";\n"
    return dummyFuncDeclare


def generateHeaderFile(namespace, classname, classbrief, authorinfo, date, needInterface, needPimpl):
    filenamepre = generateFilenamePre(namespace, classname)
    filename = filenamepre + ".h"
    content = generateFileDoxygen(filename, classbrief, authorinfo, date)
    content = content + generateIncludeGuardBegin(filenamepre)
    content = content + generateIncludeFiles(namespace, classname, needInterface, needPimpl)
    content = content + generateNamespaceBegin(namespace)
    content = content + generateForwardDeclareImp(classname, needPimpl)
    content = content + generateClassHeadCommentBlock(classname, isHeader=True)
    content = content + generateClassDoxygen(classbrief)
    content = content + generateDeclareClass(classname, needInterface)
    content = content + generateDeclareImp(classname, needPimpl)
    content = content + generateDeclareCtorDtor(classname)
    content = content + generateDummyFunctionVersion(needInterface)

    content = content + generateCloseDeclareClass()
    content = content + generateNamespaceEnd(namespace)
    content = content + generateIncludeGuardEnd(filenamepre)

    return content


def generateIncludeFilesForCpp(namespace, classname, needPimpl):
    filenamepre = generateFilenamePre(namespace, classname)
    h_filename = filenamepre + ".h"
    includes = "#include <" + h_filename + ">\n\n"
    if needPimpl:
        impClassName = generateImpClassname(classname)
        impFilePre = generateFilenamePre(namespace, impClassName)
        impFileName = impFilePre + ".h"
        includes = includes + "#include <" + impFileName + ">\n\n"
    return includes
        

def generateDefineCtor(classname, needPimpl):
    defineCtor = classname + "::" + classname + "()\n{\n"
    if needPimpl:
        impClassName = generateImpClassname(classname)
        impVar = generateMemberVar(impClassName)
        defineCtor = defineCtor + "    // inject dependencies into " + impVar + "\n"
        defineCtor = defineCtor + "    " + impVar + " = std::make_unique<" + impClassName + ">();\n"
    defineCtor = defineCtor + "}\n\n"
    return defineCtor


def generateDefineDtor(classname):
    defineDtor = classname + "::~" + classname + "()\n{\n}\n\n"
    return defineDtor


def generateDefineFunctionVersion(classname, needPimpl):
    defineFunctionVersion = "std::string " + classname + "::version() const\n{\n"
    if needPimpl:
        impClassName = generateImpClassname(classname)
        impVar = generateMemberVar(impClassName)
        defineFunctionVersion = defineFunctionVersion + "    return " + impVar + "->version();\n"
    else:
        defineFunctionVersion = defineFunctionVersion + "    return \"0.0.1\";\n"
    defineFunctionVersion = defineFunctionVersion + "}\n\n"
    return defineFunctionVersion


def generateCppFile(namespace, classname, classbrief, authorinfo, date, needPimpl):
    filenamepre = generateFilenamePre(namespace, classname)
    filename = filenamepre + ".cpp"
    content = generateFileDoxygen(filename, classbrief, authorinfo, date)
    content = content + generateIncludeFilesForCpp(namespace, classname, needPimpl)
    content = content + generateNamespaceBegin(namespace)
    content = content + generateClassHeadCommentBlock(classname, isHeader=False)
    content = content + generateDefineCtor(classname, needPimpl)
    content = content + generateDefineDtor(classname)
    content = content + generateDefineFunctionVersion(classname, needPimpl)

    content = content + generateNamespaceEnd(namespace)
    return content


UNIT_TEST_CONTENT = """#include <gtest/gtest.h>

// Subject Under Test (SUT)
#include <$$sut_header_file$$>

using namespace $$namespace$$;
using namespace ::testing;

class Test$$SutClassName$$ : public Test {
protected:
    void SetUp() {}
    void TearDown() {}
};

TEST_F(Test$$SutClassName$$, test_ctor_and_dtor)
{
    EXPECT_NO_FATAL_ERROR($$SutClassName$$ $$on_the_fly_sut_var$$;);
}

TEST_F(Test$$SutClassName$$, test_version)
{
    // Given
    $$SutClassName$$ $$on_the_fly_sut_var$$;

    // When
    auto result = $$on_the_fly_sut_var$$.vesion();

    // Then
    EXPECT_EQ(result, "0.0.1");
}
"""

def generateUnitTest(namespace, classname, needPimpl):
    sutClassName = classname
    if needPimpl:
        sutClassName = generateImpClassname(classname)
    filenamePre = generateFilenamePre(namespace, sutClassName)
    unitTestFileName = filenamePre + ".t.cpp"
    sut_header_file = generateFilenamePre(namespace, sutClassName) + ".h"
    on_the_fly_sut_var = generateOnTheFlyVar(sutClassName)
    content = UNIT_TEST_CONTENT.replace("$$sut_header_file$$", sut_header_file)
    content = content.replace("$$namespace$$", namespace)
    content = content.replace("$$SutClassName$$", sutClassName)
    content = content.replace("$$on_the_fly_sut_var$$", on_the_fly_sut_var)

    return content
        

def generateImpHeaderFile(namespace, classname, authorinfo, date):
    impClassname = generateImpClassname(classname)
    classbrief = "Implementation of " + classname
    content = generateHeaderFile(namespace, impClassname, classbrief, authorinfo, date, needInterface=False, needPimpl=False)
    return content


def generateImpCppFile(namespace, classname, authorinfo, date):
    impClassname = generateImpClassname(classname)
    classbrief = "Implementation of " + classname
    content = generateCppFile(namespace, impClassname, classbrief, authorinfo, date, needPimpl=False)
    return content


def generateMockClassName(classname):
    return classname + "Mock"


MOCK_INCLUDE_FILES= """#include <gmock/gmock.h>

#include <$$interface_header_file$$>

"""

MOCK_CLASS_DECLARE = """
class $$mockClassName$$ : public $$interfaceClassName$$ {
public:
    MOCK_CONST_METHOD0(version, std::string());
};

"""

def generateMockHeaderFile(namespace, classname):
    mockClassName = generateMockClassName(classname)
    interfaceClassName = generateInterfaceClassname(classname)
    interfaceHeaderFile = generateFilenamePre(namespace, interfaceClassName) + ".h"
    mockFileNamePre = generateFilenamePre(namespace, mockClassName)
    content = generateIncludeGuardBegin(mockFileNamePre)
    content = content + MOCK_INCLUDE_FILES.replace("$$interface_header_file$$", interfaceHeaderFile)
    content = content + generateClassHeadCommentBlock(mockClassName, isHeader=True)
    content = content + MOCK_CLASS_DECLARE
    content = content.replace("$$mockClassName$$", mockClassName)
    content = content.replace("$$interfaceClassName$$", interfaceClassName)
    content = content + generateIncludeGuardEnd(mockFileNamePre)
    return content



