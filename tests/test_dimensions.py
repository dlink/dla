#!/bin/env python

import unittest
from decimal import Decimal

from dimensions import (display_dimensions, storage_dimensions,
                        std_to_dec, dec_to_std, DimensionsError)

class TestUsers(unittest.TestCase):

    inches = [['5'    , Decimal('5.00')],
              ['5-1/4', Decimal('5.25')],
              ['5-1/2', Decimal('5.5' )],
              ['5-1/2', Decimal('5.50')],
              ['5-3/4', Decimal('5.75')],
              ['5.30' , Decimal('5.30')],
              ]
    feet = [['1', Decimal(12)],
            ['2', Decimal(2*12)],
            ['6', Decimal(6*12)],
            ['10', Decimal(10*12)],
            ]
    mix = [['2\'', Decimal(24.0000)],
           ['2\'1"', Decimal(24.0833)],
           ['2\'2"', Decimal(24.1667)],
           ['2\'3"', Decimal(24.2500)],
           ['2\'4"', Decimal(24.3333)],
           ['2\'5"', Decimal(24.4167)],
           ['2\'6"', Decimal(24.5000)],
           ['2\'7"', Decimal(24.5833)],
           ['2\'8"', Decimal(24.6667)],
           ['2\'9"', Decimal(24.7500)],
           ['2\'10"', Decimal(24.8333)],
           ['2\'11"', Decimal(24.9167)],
           ]
    dimensions = [
        ['12 x 11 x 11 in.', Decimal(12), Decimal(11), Decimal(11), 'in'],
        ['6 x 2 x 2 ft.', Decimal(6*12), Decimal(2*12), Decimal(2*12), 'ft'],
        ['6\'2" x 3\'1" x 1\'9"',
         round(Decimal((6*12)+0.1667), 4),
         round(Decimal((3*12)+0.0833), 4),
         round(Decimal((1*12)+0.7500), 4), 'mix'],
    ]

    def test_display_dimensions(self):
        for std, l, w, h, uom in self.dimensions:
            self.assertEqual(std, display_dimensions(l, w, h, uom))
    def test_display_dimensions_default_uom(self):
        for std, l, w, h, uom in self.dimensions:
            print(l, w, h, ':', display_dimensions(l,w,h))
            self.assertEqual(std, display_dimensions(l, w, h)) #, uom))
    def test_storage_dimensions(self):
        for std, l, w, h, uom in self.dimensions:
            self.assertEqual([l, w, h] , storage_dimensions(std, uom))

    def test_std_to_dec_in(self):
        for std, dec in self.inches:
            self.assertEqual(round(dec, 4), std_to_dec(std))
    def test_std_to_dec_ft(self):
        for std, dec in self.feet:
            self.assertEqual(round(dec, 4), std_to_dec(std, 'ft'))
    def test_std_to_dec_mix(self):
        for std, dec in self.mix:
            self.assertEqual(round(dec, 4), std_to_dec(std, 'mix'))
    def test_std_to_dec_error(self):
        with self.assertRaises(DimensionsError):
            std_to_dec('1\'', 'bad_uom')
        with self.assertRaises(DimensionsError):
            std_to_dec('1', 'mix')

    def test_dec_to_std_in(self):
        for std, dec in self.inches:
            self.assertEqual(std, dec_to_std(dec))
    def test_dec_to_std_ft(self):
        for std, dec in self.feet:
            self.assertEqual(std, dec_to_std(dec, 'ft'))
    def test_dec_to_std_mix(self):
        for std, dec in self.mix:
            self.assertEqual(std, dec_to_std(dec, 'mix'))
    def test_dec_to_std_fail(self):
        with self.assertRaises(DimensionsError):
            dec_to_std(5, 'bad_uom')

if __name__ == '__main__':
    unittest.main()
