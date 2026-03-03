import sys
sys.stdout.reconfigure(encoding='utf-8')

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import utils
import external_sort

class TextRedirector(object):
    # Chuyển hướng lệnh print() vào khung Text của Tkinter
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')
        self.widget.update()

    def flush(self):
        pass

class ExternalSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Sắp xếp Ngoại (External Merge Sort)")
        self.root.geometry("880x680")
        
        self.selected_file = None
        self.chunk_size = 5

        self.setup_ui()
        sys.stdout = TextRedirector(self.log_area)

    def setup_ui(self):
        # Frame 1
        btn_frame = tk.Frame(self.root, pady=5)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="1. Tạo Bộ Dữ liệu Mẫu", command=self.generate_sample_data, bg="lightblue", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="2. Chọn File Nguồn", command=self.select_file, bg="lightgreen", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="3. Bắt đầu Sắp xếp", command=self.start_sorting, bg="orange", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="4. Xem nội dung File", command=self.view_binary_file, bg="plum", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa Log", command=self.clear_log).pack(side=tk.RIGHT, padx=10)

        # Frame 2
        test_frame = tk.Frame(self.root, pady=5)
        test_frame.pack(fill=tk.X)
        
        tk.Label(test_frame, text="Tạo file test tùy chọn (Nhập số lượng <= 300):", font=("Arial", 9, "italic")).pack(side=tk.LEFT, padx=10)
        self.entry_custom = tk.Entry(test_frame, width=8, font=("Arial", 10))
        self.entry_custom.pack(side=tk.LEFT, padx=5)
        tk.Button(test_frame, text="Tạo File Test", command=self.generate_custom_data, bg="khaki").pack(side=tk.LEFT, padx=5)

        self.lbl_file = tk.Label(self.root, text="Chưa chọn file nào", fg="blue", font=("Arial", 10, "italic"))
        self.lbl_file.pack(pady=5)

        tk.Label(self.root, text="Khung minh họa quá trình & hiển thị dữ liệu:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 10), state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def generate_sample_data(self):
        print("="*50)
        print("ĐANG TẠO CÁC TẬP TIN DỮ LIỆU MẪU CỐ ĐỊNH (.bin)...")
        utils.generate_fixed_sample_data()
        print(" -> Đã tạo 'sample_15.bin', 'sample_50.bin', 'sample_100.bin'")
        print("="*50 + "\n")

    def generate_custom_data(self):
        val_str = self.entry_custom.get()
        try:
            num = int(val_str)
            if num <= 0 or num > 300:
                messagebox.showwarning("Lỗi", "Vui lòng nhập số tự nhiên từ 1 đến 300!")
                return
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập một số hợp lệ!")
            return
            
        filename = f"sample_custom_{num}.bin"
        utils.generate_custom_sample_data(filename, num)
            
        print("="*50)
        print(f"ĐÃ TẠO FILE TEST TÙY CHỈNH: '{filename}' ({num} phần tử)")
        print("="*50 + "\n")

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn tập tin dữ liệu nguồn",
            filetypes=[("Binary files", "*.bin *.dat"), ("All files", "*.*")]
        )
        if filepath:
            self.selected_file = filepath
            size = os.path.getsize(filepath)
            num_elements = size // 8
            self.lbl_file.config(text=f"Đã chọn: {os.path.basename(filepath)} | Kích thước: {size} bytes ({num_elements} số thực)")
            print(f"\nĐã chọn file nguồn: {filepath}\nSẵn sàng! Hãy bấm 'Bắt đầu Sắp xếp'.\n")

    def start_sorting(self):
        if not self.selected_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file dữ liệu nguồn trước!")
            return
            
        print("\n" + "="*50 + "\nBẮT ĐẦU CHƯƠNG TRÌNH SẮP XẾP NGOẠI\n" + "="*50)
        output_file = "sorted_" + os.path.basename(self.selected_file)
        
        list_of_runs = external_sort.create_initial_runs(self.selected_file, self.chunk_size)
        if list_of_runs:
            external_sort.merge_runs(list_of_runs, output_file)
            print(f"\nSắp xếp xong! Bấm 'Xem nội dung File' và chọn '{output_file}' để kiểm tra kết quả.")
        print("="*50 + "\n")

    def view_binary_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn tập tin nhị phân để xem",
            filetypes=[("Binary files", "*.bin *.dat"), ("All files", "*.*")]
        )
        if filepath:
            print("\n" + "-"*50)
            print(f"ĐANG ĐỌC TẬP TIN: {os.path.basename(filepath)}")
            size = os.path.getsize(filepath)
            num_elements = size // 8
            
            data = utils.read_binary_to_list(filepath)
                    
            if num_elements == 0:
                print("-> Tập tin rỗng!")
            else:
                print(f"-> Nội dung:\n{data}")

            print("-"*50 + "\n")

    def clear_log(self):
        self.log_area.configure(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ExternalSortApp(root)
    root.mainloop()