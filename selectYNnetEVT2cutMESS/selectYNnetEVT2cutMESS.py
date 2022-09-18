import os
from sys import argv
input_filename = r'201809YNnet.pha'
output_filename = r'201809YNnet_new.pha'
input_file = open(input_filename, 'r')
output_file = open(output_filename, 'w')
#检查参数
def check_arg():
    is_error = False
    if len(argv) not in [2, 4]:
        is_error = True
    elif len(argv) == 2 and not argv[1][0].isalpha():
        is_error = True
    elif len(argv) > 2 and (not argv[1][0].isdigit() or len(argv) > 2 and not argv[2][0].isdigit()):
        is_error = True
    elif len(argv) > 2 and ',' not in argv[2]:
        is_error = True
    if is_error:
        print('参数错误, 例子:')
        print(r'python t.py YN.BAS,YN.NLA')
        print(r'python t.py 20180901-20180915 26.000-26.300,99.900-99.999 YN.BAS,YN.NLA')    
        exit(0)
    #得到参数值
    rangeCheck.keys = argv[-1].split(',') 
    if len(argv) > 2:
        rangeCheck.min_date, rangeCheck.max_date = argv[1].split('-')
        rangeCheck.n1_min, rangeCheck.n1_max = [float(i) for i in argv[2].split(',')[0].split('-')]    
        rangeCheck.n2_min, rangeCheck.n2_max = [float(i) for i in argv[2].split(',')[1].split('-')]

#过滤数据
def get_data():        
    lines = input_file.readlines()
    i = 0
    while i < len(lines):
        if lines[i][0].isdigit():
            title = lines[i].strip()
            i += 1
            title_date = title[0:8]
            values = title.split(',')
            if len(values) < 3:
                continue
            n1, n2 = float(values[1]), float(values[2])
            if not rangeCheck.is_match(title_date = title_date, n1 = n1, n2 = n2):
                continue
            is_title_saved = False
            while i < len(lines) and not lines[i][0].isdigit():
                if rangeCheck.is_match(line = lines[i]):
                    #保存标题
                    if not is_title_saved:
                        output_file.write('{}\n'.format(title.strip()))
                        is_title_saved = True
                        print(title)
                    #保存数据
                    output_file.write('{}\n'.format(lines[i].strip()))
                i += 1
        else:
            i += 1
    input_file.close()
    output_file.close()
    print('saved to:', os.path.abspath(output_filename))
    
class RangeCheck:
    def __init__(self):
        self.min_date = None
        self.max_date = None
        self.n1_min = None
        self.n1_max = None
        self.n2_min = None
        self.n2_max = None
        self.keys = []
    #判断是否满足条件
    def is_match(self, title_date = None, n1 = None, n2 = None, line = None):
        if title_date != None:
            if self.max_date != None and not (title_date >= self.min_date and title_date <= self.max_date):
                return False
        if n1 != None:
            if self.n1_min != None and not(n1 >= self.n1_min and n1 <= self.n1_max):
                return False
        if n2 != None:
            if self.n2_min != None and not(n2 >= self.n2_min and n2 <= self.n2_max):
                return False
        if line != None:
            v = line.split(',')[0]
            if v not in self.keys:
                return False
        return True
rangeCheck = RangeCheck()        
check_arg()
get_data()    
