#!/bin/env python

import unittest

from pieces import Pieces

class TestPieces(unittest.TestCase):

    def test_getAll(self):
        p = Pieces()
        data = p.getAll()
        self.assertTrue(len(data) > 1)

if __name__ == '__main__':
    unittest.main()
