#  
# 
# Usage:
# Yuan Yao@KMS 2025-04-08

def convert_datetime(orig_time):
    """将原始时间字符串分解为年、月、日、时、分"""
    year = orig_time[:4]
    month = orig_time[4:6]
    day = orig_time[6:8]
    hour = orig_time[8:10]
    minute = orig_time[10:12]
    return year, month, day, hour, minute

def convert_catalog(input_file, output_file):
    """转换地震目录格式"""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # 分割每行数据
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # 跳过不完整的行
                
            orig_time = parts[0]
            latitude = parts[1]
            longitude = parts[2]
            depth = parts[3]
            magnitude = parts[4]
            
            # 处理时间
            year, month, day, hour, minute = convert_datetime(orig_time)
            
            # 写入新格式
            outfile.write(f"{longitude} {latitude} {year} {month} {day} {magnitude} {depth} {hour} {minute}\n")

# 使用示例
input_filename = "example_pal_hyp_good_gt_4_lonlat_manual_check_catalog.dat"
output_filename = "example_pal_hyp_good_gt_4_lonlat_manual_check_catalog_zmap.dat"

convert_catalog(input_filename, output_filename)
print(f"转换完成，结果已保存到 {output_filename}")
