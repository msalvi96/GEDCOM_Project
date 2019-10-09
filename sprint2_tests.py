import unittest
from gedcom_parser import GedcomTree, Family, Individual

class GedcomTreeTest(unittest.TestCase):
    """ Test class for Sprint 2 User Stories """

    def test_us08_birth_before_marriage_ofParents(self):
        """ Check if US08 works properly """

        sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged')
        debug_list = sprint2.us08_birth_before_marriage_of_parents(debug=True)
        self.assertIn('@I1@', debug_list)
        self.assertIn('@I4@', debug_list)
        self.assertIn('@I2@', debug_list)
        self.assertEqual(len(debug_list), 3)

    def test_us09_birth_before_death_ofParents(self):
        """ Check if US09 works properly  """

        sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged')
        debug_list = sprint2.us09_birth_before_death_of_parents(debug=True)
        self.assertIn('@I16@', debug_list)
        self.assertIn('@I23@', debug_list)
        self.assertIn('@I25@', debug_list)
        self.assertEqual(len(debug_list), 3)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)