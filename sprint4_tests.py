import unittest
from gedcom_parser import GedcomTree, Family, Individual

class GedcomTreeTest(unittest.TestCase):
    """ Test class for Sprint 2 User Stories """

    def test_us04_marriage_after_divorce(self):
        """ Check if User Story 04 works properly """

        sprint4 = GedcomTree(
            r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us04_marriage_after_divorce(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn("@I32@", debug_list)
        self.assertIn("@I30@", debug_list)

    def test_us05_marriage_before_death(self):
        """ Check if User Story 05 works properly """

        sprint4 = GedcomTree(
            r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us05_marriage_before_death(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn("@I7@", debug_list)
        self.assertIn("@I8@", debug_list)

    def test_us19_first_cousins_should_not_marry(self):
        """ Check if User Story 19 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us19_first_cousins_should_not_marry(debug=True)
        self.assertEqual(len(debug_list), 2)
        self.assertIn("@F15@", debug_list)
        self.assertIn("@F16@", debug_list)

    def test_us42_reject_illegitimate_dates(self):
        """ Check if User Story 42 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us42_reject_illegitimate_dates(debug=True)
        self.assertEqual(len(debug_list), 6)
        self.assertIn("@I31@", debug_list)
        self.assertIn("@I32@", debug_list)
        self.assertIn("@F13@", debug_list)
        self.assertIn("@F15@", debug_list)
        self.assertIn("@F16@", debug_list)

    def test_us23_unique_name_and_birth_date(self):
        """ Check if User Story 23 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        bug_number = sprint4.us23_unique_name_and_birth_date(debug=True)
        self.assertEqual(bug_number, 1)
        
    def test_us07_less_than_150_years_old(self):
        """ Check if User Story 07 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us07_less_than_150_years_old(debug=True)
        self.assertEqual(len(debug_list), 1)
        self.assertIn("@I7@", debug_list)
        

    def test_us11_no_bigamy(self):
        """ Check if User Story 11 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us11_no_bigamy(debug=True)
        self.assertEqual(len(debug_list), 4)
        self.assertIn("@I6@", debug_list)
        self.assertIn("@I13@", debug_list)
        self.assertIn("@I19@", debug_list)

    def test_us40_include_input_line_numbers(self):
        """ Check if User Story 40 works properly """

        sprint4 = GedcomTree(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged', pt=False, write=False)
        debug_list = sprint4.us40_include_input_line_numbers(debug=True)

        with open(r'./GEDCOM_files/Sprint4_test_GEDCOM.ged') as fp:
            for index, line in enumerate(fp):
                pass

        total_lines = index + 1

        for line_numbers in debug_list:
            self.assertTrue(0 < line_numbers)
            self.assertTrue(line_numbers < total_lines)
            self.assertFalse(line_numbers <= 0)
            self.assertFalse(line_numbers > total_lines)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
