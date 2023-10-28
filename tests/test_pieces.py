#!/bin/env python

import unittest

from pieces import Pieces, Piece

class TestPieces(unittest.TestCase):

    def test_getAll(self):
        p = Pieces()
        data = p.get()
        self.assertTrue(len(data) > 1)

    def test_piece(self):
        p = Piece(1)
        self.assertTrue(1, p.id)

    def test_piece_images(self):
        p = Piece(1)
        filepath1 = '/data/dla/images/pieces/guardian/orig/Guardian.png'
        url1 = 'images/pieces/guardian/display/Guardian.png'
        self.assertEqual(filepath1, p.images.filepaths[0])
        self.assertEqual(url1, p.images.display_urls[0])

if __name__ == '__main__':
    unittest.main()
