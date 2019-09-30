import unittest
from GEDCOMparser import GedcomTree
from GEDCOMparser import Individual
from GEDCOMparser import Family


class GedcomTreeTest (unittest.TestCase):
    def test_us14_contains_family(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        families = sprint1.us14_multiple_births_fewer_than_6(pt=False)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us15_contains_family(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        families = sprint1.us15_fewer_than_15_siblings(pt=False)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us30_list_length(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us30_list_living_married(pt=False)) == 18)
    
    def test_us31_list_length(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us31_list_living_single(pt=False)) == 25)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
