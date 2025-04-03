#  
# Usage:python extract_pha_by_lat_lon.py example_pal_hyp_good.txt example_pal_hyp_full.pha output.pha --mode lat-lon -remove-id
# -remove-id can remove pha id
# Yuan Yao@KMS 2025-04-03

import sys
import os
import argparse

def read_good_records(file_path, mode="lat-lon", tolerance=1e-4):
    """
    读取 example_pal_hyp_good.txt 的记录
    :param mode: "lat-lon"（按经纬度）或 "time"（按时间）
    :param tolerance: 浮点数容差
    """
    records = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            if mode == "lat-lon":
                                # 按经纬度匹配
                                lat = round(float(parts[1]) / tolerance) * tolerance
                                lon = round(float(parts[2]) / tolerance) * tolerance
                                records.add((lat, lon))
                            elif mode == "time":
                                # 按时间匹配（标准化为 XXXXXX.0）
                                time_str = parts[0]
                                if '.' not in time_str:
                                    time_str += ".0"
                                records.add(time_str)
                        except ValueError:
                            print(f"Warning: Invalid data in line: {line}")
        return records
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        sys.exit(1)

def extract_events(
    input_pha, output_pha, good_records, mode="lat-lon",
    remove_id=False, tolerance=1e-4
):
    """
    从 example_pal_hyp_full.pha 提取匹配的事件和震相行
    :param remove_id: 是否移除事件行末尾的编号（如 ,0）
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

                # 事件行（以数字开头）
                if line[0].isdigit():
                    parts = line.split(',')
                    if len(parts) >= 3:
                        try:
                            match = False
                            if mode == "lat-lon":
                                # 按经纬度匹配
                                lat = round(float(parts[1]) / tolerance) * tolerance
                                lon = round(float(parts[2]) / tolerance) * tolerance
                                match = (lat, lon) in good_records
                            elif mode == "time":
                                # 按时间匹配
                                time_str = parts[0]
                                if '.' in time_str:
                                    time_str = time_str.split('.')[0] + ".0"
                                match = time_str in good_records

                            if match:
                                current_event = line
                                write_mode = True
                                # 移除编号（如果启用）
                                if remove_id and ',' in line:
                                    line = ','.join(line.split(',')[:-1])
                                outfile.write(line + '\n')
                                matched_events += 1
                            else:
                                write_mode = False
                        except ValueError:
                            print(f"Warning: Invalid data in line: {line}")
                            write_mode = False
                # 震相行（以字母开头）
                elif write_mode:
                    outfile.write(line + '\n')

            print(f"Matched {matched_events} events in {input_pha}.")
            if matched_events == 0:
                print("Warning: No matching events found!")

    except FileNotFoundError:
        print(f"Error: File {input_pha} not found!")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Extract earthquake events from example_pal_hyp_full.pha based on example_pal_hyp_good.txt."
    )
    parser.add_argument("good_txt", help="Path to example_pal_hyp_good.txt")
    parser.add_argument("full_pha", help="Path to example_pal_hyp_full.pha")
    parser.add_argument("output_pha", help="Path to output example_pal_hyp_good.pha")
    parser.add_argument(
        "--mode", choices=["lat-lon", "time"], default="lat-lon",
        help="Matching mode: 'lat-lon' (default) or 'time'"
    )
    parser.add_argument(
        "--remove-id", action="store_true",
        help="Remove the trailing ID from event lines (e.g., ',0')"
    )
    args = parser.parse_args()

    print(f"Reading records from {args.good_txt} (mode: {args.mode})...")
    good_records = read_good_records(args.good_txt, mode=args.mode)
    print(f"Found {len(good_records)} unique records.")

    print(f"Extracting matching events from {args.full_pha} to {args.output_pha}...")
    extract_events(
        args.full_pha, args.output_pha, good_records,
        mode=args.mode, remove_id=args.remove_id
    )

if __name__ == "__main__":
    main()
