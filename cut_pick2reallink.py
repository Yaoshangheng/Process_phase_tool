#!/usr/bin/env python
#!Written by Yao Yuan

file = open('zsy_newmodel_test.txt', 'r', encoding = 'utf8')
file_dict = {}
def get_file(key):
    if key not in file_dict:
        file_dict[key] = open('{}.txt'.format(key), 'w', encoding = 'utf8')
    return file_dict[key]
n = 0
for line in file:
    line = line.strip()
    fields = line.split(',')
    if line.startswith('#') or len(fields) < 4 or '-' not in fields[3]:
        #print(line.strip())
        continue
    filename = fields[3][0:7].replace('-', '')
    n += 1
    print('\r', n, filename, end = '    ')
    get_file(filename).write(line + "\n")
file.close()
for filename in file_dict:
    file_dict[filename].close()
