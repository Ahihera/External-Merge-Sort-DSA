import struct
import random

def write_double(file_obj, value):
    """Ghi một số thực 8-byte vào file đang mở."""
    file_obj.write(struct.pack('d', value))

def read_double(file_obj):
    """Đọc một số thực 8-byte từ file. Trả về None nếu hết file."""
    bytes_read = file_obj.read(8)
    if not bytes_read or len(bytes_read) < 8:
        return None
    return struct.unpack('d', bytes_read)[0]

def generate_fixed_sample_data():
    """Tạo các file dữ liệu mẫu cố định (15, 50, 100 phần tử)."""
    with open("sample_15.bin", 'wb') as f:
        for _ in range(15): write_double(f, random.uniform(1.0, 100.0))
        
    with open("sample_50.bin", 'wb') as f:
        for _ in range(50): write_double(f, random.uniform(1.0, 1000.0))
            
    with open("sample_100.bin", 'wb') as f:
        for _ in range(100): write_double(f, random.uniform(1.0, 1000.0))

def generate_custom_sample_data(filename, num_elements):
    """Tạo file dữ liệu mẫu với số lượng tùy chỉnh."""
    with open(filename, 'wb') as f:
        for _ in range(num_elements): 
            write_double(f, random.uniform(1.0, 1000.0))

def read_binary_to_list(filepath):
    """Đọc toàn bộ file nhị phân và trả về một mảng (list) để hiển thị."""
    data = []
    with open(filepath, 'rb') as f:
        while True:
            val = read_double(f)
            if val is None: break
            data.append(round(val, 2))
    return data