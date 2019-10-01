"""
Author: Mrunal Salvi
SSW 555 Project 03
Analysing GEDCOM Data
"""
import os
import datetime
from prettytable import PrettyTable
import uuid


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

    def __init__(self, path, pt=False):
        self.path = path
        self.individuals = dict()
        self.families = dict()
        self.raw_data = []
        self.comment_log = []
        self.error_log = []
        self.invalid_tags = []

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

                    split_line = self.checkExceptionTag(split_line)
                    valid_line = self.checkValidTag(index, split_line)
                
        self.data_processing()

        if pt:
            
            indi_data_rows = [indi.pt_row() for indi in self.individuals.values()]
            indi_table = self.pretty_print(Individual.table_header, indi_data_rows)
            print(f'Individual Summary:\n{indi_table}')

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
            print(f'Family Summary: \n{fam_table}')


    @staticmethod
    def checkExceptionTag(split_line):
        """ Function to work on exception tags FAM/INDI """

        for value in GedcomTree.exception_list:
            if value in split_line and split_line.index(value) == 2:
                split_line.insert(1, value)
                split_line.pop()

        return split_line


    def checkValidTag(self, index, split_line):
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

                            elif line[1] in ('CHIL'):
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

        else:
            return "No data"

    def log_error(self, error_type, entity_type, user_story, line_number, entity_id, error_string):
        """ Method to log errors in a GEDCOM file """

        if error_type == "ERROR":
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

    def us33_list_orphans(self, pt=False, debug=False):
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
                
        if pt:
            orphan_table = self.pretty_print(Individual.table_header, orphan_list)
            print(f'Summary of Orphans: \n{orphan_table}')

        if debug:
            return orphan_list

    def us38_upcoming_birthdays(self, pt=False, debug=False):
        """ User Story 38 - List all living people whose birthdays occur in the next 30 days """
        
        upcoming_birthday_list = []
        debug_list = []
        time_delta = datetime.timedelta(days=30)
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.birthday >= GedcomTree.current_date and individual.birthday <= (GedcomTree.current_date + time_delta):
                    upcoming_birthday_list.append(individual.pt_row())
                    debug_list.append(individual.birthday - GedcomTree.current_date)

        if pt:
            birthday_table = self.pretty_print(Individual.table_header, upcoming_birthday_list)
            print(f'Upcoming Birthdays: \n{birthday_table}')

        if debug:
            return debug_list

    def us30_list_living_married(self, pt=False, debug=False):
        """ User story 30 list living married Author: Weihan Xu"""

        living_married_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s != 'NA':
                    living_married_list.append(individual.pt_row())
        
        if pt:
            living_married_table = self.pretty_print(Individual.table_header, living_married_list)
            print(f'Living Married: \n{living_married_table}')

        if debug:
            return living_married_list

    def us31_list_living_single(self, pt=False, debug=False):
        """ User story 31 list living single Author: Weihan Xu"""

        living_single_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s == 'NA':
                    living_single_list.append(individual.pt_row())

        if pt:
            living_single_table = self.pretty_print(Individual.table_header, living_single_list)
            print(f'Living Single: \n{living_single_table}')

        if debug:
            return living_single_list

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
                                self.log_error("ERROR", "FAMILY", "US16", family.line_number["CHIL"][0][1], {family.fam_id}, f"Child with id {child.indi_id} does not have the same last name as parent")
                                error_list.append(family)
        
        if debug:
            return error_list

class Family:
    """ Family class to initialize family information """

    table_header = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']

    def __init__(self, fam_id):
        self.fam_id = fam_id
        self.marriage_date = None
        self.divorce_date = None
        self.husband = None
        self.wife = None
        self.children = []
        self.data_lines = []

    @property
    def line_number(self):
        data_iter = iter(self.data_lines)
        line_dict = {}
        child_array = []
        for line in data_iter:
            if line[1] in ('FAM', 'HUSB', 'WIFE'):
                line_dict[line[1]] = line[3]

            elif line[1] in ('MARR', 'DIV'):
                second_line = next(data_iter)
                line_dict[line[1]] = second_line[3]

            elif line[1] in ('CHIL'):
                child_array.append((line[2], line[3]))

        line_dict['CHIL'] = child_array
        return line_dict

    @property
    def divorced(self):
        divorced = False
        if self.divorce_date:
            divorced = True

        return divorced
    
class Individual:
    """ Individual class to initialize individual information """

    table_header = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']

    def __init__(self, indi_id):
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
        if self.birth_date:
            age = GedcomTree.current_date - self.birth_date if not self.death_date else self.death_date - self.birth_date
            return (age.days + age.seconds // 86400) // 365
        else:
            return 'No birth date.'

    @property
    def alive(self):
        alive = True
        if self.death_date:
            alive = False

        return alive

    @property
    def birthday(self):
        if self.birth_date:        
            birthday = datetime.datetime(GedcomTree.current_date.year, self.birth_date.month, self.birth_date.day)
            return birthday

    @property
    def full_name(self):
        if self.name and len(self.name.split('/')) >= 2:
            name = [x.strip() for x in self.name.split('/')]
            return {'firstName': name[0], 'lastName': name[1]}

    def pt_row(self):
        return [self.indi_id, self.name, self.sex, self.birth_date.strftime("%Y-%m-%d"), self.age, self.alive, self.death_date.strftime("%Y-%m-%d") if self.death_date else 'NA', self.fam_c, self.fam_s]


if __name__ == "__main__":
    """ Workflow """

    sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=True)

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