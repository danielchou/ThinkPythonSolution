# Python 語法速查表 - 第 14 章：檔案

## 檔案基本操作
```python
# 開啟檔案
file = open('example.txt', 'r')  # 讀取模式
file = open('example.txt', 'w')  # 寫入模式（覆蓋原有內容）
file = open('example.txt', 'a')  # 附加模式（在檔案末尾添加內容）
file = open('example.txt', 'rb')  # 二進制讀取模式

# 關閉檔案
file.close()

# 使用 with 語句（推薦，自動關閉檔案）
with open('example.txt', 'r') as file:
    content = file.read()
```

## 讀取檔案
```python
# 讀取整個檔案內容
with open('example.txt', 'r') as file:
    content = file.read()

# 讀取一行
with open('example.txt', 'r') as file:
    line = file.readline()

# 讀取所有行到列表
with open('example.txt', 'r') as file:
    lines = file.readlines()

# 逐行讀取（高效處理大檔案）
with open('example.txt', 'r') as file:
    for line in file:
        print(line.strip())  # strip() 移除行尾的換行符
```

## 寫入檔案
```python
# 寫入字串
with open('example.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is a new line.')

# 寫入多行
lines = ['First line\n', 'Second line\n', 'Third line\n']
with open('example.txt', 'w') as file:
    file.writelines(lines)
```

## 檔案指標操作
```python
with open('example.txt', 'r') as file:
    # 移動檔案指標
    file.seek(0)      # 移動到檔案開頭
    file.seek(10)     # 移動到第 10 個字節
    file.seek(0, 2)   # 移動到檔案末尾
    
    # 獲取當前檔案指標位置
    position = file.tell()
```

## 使用 pathlib 模組
```python
from pathlib import Path

# 建立 Path 對象
p = Path('example.txt')
p = Path('folder/example.txt')
p = Path.home() / 'documents' / 'example.txt'

# 檔案操作
p.exists()           # 檢查檔案是否存在
p.is_file()          # 檢查是否為檔案
p.is_dir()           # 檢查是否為目錄
p.stat()             # 獲取檔案狀態（大小、修改時間等）

# 讀寫檔案
content = p.read_text()              # 讀取文字檔案
p.write_text('Hello, World!')        # 寫入文字檔案
binary_data = p.read_bytes()         # 讀取二進制檔案
p.write_bytes(b'Binary data')        # 寫入二進制檔案

# 路徑操作
p.name               # 檔案名稱
p.stem               # 不含副檔名的檔案名稱
p.suffix             # 副檔名
p.parent             # 父目錄
```

## 目錄操作
```python
import os
from pathlib import Path

# 使用 os 模組
os.listdir('.')                          # 列出目錄內容
os.mkdir('new_directory')                # 創建目錄
os.makedirs('path/to/new/directory')     # 創建多級目錄
os.rmdir('directory')                    # 刪除空目錄
os.rename('old.txt', 'new.txt')          # 重命名檔案或目錄

# 使用 pathlib
p = Path('.')
[x for x in p.iterdir()]                 # 列出目錄內容
Path('new_directory').mkdir()            # 創建目錄
Path('path/to/new/directory').mkdir(parents=True)  # 創建多級目錄
```

## 檔案路徑處理
```python
import os
from pathlib import Path

# 使用 os.path
file_path = os.path.join('folder', 'subfolder', 'file.txt')
os.path.basename(file_path)              # 'file.txt'
os.path.dirname(file_path)               # 'folder/subfolder'
os.path.abspath(file_path)               # 絕對路徑
os.path.exists(file_path)                # 檢查檔案是否存在

# 使用 pathlib
p = Path('folder') / 'subfolder' / 'file.txt'
p.name                                   # 'file.txt'
p.parent                                 # 'folder/subfolder'
p.absolute()                             # 絕對路徑
p.exists()                               # 檢查檔案是否存在
```

## 檔案模式與編碼
```python
# 指定編碼
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 處理編碼錯誤
with open('example.txt', 'r', encoding='utf-8', errors='ignore') as file:
    content = file.read()

# 二進制模式
with open('image.jpg', 'rb') as file:
    binary_data = file.read()

# 文字與二進制模式的區別
# - 文字模式：處理字串，自動處理換行符
# - 二進制模式：處理位元組，不處理換行符
```

## 臨時檔案
```python
import tempfile

# 創建臨時檔案
with tempfile.NamedTemporaryFile() as temp:
    temp.write(b'Some data')
    temp.flush()
    # 檔案會在 with 區塊結束後自動刪除

# 創建臨時目錄
with tempfile.TemporaryDirectory() as temp_dir:
    # 使用 temp_dir 作為臨時目錄路徑
    pass  # 目錄會在 with 區塊結束後自動刪除
```
