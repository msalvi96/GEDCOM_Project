"""
Authors: Mrunal Salvi, David Ovsiew, Vineet Singh, Weihan Xu
SSW 555
Analysing GEDCOM Data
"""
import os
import datetime
import uuid
from prettytable import PrettyTable

class GedcomTree:
    """ GEDCOM Tree class to process and store data from GEDCOM files """

    valid_dict = {'0': ['INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE'],
                  '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
                  '2': ['DATE']}

    exception_list = ['FAM', 'INDI']

    indi_dict = {
        'NAME': 'name',
        'SEX': 'sex',
        'BIRT': 'birth_date',
        'DEAT': 'death_date',
        'FAMC': 'fam_c',
        'FAMS': 'fam_s'
    }

    fam_dict = {
        'MARR': 'marriage_date',
        'HUSB': 'husband',
        'WIFE': 'wife',
        'DIV': 'divorce_date',
        'CHIL': 'children',
    }

    current_date = datetime.datetime.today()
    date_format = "%Y-%m-%d"

    def __init__(self, path, pt=False, write=False):
        self.path = path
        self.individuals = dict()
        self.families = dict()
        self.raw_data = []
        self.comment_log = []
        self.error_log = []
        self.invalid_tags = []
        self.write_to_file = []

        if not os.path.exists(self.path):
            raise FileNotFoundError

        try:
            fp = open(self.path, 'r')

        except FileNotFoundError:
            print("Cant Open:")

        else:
            with fp:
                for index, line in enumerate(fp):
                    line = line.strip('\n')
                    split_line = line.split(' ', 2)

                    split_line = self.check_exception_tag(split_line)
                    valid_line = self.check_valid_tag(index, split_line)

        self.data_processing()

        indi_data_rows = [indi.pt_row() for indi in self.individuals.values()]
        indi_table = self.pretty_print(Individual.table_header, indi_data_rows)

        family_data_rows = []
        for fam in self.families.values():
            if fam.husband:
                husband_id = fam.husband

            if fam.wife:
                wife_id = fam.wife

            for individual in self.individuals.values():
                if husband_id == individual.indi_id:
                    husband_name = individual.name

                if wife_id == individual.indi_id:
                    wife_name = individual.name

            family_data_rows.append([fam.fam_id, fam.marriage_date.strftime(GedcomTree.date_format) if fam.marriage_date else 'NA', fam.divorced, husband_id, husband_name, wife_id, wife_name, [child for child in fam.children]])
        fam_table = self.pretty_print(Family.table_header, family_data_rows)

        if pt:
            print(f'Individual Summary:\n{indi_table}')
            print(f'Family Summary: \n{fam_table}')

        if write:
            indi_header = "Individual Summary:"
            self.write_to_file.append([indi_header, indi_table])
            fam_header = "Family Summary:"
            self.write_to_file.append([fam_header, fam_table])


    @staticmethod
    def check_exception_tag(split_line):
        """ Function to work on exception tags FAM/INDI """

        for value in GedcomTree.exception_list:
            if value in split_line and split_line.index(value) == 2:
                split_line.insert(1, value)
                split_line.pop()

        return split_line


    def check_valid_tag(self, index, split_line):
        """ Function to check valid tags """

        level = split_line[0]
        if level in GedcomTree.valid_dict.keys():
            if split_line[1] in GedcomTree.valid_dict[level]:
                self.raw_data.append((*split_line, index))

            else:
                self.invalid_tags.append((*split_line, index))

        else:
            self.invalid_tags.append((*split_line, index))

        return split_line

    def data_processing(self):
        """ Function to process the raw data and assign individuals and families to data structure. """

        data_iter = iter(self.raw_data)

        while True:
            try:
                line = next(data_iter)

            except StopIteration:
                break

            else:

                #Conditional statement for comment lines
                if line[0] == '0' and line[1] in ('HEAD', 'TRLR', 'NOTE'):
                    self.comment_log.append(line)

                #While loop to iterate over INDI tags
                while len(line) == 4 and line[0] == '0' and line[1] == "INDI":

                    indi = Individual(line[2])  #creating new individual with id in line
                    indi.data_lines.append(line) #for storing corresponding line numbers
                    self.individuals[uuid.uuid4()] = indi    #store object in 'individuals' dictionary with key as id and value as object
                    line = next(data_iter)

                    while line[0] != '0':   #loop until next line level becomes 0
                        indi.data_lines.append(line) #for storing corresponding line numbers
                        if line[0] == '1' and line[1] in GedcomTree.indi_dict.keys():
                            if line[1] in ('DEAT', 'BIRT'):
                                second_line = next(data_iter)
                                indi.data_lines.append(second_line) #for storing corresponding line numbers
                                setattr(indi, GedcomTree.indi_dict[line[1]], datetime.datetime.strptime(second_line[2], '%d %b %Y')) #set individual attribute

                            else:
                                setattr(indi, GedcomTree.indi_dict[line[1]], line[2]) #set individual attribute

                        line = next(data_iter)

                #while loop to iterate over FAM tags
                while len(line) == 4 and line[0] == '0' and line[1] == "FAM":
                    family = Family(line[2]) #creating new family with id in line
                    family.data_lines.append(line) #for storing corresponding line number
                    self.families[uuid.uuid4()] = family #store object in 'families' dictionary with key as id and value as object
                    line = next(data_iter)

                    while line[0] != '0':   #loop until next line level becomes 0
                        family.data_lines.append(line) #for storing corresponding line numbers
                        if line[0] == '1' and line[1] in GedcomTree.fam_dict.keys():
                            if line[1] in ('MARR', 'DIV'):
                                second_line = next(data_iter)
                                family.data_lines.append(second_line) #for storing corresponding line numbers
                                setattr(family, GedcomTree.fam_dict[line[1]], datetime.datetime.strptime(second_line[2], '%d %b %Y')) #set familiy attributes

                            elif line[1] in ('HUSB', 'WIFE'):
                                setattr(family, GedcomTree.fam_dict[line[1]], line[2]) #assign 'individual' objects to family properties

                            elif line[1] == 'CHIL':
                                family.children.append(line[2]) # append children list using individual objects.

                            line = next(data_iter)

    @staticmethod
    def pretty_print(fields, data_rows):
        """ Method to print pretty tables """

        table = PrettyTable()
        table.field_names = fields
        if len(data_rows) != 0:
            for row in data_rows:
                table.add_row(row)

            return table

        return "No data"

    def log_error(self, error_type, entity_type, user_story, line_number, entity_id, error_string):
        """ Method to log errors in a GEDCOM file """

        if error_type in ("ERROR", "ANOMALY"):
            if entity_type in ("FAMILY", "INDIVIDUAL"):
                self.error_log.append(f'{error_type}: {entity_type}: {user_story}: {line_number}: {entity_id}: {error_string}')

    def us14_multiple_births_fewer_than_6(self, debug=False):
        """ User Story 14 - No more than 5 siblings should be born at a time """

        family_list = []
        for family in self.families.values():
            birthday_list = []
            checked_birthdays = []
            for child in family.children:
                for individual in self.individuals.values():
                    if individual.indi_id == child:
                        birthday_list.append(individual.birth_date)

            for bday in birthday_list:
                if birthday_list.count(bday) > 5 and checked_birthdays.count(bday) == 0:
                    checked_birthdays.append(bday)
                    family_list.append(family.fam_id)
                    self.log_error("ERROR", "FAMILY", "US14", family.line_number["CHIL"][0][1], family.fam_id, f"{birthday_list.count(bday)} children born on the same day")

        if debug:
            return family_list

    def us15_fewer_than_15_siblings(self, debug=False):
        """ User Story 15 - There should be fewer than 15 children in a family """

        family_list = []
        for family in self.families.values():
            if len(family.children) >= 15:
                family_list.append(family.fam_id)
                self.log_error("ERROR", "FAMILY", "US15", family.line_number["CHIL"][0][1], family.fam_id, f"Family has {len(family.children)} children")
        if debug:
            return family_list

    def us33_list_orphans(self, pt=False, debug=False, write=False):
        """ User Story 33 - List all orphaned children (both parents dead and child < 18 years old) """

        orphan_list = []
        for family in self.families.values():
            if family.husband and family.wife:
                for individual in self.individuals.values():
                    if family.husband == individual.indi_id:
                        husband = individual

                    if family.wife == individual.indi_id:
                        wife = individual

                if husband.death_date and wife.death_date and len(family.children) != 0:
                    for child in family.children:
                        for individual in self.individuals.values():
                            if child == individual.indi_id:
                                child_indi = individual

                        if child_indi.age < 18:
                            orphan_list.append(child_indi.pt_row())

        orphan_table = self.pretty_print(Individual.table_header, orphan_list)

        if pt:
            print(f'Summary of Orphans: \n{orphan_table}')

        if debug:
            return orphan_list

        if write:
            orphan_header = "Summary of Orphans:"
            self.write_to_file.append([orphan_header, orphan_table])

    def us38_upcoming_birthdays(self, pt=False, debug=False, write=False):
        """ User Story 38 - List all living people whose birthdays occur in the next 30 days """

        upcoming_birthday_list = []
        debug_list = []
        time_delta = datetime.timedelta(days=30)
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.birthday >= GedcomTree.current_date and individual.birthday <= (GedcomTree.current_date + time_delta):
                    upcoming_birthday_list.append(individual.pt_row())
                    debug_list.append(individual.birthday - GedcomTree.current_date)

        birthday_table = self.pretty_print(Individual.table_header, upcoming_birthday_list)

        if pt:
            print(f'Upcoming Birthdays: \n{birthday_table}')

        if debug:
            return debug_list

        if write:
            birthday_header = "Upcoming Birthdays:"
            self.write_to_file.append([birthday_header, birthday_table])

    def us30_list_living_married(self, pt=False, debug=False, write=False):
        """ User story 30 list living married Author: Weihan Xu"""

        living_married_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s != 'NA':
                    living_married_list.append(individual.pt_row())

        living_married_table = self.pretty_print(Individual.table_header, living_married_list)

        if pt:
            print(f'Living Married: \n{living_married_table}')

        if debug:
            return living_married_list

        if write:
            living_header = "Living Married:"
            self.write_to_file.append([living_header, living_married_table])

    def us31_list_living_single(self, pt=False, debug=False, write=False):
        """ User story 31 list living single Author: Weihan Xu"""

        living_single_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s == 'NA':
                    living_single_list.append(individual.pt_row())

        living_single_table = self.pretty_print(Individual.table_header, living_single_list)

        if pt:
            print(f'Living Single: \n{living_single_table}')

        if debug:
            return living_single_list

        if write:
            single_header = "Living Single:"
            self.write_to_file.append([single_header, living_single_table])

    def us22_unique_ids(self, debug=False):
        """ User story 22 - All individual and family ids should be unique """

        unique_indi_ids = []
        unique_fam_ids = []
        overall_unique_ids = []
        overall_duplicate_ids = []
        for individual in self.individuals.values():
            if individual.indi_id in unique_indi_ids:
                self.log_error("ERROR", "INDIVIDUAL", "US22", individual.line_number["INDI"], individual.indi_id, f"{individual.indi_id} already exists.")
                overall_duplicate_ids.append(individual.indi_id)
            else:
                unique_indi_ids.append(individual.indi_id)
                overall_unique_ids.append(individual.indi_id)
        for family in self.families.values():
            if family.fam_id in unique_fam_ids:
                self.log_error("ERROR", "FAMILY", "US22", family.line_number["FAM"], family.fam_id, f"{family.fam_id} already exists.")
                overall_duplicate_ids.append(individual.indi_id)
            else:
                unique_fam_ids.append(family.fam_id)
                overall_unique_ids.append(individual.indi_id)

        if debug:
            return overall_unique_ids, overall_duplicate_ids

    def us16_male_lastname(self, debug=False):
        """ User Story 16 - All male members in a family should have the same last name """

        error_list = []
        for family in self.families.values():
            children_individual = []
            if family.husband:
                for individual in self.individuals.values():
                    if family.husband == individual.indi_id:
                        husband_last_name = individual.full_name["lastName"]
                        break
                if husband_last_name and len(family.children) != 0:
                    for child_id in family.children:
                        for individual in self.individuals.values():
                            if child_id == individual.indi_id:
                                children_individual.append(individual)

                    for child in children_individual:
                        child_last_name = child.full_name["lastName"]
                        if child.sex == 'M':
                            if child_last_name != husband_last_name:
                                self.log_error("ERROR", "FAMILY", "US16", family.line_number["CHIL"][0][1], family.fam_id, f"Child with id {child.indi_id} does not have the same last name as parent")
                                error_list.append(family)

        if debug:
            return error_list

    def us08_birth_before_marriage_of_parents(self, debug=False):
        """ User Story 08 - Children should be born after marriage of parents and not more than 9 months after their divorce """

        debug_list = []
        for family in self.families.values():
            if family.marriage_date:
                children_list = []

                for individual in self.individuals.values():
                    for children in family.children:
                        if individual.indi_id == children:
                            children_list.append(individual)

                for child in children_list:
                    if child.birth_date < family.marriage_date:
                        self.log_error("ANOMALY", "FAMILY", "US08", family.line_number["CHIL"][0][1], family.fam_id, f"Child with id {child.indi_id} born {child.birth_date.strftime(GedcomTree.date_format)} before marriage of parents on {family.marriage_date.strftime(GedcomTree.date_format)}")
                        debug_list.append(child.indi_id)
                    if family.divorced and child.birth_date > (family.divorce_date + datetime.timedelta(9*365/12)):
                        self.log_error("ANOMALY", "FAMILY", "US08", family.line_number["CHIL"][0][1], family.fam_id, f"Child with id {child.indi_id} born {child.birth_date.strftime(GedcomTree.date_format)} after the divorce of parents on {family.divorce_date.strftime(GedcomTree.date_format)}")
                        debug_list.append(child.indi_id)

        if debug:
            return debug_list

    def us09_birth_before_death_of_parents(self, debug=False):
        """ User Story 09 - Children should be born before death of mother and before 9 months after death of father """

        debug_list = []
        for family in self.families.values():
            if family.husband and family.wife and len(family.children) != 0:
                children_list = []

                for individual in self.individuals.values():
                    if individual.indi_id == family.husband:
                        husband = individual

                    if individual.indi_id == family.wife:
                        wife = individual

                    for children in family.children:
                        if individual.indi_id == children:
                            children_list.append(individual)

                for child in children_list:
                    if wife.death_date and child.birth_date > wife.death_date:
                        self.log_error("ANOMALY", "FAMILY", "US09", family.line_number["CHIL"][0][1], family.fam_id, f"Child with id {child.indi_id} born {child.birth_date.strftime(GedcomTree.date_format)} after mother's death on {wife.death_date.strftime(GedcomTree.date_format)}")
                        debug_list.append(child.indi_id)

                    if husband.death_date and child.birth_date > (husband.death_date + datetime.timedelta(9*365/12)):
                        self.log_error("ANOMALY", "FAMILY", "US09", family.line_number["CHIL"][0][1], family.fam_id, f"Child with id {child.indi_id} born {child.birth_date.strftime(GedcomTree.date_format)} more than 9 months after father's death on {husband.death_date.strftime(GedcomTree.date_format)}")
                        debug_list.append(child.indi_id)

        if debug:
            return debug_list

    def us27_include_individual_ages(self, pt = True, debug=False):
        """ User Story 27 - Include person's current age when listing individuals """

        indi_detail_list = list()
        table_header = ['ID', 'Name', 'Age']
        for individual in self.individuals.values():
            indi_detail_list.append([individual.indi_id, individual.name, individual.age])

        indi_table = self.pretty_print(table_header, indi_detail_list)

        if pt:
            print(f'Individuals with age: \n{indi_table}')

    def us06_divorce_before_death(self, pt = True, debug=False):
        """ User Story 27 - Divorce can only occur before death of both spouses """

        divorcee_details = list()
        table_header = ['Husband', 'H_Alive', 'Wife', 'W_Alive', 'Divorced']
        for family in self.families.values():
            if family.divorced:
                for individual_h in self.individuals.values():
                    if individual_h.indi_id == family.husband and individual_h.alive == True:
                        for individual_w in self.individuals.values():
                            if individual_w.indi_id == family.wife and individual_w.alive == True:
                                divorcee_details.append([individual_h.name, individual_h.alive, individual_w.name, individual_w.alive, family.divorced])

        divorcee_table = self.pretty_print(table_header, divorcee_details)

        if pt:
            print(f'Divorced couple details: \n{divorcee_table}')

