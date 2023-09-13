#!/bin/env python

from vlib import db

def tests():
    ddb = db.getInstance()
    print('Test Connection')
    results = ddb.query('show tables')
    print(f'show tables: {results}')
    print()

    print('Test Singleton')
    ddb2 = db.getInstance()
    check = id(ddb) == id(ddb2)
    print(f'ddb1 instance: {id(ddb)}')
    print(f'ddb2 instance: {id(ddb2)}, check: {check}')
    print()

tests()
