#!/usr/bin/python

import sqlite3
import sys
import os

outTable = "MyTable"
outFile = "myDb.sqlite3"
inFile = sys.argv[1]

def readLine(f):
    l = f.readline()
    if not l:
        return None
    return l.strip()

def findSep(line):
    separators = [',', ';', '|']
    maxCnt = 0
    sep = None
    for s in separators:
        l = line.split(s)
        if len(l) > maxCnt:
            sep = s
    return sep

def quote(cols):
    return map(lambda x: "'" + x.strip() "'", cols)

def format(line, sep):
    cols = line.split(sep)
    cols = quote(cols)
    cols = ','.join(cols)
    return cols

with open(inFile) as f:
    head = readLine(f)
    sep = findSep(head)

    os.unlink(outFile)
    conn = sqlite3.connect(outFile)
    curs = conn.cursor()

    head = format(head, sep)

    curs.execute('CREATE TABLE IF NOT EXISTS %s (%s)' % (outTable, head))

    while True:
        vals = readLine(f)
        if not vals:
            break
        vals = format(vals, sep)
        curs.execute('INSERT INTO %s VALUES (%s)' % (outTable, vals))
        conn.commit()

conn.close()
