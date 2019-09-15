"""
Author: Mrunal Salvi
SSW 555 Project 02
Practice Working with GEDCOM Data
"""
raw = []

def checkValidTag(split_line):
    """ Function to check valid tags """
    

    valid_dict = {'0': ['INDI', 'FAM', 'HEAD', 'TRLR', 'NOTE'],
                '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
                '2': ['DATE']}

    level = split_line[0]

    if level in valid_dict.keys():
        if split_line[1] in valid_dict[level]:
            split_line.insert(2, 'Y')
            raw.append(split_line)

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

                

                output_line = line.split(' ', 2)             
                output_line = checkExceptionTag(output_line)
                output_line = checkValidTag(output_line)
                
#                 print(f'<--{"|".join(output_line)}')
                # raw.append(output_line)
    
    data_iter = iter(raw)
    while True:
        new = next(data_iter)
        if new[0] == '0' and new[1] == 'INDI':
            print(new)

        if new[0] != '0' and new[1] != 'INDI':
            print(new)
    
#     for i in data_iter:
# #         print(i)
#         if i[0] == '0' and (i[1] == "INDI" or i[1] == "FAM"):
# #             further = True
# #             print(i)
#             while True:
#                 new = next(data_iter)
#                 if new[0] != '0' and (new[1] != "INDI" or new[1] != "FAM"):
#                     print(new[0], new[1])

#                 elif new[0] == '0' and (new[1] == "INDI" or new[1] == "FAM"):
#                     break

#                 else:
#                     continue
#             while next(data_iter)[0] != '0':
#                 print(next(data_iter))

# class Individual:

#     def __init__(self):
#         self.id = ''
#         self.name = ''


# x = Individual()
# x['id'] = '1024'
# x['name'] = 'mrunal'
# print(x.name, x.id)