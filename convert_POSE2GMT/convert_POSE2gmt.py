import pandas as pd
import math
from obspy import UTCDateTime

def calculate_new_coordinates(lon, lat, offset_km, azimuth_deg):
    """
    根据原坐标、偏移距离和方位角计算新坐标 (简单平面近似计算，适合小范围)
    """
    R = 6371.0  # 地球半径 km
    azimuth_rad = math.radians(azimuth_deg)

    new_lat = lat + (offset_km / R) * (180 / math.pi) * math.cos(azimuth_rad)
    new_lon = lon + (offset_km / R) * (180 / math.pi) * math.sin(azimuth_rad) / math.cos(math.radians(lat))

    return new_lon, new_lat

def convert_fms_format(input_csv, output_txt, offset_km=0.0, azimuth_deg=0.0,
                       id_mode="kms_time", fixed_id="KMS", add_quality=False,
                       filter_quality=False, desired_quality=None):
    """
    转换震源机制csv文件为指定格式
    """
    # 读取CSV
    df = pd.read_csv(input_csv)

    with open(output_txt, 'w') as f_out:
        for idx, row in df.iterrows():
            lon = row['longitude']
            lat = row['latitude']
            depth = row['depth']
            strike = row['strike']
            dip = row['dip']
            rake = row['rake']
            magnitude = row['magnitude']
            time_str = row['time']  # UTC时间字符串
            quality_rank = str(row.get('quality_rank', '')).strip().upper()  # 质量等级，大写

            # 如果需要筛选质量等级
            if filter_quality and (quality_rank != desired_quality):
                continue  # 跳过不符合要求的记录

            # 生成ID
            if id_mode == "kms_time":
                try:
                    event_time = UTCDateTime(time_str)
                    event_id = f"KMS{event_time.year:04d}{event_time.month:02d}{event_time.day:02d}" \
                               f"{event_time.hour:02d}{event_time.minute:02d}{event_time.second:02d}"
                except Exception as e:
                    print(f"时间格式解析错误: {time_str}, 使用默认ID")
                    event_id = "KMS000000000000"
            elif id_mode == "fixed":
                if add_quality:
                    event_id = f"{fixed_id}_{quality_rank}"
                else:
                    event_id = fixed_id
            else:
                raise ValueError("id_mode 只能是 'kms_time' 或 'fixed'。")

            # 计算新的坐标
            new_lon, new_lat = calculate_new_coordinates(lon, lat, offset_km, azimuth_deg)

            # 写入一行（空格分隔）
            f_out.write(f"{lon:.6f} {lat:.6f} {depth:.2f} {strike:.1f} {dip:.1f} {rake:.1f} {magnitude:.2f} {new_lon:.6f} {new_lat:.6f} {event_id}\n")

    print(f"转换完成，结果保存至 {output_txt}")

if __name__ == "__main__":
    # ======= 配置部分 =======
    input_csv = "example_fms.csv"  # 输入文件路径
    output_txt = "example_converted.txt"  # 输出文件路径

    offset_km = float(input("请输入偏移距离 (单位: km)："))
    azimuth_deg = float(input("请输入偏移方向 (单位: 度，北为0度，顺时针)："))

    id_mode = input("请选择ID模式（'kms_time' 或 'fixed'）：").strip().lower()
    if id_mode not in ["kms_time", "fixed"]:
        raise ValueError("ID模式输入错误，必须是 'kms_time' 或 'fixed'。")

    fixed_id = "KMS"
    if id_mode == "fixed":
        fixed_id = input("请输入固定ID前缀（例如 KMS_TEST）：").strip()

    add_quality_input = input("是否在ID后加上质量等级？(y/n)：").strip().lower()
    add_quality = add_quality_input == "y"

    filter_quality_input = input("是否只处理特定质量等级？(y/n)：").strip().lower()
    filter_quality = filter_quality_input == "y"
    desired_quality = None
    if filter_quality:
        desired_quality = input("请输入需要保留的质量等级（例如 A 或 B 或 C）：").strip().upper()

    # ========================

    convert_fms_format(
        input_csv, output_txt,
        offset_km, azimuth_deg,
        id_mode, fixed_id, add_quality,
        filter_quality, desired_quality
    )
