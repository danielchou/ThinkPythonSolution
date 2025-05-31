# -*- coding: utf-8 -*-
# 從 chap19.ipynb 轉換而來
# 使用 ipynb_to_py.py 腳本自動轉換

# 你可以從以下網站訂購《Think Python 3e》的紙本版和電子書：
# [Bookshop.org](https://bookshop.org/a/98697/9781098155438) 和
# [Amazon](https://www.amazon.com/_/dp/1098155432?smid=ATVPDKIKX0DER&_encoding=UTF8&tag=oreilly20-20&_encoding=UTF8&tag=greenteapre01-20&linkCode=ur2&linkId=e2a529f94920295d27ec8a06e757dc7c&camp=1789&creative=9325).

# # 最後的思考 (Final thoughts)

# 學習程式設計並不容易，但如果你能堅持到這裡，你已經有了一個很好的開始。
# 現在我有一些關於如何繼續學習以及如何應用所學知識的建議。
#
# 這本書旨在作為程式設計的概括性介紹，所以我們沒有專注於特定的應用領域。
# 根據你的興趣，你可以在許多領域應用你的新技能。
#
# 如果你對資料科學 (Data Science) 感興趣，我寫的三本書你可能會喜歡：
#
# * 《Think Stats: Exploratory Data Analysis》(統計思維：探索性資料分析)，O'Reilly Media 出版，2014年。
#
# * 《Think Bayes: Bayesian Statistics in Python》(貝氏思維：Python 中的貝氏統計)，O'Reilly Media 出版，2021年。
#
# * 《Think DSP: Digital Signal Processing in Python》(數位訊號處理思維：Python 中的數位訊號處理)，O'Reilly Media 出版，2016年。

# 如果你對物理建模和複雜系統感興趣，你可能會喜歡：
#
# * 《Modeling and Simulation in Python: An Introduction for Scientists and Engineers》(Python 中的建模與模擬：科學家與工程師入門)，No Starch Press 出版，2023年。
#
# * 《Think Complexity: Complexity Science and Computational Modeling》(複雜性科學思維：複雜性科學與計算建模)，O'Reilly Media 出版，2018年。
#
# 這些書使用了 NumPy、SciPy、pandas 以及其他用於資料科學和科學計算的 Python 函式庫。

# 這本書試圖在程式設計的一般原則和 Python 的細節之間找到平衡。
# 因此，它並沒有包含 Python 語言的每一個特性。
# 想了解更多關於 Python 的知識以及如何善用它的建議，我推薦 Luciano Ramalho 的
# 《Fluent Python: Clear, Concise, and Effective Programming》(流暢的 Python：清晰、簡潔且有效的程式設計)，第二版，O'Reilly Media 出版，2022年。
#
# 在學習了程式設計入門之後，一個常見的下一步是學習資料結構和演算法。
# 我正在撰寫一本關於這個主題的書，叫做《Data Structures and Information Retrieval in Python》(Python 中的資料結構與資訊檢索)。
# 免費的電子版可以從 Green Tea Press 取得：<https://greenteapress.com>。

# 當你開始處理更複雜的程式時，你會遇到新的挑戰。
# 你可能會發現回顧本書中關於除錯 (debugging) 的章節會很有幫助。
# 特別是，請記住[第十二章](section_debugging_12)提到的除錯六字訣 (Six R's of debugging)：
# 閱讀 (Reading)、執行 (Running)、思考 (Ruminating)、小黃鴨除錯法 (Rubber-ducking)、退回 (Retreating) 和休息 (Resting)。
# (譯註：section_debugging_12 指的是書中對應章節的連結，這裡無法直接點擊，但可以理解為一個章節參考)
#
# 這本書建議了一些有助於除錯的工具，包括 `print` 和 `repr` 函數，
# [第十一章](section_debugging_11)中的 `structshape` 函數 —— 以及
# [第十四章](section_debugging_14)中的內建函數 `isinstance`、`hasattr` 和 `vars`。
# (譯註：同樣，這些章節連結是指向書中內容的)

# 書中也建議了測試程式的工具，包括 `assert` 陳述式、`doctest` 模組和 `unittest` 模組。
# 在你的程式中加入測試是預防和偵測錯誤、節省除錯時間的最佳方法之一。
#
# 但是最好的除錯是你不需要做的那種。
# 如果你使用[第六章](section_incremental)中描述的漸進式開發過程 (incremental development process) ——
# 並且邊做邊測試 —— 你犯的錯誤會更少，而且犯錯時也能更快找到它們。
# (譯註：section_incremental 指的是書中對應章節的連結)
# 另外，請記住[第四章](section_encapsulation)的封裝 (encapsulation) 和泛化 (generalization)，
# 這在你在 Jupyter notebook 中開發程式碼時特別有用。
# (譯註：section_encapsulation 指的是書中對應章節的連結)

# 在這本書中，我一直建議使用虛擬助理來幫助你學習、編程和除錯。
# 我希望你覺得這些工具很有用。
#
# 除了像 ChatGPT 這樣的虛擬助理之外，你可能還想使用像 Copilot 這樣在你輸入時自動補全程式碼的工具。
# 我一開始沒有推薦使用這些工具，因為它們對初學者來說可能會讓人不知所措。
# 但你現在可以開始探索它們了。
#
# 有效地使用 AI 工具需要一些實驗和反思，才能找到適合你的流程。
# 如果你覺得把程式碼從 ChatGPT 複製到 Jupyter 很麻煩，你可能會比較喜歡 Copilot 這樣的工具。
# 但是，你為了撰寫提示 (prompt) 和解讀回應所做的認知工作，可能和工具產生的程式碼一樣有價值，
# 這與小黃鴨除錯法的精神是相同的。

# 隨著你程式設計經驗的增加，你可能會想探索其他的開發環境。
# 我認為 Jupyter notebook 是一個很好的起點，但它們相對較新，
# 也不如傳統的整合開發環境 (IDE, Integrated Development Environment) 那麼普及。
# 對於 Python 來說，最受歡迎的 IDE 包括 PyCharm 和 Spyder ——
# 還有經常推薦給初學者的 Thonny。
# 其他 IDE，像是 Visual Studio Code 和 Eclipse，也適用於其他程式語言。
# 或者，作為一個更簡單的替代方案，你可以用任何你喜歡的文字編輯器來寫 Python 程式。
#
# 在你繼續你的程式設計旅程時，你不必孤軍奮戰！
# 如果你住在城市裡或附近，很有可能有一個你可以加入的 Python 使用者群組。
# 這些群組通常對初學者很友善，所以不要害怕。
# 如果你附近沒有群組，你也許可以遠端參與活動。
# 另外，多留意區域性的 Python 研討會。

# 提升程式設計技能的最佳方法之一是學習另一種語言。
# 如果你對統計和資料科學感興趣，你可能想學習 R 語言。
# 但我特別推薦學習一種函數式語言，像是 Racket 或 Elixir。
# 函數式程式設計需要一種不同的思考方式，這會改變你對程式的看法。
#
# 祝你好運！

# (這個儲存格是空的)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)