#!/usr/bin/env python
# coding: utf-8

import json
import sys
import re
import os

def clean_python_file(input_file, output_file=None):
    """清理 Python 檔案中的 '# In[n]:' 標記"""
    
    # 如果沒有指定輸出檔案，則覆蓋輸入檔案
    if output_file is None:
        output_file = input_file
    
    # 讀取 Python 檔案
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正則表達式移除 '# In[n]:' 標記
    cleaned_content = re.sub(r'\n# In\[\d+\]:\s*', '\n', content)
    
    # 寫入清理後的內容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"已成功清理 Python 檔案 {input_file} 並保存到 {output_file}")


def clean_notebook(input_file, output_file=None):
    """清理 Jupyter Notebook 中的 'In[n]:' 標記和空的程式碼區塊"""
    
    # 如果沒有指定輸出檔案，則覆蓋輸入檔案
    if output_file is None:
        output_file = input_file
    
    # 讀取 notebook 檔案
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # 過濾掉 'In[n]:' 標記的 markdown 區塊和空的程式碼區塊
    filtered_cells = []
    for cell in notebook['cells']:
        # 檢查是否為 markdown 區塊且僅包含 'In[n]:' 標記
        if cell['cell_type'] == 'markdown' and len(cell['source']) == 1:
            source = cell['source'][0]
            if re.match(r'^In\[\d+\]:$', source.strip()):
                continue  # 跳過這個 cell
        
        # 檢查是否為空的程式碼區塊
        if cell['cell_type'] == 'code' and (not cell['source'] or ''.join(cell['source']).strip() == ''):
            continue  # 跳過這個 cell
        
        # 保留其他區塊
        filtered_cells.append(cell)
    
    # 更新 notebook 的 cells
    notebook['cells'] = filtered_cells
    
    # 寫入清理後的 notebook
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"已成功清理 {input_file} 並保存到 {output_file}")
    print(f"移除了 {len(notebook['cells']) - len(filtered_cells)} 個不需要的區塊")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  清理 Jupyter Notebook: python clean_notebook.py <input_notebook> [output_notebook]")
        print("  清理 Python 檔案: python clean_notebook.py --py <input_python_file> [output_python_file]")
        print("  批次清理目錄中的 Python 檔案: python clean_notebook.py --batch-py <input_directory> [output_directory]")
        sys.exit(1)
    
    # 處理批次清理 Python 檔案的情況
    if sys.argv[1] == "--batch-py":
        if len(sys.argv) < 3:
            print("錯誤: 請指定輸入目錄")
            sys.exit(1)
        
        input_directory = sys.argv[2]
        output_directory = sys.argv[3] if len(sys.argv) > 3 else input_directory
        
        # 確保輸出目錄存在
        os.makedirs(output_directory, exist_ok=True)
        
        # 獲取目錄中的所有 .py 檔案
        py_files = [f for f in os.listdir(input_directory) if f.endswith('.py')]
        
        if not py_files:
            print(f"在 {input_directory} 中找不到任何 .py 檔案")
            sys.exit(1)
        
        # 清理每個檔案
        for py_file in py_files:
            input_path = os.path.join(input_directory, py_file)
            output_path = os.path.join(output_directory, py_file)
            clean_python_file(input_path, output_path)
        
        print(f"已成功清理 {len(py_files)} 個 Python 檔案")
    
    # 處理清理單一 Python 檔案的情況
    elif sys.argv[1] == "--py":
        if len(sys.argv) < 3:
            print("錯誤: 請指定輸入檔案")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        clean_python_file(input_file, output_file)
    
    # 處理清理 Jupyter Notebook 的情況
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        clean_notebook(input_file, output_file)