class Family:
    """ Family class to initialize family information """

    table_header = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']

    def __init__(self, fam_id):
        """ Initialise properties for family object """

        self.fam_id = fam_id
        self.marriage_date = None
        self.divorce_date = None
        self.husband = None
        self.wife = None
        self.children = []
        self.data_lines = []

    @property
    def line_number(self):
        """ Associate GEDCOM source line numbers with family object """

        data_iter = iter(self.data_lines)
        line_dict = {}
        child_array = []
        for line in data_iter:
            if line[1] in ('FAM', 'HUSB', 'WIFE'):
                line_dict[line[1]] = line[3]

            elif line[1] in ('MARR', 'DIV'):
                second_line = next(data_iter)
                line_dict[line[1]] = second_line[3]

            elif line[1] == 'CHIL':
                child_array.append((line[2], line[3]))

        line_dict['CHIL'] = child_array
        return line_dict

    @property
    def divorced(self):
        """ Define family objecct property divorced """

        divorced = False
        if self.divorce_date:
            divorced = True

        return divorced

class Individual:
    """ Individual class to initialize individual information """

    table_header = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']

    def __init__(self, indi_id):
        """ Initialize properties of Individual object """

        self.indi_id = indi_id
        self.name = ''
        self.sex = ''
        self.birth_date = None
        self.death_date = None
        self.fam_c = 'NA'
        self.fam_s = 'NA'
        self.data_lines = []

    @property
    def line_number(self):
        """ Associate GEDCOM source lines with Individual object """

        data_iter = iter(self.data_lines)
        line_dict = {}

        for line in data_iter:
            if line[1] in ('INDI', 'NAME', 'SEX', 'FAMC', 'FAMS'):
                line_dict[line[1]] = line[3]

            elif line[1] in ('BIRT', 'DEAT'):
                second_line = next(data_iter)
                line_dict[line[1]] = second_line[3]

        return line_dict

    @property
    def age(self):
        """ Associate age with Individual object """

        if self.birth_date:
            age = GedcomTree.current_date - self.birth_date if not self.death_date else self.death_date - self.birth_date
            return (age.days + age.seconds // 86400) // 365

    @property
    def alive(self):
        """ Set alive status to true or false """

        alive = True
        if self.death_date:
            alive = False

        return alive

    @property
    def birthday(self):
        """ Set birthday for the individual """

        if self.birth_date:
            birthday = datetime.datetime(GedcomTree.current_date.year, self.birth_date.month, self.birth_date.day)
            return birthday

    @property
    def full_name(self):
        """ Split the name of Individual and have two properties in full_name i.e firstName and lastName """

        if self.name and len(self.name.split('/')) >= 2:
            name = [x.strip() for x in self.name.split('/')]
            return {'firstName': name[0], 'lastName': name[1]}

    def pt_row(self):
        """ Returns a list of relevant data of the Individual for PrettyTable """

        return [self.indi_id, self.name, self.sex, self.birth_date.strftime("%Y-%m-%d"), self.age, self.alive, self.death_date.strftime("%Y-%m-%d") if self.death_date else 'NA', self.fam_c, self.fam_s]

def sprint1_main():
    """ Main function to run Sprint 1 User Stories """

    sprint1 = GedcomTree(r'./GEDCOM_files/Sprint1_test_GEDCOM.ged', pt=True)
    sprint1.us16_male_lastname()
    sprint1.us22_unique_ids()
    sprint1.us14_multiple_births_fewer_than_6()
    sprint1.us15_fewer_than_15_siblings()
    sprint1.us31_list_living_single(pt=True)
    sprint1.us30_list_living_married(pt=True)
    sprint1.us38_upcoming_birthdays(pt=True)
    sprint1.us33_list_orphans(pt=True)

    for errors in sprint1.error_log:
        print(errors)

    write = False

    if write:
        try:
            fp = open(r'./test_results/sprint1_results.txt', 'w')

        except FileNotFoundError:
            print("Can't Open!")
        else:
            with fp:
                sprint = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=False, write=True)
                sprint.us14_multiple_births_fewer_than_6()
                sprint.us15_fewer_than_15_siblings()
                sprint.us33_list_orphans(write=True)
                sprint.us38_upcoming_birthdays(write=True)
                sprint.us30_list_living_married(write=True)
                sprint.us31_list_living_single(write=True)
                sprint.us22_unique_ids()
                sprint.us16_male_lastname()

                for i in sprint.write_to_file:
                    for content in i:
                        fp.write(f'{str(content)}\n')

                for errors in sprint.error_log:
                    fp.write(f'{errors}\n')

def sprint2_main():
    """ Main function to run Sprint 2 User Stories """

    sprint2 = GedcomTree(r'./GEDCOM_files/Sprint2_test_GEDCOM.ged', pt=True)
    sprint2.us08_birth_before_marriage_of_parents()
    sprint2.us09_birth_before_death_of_parents()

    print('Error Log:')
    for errors in sprint2.error_log:
        print(f'{errors}\n')

if __name__ == "__main__":
    sprint2_main()
