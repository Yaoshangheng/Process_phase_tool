""" Written by Yuan Yao 
    with python
"""
import os
in_names = [r'phase_out1.dat', r'phase_out2.dat']
out_name = 'phase_all.dat'
out_file = open(out_name, 'w')
seq_no = 0
pcnt = 0
scnt = 0
#合并每个文件
for name in in_names:
    f = open(name, 'r')
    for line in f:
        if ' P' in line:
            pcnt += 1
            out_file.write(line)
        elif ' S' in line:
            scnt += 1
            out_file.write(line)
        elif line.startswith('#'):
            #修改序号
            line = line.strip()
            i = len(line) - 1
            while i >= 0 and line[i].isdigit():
                i -= 1
            line = line[0:i].strip() + '{:>11d}'.format(seq_no)
            seq_no += 1
            out_file.write(line + "\n")
            print(line.strip())
    f.close()
out_file.close()
print('saved to:', os.path.abspath(out_name))
print('P', pcnt)
print('S', scnt)

