#!/bin/env python

import unittest
import os

from users import Users

class TestConf(unittest.TestCase):

    def test_getCurrentUser(self):
        test_username = os.getenv('USER')
        app_username = Users().getCurrentUser().username
        self.assertEqual(app_username, test_username)

if __name__ == '__main__':
    unittest.main()
