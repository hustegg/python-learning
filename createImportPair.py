#!/usr/bin/env python

import xlrd
import xlwt
import sys
import traceback
from ipaddress import IPv4Address, IPv4Network
from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import abspath, basename
from operator import itemgetter

gConf = {}

def parseArgs():
    desc = u"""
    Please confirm that :
    1. module xlrd, xlwt are available
    2. excel format witten as follow:
        --------------------------------------------------------
        | IP\u5730\u5740 | \u56fa\u8d44\u53f7/\u8bbe\u5907\u540d\u79f0 |  \u7f51\u6bb5\u540d\u79f0  |   \u673a\u67b6\u540d\u79f0   |
        --------------------------------------------------------
        | ${ip1} | ${machine id1}  | ${subnet1} | ${shelf id1} |
        --------------------------------------------------------
        | ${ip2} | ${machine id2}  | ${subnet2} | ${shelf id1} |
        --------------------------------------------------------
        | ${ip3} | ${machine id3}  | ${subnet3} | ${shelf id2} |
        --------------------------------------------------------
        .
        .
        .

    """.encode('gb2312')
    parser = ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--srcFile', dest='SRCFILE', required=True, help="xls source file")
    parser.add_argument('-p', '--pairMode', dest='PAIRMODE', action='store_true', help="create pairing machine list as appendix in sheet 'pair' which should be removed before loading with sheet 'bachelor'")
    parser.add_argument('-s', '--simple', dest='SIMPLE', action='store_true', default=False, help="peers may take risk by shelf failure while both stay on the same shelf")

    return parser
    
