#!/usr/bin/env python

import sys
import os.path
import re
import types
from optparse import OptionParser

def parse_options():
    version = 1.0
    usage = '''
    usage: ./%prog [options] args
    examp: ./%prog -s D -t C [-f file_name | -c notation_chars]
    '''
    parser = OptionParser(version=version, usage=usage)
    parser.add_option('-s', '--source-major', dest='srcMajor', default='', help='original major')
    parser.add_option('-t', '--target-major', dest='tgtMajor', default='', help='target major you need')
    parser.add_option('-f', '--from-file', dest='fileName', default='', help='file name of notation')
    parser.add_option('-c', '--notation-chars', dest='noteChars', default='', help='notation chars')
    return parser

def pout(s):
    print s + ' ',

def mkOctets(octStr):
    if not octStr:
        return None

    octList = [ i for i in octStr.split(' ') if i ]

    return octList

def parseNote(octElem):
    if octElem in monoChars:
        return octElem
        
    numNote = int(re.search(r'[1-7]', octElem).group())
    cSharp = octElem.count('#')
    cFall = octElem.count('b')
    cAdd = octElem.count('+')
    cDash = octElem.count('-')

    note = gapMap[numNote - 1] + 1*cSharp + (-1)*cFall + 12*cAdd + (-12)*cDash

    return note

def modNote(note):
    
    note -= valMajorMod
    return note

def baseTone(tone):
    for t in reversed(gapMap):
        if tone >= t:
            return t


def displayNote(note):
    
    locNote = note % 12
    numNote = baseTone(locNote)
    cSharp = locNote - numNote
    cAdd = max(note / 12, 0)
    cDash = abs(min(note / 12, 0))
    return cAdd*'+' + cDash*'-' + cSharp*'#' + str(gapMap.index(numNote) + 1)


def checkMajor(wMajor):
    if not valMajorMap.has_key(wMajor):
        return False

    return True


def checkNote(octElem):
    cchar = {}
    if octElem in monoChars:
        return True

    for i in octElem:
        if i not in validChars:
            return False
        if cchar.has_key(i):
            cchar[i] += 1
        else:
            cchar[i] = 1

    for k, v in cchar.items():
        if v > 1 and k not in polyChars:
            return False

    return True


if __name__ == '__main__':

    parser = parse_options()
    (options, args) = parser.parse_args()
    srcMajor = options.srcMajor.upper()
    tgtMajor = options.tgtMajor.upper()
    fileName = options.fileName
    noteChars = options.noteChars

    octOrig = ""
    octList = []
    srcNoteList = []
    tgtNoteList = []
    monoChars = ('0', '-', '|')
    polyChars = ('+', '-')
    validChars = ('0', '1', '2', '3', '4', '5', '6', '7', '+', '-', '#', 'b', '|')
    valMajorMap = {'C':0, 'D':2, 'E':4, 'F':6, 'G':8, 'A':10, 'B':12}
    gapMap = (0, 2, 4, 5, 7, 9, 11)
    valSrcMajor = valMajorMap[srcMajor]
    valTgtMajor = valMajorMap[tgtMajor]
    valMajorMod = valTgtMajor - valSrcMajor

    if not checkMajor(srcMajor) or not checkMajor(tgtMajor):
        pout("Invalid Major %s -> %s", srcMajor, tgtMajor)
        sys.exit(1)

    if os.path.isfile(fileName):
        with open(fileName, 'r') as f:
            octOrig = f.read()
    elif noteChars:
        octOrig = noteChars
    else:
        pout("Invalid input")
        sys.exit(1)

    octList = [ str(i) for i in octOrig.split(' ') if checkNote(str(i)) ]

    for oct in octList:
        srcNoteList.append(parseNote(oct))

    for note in srcNoteList:
        if type(note) is types.IntType:
            tgtNoteList.append(modNote(note))
        else:
            tgtNoteList.append(note)
    
    for note in tgtNoteList:
        if not type(note) is types.IntType:
            pout(note)
        else:
            pout(displayNote(note))
