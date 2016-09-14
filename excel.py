#!/usr/bin/env python

from MySQLdb import connect
from optparse import OptionParser
from datetime import datetime
import traceback
import MySQLdb.cursors
import xlwt
import xlrd

gConf = {}

def parseOptions():
    version = 1.0
    usage = '''
    usage: ./%prog [options] arg
    examp: ./%prog -h host -t db.table -w sql -o file.xls 
    '''

    parser = OptionParser(version=version, usage=usage)
    parser.add_option('-x', '--execute', dest='EXECUTE', default='download', help='upload or download')
    parser.add_option('-f', '--host', dest='HOST', help='hostname or ip')
    parser.add_option('-u', '--user', dest='USER', help='username default query user')
    parser.add_option('-p', '--password', dest='PSWD', help='password default query password')
    parser.add_option('-d', '--database', dest='DATABASE', help='table name database')
    parser.add_option('-c', '--charset', dest='CHARSET', default='gb2312', help='charset of text')
    parser.add_option('-s', '--db-charset', dest='DBCHARSET', default='latin1', help='charset of connection')
    parser.add_option('-t', '--table', dest='TABLE', help='table name')
    parser.add_option('-w', '--where', dest='WHERE', default=None, help='condition in where')
    parser.add_option('-i', '--infile', dest='INFILE', default='table.xls', help='input file name')
    parser.add_option('-o', '--outfile', dest='OUTFILE', default='table.xls', help='output file name')

    return parser


def download(inCur, inSQL):
    vCur = inCur
    vSQL = inSQL
    vCnt = vCur.execute(vSQL)
    vHeader = tuple([ i[0] for i in vCur.description ])
    vHType = tuple([ i[1] for i in vCur.description ])
    vRecords = vCur.fetchall()
    vColWidMap = gConf['COLWIDTH']

    vBook = xlwt.Workbook()
    vSheet = vBook.add_sheet('sheet1')

    for i, t in enumerate(vHType):
        vColSetWidth = vSheet.col(i)
        vColSetWidth.width = max(vColWidMap[vHType[i]], len(vHeader[i]) + 1) * 256

    for ic, cell in enumerate(vHeader):
        vSheet.write(0, ic, cell)
    
    for ir, row in enumerate(vRecords, 1):
        for ic, cell in enumerate(row):
            if isinstance(cell, datetime):
                cellStr = str(cell)
            elif isinstance(cell, unicode):
                cellStr = cell.encode('raw_unicode_escape').decode(gConf['CHARSET'])
            elif isinstance(cell, str):
                cellStr = cell.strip()
            else:
                cellStr = cell
            vSheet.write(ir, ic, cellStr, gConf['XF'].get(vHType[ic], gConf['XF'][-1]))
    
    vBook.save(gConf['OUTFILE'])


def upload(inCur):
    vCur = inCur
    vWorkbook = xlrd.open_workbook(gConf['INFILE'])
    vSheet = vWorkbook.sheet_by_index(0)
    vRowNum = vSheet.nrows
    vColNum = vSheet.ncols

    vColName = vSheet.row_values(0)
    vSQLFmt = "INSERT INTO {0}.{1} SET ".format(gConf['DATABASE'], gConf['TABLE'])

#    vCnt = vCur.execute('BEGIN')
    print "BEGIN;"
    for r in xrange(1, vRowNum):
        vCurRow = vSQLFmt + ", ".join([ "{0} = '{1}'".format(i, j.strip().encode(gConf['CHARSET'])) if isinstance(j, unicode) else "{0} = {1}".format(i, j) for i, j in zip(vColName, vSheet.row_values(r)) ])
        print vCurRow + ';'
#    vCnt = vCur.execute(vCurRow)        
#    vCnt = vCur.execute('ROLLBACK')


    



parser = parseOptions()
(options, args) = parser.parse_args()

gConf['EXECUTE'] = options.EXECUTE
gConf['HOST'] = options.HOST
gConf['USER'] = options.USER
gConf['PSWD'] = options.PSWD
gConf['DATABASE'] = options.DATABASE
gConf['CHARSET'] = options.CHARSET
gConf['DBCHARSET'] = options.DBCHARSET
gConf['TABLE'] = options.TABLE
gConf['WHERE'] = "WHERE {0}".format(options.WHERE) if options.WHERE else ''
gConf['OUTFILE'] = options.OUTFILE if options.OUTFILE else "{0}.xls".format(options.TABLE)
gConf['INFILE'] = options.INFILE if options.INFILE else "{0}.xls".format(options.TABLE)


gConf['COLWIDTH'] = {2:3, 3:3, 4:3, 7:10, 10:5, 11:5, 12:10, 252:5, 253:10}
gConf['XF'] = { -1:xlwt.easyxf(), 
                7:xlwt.easyxf(num_format_str = 'yyyy-mm-dd hh:mm:ss'),
                10:xlwt.easyxf(num_format_str = 'yyyy-mm-dd hh:mm:ss'),
                11:xlwt.easyxf(num_format_str = 'yyyy-mm-dd hh:mm:ss'),
                12:xlwt.easyxf(num_format_str = 'yyyy-mm-dd hh:mm:ss')
                }

dbConf = {'host':gConf['HOST'], 'port':3306, 'user':gConf['USER'], 'passwd':gConf['PSWD'], 'db':gConf['DATABASE'], 'charset':gConf['DBCHARSET'], 'cursorclass':MySQLdb.cursors.Cursor, 'autocommit':False}


try:
    sdb = connect(host=dbConf['host'], port=dbConf['port'], user=dbConf['user'], passwd=dbConf['passwd'], charset=dbConf['charset'], cursorclass=dbConf['cursorclass'], autocommit=dbConf['autocommit'])
    sdb = connect(**dbConf)
    scur = sdb.cursor()
    
    if gConf['EXECUTE'] == 'download':
        SQL = "SELECT * FROM {0} {1}".format(gConf['TABLE'], gConf['WHERE'])
        download(scur, SQL)
    elif gConf['EXECUTE'] == 'upload':
        upload(scur)
    else:
        print "What on earth do you want ?"

except Exception as e:
    print traceback.print_exc()
finally:
    scur.close()
    sdb.close()




