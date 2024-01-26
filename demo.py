import os
import re
from decimal import Decimal
from datetime import datetime
import csv

file_path = "0000962.dat"#.dat文件路径
output_path = "output.csv"#输出文件路径


def read(file_path,output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # 写入列名
        csv_writer.writerow(["股票代码", "时间", "昨收价", "成交量", "成交额", "开盘价", "最高价", "最低价", "收盘价"])

        with open(file_path, 'rb') as file:
            match = re.search(r'(\d+)', file_path)
            if match:
                full_string = match.group(0)
                extracted_string = full_string[:-1]  # 去掉末尾的数字
                print("股票代码:", extracted_string)
                fsize = os.path.getsize(file_path)
                print("文件字节大小:", fsize)
            else:
                print("无法识别文件对应股票代码")

            for i in range(int(fsize / 44)):  # 根据文件字节数确定循环数
                timestamp_bytes = file.read(8)

                # 将8个字节的时间戳数据转换为整数
                timestamp_integer = int.from_bytes(timestamp_bytes, byteorder='little')

                # 将整数形式的时间戳转换为字符串
                timestamp_str = str(timestamp_integer)

                # 使用字符串切片将时间戳转换为时间格式
                year = int(timestamp_str[:4])
                month = int(timestamp_str[4:6])
                day = int(timestamp_str[6:8])
                hour = int(timestamp_str[8:10])
                minute = int(timestamp_str[10:12])
                second = int(timestamp_str[12:14])

                # 创建时间对象
                timestamp_datetime = datetime(year, month, day, hour, minute, second)

                # 继续读取另外四个字节
                second_four_bytes = file.read(4)
                Yesterday_close = int.from_bytes(second_four_bytes, byteorder='little') / 1000

                volume = file.read(8)
                Volume = int.from_bytes(volume, byteorder='little')
                Volume = Decimal(Volume / 1000).quantize(Decimal('0'))  # 原数据四舍五入得到的成交量

                turnover = file.read(8)
                Turnover = int.from_bytes(turnover, byteorder='little')
                Turnover = Decimal(Turnover / 100000).quantize(Decimal('0')) / 100  # 原数据四舍五入得到的成交额

                open_bytes = file.read(4)
                Open = int.from_bytes(open_bytes, byteorder='little') / 1000

                high_bytes = file.read(4)
                High = int.from_bytes(high_bytes, byteorder='little') / 1000

                low_bytes = file.read(4)
                Low = int.from_bytes(low_bytes, byteorder='little') / 1000

                close_bytes = file.read(4)
                Close = int.from_bytes(close_bytes, byteorder='little') / 1000

                # 将数据写入CSV文件
                csv_writer.writerow(
                    [extracted_string, timestamp_datetime, Yesterday_close, Volume, Turnover, Open, High, Low, Close])

    # 打印完成消息
    print(f"数据已写入CSV文件: {output_path}")

read(file_path,output_path)

