"""
Author: Mrunal Salvi
SSW 555 Project 02
Practice Working with GEDCOM Data
"""
import os
# valid = {
#     '0': {
#         'INDI': {
#             '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS'],
#             '2': ['DATE']
#         },
#         'FAM': {
#             '1': ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
#             '2': ['DATE']
#         }
#     }
# }

class GedcomTree:

    valid_dict = {'0': ['INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE'],
            '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
            '2': ['DATE']}

    exception_list = ['FAM', 'INDI']

    def __init__(self, path):
        self.path = path
        self.individuals = dict()
        self.families = dict()

        if not os.path.exists(self.path):
            raise FileNotFoundError

        try:
            fp = open(self.path, 'r')

        except FileNotFoundError:
            print("Cant Open:")

        else:
            with fp:
                for line in fp:
                    line.strip()
                    split_line = line.split(' ', 2)

                    split_line = self.checkExceptionTag(split_line)
                    level, tag, args = self.checkValidTag(split_line)
                    print(f"Level: {level}, Tag: {tag}, Args: {args}")

                    # else:
                        # level, tag, args = line.split(' ', 2)
                        # print(line.split(' ', 2))

                    # print(f'level: {level}  tag: {tag}  args: {args}')

    def checkExceptionTag(self, split_line):
        """ Function to work on exception tags FAM/INDI """

        for value in GedcomTree.exception_list:
            if value in split_line and split_line.index(value) == 2:
                split_line.insert(1, value)
                split_line.pop()

        return split_line

    def checkValidTag(self, split_line):
        """ Function to check valid tags """

        level = split_line[0]
        args = None
        tag = None

        if level in GedcomTree.valid_dict.keys():
            remaining = split_line[1:]

            if len(remaining) == 2 and remaining[0] in GedcomTree.valid_dict[level]:
                tag = remaining[0]
                args = remaining[1]

            elif len(remaining) == 1 and remaining[0] in GedcomTree.valid_dict[level]:
                tag = remaining[0]

        return level, tag, args
            
        
            # if split_line[1] in GedcomTree.valid_dict[level]:
            
        #         return 

        #     else:
        #         split_line.insert(2, 'N')

        # else:
        #     split_line.insert(2, 'N')

        # return split_line
            



class Family:

    def __init__(self):
        pass

class Individual(Family):
    pass
    





if __name__ == "__main__":
    """ Workflow """

    x = GedcomTree(r'./proj02test.ged')
    # new_list = []
    # try:
    #     fp = open(r'./proj02test.ged', 'r')

    # except FileNotFoundError:
    #     print("Cant Open:")

    # else:
    #     with fp:
    #         for line in fp:
    #             # line = line.strip()
    #             for i in range(8):
    #                 print(next(lines).strip())

                # output_line = line.split(' ', 2)             
                # output_line = checkExceptionTag(output_line)
                # output_line = checkValidTag(output_line)
                
                # print(f'<--{"|".join(output_line)}')