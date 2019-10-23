import unittest
from gedcom_parser import GedcomTree, Family, Individual

class GedcomTreeTest(unittest.TestCase):
    """ Test class for Sprint 2 User Stories """

    def test_us25_unique_first_names_inFamilies(self):
        """ Check if User Story 25 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us25_unique_first_names_inFamilies(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn('@F8@', debug_list)
        self.assertIn('@F10@', debug_list)

    def test_us18_siblings_should_not_marry(self):
        """ Check if User Story 18 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us18_siblings_should_not_marry(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn('@F6@', debug_list)
        self.assertIn('@F14@', debug_list)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)