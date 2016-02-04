import nameIterator as nmi
import jankyTerminal as janky
import unittest


class TestnameIterator(unittest.TestCase):
    """docstring for TestnameIterator"""

    def test_iterateDevice(self):
        self.assertEqual(nmi.iterateDevice(
            "test_chip234_device123.txt"), "test_chip234_device124.txt")

    def test_iterateChip(self):
        self.assertEqual(nmi.iterateChip(
            "test_chip234_device123.txt"), "test_chip235_device1.txt")


class TestjankyTerminal(unittest.TestCase):
    """docstring for TestjankyTerminal"""

    def test_handler(self):
        self.assertEqual(janky.handler('q', 'test'), ("nosave", False))
        self.assertEqual(
            janky.handler('c', 'test_chip234_device123.txt'),
            ('test_chip235_device1.txt', True))
        self.assertEqual(
            janky.handler('d','test_chip234_device123.txt'),
            ('test_chip234_device124.txt', True))
