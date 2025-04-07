#  
# 
# Usage:python extract_pha_by_lat_lon.py example_pal_hyp_good.txt example_pal_hyp_full.pha output.pha --mode lat-lon -remove-id
# Yuan Yao@KMS 2025-04-07

def is_event_header(line):
    """检查是否是事件头行（包含日期、经纬度等信息）"""
    line = line.strip()
    if not line:
        return False
    parts = line.split(',')
    return len(parts) >= 3 and all(part.replace('.', '').replace('-', '').isdigit() for part in parts[:3])

def filter_by_coordinates(input_file, output_file, min_lon, max_lon, min_lat, max_lat):
    """根据经纬度范围筛选地震事件"""
    selected_count = 0
    total_count = 0
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_event = []
        in_selected_area = False
        
        for line in infile:
            stripped_line = line.strip()
            
            # 如果是事件头行
            if is_event_header(stripped_line):
                total_count += 1
                # 如果有正在处理的事件，且在当前区域，则写入
                if current_event and in_selected_area:
                    outfile.writelines(current_event)
                    selected_count += 1
                
                # 开始新事件
                current_event = [line]
                parts = stripped_line.split(',')
                try:
                    lon = float(parts[2])  # 经度是第三列
                    lat = float(parts[1])  # 纬度是第二列
                    in_selected_area = (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)
                except (IndexError, ValueError):
                    in_selected_area = False
            
            # 如果是震相数据行或空行
            else:
                if current_event:
                    current_event.append(line)
        
        # 写入最后一个事件（如果在选定区域内）
        if current_event and in_selected_area:
            outfile.writelines(current_event)
            selected_count += 1
    
    return total_count, selected_count

def main():
    # 直接在脚本中设置参数
    input_file = "example_pal_hyp_good_gt_4.pha"  # 输入文件名
    output_file = "filtered_events.pha"      # 输出文件名
    min_lon = 98.0   # 最小经度
    max_lon = 98.2   # 最大经度
    min_lat = 24.19   # 最小纬度
    max_lat = 24.38   # 最大纬度
    
    total, selected = filter_by_coordinates(input_file, output_file, min_lon, max_lon, min_lat, max_lat)
    
    # 打印结果
    print("地震事件筛选结果：")
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"经度范围: {min_lon} 到 {max_lon}")
    print(f"纬度范围: {min_lat} 到 {max_lat}")
    print(f"总事件数: {total}")
    print(f"筛选出的事件数: {selected}")
    print(f"筛选完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()