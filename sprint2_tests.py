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

    def test_us35_list_recent_births(self):
        """ Check if US35 works properly """

        sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged')
        recent_births = sprint2.us35_list_recent_births(debug=True)
        # self.assertIn('@I16@', recent_births[0])
        self.assertEqual(len(recent_births), 1)
        for time_delta in recent_births:
            self.assertTrue(time_delta.days < 30)

    def test_us36_list_recent_deaths(self):
        """ Check if US36 works properly """

        sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged')
        recent_deaths = sprint2.us36_list_recent_deaths(debug=True)
        # self.assertIn('@I31@', recent_deaths[0])
        self.assertEqual(len(recent_deaths), 1)
        for time_delta in recent_deaths:
            self.assertTrue(time_delta.days < 30)

    def test_us21_correct_gender(self):
        """ Check if all the wrong gender elements are included """

        sprint2 = GedcomTree(r'./GEDCOM_files/U17_21_test.ged')
        wrong_gender_list = sprint2.us21_correct_gender_for_role(debug=True)
        self.assertEqual(len(wrong_gender_list), 4)

    def test_us17_no_child_marry(self):
        """ Check if all the wrong marriage elements are included """

        sprint2 = GedcomTree(r'./GEDCOM_files/U17_21_test.ged')
        wrong_marry_list = sprint2.us17_no_marriage_to_children(debug=True)
        self.assertEqual(len(wrong_marry_list), 3)

    def test_us06_divorce_before_death(self):
        """ Check if User Story 06 Works Properly """

        sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged')
        debug_list = sprint2.us06_divorce_before_death(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn("@I25@", debug_list)
        self.assertIn("@I26@", debug_list)

    def test_us27_include_individual_ages(self):
        """ Check if User Story 27 works properly """
        pass

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)