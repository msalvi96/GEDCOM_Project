"""
Author: Mrunal Salvi
SSW 555 Project 03
Analysing GEDCOM Data
"""
import os
import datetime
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
            
            indi_table = self.pretty_print(Individual.table_header, self.individuals.values())
            print(f'Individual Summary:\n{indi_table}')

            fam_table = self.pretty_print(Family.table_header, self.families.values())
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
                    self.individuals[line[2]] = indi    #store object in 'individuals' dictionary with key as id and value as object
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
                    self.families[line[2]] = family #store object in 'families' dictionary with key as id and value as object
                    line = next(data_iter)

                    while line[0] != '0':   #loop until next line level becomes 0
                        family.data_lines.append(line) #for storing corresponding line numbers
                        if line[0] == '1' and line[1] in GedcomTree.fam_dict.keys():
                            if line[1] in ('MARR', 'DIV'):
                                second_line = next(data_iter)
                                family.data_lines.append(second_line) #for storing corresponding line numbers
                                setattr(family, GedcomTree.fam_dict[line[1]], datetime.datetime.strptime(second_line[2], '%d %b %Y')) #set familiy attributes

                            elif line[1] in ('HUSB', 'WIFE'):
                                setattr(family, GedcomTree.fam_dict[line[1]], self.individuals[line[2]]) #assign 'individual' objects to family properties

                            elif line[1] in ('CHIL'):
                                family.children.append(self.individuals[line[2]]) # append children list using individual objects.

                            line = next(data_iter)

    @staticmethod
    def pretty_print(fields, data_rows):
        """ Method to print pretty tables """
        
        table = PrettyTable()
        table.field_names = fields
        for row in data_rows:
            table.add_row(row.pt_row())

        return table

    def us14_multiple_births_fewer_than_6(self, pt=False):
        """ User Story 14 - No more than 5 siblings should be born at a time """

        birthday_list = []
        checked_birthdays = []
        for family in self.families.values():
            for child in family.children:
                for individual in self.individuals.values():
                    if individual.indi_id == child.indi_id:
                        birthday_list.append(individual.birth_date)
            for bday in birthday_list:
                if birthday_list.count(bday) > 5 and checked_birthdays.count(bday) == 0 and pt:
                    print(f'ERROR: FAMILY: US014: '+family.fam_id+': '+str(birthday_list.count(bday))+' children born on same day.')
                    checked_birthdays.append(bday)
            birthday_list.clear()
            checked_birthdays.clear()

    def us15_fewer_than_15_siblings(self, pt=False):
        """ User Story 15 - There should be fewer than 15 children in a family """

        for family in self.families.values():
            if len(family.children) >= 15:
                if pt:
                    print(f'ERROR: FAMILY: US015: '+family.fam_id+': Family has '+str(len(family.children))+' children.')

    def us33_list_orphans(self, pt=False):
        """ User Story 33 - List all orphaned children (both parents dead and child < 18 years old) """
        
        orphan_list = []
        for family in self.families.values():
            if family.husband.death_date and family.wife.death_date and len(family.children) != 0:
                for child in family.children:
                    if child.age < 18:
                        orphan_list.append(child)
                
        if pt:
            orphan_table = self.pretty_print(Individual.table_header, orphan_list)
            print(f'Summary of Orphans: \n{orphan_table}')

        return orphan_list

    def us38_upcoming_birthdays(self, pt=False):
        """ User Story 38 - List all living people whose birthdays occur in the next 30 days """
        
        upcoming_birthday_list = []
        time_delta = datetime.timedelta(days=30)
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.birthday >= GedcomTree.current_date and individual.birthday <= (GedcomTree.current_date + time_delta):
                    upcoming_birthday_list.append(individual)

        if pt:
            birthday_table = self.pretty_print(Individual.table_header, upcoming_birthday_list)
            print(f'Upcoming Birthdays: \n{birthday_table}')

        return upcoming_birthday_list

    def us30_list_living_married(self, pt=False):
        """ User story 30 list living married Author: Weihan Xu"""

        living_married_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s != 'NA':
                    living_married_list.append(individual)
        
        if pt:
            living_married_table = self.pretty_print(Individual.table_header, living_married_list)
            print(f'Living Married: \n{living_married_table}')
            print(f'There are {len(living_married_list)} living married')
        
        return living_married_list

    def us31_list_living_single(self, pt=False):
        """ User story 31 list living single Author: Weihan Xu"""

        living_single_list = []
        for individual in self.individuals.values():
            if not individual.death_date:
                if individual.fam_s == 'NA':
                    living_single_list.append(individual)

        if pt:
            living_single_table = self.pretty_print(Individual.table_header, living_single_list)
            print(f'Living Single: \n{living_single_table}')
            print(f'There are {len(living_single_list)} living single')

        return living_single_list

    def us22_Unique_IDs(self, pt=False):
        """ US-22: All individual IDs should be unique and all family IDs should be unique, 
        Author: Vineet Singh """

        ind_id = list()
        dup_id_val = list()
        for indiv in self.individuals:
            ind_id.append(indiv)
        
        dup_indiv_id = [item for item, count in collections.Counter(ind_id).items() if count > 1]
        if len(dup_indiv_id) != 0:
            for indiv in self.individuals.values():
                for i in dup_indiv_id:
                    if indiv.ind_id == i:
                        dup_id_val.append(indiv)

        if pt:
            dup_indiv_table = self.pretty_print(Individual.table_header, dup_id_val)
            print(f'Individual information with duplicate id: \n{dup_indiv_table}')

        fam_id = list()
        dup_fam_val = list()
        for fam in self.families:
            fam_id.append(fam)
        
        dup_fam_id = [item for item, count in collections.Counter(fam_id).items() if count > 1]
        if len(dup_fam_id) != 0:
            for fam in self.families.values():
                for i in dup_fam_id:
                    if fam.fam_id == i:
                        dup_fam_val.append(fam)

        if pt:
            dup_fam_table = self.pretty_print(Individual.table_header, dup_fam_val)
            print(f'Family information with duplicate id: \n{dup_fam_table}')

        return len(dup_indiv_id), len(dup_fam_id)


    def us16_male_lastname(self, pt=False, debug=False):
        """ US-22: All male members of a family should have the same last name, 
        Author: Vineet Singh """

        error_list = list()
        for family in self.families.values():
            f_lastName = family.husband.last_name
            for children in family.children:
                if children.sex == 'M':
                    if children.last_name == f_lastName:
                        continue
                    else:
                        error_list.append(family.fam_id)
                        self.error_log.append('ERROR: FAMILY: US016: ' + family.fam_id + 
                        ': Family male do not have same last name')

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
    
    def pt_row(self):
        return [self.fam_id, self.marriage_date.strftime("%Y-%m-%d") if self.marriage_date else 'NA', self.divorced, self.husband.indi_id, self.husband.name, self.wife.indi_id, self.wife.name, [child.indi_id for child in self.children]]

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
    def first_name(self):
        if self.name and len(self.name.split('/')) >= 2:
            name = self.name.split('/')
            first_name = name[0]
            return first_name
    
    @property
    def last_name(self):
        if self.name and len(self.name.split('/')) >= 2:
            name = self.name.split('/')
            last_name = name[1]
            return last_name
            

    def pt_row(self):
        return [self.indi_id, self.name, self.sex, self.birth_date.strftime("%Y-%m-%d"), self.age, self.alive, self.death_date.strftime("%Y-%m-%d") if self.death_date else 'NA', self.fam_c, self.fam_s]


if __name__ == "__main__":
    """ Workflow """

    sprint1 = GedcomTree(r'./Sprint1_test_GEDCOM.ged', pt=True)

    ms_us33 = sprint1.us33_list_orphans(pt=True)
    ms_us38 = sprint1.us38_upcoming_birthdays(pt=True)
    sprint1.us14_multiple_births_fewer_than_6(pt=True)
    sprint1.us15_fewer_than_15_siblings(pt=True)
    sprint1.us30_list_living_married(pt=True)
    sprint1.us31_list_living_single(pt=True)
    

