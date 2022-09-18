""" Written by Yuan Yao 
    with python
"""
import os
from obspy import UTCDateTime
reloc_path = r'msms_reloc_main.csv'
mess_path = r'ZSYMESSdetect_2016-2017.pha'
out_path = r'phase_out.dat'
reloc_file = open(reloc_path, 'r')
mess_file = open(mess_path, 'r')
out_file = open(out_path, 'w')
time_dict = {}
#判断是不是数据行
def is_header(line):
    return line[0].isdigit()

#得到所有要提取的日期
for reloc in reloc_file:
    key = reloc.split(',')[0]
    key = str(UTCDateTime(key))
    time_dict[key] = reloc
#从MESS提取数据
lines = mess_file.readlines()
i = 0
seqno = 0
while i < len(lines):
    if is_header(lines[i]):
        values = lines[i].split(',')
        timeO = values[1] #第二列日期
        #提取数据
        if timeO not in time_dict:
            i += 1
        else:
            #得到标题
            utime = UTCDateTime(lines[i].split(',')[1])
            formater = '# {:4d} {:2d} {:2d} {:2d} {:2d} {:>5.2f} {:>8.4f} {:>9.4f} {:>7.2f} {:>5.2f}  0.00  0.00  0.00 {:>10d}'
            values = time_dict[timeO].split(',')
            v1 = eval(values[1]) 
            v2 = eval(values[2])
            v3 = eval(values[3])
            v4 = eval(values[4])
            year = utime.year
            month = utime.month
            day = utime.day
            hour = utime.hour
            minute = utime.minute
            second = utime.second + utime.microsecond/10**6
            title = formater.format(year, month, day, hour, minute, second, v1, v2, v3, v4, seqno)
            print(title)
            out_file.write(title + "\n")
            seqno += 1
            i += 1
            #得到数据
            formatter = '{} {:>13.3f} {:>7.3f} {:>3}'
            while i < len(lines) and not is_header(lines[i]):
                values = lines[i].split(',')
                b = values[0].split('.')[1]
                timeO = UTCDateTime(timeO)
                timeP = UTCDateTime(values[1])
                timeS = UTCDateTime(values[2])
                out_file.write(formatter.format(b, timeP-timeO, 1, 'P') + "\n")
                out_file.write(formatter.format(b, timeS-timeO, 1, 'S') + "\n")
                i += 1
    else:
        i += 1
out_file.close()
mess_file.close()
reloc_file.close()
print('saved to:', os.path.abspath(out_path))

