import unittest
from GEDCOMparser import GedcomTree
from GEDCOMparser import Individual
from GEDCOMparser import Family


class GedcomTreeTest (unittest.TestCase):
    def test_us30_list_length(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us30_list_living_married(pt=False)) == 18)
    
    def test_us31_list_length(self):
        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us31_list_living_single(pt=False)) == 25)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