class EmptyMachineList(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EmptyMachinePair(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class shelfList(object):
    def __init__(self, simple=False):
        self.simple = simple
        self._items = []
        self._items.append([])
    
    def __getitem__(self, index):
        if index < 0:
            if index + self.__len__() < 0:
                raise IndexError
            else:
                return self._items[index]
        return self._items[index + 1]

    def __len__(self):
        return self._items.__len__() - 1

    def __resort__(self):
        self._items[0].sort(key=itemgetter(1), reverse=True)

    def __iter__(self):
        return self

    def append(self, mList):
        if not isinstance(mList, machineList):
            raise ValueError
        self._items.append(mList)
        self._items[0].append([self._items.__len__() - 1, mList._items[0]])
        self.__resort__()

    def pop(self):
        if len(self._items[0]) < 2 or not (self._items[0][0][1][0] > 0 and self._items[0][1][1][0] > 0):
            if self.simple and self._items[0][0][1][0] >= 2:
                _p1 = self._items[self._items[0][0][0]].pop()
                _p2 = self._items[self._items[0][0][0]].pop()
                return (_p1, _p2)
            else:
                raise EmptyMachinePair('No machine in pair')
        _p1 = self._items[self._items[0][0][0]].pop()
        _p2 = self._items[self._items[0][1][0]].pop()
        self.__resort__()
        return (_p1, _p2)
 
    def next(self):
        if len(self._items[0]) < 2 or not (self._items[0][0][1][0] > 0 and self._items[0][1][1][0] > 0):
            if self.simple and self._items[0][0][1][0] >= 2:
                _p1 = self._items[self._items[0][0][0]].pop()
                _p2 = self._items[self._items[0][0][0]].pop()
                return (_p1, _p2)
            else:
                raise StopIteration
        _p1 = self._items[self._items[0][0][0]].pop()
        _p2 = self._items[self._items[0][1][0]].pop()
        self.__resort__()
        return (_p1, _p2)
 
    def bachelor(self):
        if len(self._items[0]) > 1 and reduce(lambda x, y: x+y, [ i[1][0] for i in self._items[0] ][1:]) != 0:
            raise StopIteration('NOT NOW')
        for m in self._items[self._items[0][0][0]]:
            yield m



class machineList(object):
    def __init__(self):
        self._items = [[0]]

    def __getitem__(self, index):
        if index < 0:
            if index + self.__len__() < 0:
                raise IndexError
            else:
                return self._items[index]
        return self._items[index + 1]

    def __len__(self):
        return self._items.__len__() - 1

    def __iter__(self):
        return self

    def append(self, value):
        self._items.append(value)
        self._items[0][0] = self.__len__()

    def pop(self):
        if self._items[0][0] < 1:
            raise EmptyMachineList("No machine left")
        _p = self._items.pop()
        self._items[0][0] = self.__len__()
        return _p

    def next(self):
        if self._items[0][0] < 1:
            raise StopIteration
        _p = self._items.pop()
        self._items[0][0] = self.__len__()
        return _p


class machinePair(object):
    def __init__(self, inFile, simple=False):
        self.simple = simple
        self.srcFile = inFile
        self.colWidth = 256 * 16
        self.dstFile = abspath(''.join(basename(inFile).split('.')[:-1]) + '.output.xls')
        self.srcBook = xlrd.open_workbook(self.srcFile)
        self.dstBook = xlwt.Workbook()
        self.srcSheet = self.srcBook.sheet_by_index(0)
        self.dstSheet = self.dstBook.add_sheet(u'\u7533\u8bf7\u5185\u7f51IP')
        self.vSrcHeader = self.srcSheet.row_values(0)
        self.vPairHeader = self.vSrcHeader * 2
        self.vBachelorHeader = self.vSrcHeader
        self.vDstHeader = (u'\u56fa\u8d44\u7f16\u53f7/\u5185\u7f51IP', u'\u7533\u8bf7IP\u4e2a\u6570', u'vlan\u5207\u6362', u'\u7533\u8bf7\u4e3aVIP', u'\u5bb9\u707e\u670d\u52a1\u5668\u56fa\u8d44\u53f7', u'\u6307\u5b9aIP', u'\u6307\u5b9a\u7f51\u6bb5', u'IP\u5c5e\u6027')
        self.srcRowNum = self.srcSheet.nrows
        self.srcColNum = self.srcSheet.ncols
        self.machineList = []
        self.machineBucket = {}
        self.machineApply = [self.vDstHeader]
        self.machinePair = [self.vPairHeader]
        self.machineBachelor = [self.vBachelorHeader]
        self.machineLeft = []
        self.reqNum = 1
        self.isVlanChange = u'\u5426'
        self.isVip = u'\u662f'
        self.specIp = None
        self.ipAttr = None

    def alignHeader(self, vSheet, vHeader):
        for i in range(len(vHeader)):
            _colSetWidth = vSheet.col(i)
            _colSetWidth.width = self.colWidth


    def creatMachineBucket(self):
        for i in xrange(1, self.srcSheet.nrows):
            ip, mid, subnet, shelfid = self.srcSheet.row_values(i, 0, 4)
            self.machineList.append(tuple((IPv4Address(ip), mid, IPv4Network(subnet), shelfid)))
            self.machineList.sort(key=itemgetter(2,3,0))

        self.srcBook.release_resources()

        for machine in self.machineList:
            if not self.machineBucket.has_key(machine[2]):
                self.machineBucket[machine[2]] = shelfList(self.simple)

            if len(self.machineBucket[machine[2]]) < 1 or (machine[3] != self.machineBucket[machine[2]][-1][-1][3] and not self.simple):
                mList = machineList()
                mList.append(machine)
                self.machineBucket[machine[2]].append(mList)
                self.machineBucket[machine[2]].__resort__()
            else:
                self.machineBucket[machine[2]][-1].append(machine)
                self.machineBucket[machine[2]].__resort__()


    def creatMachinePair(self):

        for subnet in self.machineBucket:
            for _p1, _p2 in self.machineBucket[subnet]:
                self.machineApply.append((str(_p1[0]), self.reqNum, self.isVlanChange, self.isVip, _p2[1], self.specIp, str(_p2[2]), self.ipAttr))
                self.machinePair.append((str(_p1[0]), _p1[1], str(_p1[2]), _p1[3], str(_p2[0]), _p2[1], str(_p2[2]), _p2[3]))

            for _p1 in self.machineBucket[subnet].bachelor():
                self.machineBachelor.append((str(_p1[0]), _p1[1], str(_p1[2]), _p1[3]))

        print "\nAll machine pair [{0}/{1}] created.".format((len(self.machineApply) - 1) * 2, self.srcRowNum - 1)
        print "\nOutput file located at {0}.".format(self.dstFile)
        print "\nFollowing machines left [{0}] without peer :\n".format(len(self.machineBachelor) - 1)
        for singleDog in self.machineBachelor[1:]:
            print singleDog
        print "\n"

        self.alignHeader(self.dstSheet, self.vDstHeader)
        for ir, row in enumerate(self.machineApply):
            for ic, cell in enumerate(row):
                self.dstSheet.write(ir, ic, cell)

        if gConf['PAIRMODE']:
            self.pairSheet = self.dstBook.add_sheet('pair')
            self.bachelorSheet = self.dstBook.add_sheet('bachelor')
            self.alignHeader(self.pairSheet, self.vPairHeader)
            self.alignHeader(self.bachelorSheet, self.vBachelorHeader)
            for ir, row in enumerate(self.machinePair):
                for ic, cell in enumerate(row):
                    self.pairSheet.write(ir, ic, cell)
        
            for ir, row in enumerate(self.machineBachelor):
                for ic, cell in enumerate(row):
                    self.bachelorSheet.write(ir, ic, cell)



        self.dstBook.save(self.dstFile)



if __name__ == '__main__':

    parser = parseArgs()
    options = parser.parse_args()
    gConf['SRCFILE'] = options.SRCFILE
    gConf['PAIRMODE'] = options.PAIRMODE
    gConf['SIMPLE'] = options.SIMPLE

    m = machinePair(gConf['SRCFILE'], simple=gConf['SIMPLE'])
    m.creatMachineBucket()
    m.creatMachinePair()

