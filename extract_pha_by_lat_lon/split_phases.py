#  
# 
# Usage:python extract_pha_by_lat_lon.py example_pal_hyp_good.txt example_pal_hyp_full.pha output.pha --mode lat-lon -remove-id
# Yuan Yao@KMS 2025-04-07

import sys

def is_event_header(line):
    """检查是否是事件头行（包含日期、经纬度等信息）"""
    line = line.strip()
    if not line:
        return False
    parts = line.split(',')
    return len(parts) >= 5 and all(part.replace('.', '').replace('-', '').isdigit() for part in parts[:5])

def process_pha_file(input_file, max_phases):
    """处理PHA文件并返回分类后的事件列表"""
    events_leq = []  # 震相行≤max_phases的事件
    events_gt = []   # 震相行>max_phases的事件
    
    with open(input_file, 'r') as f:
        current_event = []
        phase_count = 0
        
        for line in f:
            line = line.strip()
            if not line:
                continue  # 跳过空行
            
            if is_event_header(line):
                # 保存上一个事件（如果有）
                if current_event:
                    if phase_count <= max_phases:
                        events_leq.append(current_event)
                    else:
                        events_gt.append(current_event)
                
                # 开始新事件
                current_event = [line]
                phase_count = 0
            else:
                current_event.append(line)
                phase_count += 1
        
        # 处理最后一个事件
        if current_event:
            if phase_count <= max_phases:
                events_leq.append(current_event)
            else:
                events_gt.append(current_event)
    
    return events_leq, events_gt

def write_events_to_file(events, output_file):
    """将事件列表写入文件"""
    with open(output_file, 'w') as f:
        for event in events:
            f.write('\n'.join(event) + '\n')

def main():
    if len(sys.argv) != 3:
        print("使用方法: python split_phases.py <输入文件> <最大震相行数>")
        print("示例: python split_phases.py example_pal_hyp_good.pha 12")
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        max_phases = int(sys.argv[2])
    except ValueError:
        print("错误: 最大震相行数必须是整数")
        sys.exit(1)
    
    # 生成输出文件名
    base_name = input_file.rsplit('.', 1)[0]
    output_leq = f"{base_name}_leq_{max_phases}.pha"
    output_gt = f"{base_name}_gt_{max_phases}.pha"
    
    # 处理文件
    events_leq, events_gt = process_pha_file(input_file, max_phases)
    
    # 写入文件
    write_events_to_file(events_leq, output_leq)
    write_events_to_file(events_gt, output_gt)
    
    # 输出统计信息
    print(f"处理完成:")
    print(f"- 震相行 ≤ {max_phases} 的事件: {len(events_leq)} 个 (保存到 {output_leq})")
    print(f"- 震相行 > {max_phases} 的事件: {len(events_gt)} 个 (保存到 {output_gt})")
    print(f"总事件数: {len(events_leq) + len(events_gt)}")

if __name__ == "__main__":
    main()
