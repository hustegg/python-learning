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
    desc = u'''
    Please confirm that :
    1. module xlrd, xlwt are available
    2. excel format witten as follow:
        ---------------------------------------
        |    \u56fa\u8d44\u7f16\u53f7    | \u5185\u7f51IP |   \u7f51\u6bb5    |
        ---------------------------------------
        | ${machine id1} | ${ip1} | ${subnet1}|
        ---------------------------------------
        | ${machine id2} | ${ip2} | ${subnet2}|
        ---------------------------------------
        | ${machine id3} | ${ip3} | ${subnet3}|
        ---------------------------------------
        .
        .
        .

    '''

    parser = ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--srcFile', dest='SRCFILE', required=True, help="xls source file")
    parser.add_argument('-p', '--pairMode', dest='PAIRMODE', action='store_true', help="create pairing machine list as appendix in sheet 'pair'")

    return parser
    


class machinePair(object):
    def __init__(self, inFile):
        self.srcFile = inFile
        self.colWidth = 256 * 16
        self.dstFile = abspath(''.join(basename(inFile).split('.')[:-1]) + '.output.xls')
        self.srcBook = xlrd.open_workbook(self.srcFile)
        self.dstBook = xlwt.Workbook()
        self.pairBook = xlwt.Workbook()
        self.srcSheet = self.srcBook.sheet_by_index(0)
        self.dstSheet = self.dstBook.add_sheet(u'\u7533\u8bf7\u5185\u7f51IP')
        self.pairSheet = self.dstBook.add_sheet('pair')
        self.vSrcHeader = self.srcSheet.row_values(0)
        self.vPairHeader = self.vSrcHeader * 2
        self.vDstHeader = (u'\u56fa\u8d44\u7f16\u53f7/\u5185\u7f51IP', u'\u7533\u8bf7IP\u4e2a\u6570', u'vlan\u5207\u6362', u'\u7533\u8bf7\u4e3aVIP', u'\u5bb9\u707e\u670d\u52a1\u5668\u56fa\u8d44\u53f7', u'\u6307\u5b9aIP', u'\u6307\u5b9a\u7f51\u6bb5', u'IP\u5c5e\u6027')
        self.srcRowNum = self.srcSheet.nrows
        self.srcColNum = self.srcSheet.ncols
        self.machineList = []
        self.machinePair = [self.vPairHeader]
        self.machineApply = [self.vDstHeader]
        self.machineLeft = []
        self.reqNum = 1
        self.isVlanChange = u'\u5426'
        self.isVip = u'\u662f'
        self.specIp = None
        self.ipAttr = None

        for sheet in (self.dstSheet, self.pairSheet):
            for i in range(max(len(self.vPairHeader), len(self.vDstHeader))):
                _colSetWidth = sheet.col(i)
                _colSetWidth.width = self.colWidth


    def getMachineList(self):
        for i in xrange(1, self.srcSheet.nrows):
            mid, ip, subnet = self.srcSheet.row_values(i, 0, 3)
            self.machineList.append(tuple((mid, IPv4Address(ip), IPv4Network(subnet))))
        self.srcBook.release_resources()


    def putMachinePair(self):

        self.machineList.sort(key=itemgetter(2,1))
        while self.machineList:
            try:
                if self.machineList[0][2] == self.machineList[1][2]:
                    _p1 = self.machineList.pop(0)
                    _p2 = self.machineList.pop(0)
                    self.machineApply.append((str(_p1[1]), self.reqNum, self.isVlanChange, self.isVip, _p2[0], self.specIp, str(_p2[2]), self.ipAttr))
                    self.machinePair.append((_p1[0], str(_p1[1]), str(_p1[2]), _p2[0], str(_p2[1]), str(_p2[2])))
                else:
                    _p1 = self.machineList.pop(0)
                    self.machineLeft.append(_p1)
                    self.machinePair.append((_p1[0], str(_p1[1]), str(_p1[2])))
            except IndexError as e:
                _p1 = self.machineList.pop(0)
                self.machineLeft.append(_p1)
                self.machinePair.append((_p1[0], str(_p1[1]), str(_p1[2])))
                print "\nAll machine pair [{0}/{1}] created.".format((len(self.machineApply) - 1) * 2, self.srcRowNum - 1)
                print "Output file located at {0}.".format(self.dstFile)
            except Exception as e:
                print traceback.format_exc()
                sys.exit(1)
 
        for ir, row in enumerate(self.machineApply):
            for ic, cell in enumerate(row):
                self.dstSheet.write(ir, ic, cell)

        if gConf['PAIRMODE']:
            for ir, row in enumerate(self.machinePair):
                for ic, cell in enumerate(row):
                    self.pairSheet.write(ir, ic, cell)

        self.dstBook.save(self.dstFile)



if __name__ == '__main__':

    parser = parseArgs()
    options = parser.parse_args()
    gConf['SRCFILE'] = options.SRCFILE
    gConf['PAIRMODE'] = options.PAIRMODE

    m = machinePair(gConf['SRCFILE'])
    m.getMachineList()
    m.putMachinePair()

    print "\nFollowing machine left [{0}] without peer :".format(len(m.machineLeft))
    for i in m.machineLeft:
        print i
    print "\n"
