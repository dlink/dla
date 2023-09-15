#!/bin/env python

import unittest

from pieces import Pieces, Piece

class TestPieces(unittest.TestCase):

    def test_getAll(self):
        p = Pieces()
        data = p.getAll()
        self.assertTrue(len(data) > 1)

    def test_piece(self):
        p = Piece(1)
        self.assertTrue(1, p.id)

    def test_piece_images(self):
        p = Piece(1)
        filepath1 = '/data/dla/images/pieces/gardian/Guardian.png'
        url1 = 'images/pieces/gardian/Guardian.png'
        self.assertEqual(filepath1, p.images.filepaths[0])
        self.assertEqual(url1, p.images.urls[0])

if __name__ == '__main__':
    unittest.main()
