import os
import patoolib
import zipfile
import concurrent.futures
from PyInquirer import prompt

folder_path = "/Users/developments/Downloads/NSTH-CTDL&GT"
password = "http://nhasachtinhoc.blogspot.com"
output_dir = "/Users/developments/Downloads/NSTH-CTDL&GT"


files_to_delete = [
    "Nhà Sách Tin Học - chia sẻ tài liệu, khóa học.url",
    "Mời tham gia vào group để nhận được nhiều tài liệu hơn.url",
    "Lưu ý quan trọng.txt",
    "Like trang để nhận giáo trình và khóa học mới nhất.url"
]

questions = [
    {
        'type': 'input',
        'name': 'num_threads',
        'message': 'Nhập số luồng đi anh:',
        'validate': lambda val: val.isdigit() and int(val) > 0
    }
]

answers = prompt(questions)
num_threads = int(answers['num_threads'])

def extract_rar(rar_file_path):
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(rar_file_path))[0])

    patoolib.extract_archive(rar_file_path, outdir=output_path, password=password)
    

    os.remove(rar_file_path)
    
    print(f"Tệp RAR '{os.path.basename(rar_file_path)}' đã được giải nén và xoá.")
    
    process_extracted_dir(output_path)

def extract_zip(zip_file_path):
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(zip_file_path))[0])
    

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)
    

    os.remove(zip_file_path)
    
    print(f"Tệp ZIP '{os.path.basename(zip_file_path)}' đã được giải nén và xoá.")
    
    process_extracted_dir(output_path)

def process_extracted_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for filename in files_to_delete:
            file_path = os.path.join(root, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Tệp '{filename}' đã được xoá từ {root}")

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith(".rar"):
            executor.submit(extract_rar, file_path)
        elif filename.endswith(".zip"):
            executor.submit(extract_zip, file_path)
