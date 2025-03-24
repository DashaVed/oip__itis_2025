import unittest

from boolean_search_hw3 import boolean_search
from inverted_index_hw3 import build_inverted_index


class BooleanSearchTest(unittest.TestCase):
    def setUp(self):
        self.inverted_index = build_inverted_index()

    def test_simple(self):
        result = boolean_search("шершавый", self.inverted_index)
        self.assertEqual(result, {"70", "34"})

    def test_operator_and(self):
        result = boolean_search("антоцианы AND белые", self.inverted_index)
        self.assertEqual(result, {"11", "100", "85"})

    def test_operator_or(self):
        result = boolean_search("фиолетовый OR анцупова", self.inverted_index)
        self.assertEqual(result, {"35", "99", "36", "79"})

    def test_operator_not(self):
        result = boolean_search("NOT истод", self.inverted_index)
        self.assertEqual(result, set([str(i) for i in range(2, 121)]) - {"98", "99"})

    def test_operator_and_not(self):
        result = boolean_search("ангины AND (NOT генеративные)", self.inverted_index)
        self.assertEqual(result, {"94"})

    def test_complex_query(self):
        result = boolean_search("(ива AND ивы) OR (прямые AND прутовидная) OR неглубоко", self.inverted_index)
        self.assertEqual(result, {"96", "91", "92", "9"})

    def test_complex_query2(self):
        result = boolean_search("(ива OR ивы) AND (NOT прямые)", self.inverted_index)
        self.assertEqual(result, {"94", "93", "91", "95"})

    def test_complex_query3(self):
        result = boolean_search("(трудов OR (ивы AND триандрин)) AND (NOT прямые)", self.inverted_index)
        self.assertEqual(result, {"90", "89"})

    def test_complex_query4(self):
        result = boolean_search("(трудов OR (ивы AND триандрин) OR веток) AND (NOT прямые)", self.inverted_index)
        self.assertEqual(result, {"90", "89", "94", "93", "95"})
