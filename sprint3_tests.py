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

    def test_us24_unique_families_by_spouse(self):
        """ Check if User Story 24 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us24_unique_families_by_spouse(debug=True)
        self.assertEqual(len(debug_list), 1)
        self.assertIn('@F15@', debug_list)

    def test_us39_list_upcoming_anniversaries(self):
        """ Check if User Story 39 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us39_list_upcoming_anniversaries(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn('@F1@', debug_list)
        self.assertIn('@F7@', debug_list)

    def test_us29_us29_list_deceased(self):
        """ Check if User Story 29 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us29_list_deceased(debug=True)
        self.assertEqual(len(debug_list), 6)
        self.assertIn('@I7@', debug_list)
        self.assertIn('@I8@', debug_list)

    def test_us10_marry_after_14(self):
        """ Check if User Story 10 works properly """

        sprint3 = GedcomTree(r'./GEDCOM_files/Sprint3_test_GEDCOM.ged')
        debug_list = sprint3.us10_marry_after_14(debug=True)
        self.assertEqual(len(debug_list), 5)
        self.assertIn('@I3@', debug_list)
        self.assertIn('@I17@', debug_list)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
