#  
# 
# 
# Yuan Yao@KMS 2025-04-03

import sys
import os

def read_good_records(file_path, tolerance=1e-4):
    """
    读取 example_pal_hyp_good.txt 的经纬度，并存储为 (lat, lon) 集合
    :param tolerance: 浮点数匹配容差（默认 0.0001）
    """
    good_records = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            lat = float(parts[1])  # 纬度（第2列）
                            lon = float(parts[2])  # 经度（第3列）
                            # 标准化浮点数（避免精度问题）
                            lat_rounded = round(lat / tolerance) * tolerance
                            lon_rounded = round(lon / tolerance) * tolerance
                            good_records.add((lat_rounded, lon_rounded))
                        except ValueError:
                            print(f"Warning: Invalid lat/lon in line: {line}")
        return good_records
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        sys.exit(1)

def extract_events_by_lat_lon(input_pha, good_records, output_pha, tolerance=1e-4):
    """
    从 example_pal_hyp_full.pha 提取匹配经纬度的事件和震相行
    """
    try:
        if os.path.getsize(input_pha) == 0:
            print(f"Error: {input_pha} is empty!")
            sys.exit(1)

        with open(input_pha, 'r') as infile, open(output_pha, 'w') as outfile:
            current_event = None
            write_mode = False
            matched_events = 0

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                # 检查是否是事件行（以数字开头）
                if line[0].isdigit():
                    parts = line.split(',')
                    if len(parts) >= 3:
                        try:
                            lat = float(parts[1])  # 纬度（第2列）
                            lon = float(parts[2])  # 经度（第3列）
                            # 标准化浮点数
                            lat_rounded = round(lat / tolerance) * tolerance
                            lon_rounded = round(lon / tolerance) * tolerance
                            # 检查是否在 good_records 中
                            if (lat_rounded, lon_rounded) in good_records:
                                current_event = line
                                write_mode = True
                                outfile.write(line + '\n')
                                matched_events += 1
                            else:
                                write_mode = False
                                current_event = None
                        except ValueError:
                            print(f"Warning: Invalid lat/lon in line: {line}")
                            write_mode = False
                else:
                    # 震相行，仅在匹配的事件后写入
                    if write_mode and current_event:
                        outfile.write(line + '\n')

            print(f"Matched {matched_events} events in {input_pha}.")
            if matched_events == 0:
                print("Warning: No matching events found!")

    except FileNotFoundError:
        print(f"Error: File {input_pha} not found!")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        print("Usage: python extract_pha_by_lat_lon.py example_pal_hyp_good.txt example_pal_hyp_full.pha example_pal_hyp_good.pha")
        sys.exit(1)

    good_txt = sys.argv[1]
    full_pha = sys.argv[2]
    good_pha = sys.argv[3]

    print(f"Reading lat/lon records from {good_txt}...")
    good_records = read_good_records(good_txt)
    print(f"Found {len(good_records)} unique (lat, lon) records.")

    print(f"Extracting matching events from {full_pha} to {good_pha}...")
    extract_events_by_lat_lon(full_pha, good_records, good_pha)

if __name__ == "__main__":
    main()