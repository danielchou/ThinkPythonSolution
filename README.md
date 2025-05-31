# Think Python, 3rd Edition

這個目錄包含 [Think Python](https://greenteapress.com/wp/think-python-3rd-edition/) 第三版的原始筆記本，其中包含練習題的解答。

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
