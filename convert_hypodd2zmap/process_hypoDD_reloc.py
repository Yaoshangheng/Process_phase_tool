input_file = 'hypoDD.reloc'
output_file = 'hypoDD_reloc_zmap.dat'

# 读取输入文件并提取指定列数据
with open(input_file, 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    columns = line.strip().split()
    if len(columns) >= 17:
        data.append([
            columns[2],   # 第3列
            columns[1],   # 第2列
            columns[10],  # 第11列
            columns[11],  # 第12列
            columns[12],  # 第13列
            columns[16],  # 第17列
            columns[3],   # 第4列
            columns[13],  # 第14列
            columns[14]   # 第15列
        ])

# 写入输出文件
with open(output_file, 'w') as file:
    for row in data:
        file.write(' '.join(row) + '\n')