# -*- coding: utf-8 -*-
# 從 jupyter_intro.ipynb 轉換而來
# 使用 ipynb_to_py.py 腳本自動轉換

# # Jupyter 上的 *Think Python*
#
# 這是為正在閱讀 Allen B. Downey 所著的第三版 [*Think Python*](https://greenteapress.com/wp/think-python-3rd-edition) 的讀者準備的 Jupyter Notebook 簡介。
#
# Jupyter Notebook 是一種包含文字、程式碼以及程式碼執行結果的文件。
# 你可以像讀書一樣閱讀 Notebook，但你也可以執行其中的程式碼、修改它，以及開發新的程式。
#
# Jupyter Notebook 在網頁瀏覽器中執行，所以你不需要安裝任何新的軟體就可以執行它們。
# 但是它們必須連接到一個 Jupyter 伺服器。
#
# 你可以自己安裝並執行一個伺服器，但要開始的話，使用像 [Colab](https://colab.research.google.com/) 這樣的服務會比較容易，
# Colab 是由 Google 維運的。
#
# [在本書的起始頁面](https://allendowney.github.io/ThinkPython)，你會找到每一章的連結。
# 如果你點擊其中一個連結，它會在 Colab 上開啟一個 Notebook。

# 如果你正在 Colab 上閱讀這個 Notebook，你應該會在左上角看到一個橘色的標誌，看起來像字母 `CO`。
#
# 如果你不是在 Colab 上執行這個 Notebook，[你可以點擊這裡在 Colab 上開啟它](https://colab.research.google.com/github/AllenDowney/ThinkPython/blob/v3/chapters/jupyter_intro.ipynb)。

# ## 什麼是 Notebook？
#
# Jupyter Notebook 由許多「儲存格 (cell)」組成，每個儲存格可以包含文字或程式碼。
# 這個儲存格包含的是文字。
#
# 下面這個儲存格包含的是程式碼。

print('哈囉') # "Hello" 的中文翻譯

# 點擊上一個儲存格來選取它。
# 你應該會在左邊看到一個按鈕，上面有一個圓圈包著三角形，這是「播放 (Play)」的圖示。
# 如果你按下這個按鈕，Jupyter 會執行儲存格中的程式碼並顯示結果。
#
# 當你第一次在 Notebook 中執行程式碼時，可能需要幾秒鐘來啟動。
# 如果是你沒有寫過的 Notebook，你可能會收到一個警告訊息。
# 如果你執行的是來自你信任來源的 Notebook (我希望我包括在內)，你可以按下「仍然執行 (Run Anyway)」。

# 除了點擊「播放」按鈕，你也可以按住 `Shift` 鍵再按 `Enter` 鍵來執行儲存格中的程式碼。
#
# 如果你正在 Colab 上執行這個 Notebook，你應該會在左上方看到寫著「+ 程式碼 (+ Code)」和「+ 文字 (+ Text)」的按鈕。
# 第一個按鈕會新增一個程式碼儲存格，第二個會新增一個文字儲存格。
# 如果你想試試看，請點擊選取這個儲存格，然後按下「+ 文字 (+ Text)」按鈕。
# 一個新的儲存格應該會出現在這個儲存格的下方。

# 在儲存格中加入一些文字。
# 你可以用按鈕來設定格式，或者你可以使用 [Markdown](https://www.markdownguide.org/basic-syntax/) 來標記文字。
# (Markdown 是一種輕量級標記語言，可以用簡單的符號來設定文字格式，例如用 *斜體* 或 **粗體**)
# 完成後，按住 `Shift` 鍵再按 `Enter` 鍵，這樣會格式化你剛才輸入的文字，然後移動到下一個儲存格。

# Jupyter 隨時都處於以下兩種模式之一：
#
# * 在 **命令模式 (command mode)** 中，你可以執行影響儲存格的操作，例如新增和移除整個儲存格。
#
# * 在 **編輯模式 (edit mode)** 中，你可以編輯儲存格的內容。
#
# 對於文字儲存格，你處於哪種模式是很明顯的。
# 在編輯模式下，儲存格會垂直分割，你正在編輯的文字在左邊，格式化後的文字在右邊。
# 並且你會在頂部看到文字編輯工具。
# 在命令模式下，你只會看到格式化後的文字。
#
# 對於程式碼儲存格，差異比較細微，但如果儲存格中有游標，你就處於編輯模式。
#
# 要從編輯模式切換到命令模式，請按 `ESC` 鍵。
# 要從命令模式切換到編輯模式，請按 `Enter` 鍵。

# 當你完成 Notebook 的工作後，你可以關閉視窗，但你所做的任何變更都會消失。
# 如果你做了任何想保留的變更，請開啟左上角的「檔案 (File)」選單。
# 你會看到幾種儲存 Notebook 的方式。
#
# * 如果你有 Google 帳戶，你可以把 Notebook 儲存到你的雲端硬碟 (Drive) 中。
#
# * 如果你有 GitHub 帳戶，你可以把它儲存到 GitHub 上。
#
# * 或者，如果你想把 Notebook 儲存到你的電腦上，選擇「下載 (Download)」，然後選擇「下載 .ipynb (.ipynb Download)」。
#   副檔名 ".ipynb" 表示它是一個 Notebook 檔案，與 ".py" 不同，".py" 表示只包含 Python 程式碼的檔案。

# ## *Think Python* 的程式碼
#
# 在每個 Notebook 的開頭，你會看到像下面這樣的程式碼儲存格：

from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("已下載 " + str(local)) # 已中文化
    return filename

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/thinkpython.py')

import thinkpython

# 你不需要知道這段程式碼是如何運作的，但當你讀完這本書的時候，大部分內容對你來說就會有意義了。
# 如你所猜測的，它會下載一個檔案 —— 具體來說，它會下載 `thinkpython.py`，
# 這個檔案包含了專為本書提供的 Python 程式碼。
# 最後一行「匯入 (imports)」了這些程式碼，這表示我們可以在 Notebook 中使用這些程式碼。
#
# 在其他章節中，你會看到下載 `diagram.py` (用於產生書中的圖表)
# 和 `jupyturtle.py` (在好幾章中用於建立海龜繪圖) 的程式碼。
#
# 在某些地方，你會看到像這樣以 `%%expect` 開頭的儲存格。

%%expect SyntaxError

# abs 42 # 這裡的語法是錯誤的，abs() 函數呼叫需要括號，例如 abs(42)

# `%%expect` 不是 Python 的一部分 —— 它是 Jupyter 的一個「魔法指令 (magic command)」，
# 表示我們預期這個儲存格會產生一個錯誤。
# 當你看到這個指令時，表示這個錯誤是刻意設計的，通常是為了警告你一個常見的陷阱。

# 想了解更多關於在 Colab 上執行 Jupyter Notebook 的資訊，[請點擊這裡](https://colab.research.google.com/notebooks/basic_features_overview.ipynb)。
#
# 或者，如果你準備好開始了，[請點擊這裡閱讀第一章](https://colab.research.google.com/github/AllenDowney/ThinkPython/blob/v3/chapters/chap01.ipynb)。

# *Think Python*, 第三版。
#
# Copyright 2023 [Allen B. Downey](https://allendowney.com)
#
# 授權條款: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
# (創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際)

# (這個儲存格是空的)