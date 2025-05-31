import nbformat as nbf
import re
import sys

def py_to_ipynb(py_file, ipynb_file):
    """將 Python 檔案轉換為 Jupyter Notebook 檔案，改進版本
    更準確地處理程式碼區塊與說明文字區塊的對應關係
    """
    
    # 讀取 Python 檔案
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 創建一個新的 notebook 物件
    nb = nbf.v4.new_notebook()
    
    # 檢查是否有使用特殊標記 (# %% [markdown] 或 # %% [code])
    has_special_markers = re.search(r'# %% \[(markdown|code)\]', content) is not None
    
    if has_special_markers:
        # 使用特殊標記處理
        process_with_markers(content, nb)
    else:
        # 使用傳統方式處理
        process_traditional(content, nb)
    
    # 寫入 notebook 檔案
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"已成功將 {py_file} 轉換為 {ipynb_file}")

def process_with_markers(content, nb):
    """使用特殊標記處理內容"""
    # 分割內容為帶有標記的區塊
    blocks = re.split(r'# %% \[(markdown|code)\]', content)
    
    # 第一個區塊可能是空的或沒有標記的程式碼
    if blocks[0].strip():
        nb.cells.append(nbf.v4.new_code_cell(blocks[0].strip()))
    
    # 處理剩餘的區塊
    for i in range(1, len(blocks), 2):
        if i < len(blocks):
            block_type = blocks[i]  # markdown 或 code
            block_content = blocks[i+1].strip() if i+1 < len(blocks) else ""
            
            if block_content:
                if block_type == 'markdown':
                    # 處理 markdown 內容 - 移除每行開頭的 # 符號
                    markdown_lines = []
                    for line in block_content.split('\n'):
                        if line.startswith('#'):
                            markdown_lines.append(line[1:].lstrip())
                        else:
                            markdown_lines.append(line)
                    
                    nb.cells.append(nbf.v4.new_markdown_cell('\n'.join(markdown_lines)))
                else:  # code
                    nb.cells.append(nbf.v4.new_code_cell(block_content))

def process_traditional(content, nb):
    """使用傳統方式處理內容，但改進了識別邏輯"""
    # 分割內容為單元格
    # 使用 "# In[數字]:" 作為分隔符
    cells_content = re.split(r'# In\[\d+\]:', content)
    
    # 處理所有單元格
    for cell_idx, cell_content in enumerate(cells_content):
        if not cell_content.strip():
            continue
            
        # 識別連續的註釋區塊作為 markdown
        # 使用更精確的正則表達式來捕獲連續的註釋行
        markdown_blocks = []
        code_blocks = []
        
        # 按行分割內容
        lines = cell_content.split('\n')
        
        current_block = []
        current_type = None  # 'markdown' 或 'code'
        
        for line in lines:
            line_stripped = line.strip()
            
            # 跳過空行
            if not line_stripped:
                if current_block and current_type:
                    if current_type == 'markdown':
                        markdown_blocks.append('\n'.join(current_block))
                    else:  # code
                        code_blocks.append('\n'.join(current_block))
                    current_block = []
                    current_type = None
                continue
                
            # 判斷行類型
            if line_stripped.startswith('#') and not line_stripped.startswith('#!/') and not line_stripped.startswith('# coding:'):
                # 這是註釋行
                if current_type == 'code' and current_block:
                    # 結束當前程式碼區塊
                    code_blocks.append('\n'.join(current_block))
                    current_block = []
                
                current_type = 'markdown'
                # 移除 # 符號並保留縮排
                markdown_line = line_stripped[1:].lstrip()
                current_block.append(markdown_line)
            else:
                # 這是程式碼行
                if current_type == 'markdown' and current_block:
                    # 結束當前 markdown 區塊
                    markdown_blocks.append('\n'.join(current_block))
                    current_block = []
                
                current_type = 'code'
                current_block.append(line)
        
        # 處理最後一個區塊
        if current_block:
            if current_type == 'markdown':
                markdown_blocks.append('\n'.join(current_block))
            else:  # code
                code_blocks.append('\n'.join(current_block))
        
        # 添加 markdown 和程式碼單元格到 notebook
        for markdown in markdown_blocks:
            if markdown.strip():
                nb.cells.append(nbf.v4.new_markdown_cell(markdown))
        
        for code in code_blocks:
            if code.strip():
                nb.cells.append(nbf.v4.new_code_cell(code))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python py_to_ipynb.py <input_py_file> <output_ipynb_file>")
        print("\n特殊格式說明:")
        print("  在 Python 檔案中，您可以使用以下特殊標記來明確區分 markdown 和程式碼:")
        print("  # %% [markdown]  - 標記下方內容為 markdown (每行以 # 開頭)")
        print("  # %% [code]     - 標記下方內容為程式碼")
        print("  使用這些標記可以確保更準確的轉換")
        sys.exit(1)
    
    py_file = sys.argv[1]
    ipynb_file = sys.argv[2]
    
    py_to_ipynb(py_file, ipynb_file)
