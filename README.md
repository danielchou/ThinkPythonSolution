# Think Python, 3rd Edition

這個目錄包含 [Think Python](https://greenteapress.com/wp/think-python-3rd-edition/) 第三版的原始筆記本，其中包含練習題的解答。

## Python 語法精簡 Cheatsheet

本專案提供了一系列 Python 語法精簡 Cheatsheet，整合了各章節的 Python 語法重點，幫助學生快速回顧和學習。由於內容豐富，我們將其分為多個檔案：

### 基礎篇 (第 1-10 章)
- [Python 語法精簡 Cheatsheet (第 1-10 章)](./Python_Cheatsheet.md)：涵蓋基本算術運算、變數與賦值、函式定義與呼叫、條件判斷與迴圈、字串處理、列表操作和字典使用等基礎主題。

### 進階篇 (第 11-19 章)
- [第 11 章：元組](./Python_Cheatsheet_Ch11.md)：元組的建立、操作和應用
- [第 12 章：資料結構選擇](./Python_Cheatsheet_Ch12.md)：集合、集合運算和實際應用
- [第 13 章：資料格式](./Python_Cheatsheet_Ch13.md)：字串格式化、JSON、CSV、XML 和序列化
- [第 14 章：檔案處理](./Python_Cheatsheet_Ch14.md)：檔案操作、pathlib 使用、目錄處理和臨時檔案
- [第 15 章：類別與物件](./Python_Cheatsheet_Ch15.md)：類別定義、實例和類別變數、私有屬性、屬性裝飾器、靜態和類別方法、特殊方法和 OOP 概念
- [第 16 章：類別與函式](./Python_Cheatsheet_Ch16.md)：時間類別範例、純函式與修改器、原型開發與規劃開發、調試技巧
- [第 17 章：類別與方法](./Python_Cheatsheet_Ch17.md)：物件導向方法、方法類型、運算符重載、鴨子型別和多態
- [第 18 章：繼承](./Python_Cheatsheet_Ch18.md)：基本繼承、多重繼承、抽象基類、繼承與組合的選擇、方法覆寫與擴展
- [第 19 章：特殊方法](./Python_Cheatsheet_Ch19.md)：基本特殊方法、比較特殊方法、數值運算特殊方法、容器特殊方法、屬性存取特殊方法

這些 Cheatsheet 是方便的學習參考資料，特別適合需要快速複習 Python 語法的學生。每個檔案都包含詳細的程式碼範例和中文解釋。

## 檔案轉換工具

本專案提供兩種將 Python 檔案 (.py) 轉換為 Jupyter Notebook (.ipynb) 的方法：

### 1. 自製轉換腳本 (py_to_ipynb.py)

一個簡單的轉換工具，支援基本的轉換功能。使用方法：

```bash
python py_to_ipynb.py <input_py_file> <output_ipynb_file>
```

為了獲得更好的轉換結果，可以在原始 Python 檔案中使用特殊標記：

- `# %% [markdown]` - 標記下方內容為 markdown (每行以 # 開頭)
- `# %% [code]` - 標記下方內容為程式碼

### 2. jupytext (推薦)

更強大、更準確的轉換工具，能夠正確保留程式碼區塊的完整性。安裝：

```bash
pip install jupytext
```

使用方法：

```bash
jupytext --to notebook <input_py_file> -o <output_ipynb_file>
```

```bash
# 清理 Python 檔案內的ln[n] 標記
# 並保留原始 Python 檔案
python clean_notebook.py --py soln_translated\chapter0a.py

# 轉換 Python 檔案為 Jupyter Notebook
jupytext --to notebook --from py:light --update soln_translated\chapter0a.py -o soln_translated_ipynb\chapter0a.ipynb
```

### 3. ipynb_to_py.py (Jupyter Notebook 轉 Python)

將 Jupyter Notebook (.ipynb) 檔案轉換為 Python (.py) 檔案的工具。支援單一檔案轉換和批次轉換整個目錄。使用方法：

```bash
# 轉換單一檔案
python ipynb_to_py.py <input_ipynb_file> [output_py_file]

# 批次轉換整個目錄
python ipynb_to_py.py --batch <input_directory> [output_directory]
```

轉換後的 Python 檔案會保留原始 Jupyter Notebook 的單元格結構，將 markdown 單元格轉換為 Python 註釋，並保留程式碼單元格的內容。

如果您正在製作本書的翻譯或其他修改版本，建議 fork 此儲存庫。
