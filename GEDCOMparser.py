"""
Author: Mrunal Salvi
SSW 555 Project 03
Analysing GEDCOM Data
"""
import os
from datetime import datetime
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

    def __init__(self, path, pt=False):
        self.path = path
        self.individuals = dict()
        self.families = dict()
        self.raw_data = []
        self.comment_log = []
        self.error_log = []
        self.indi_table = PrettyTable()
        self.fam_table = PrettyTable()

        if not os.path.exists(self.path):
            raise FileNotFoundError

        try:
            fp = open(self.path, 'r')

        except FileNotFoundError:
            print("Cant Open:")

        else:
            with fp:
                for line in fp:
                    line = line.strip('\n')
                    split_line = line.split(' ', 2)

                    split_line = self.checkExceptionTag(split_line)
                    valid_line = self.checkValidTag(split_line)
                
        self.data_processing()

        if pt:

            self.indi_table.field_names = Individual.table_header
            for indis in self.individuals.values():
                self.indi_table.add_row(indis.pt_row())

            print(f'Individual Summary:\n{self.indi_table}')


            self.fam_table.field_names = Family.table_header
            for fam in self.families.values():
                self.fam_table.add_row(fam.pt_row())


            print(f'Family Summary: \n{self.fam_table}')


    @staticmethod
    def checkExceptionTag(split_line):
        """ Function to work on exception tags FAM/INDI """

        for value in GedcomTree.exception_list:
            if value in split_line and split_line.index(value) == 2:
                split_line.insert(1, value)
                split_line.pop()

        return split_line


    def checkValidTag(self, split_line):
        """ Function to check valid tags """

        level = split_line[0]
        if level in GedcomTree.valid_dict.keys():
            if split_line[1] in GedcomTree.valid_dict[level]:
                self.raw_data.append(split_line)

            else:
                self.error_log.append(split_line)

        else:
            self.error_log.append(split_line)

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
                while len(line) == 3 and line[0] == '0' and line[1] == "INDI":
                    indi = Individual(line[2])  #creating new individual with id in line
                    self.individuals[line[2]] = indi    #store object in 'individuals' dictionary with key as id and value as object
                    line = next(data_iter)

                    while line[0] != '0':   #loop until next line level becomes 0
                        if line[0] == '1' and line[1] in GedcomTree.indi_dict.keys():
                            if line[1] in ('DEAT', 'BIRT'):
                                second_line = next(data_iter)  
                                setattr(indi, GedcomTree.indi_dict[line[1]], datetime.strptime(second_line[2], '%d %b %Y')) #set individual attribute

                            else:
                                setattr(indi, GedcomTree.indi_dict[line[1]], line[2]) #set individual attribute

                        line = next(data_iter)

                #while loop to iterate over FAM tags
                while len(line) == 3 and line[0] == '0' and line[1] == "FAM":
                    family = Family(line[2]) #creating new family with id in line
                    self.families[line[2]] = family #store object in 'families' dictionary with key as id and value as object
                    line = next(data_iter)

                    while line[0] != '0':   #loop until next line level becomes 0
                        if line[0] == '1' and line[1] in GedcomTree.fam_dict.keys():
                            if line[1] in ('MARR', 'DIV'):
                                second_line = next(data_iter)
                                setattr(family, GedcomTree.fam_dict[line[1]], datetime.strptime(second_line[2], '%d %b %Y')) #set familiy attributes

                            elif line[1] in ('HUSB', 'WIFE'):
                                setattr(family, GedcomTree.fam_dict[line[1]], self.individuals[line[2]]) #assign 'individual' objects to family properties

                            elif line[1] in ('CHIL'):
                                family.children.append(self.individuals[line[2]]) # append children list using individual objects.

                            line = next(data_iter)


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

    @property
    def age(self):
        if self.birth_date:
            age = datetime.today() - self.birth_date if not self.death_date else self.death_date - self.birth_date
            return (age.days + age.seconds // 86400) // 365
        else:
            return 'No birth date.'

    @property
    def alive(self):
        alive = True
        if self.death_date:
            alive = False

        return alive

    def pt_row(self):
        return [self.indi_id, self.name, self.sex, self.birth_date.strftime("%Y-%m-%d"), self.age, self.alive, self.death_date.strftime("%Y-%m-%d") if self.death_date else 'NA', self.fam_c, self.fam_s]


if __name__ == "__main__":
    """ Workflow """

    x = GedcomTree(r'./Mrunal_Salvi_GEDCOM.ged', pt=True)