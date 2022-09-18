'''
Written by Yuan Yao.
The functions:
1.convertMESS2PAL input pha
2.By changing file_path
3.add event id

'''
file_path = 'ZSYtmp201701.pha' #要修改的文件路径
import os
from sys import argv
import re
def main(file_path):
    num = 1
    r = re.compile(r'^[0-9]+_[0-9]+')
    file_path = os.path.abspath(file_path)
    out_path = os.path.join(os.path.dirname(file_path), "new_" + os.path.basename(file_path)) #修改后的文件路径
    out_file = open(out_path, "w") #写文件
    in_file = open(file_path, "r") #读文件
    for line in in_file:
        #后面添加数字
        if r.match(line):
            out_file.write(line.strip() + "," + str(num) + "\n")
            num += 1 #数字递增
        else:
            out_file.write(line)
    in_file.close()
    out_file.close()
    print("saved to:", out_path)

#从命令行参数读入文件路径
if len(argv) > 1:
    file_path = argv[1]
main(file_path = file_path)

