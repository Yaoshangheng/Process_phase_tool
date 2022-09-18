from obspy import UTCDateTime
import os, datetime
input_filename = r'1.dat'
output_pha_filename = r'2.pha'
output_ctlg_filename = r'3.ctlg'

#从一行里读时间字符串返回，例如00:47:19.75
def get_time(line_str):
    for v in line_str.split():
        if v.count(':') == 2:
            return v

def main():
    input_file = open(input_filename, 'r', encoding = 'utf8')
    output_pha = open(output_pha_filename, 'w')
    output_ctlg = open(output_ctlg_filename, 'w')
    seq_no = 0
    lines = input_file.readlines()
    i = 0
    while i < len(lines):
        if ':' in lines[i] and '/' in lines[i]: #数据单元的标题
            values = lines[i].split()
            date = values[1]
            is_ignore = False
            #如果缺少数据,舍弃这个数据单元
            if len(values) < 9:
                is_ignore = True
            else:
                #得到标题写到文件
                date_time = UTCDateTime(values[1] + ' ' + values[2]) - datetime.timedelta(hours=8)
                date_time = date_time.strftime('%Y%m%d%H%M%S.%f')[:-4]
                title = '{},{},{},{},{},{}'.format(date_time,values[3],values[4],values[5],values[6],seq_no)
                #title = '{},{},{},{},{}'.format(date_time,values[3],values[4],values[5],values[6])
                is_title_writed = False
            #跳过标题继续读数据
            i += 1
            while i < len(lines) and not (':' in lines[i] and '/' in lines[i]):
                #读前两行的数据
                if not is_ignore and lines[i][0].isalpha():
                    match_line1 = None
                    match_line2 = None
                    v1, v2 = lines[i].split()[0:2]
                    #读前两行的数据
                    while i < len(lines):
                        #第一行数据有Pg或者Pn，第二行数据必须有Sg，才提取
                        if match_line1 == None and (' Pg ' in lines[i] or ' Pn ' in lines[i]):
                            match_line1 = lines[i]
                        elif match_line1 != None and match_line2 == None and ' Sg ' in lines[i]:
                            match_line2 = lines[i]
                        #读到下一个数据块返回
                        i += 1
                        if i < len(lines) and lines[i][0].isalpha():
                            break
                    if match_line1 != None and match_line2 != None:
                        time1 = get_time(match_line1)
                        time2 = get_time(match_line2)
                        date_time1 = UTCDateTime('{} {}'.format(date, time1)) - datetime.timedelta(hours=8)
                        date_time2 = UTCDateTime('{} {}'.format(date, time2)) - datetime.timedelta(hours=8)
                        if not is_title_writed:
                            seq_no += 1
                            print(title)
                            is_title_writed = True
                            output_pha.write(title + '\n')
                            output_ctlg.write(title + '\n')
                        output_pha.write('{}.{},{},{},1,1\n'.format(v1, v2, date_time1, date_time2))
                else:
                    i += 1
        else:
            i += 1
    input_file.close()
    output_pha.close()
    output_ctlg.close()
    print('saved:')
    print(os.path.abspath(output_pha_filename))
    print(os.path.abspath(output_ctlg_filename))
main()

