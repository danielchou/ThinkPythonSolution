import json
import sys
import os
import glob
from pathlib import Path

def ipynb_to_py(ipynb_file, py_file=None):
    """將 Jupyter Notebook 檔案轉換為 Python 檔案
    
    Args:
        ipynb_file: 輸入的 .ipynb 檔案路徑
        py_file: 輸出的 .py 檔案路徑（如果未指定，將使用相同的檔名但副檔名為 .py）
    """
    # 如果未指定輸出檔案，則使用相同的檔名但副檔名為 .py
    if py_file is None:
        py_file = os.path.splitext(ipynb_file)[0] + '.py'
    
    # 讀取 Jupyter Notebook 檔案
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # 開始轉換
    py_content = []
    
    # 添加標頭註釋
    py_content.append(f"# 從 {os.path.basename(ipynb_file)} 轉換而來")
    py_content.append("# 使用 ipynb_to_py.py 腳本自動轉換")
    py_content.append("")
    
    # 處理每個單元格
    for i, cell in enumerate(notebook['cells']):
        # 添加單元格分隔符
        py_content.append(f"# In[{i}]:")
        
        # 根據單元格類型處理內容
        if cell['cell_type'] == 'markdown':
            # 將 markdown 轉換為註釋
            for line in cell['source']:
                # 移除行尾的換行符
                line = line.rstrip('\n')
                # 添加 # 前綴
                py_content.append(f"# {line}")
        elif cell['cell_type'] == 'code':
            # 直接添加程式碼
            for line in cell['source']:
                # 移除行尾的換行符
                line = line.rstrip('\n')
                py_content.append(line)
        
        # 添加空行分隔不同單元格
        py_content.append("")
    
    # 寫入 Python 檔案
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(py_content))
    
    print(f"已成功將 {ipynb_file} 轉換為 {py_file}")
    return py_file

def batch_convert(directory, output_directory=None):
    """批次轉換目錄中的所有 .ipynb 檔案
    
    Args:
        directory: 包含 .ipynb 檔案的目錄
        output_directory: 輸出 .py 檔案的目錄（如果未指定，將使用相同的目錄）
    """
    # 如果未指定輸出目錄，則使用相同的目錄
    if output_directory is None:
        output_directory = directory
    else:
        # 確保輸出目錄存在
        os.makedirs(output_directory, exist_ok=True)
    
    # 獲取目錄中的所有 .ipynb 檔案
    ipynb_files = glob.glob(os.path.join(directory, "*.ipynb"))
    
    if not ipynb_files:
        print(f"在 {directory} 中找不到任何 .ipynb 檔案")
        return []
    
    converted_files = []
    for ipynb_file in ipynb_files:
        # 計算輸出檔案路徑
        base_name = os.path.basename(ipynb_file)
        py_file = os.path.join(output_directory, os.path.splitext(base_name)[0] + '.py')
        
        # 轉換檔案
        converted_file = ipynb_to_py(ipynb_file, py_file)
        converted_files.append(converted_file)
    
    return converted_files

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("用法:")
        print("  1. 轉換單一檔案: python ipynb_to_py.py <input_ipynb_file> [output_py_file]")
        print("  2. 批次轉換目錄: python ipynb_to_py.py --batch <input_directory> [output_directory]")
        sys.exit(1)
    
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("錯誤: 請指定輸入目錄")
            sys.exit(1)
        
        input_directory = sys.argv[2]
        output_directory = sys.argv[3] if len(sys.argv) > 3 else None
        
        converted_files = batch_convert(input_directory, output_directory)
        if converted_files:
            print(f"已成功轉換 {len(converted_files)} 個檔案")
    else:
        ipynb_file = sys.argv[1]
        py_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        ipynb_to_py(ipynb_file, py_file)
