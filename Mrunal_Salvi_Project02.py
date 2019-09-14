"""
Author: Mrunal Salvi
SSW 555 Project 02
Practice Working with GEDCOM Data
"""
import itertools

raw_data = []

def checkValidTag(split_line):
    """ Function to check valid tags """

    valid_dict = {'0': ['INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE'],
                '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
                '2': ['DATE']}

    level = split_line[0]
    
    if level in valid_dict.keys():
        if split_line[1] in valid_dict[level]:
            # split_line.insert(2, 'Y')
            raw_data.append(split_line)

        else:
            split_line.insert(2, 'N')

    else:
        split_line.insert(2, 'N')

    return split_line


def checkExceptionTag(split_line):
    """ Function to work on exception tags FAM/INDI """

    exception_list = ['FAM', 'INDI']
    
    for value in exception_list:
        if value in split_line and split_line.index(value) == 2:
            split_line.insert(1, value)
            split_line.pop()

    return split_line




if __name__ == "__main__":
    """ Workflow """

    try:
        fp = open(r'./proj02test.ged', 'r')

    except FileNotFoundError:
        print("Cant Open:")

    else:
        with fp:
            for line in fp:
                line = line.strip()

                # print(f'-->{line}')

                output_line = line.split(' ', 2)             
                output_line = checkExceptionTag(output_line)
                output_line = checkValidTag(output_line)
                
            for i, j, k in iter(raw_data):
                print(i, j, k)
                # level = i[0]
                # tag = i[1]
                # if level == '0' and tag in ('IND', 'FAM'):


            # for group, lines in itertools.groupby(fp, lambda l: l.startswith("0")):
            #     print (group, list(lines))
