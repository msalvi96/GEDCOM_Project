import unittest
from GEDCOMparser import GedcomTree
from GEDCOMparser import Individual
from GEDCOMparser import Family

class GedcomTreeTest (unittest.TestCase):
    """ Test class for Sprint 1 User Stories"""

    def test_us14_multiple_births_fewer_than_6(self):
        """ Check if US14 works properly """

        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        families = sprint1.us14_multiple_births_fewer_than_6(debug=True)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us15_fewer_than_15_siblings(self):
        """ Check if US15 works properly """

        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        families = sprint1.us15_fewer_than_15_siblings(debug=True)
        self.assertIn('@F6@', families)
        self.assertEqual(len(families), 1)

    def test_us30_list_living_married(self):
        """ Check if US30 works properly """

        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us30_list_living_married(pt=False, debug=True)) == 18)
    
    def test_us31_list_living_single(self):
        """ Check if US31 works properly """

        sprint1 = GedcomTree(r'./Mrunal_Salvi_GEDCOM_us14us15.ged', pt=False)
        self.assertTrue(len(sprint1.us31_list_living_single(pt=False, debug=True)) == 25)

    def test_us22_unique_ids(self):
        """ Check if US22 works properly """

        sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=False)
        unique_ids, duplicate_ids = sprint1.us22_unique_ids(debug=True)
        self.assertTrue(len(unique_ids) == 64)
        self.assertTrue(len(duplicate_ids) == 2)
        self.assertFalse(len(duplicate_ids) == 0)

    def test_us16_male_lastname(self):
        """ Check if US16 works properly """
        sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=False)
        error = sprint1.us16_male_lastname(debug=True)
        self.assertTrue(len(error) == 1)

    def test_us33_list_orphans(self):
        """ Check if US33 works properly """

        sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=False)
        orphans = sprint1.us33_list_orphans(debug=True)
        self.assertTrue(len(orphans) == 1)
        self.assertFalse(len(orphans) == 0)

    def test_us38_upcoming_birthdays(self):
        """ Check if US38 works properly """

        sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=False)
        debug_list = sprint1.us38_upcoming_birthdays(pt=False, debug=True)
        for time_delta in debug_list:
            self.assertTrue(time_delta.days < 30)





if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)