import os
import heapq
from utils import read_double, write_double

def create_initial_runs(input_filename, chunk_size):
     # Chia file lớn thành các Runs đã sắp xếp trong RAM.
    print(f"\n CHIA FILE VÀ SẮP XẾP NỘI TẠI (CHUNK SIZE = {chunk_size})")
    runs = []
    run_index = 0
    with open(input_filename, 'rb') as f:
        while True:
            chunk = []
            for _ in range(chunk_size):
                val = read_double(f)
                if val is None: break
                chunk.append(val)
            
            if not chunk: break
            chunk.sort()
            
            run_filename = f"temp_run_{run_index}.bin"
            with open(run_filename, 'wb') as out_f:
                for val in chunk:
                    write_double(out_f, val)
                    
            runs.append(run_filename)
            print(f" -> Tạo run '{run_filename}': {[round(x, 2) for x in chunk]}")
            run_index += 1
    return runs

def merge_runs(run_filenames, output_filename):
    # Trộn các Runs lại bằng cấu trúc Min-Heap.
    print("\n TRỘN CÁC RUNS (K-WAY MERGE BẰNG MIN-HEAP)")
    open_files = []
    min_heap = []
    
    for i, filename in enumerate(run_filenames):
        f = open(filename, 'rb')
        open_files.append(f)
        val = read_double(f)
        if val is not None:
            heapq.heappush(min_heap, (val, i))
            print(f" -> Nạp giá trị {val:.2f} từ '{filename}' vào Buffer.")

    print("\nĐang tiến hành trộn...")
    step = 1
    with open(output_filename, 'wb') as out_f:
        while min_heap:
            smallest_val, file_index = heapq.heappop(min_heap)
            write_double(out_f, smallest_val)
            print(f" Bước {step}: Ghi {smallest_val:.2f} -> (Rút từ {run_filenames[file_index]})")
            
            next_val = read_double(open_files[file_index])
            if next_val is not None:
                heapq.heappush(min_heap, (next_val, file_index))
            step += 1

    for f in open_files: f.close()
    
    print("\nDọn dẹp file tạm...")
    for filename in run_filenames:
        os.remove(filename)
    print(f"\n File kết quả được lưu tại: '{output_filename}'")