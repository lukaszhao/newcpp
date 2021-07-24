#!python


from typing import ForwardRef


def generateMemberVar(classname):
    memberVar = "m_"
    if len(classname) > 0:
        memberVar = memberVar + classname[0].lower()
    if len(classname) > 1:
        memberVar = memberVar + classname[1:]
    return memberVar


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
    return "#include <" + filenamepre + ".h>\n"

def generateIncludeFiles(namespace, classname, needInterface, needPimpl):
    includeBlock = ""
    if needInterface:
        includeBlock = includeBlock + includeInterfaceHeader(namespace, classname)
    else:
        includeBlock = includeBlock + "#include <string>\n"
    if needPimpl:
        includeBlock = includeBlock + "#include <memory>\n"
    if len(includeBlock) != 0:
        includeBlock = includeBlock + "\n"
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
    std::shared_ptr<$$impclassname$$> $$impMemberVar$$;

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
