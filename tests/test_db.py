#!/bin/env python

import unittest

from vlib import db

class TestDb(unittest.TestCase):    

    def test_query(self):
        db_ = db.getInstance()
        sql = 'select id from pieces where id = 1'
        results = db_.query(sql)
        self.assertEqual(1, results[0]['id'])
        
if __name__ == '__main__':
    unittest.main()
