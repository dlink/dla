#!/bin/env python

import unittest
from decimal import Decimal

from dimensions import std_to_dec, dec_to_std

class TestUsers(unittest.TestCase):

    numbers = [['5-1/4', Decimal(5.25)],
               ['5-1/2', Decimal(5.5)],
               ['5-3/4', Decimal(5.75)],
               ['5.30', Decimal(5.3)],
               ]
    def test_std_to_dec(self):
        for std, dec in self.numbers:
            self.assertEqual(round(dec, 2), std_to_dec(std))

    def test_dec_to_std(self):
        print()
        for std, dec in self.numbers:
            self.assertEqual(std, dec_to_std(dec))

if __name__ == '__main__':
    unittest.main()
