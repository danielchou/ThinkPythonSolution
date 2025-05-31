#!/usr/bin/env python
# coding: utf-8

# 你可以從
# [Bookshop.org](https://bookshop.org/a/98697/9781098155438) 和
# [Amazon](https://www.amazon.com/_/dp/1098155432?smid=ATVPDKIKX0DER&_encoding=UTF8&tag=oreilly20-20&_encoding=UTF8&tag=greenteapre01-20&linkCode=ur2&linkId=e2a529f94920295d27ec8a06e757dc7c&camp=1789&creative=9325)
# 訂購《Think Python 3e》的實體書和電子書版本。

# In[1]:


from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("已下載 " + str(local)) # 譯註：這裡顯示下載完成的檔案路徑
    return filename

download('https://github.com/AllenDowney/ThinkPython/raw/v3/thinkpython.py');
download('https://github.com/AllenDowney/ThinkPython/raw/v3/diagram.py');

import thinkpython


# # 變數與陳述句
#
# 在上一章，我們用了運算子來寫一些做算術運算的運算式。
#
# 在這一章，你會學到關於變數和陳述句、`import` 陳述句，還有 `print` 函式。
# 我也會介紹更多我們用來談論程式的詞彙，包括「引數」和「模組」。
#

# ## 變數
#
# **變數** 是一個指向某個值的名稱。
# 要建立一個變數，我們可以寫一個像這樣的 **賦值陳述句** (assignment statement)。

# In[2]:


n = 17


# 賦值陳述句有三個部分：左邊是變數的名稱，中間是等號 `=`，右邊是一個運算式。
# 在這個例子裡，運算式是一個整數。
# 在下面的例子裡，運算式是一個浮點數。

# In[3]:


pi = 3.141592653589793


# 而在下面的例子裡，運算式是一個字串。

# In[4]:


message = 'And now for something completely different' # 譯註：這是蒙提·派森的經典台詞「現在來看點完全不一樣的」


# 當你執行一個賦值陳述句時，不會有任何輸出。
# Python 會建立這個變數並給它一個值，但賦值陳述句本身沒有看得見的效果。
# 不過，建立變數之後，你就可以把它當作一個運算式來使用。
# 所以我們可以像這樣顯示 `message` 的值：

# In[5]:


message


# 你也可以把變數當作運算式的一部分，跟算術運算子一起用。

# In[6]:


n + 25


# In[7]:


2 * pi


# 你也可以在呼叫函式的時候使用變數。

# In[8]:


round(pi) # 譯註：round() 函式會將浮點數四捨五入到最接近的整數


# In[9]:


len(message) # 譯註：len() 函式會回傳字串的長度


# ## 狀態圖
#
# 在紙上表示變數的一個常見方法是寫下名稱，然後用箭頭指向它的值。

# In[10]:


import math

from diagram import make_binding, Frame # 譯註：這是書中用來畫圖的工具

# 譯註：以下程式碼是為了產生一個變數狀態的示意圖
binding = make_binding("message", 'And now for something completely different')
binding2 = make_binding("n", 17)
binding3 = make_binding("pi", 3.141592653589793)

frame = Frame([binding2, binding3, binding])


# In[11]:


from diagram import diagram, adjust # 譯註：這是書中用來畫圖的工具


width, height, x, y = [3.62, 1.01, 0.6, 0.76] # 譯註：圖表的繪製參數
ax = diagram(width, height)
bbox = frame.draw(ax, x, y, dy=-0.25)
# adjust(x, y, bbox) # 譯註：調整圖表位置的函式，這裡被註解掉了


# 這種圖叫做 **狀態圖** (state diagram)，因為它顯示了每個變數處於什麼狀態（把它想成是變數的「心理狀態」）。
# 我們會在整本書中用狀態圖來表示 Python 如何儲存變數和它們的值的模型。

# ## 變數名稱
#
# 變數名稱可以隨你喜歡取多長。它們可以包含字母和數字，但不能以數字開頭。
# 使用大寫字母是合法的，但習慣上變數名稱只用小寫字母。
#
# 變數名稱中唯一可以出現的標點符號是底線 `_`。它常用在有多個單字的名稱中，例如 `your_name` 或 `airspeed_of_unladen_swallow`（譯註：未負重燕子的空速，另一個蒙提·派森梗）。
#
# 如果你給變數取了一個不合法的名稱，你會得到一個語法錯誤。
# 名稱 `million!` 不合法，因為它包含標點符號。

# In[12]:


get_ipython().run_cell_magic('expect', 'SyntaxError', '\nmillion! = 1000000\n') # 譯註：這裡預期會發生語法錯誤 (SyntaxError)


# `76trombones` 不合法，因為它以數字開頭。

# In[13]:


get_ipython().run_cell_magic('expect', 'SyntaxError', "\n76trombones = 'big parade'\n") # 譯註：這裡預期會發生語法錯誤


# `class` 也不合法，但原因可能不太明顯。

# In[14]:


get_ipython().run_cell_magic('expect', 'SyntaxError', "\nclass = 'Self-Defence Against Fresh Fruit'\n") # 譯註：這裡預期會發生語法錯誤，「對抗新鮮水果的自衛術」，又一個蒙提·派森梗


# 原來 `class` 是一個 **關鍵字** (keyword)，它是一個特殊的字，用來指定程式的結構。
# 關鍵字不能當作變數名稱。
#
# 這裡是 Python 關鍵字的完整列表：

# ```
# False      await      else       import     pass
# None       break      except     in         raise
# True       class      finally    is         return
# and        continue   for        lambda     try
# as         def        from       nonlocal   while
# assert     del        global     not        with
# async      elif       if         or         yield
# ```

# In[15]:


from keyword import kwlist # 譯註：kwlist 是一個包含所有 Python 關鍵字的列表

len(kwlist) # 譯註：顯示 Python 關鍵字的數量


# 你不需要記住這個列表。在大多數的開發環境中，關鍵字會用不同的顏色顯示；如果你想用關鍵字當變數名稱，你就會知道了。

# ## import 陳述句
#
# 為了使用某些 Python 功能，你必須 **匯入** (import) 它們。
# 例如，下面的陳述句匯入了 `math` 模組。

# In[16]:


import math


# **模組** (module) 是一堆變數和函式的集合。
# math 模組提供了一個叫做 `pi` 的變數，它包含了數學常數 $\pi$ 的值。
# 我們可以像這樣顯示它的值。

# In[17]:


math.pi


# 要使用模組中的變數，你必須在模組名稱和變數名稱之間使用 **點運算子** (`.`)。
#
# math 模組也包含函式。
# 例如，`sqrt` 計算平方根。

# In[18]:


math.sqrt(25)


# 而 `pow` 計算一個數字的次方。

# In[19]:


math.pow(5, 2) # 譯註：計算 5 的 2 次方


# 到目前為止，我們看過兩種計算次方的方法：可以用 `math.pow` 函式，也可以用次方運算子 `**`。
# 兩種都可以，但運算子比函式更常用。

# ## 運算式與陳述句
#
# 到目前為止，我們已經看過幾種運算式。
# 一個運算式可以是一個單獨的值，像是整數、浮點數或字串。
# 它也可以是一堆值和運算子的組合。
# 而且它可以包含變數名稱和函式呼叫。
# 這裡有一個包含好幾個這些元素的運算式。

# In[20]:


19 + n + round(math.pi) * 2


# 我們也看過幾種陳述句。
# **陳述句** (statement) 是一段有效果但沒有值的程式碼。
# 例如，賦值陳述句會建立一個變數並給它一個值，但陳述句本身沒有值。

# In[21]:


n = 17


# 同樣地，import 陳述句有效果——它匯入一個模組，讓我們可以使用它包含的變數和函式——但它沒有看得見的效果。

# In[22]:


import math


# 計算運算式的值叫做 **求值** (evaluation)。
# 執行一個陳述句叫做 **執行** (execution)。

# ## print 函式
#
# 當你對一個運算式求值時，結果會被顯示出來。(在 Jupyter Notebook 或 Python 直譯器環境中)

# In[23]:


n + 1


# 但如果你對多個運算式求值，只有最後一個的值會被顯示出來。(在 Jupyter Notebook 或 Python 直譯器的一個儲存格/輸入行中)

# In[24]:


n + 2
n + 3


# 要顯示多個值，你可以使用 `print` 函式。

# In[25]:


print(n+2)
print(n+3)


# 它對浮點數和字串也有效。

# In[26]:


print('pi 的值大約是') # 譯註：將英文改為中文
print(math.pi)


# 你也可以使用一連串用逗號隔開的運算式。

# In[27]:


print('pi 的值大約是', math.pi) # 譯註：將英文改為中文


# 注意 `print` 函式會在值之間放一個空格。

# ## 引數 (Arguments)
#
# 當你呼叫一個函式時，括號裡的運算式叫做 **引數** (argument)。
# 一般來說我會解釋為什麼，但在這個例子中，這個詞的技術含義和它的一般含義幾乎沒有關係，所以我甚至不打算試著解釋。
#
# 我們目前看過的一些函式只需要一個引數，像是 `int`。

# In[28]:


int('101') # 譯註：將字串 '101' 轉換為整數 101


# 有些需要兩個，像是 `math.pow`。

# In[29]:


math.pow(5, 2) # 譯註：5 的 2 次方


# 有些函式可以接受額外的、可選的引數。
# 例如，`int` 可以接受第二個引數，用來指定數字的基底（進位制）。

# In[30]:


int('101', 2) # 譯註：將二進位的 '101' 轉換為十進位的 5


# 二進位的數字序列 `101` 代表十進位的數字 5。
#
# `round` 也可以接受一個可選的第二個引數，也就是要四捨五入到的小數位數。

# In[31]:


round(math.pi, 3) # 譯註：將 pi 四捨五入到小數點後三位


# 有些函式可以接受任意數量的引數，像是 `print`。

# In[32]:


print('任意', '數量', '的', '引數') # 譯註：將英文改為中文


# 如果你呼叫函式時提供了太多引數，那會是個 `TypeError` (型別錯誤)。

# In[33]:


get_ipython().run_cell_magic('expect', 'TypeError', "\nfloat('123.0', 2)\n") # 譯註：這裡預期會發生 TypeError，因為 float() 不接受第二個引數


# 如果你提供的引數太少，那也是個 `TypeError`。

# In[34]:


get_ipython().run_cell_magic('expect', 'TypeError', '\nmath.pow(2)\n') # 譯註：這裡預期會發生 TypeError，因為 math.pow() 需要兩個引數


# 如果你提供了一個函式無法處理的型別的引數，那也是個 `TypeError`。

# In[35]:


get_ipython().run_cell_magic('expect', 'TypeError', "\nmath.sqrt('123')\n") # 譯註：這裡預期會發生 TypeError，因為 math.sqrt() 不能處理字串


# 這種檢查在你剛開始學的時候可能會有點煩人，但它能幫助你偵測和修正錯誤。

# ## 註解 (Comments)
#
# 隨著程式越來越大、越來越複雜，它們也越來越難閱讀。
# 形式語言很精煉，常常很難看懂一段程式碼在做什麼以及為什麼這麼做。
#
# 因此，在你的程式中加入筆記，用自然語言解釋程式在做什麼，是個好主意。
# 這些筆記叫做 **註解** (comments)，它們以 `#` 符號開頭。

# In[36]:


# 42分42秒的總秒數
seconds = 42 * 60 + 42


# 在這個例子中，註解自己佔了一行。你也可以把註解放在一行的結尾：

# In[37]:


miles = 10 / 1.61     # 10公里換算成英里


# 從 `#` 到行尾的所有內容都會被忽略——它對程式的執行沒有任何影響。
#
# 註解在記錄程式碼中不明顯的特性時最有用。
# 我們可以合理地假設讀者能看懂程式碼在 *做什麼*；解釋 *為什麼* 這麼做更有用。
#
# 這個註解和程式碼重複了，沒什麼用：

# In[38]:


v = 8     # 把 8 賦值給 v


# 這個註解包含了程式碼中沒有的有用資訊：

# In[39]:


v = 8     # 速度，單位是英里/小時


# 好的變數名稱可以減少對註解的需求，但是長的名稱可能會讓複雜的運算式難以閱讀，所以這是一個取捨。

# ## 除錯 (Debugging)
#
# 程式中可能發生三種錯誤：語法錯誤、執行期錯誤和語義錯誤。
# 區分它們有助於更快地找出問題。
#
# * **語法錯誤 (Syntax error)**：「語法」指的是程式的結構以及關於該結構的規則。如果你的程式任何地方有語法錯誤，Python 不會執行這個程式。它會立刻顯示錯誤訊息。
#
# * **執行期錯誤 (Runtime error)**：如果你的程式沒有語法錯誤，它就可以開始執行。但如果執行過程中出了問題，Python 會顯示錯誤訊息並停止。這種錯誤稱為執行期錯誤。它也被稱為 **例外** (exception)，因為它表示發生了例外情況。
#
# * **語義錯誤 (Semantic error)**：第三種錯誤是「語義」錯誤，意思是與「意義」相關。如果你的程式有語義錯誤，它會執行而不會產生錯誤訊息，但它不會做你想要它做的事。找出語義錯誤可能很棘手，因為你需要透過觀察程式的輸出來反向推敲它到底在做什麼。

# 如同我們所見，不合法的變數名稱是一個語法錯誤。

# In[40]:


get_ipython().run_cell_magic('expect', 'SyntaxError', '\nmillion! = 1000000\n') # 譯註：預期語法錯誤


# 如果你對一個運算子使用了它不支援的型別，那是一個執行期錯誤。

# In[41]:


get_ipython().run_cell_magic('expect', 'TypeError', "\n'126' / 3\n") # 譯註：預期 TypeError，字串不能除以數字


# 最後，這裡有一個語義錯誤的例子。
# 假設我們想計算 `1` 和 `3` 的平均值，但我們忘了運算順序，寫成這樣：

# In[42]:


1 + 3 / 2


# 當這個運算式被求值時，它不會產生錯誤訊息，所以沒有語法錯誤或執行期錯誤。
# 但結果不是 `1` 和 `3` 的平均值，所以程式不正確。
# 這是一個語義錯誤，因為程式執行了，但沒有做預期的事情。 (譯註：正確的平均值是 (1+3)/2 = 2，而 1 + 3/2 = 1 + 1.5 = 2.5)

# ## 詞彙表
#
# **變數 (variable):**
# 一個指向值的名稱。
#
# **賦值陳述句 (assignment statement):**
# 一個將值賦予變數的陳述句。
#
# **狀態圖 (state diagram):**
# 一種圖形表示法，用來呈現一組變數以及它們所指向的值。
#
# **關鍵字 (keyword):**
# 一個特殊的字，用來指定程式的結構。
#
# **import 陳述句 (import statement):**
# 一個讀取模組檔案的陳述句，這樣我們就可以使用它包含的變數和函式。
#
# **模組 (module):**
# 一個包含 Python 程式碼的檔案，包括函式定義，有時也包含其他陳述句。
#
# **點運算子 (dot operator):**
# 運算子 `.`，用來存取另一個模組中的函式或變數，方法是指定模組名稱，後面跟著一個點和函式/變數名稱。
#
# **求值 (evaluate):**
# 執行運算式中的運算以計算出一個值。
#
# **陳述句 (statement):**
# 一行或多行程式碼，代表一個命令或動作。
#
# **執行 (execute):**
# 執行一個陳述句並完成它所說的事情。
#
# **引數 (argument):**
# 呼叫函式時提供給函式的值。
#
# **註解 (comment):**
# 包含在程式中，提供關於程式的資訊，但對其執行沒有影響的文字。
#
# **執行期錯誤 (runtime error):**
# 導致程式顯示錯誤訊息並退出的錯誤。
#
# **例外 (exception):**
# 程式執行期間偵測到的錯誤。
#
# **語義錯誤 (semantic error):**
# 導致程式做錯事，但不會顯示錯誤訊息的錯誤。

# ## 練習

# In[43]:


# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在做練習之前先執行它。

get_ipython().run_line_magic('xmode', 'Verbose')


# ### 問問虛擬助理
#
# 再次，我鼓勵你使用虛擬助理來學習更多關於本章任何主題的知識。
#
# 如果你對我列出的任何關鍵字感到好奇，你可以問「為什麼 class 是個關鍵字？」或「為什麼變數名稱不能是關鍵字？」
#
# 你可能已經注意到 `int`、`float` 和 `str` 不是 Python 關鍵字。
# 它們是代表型別的變數，並且可以作為函式使用。
# 所以，用這些名稱作為變數或函式名稱是 *合法的*，但強烈不建議這樣做。問問助理「為什麼用 int、float 和 str 作為變數名稱是不好的？」
#
# 另外也問問，「Python 中有哪些內建函式？」
# 如果你對其中任何一個感到好奇，可以要求更多資訊。
#
# 在本章中，我們匯入了 `math` 模組並使用它提供的一些變數和函式。問問助理，「math 模組中有哪些變數和函式？」以及「除了 math 之外，還有哪些模組被認為是 Python 的核心模組？」

# ### 練習
#
# 重複我上一章的建議，每當你學習一個新功能時，你應該故意犯錯，看看會發生什麼問題。
#
# -   我們已經看到 `n = 17` 是合法的。那麼 `17 = n` 呢？ (譯註：試試看會發生什麼錯誤！)
#
# -   `x = y = 1` 怎麼樣？ (譯註：這合法嗎？x 和 y 的值會是什麼？)
#
# -   在某些語言中，每個陳述句都以分號 (`;`) 結尾。如果你在 Python 陳述句的結尾加上分號會發生什麼事？ (譯註：Python 通常不需要分號，但加了會怎樣？)
#
# -   如果你在陳述句的結尾加上句點 (`.`) 呢？ (譯註：這會是合法的 Python 語法嗎？)
#
# -   如果你拼錯了模組的名稱，試圖匯入 `maath` 會發生什麼事？ (譯註：例如打成 `import maath` 而不是 `import math`)

# ### 練習
# 練習使用 Python 直譯器當作計算機：
#
# **第 1 部分：** 半徑為 $r$ 的球體體積是 $\frac{4}{3} \pi r^3$。
# 半徑為 5 的球體體積是多少？從一個名為 `radius` 的變數開始，然後將結果賦值給一個名為 `volume` 的變數。顯示結果。加上註解說明 `radius` 的單位是公分，`volume` 的單位是立方公分。

# In[44]:


# 解答

radius = 5                            # 單位：公分
volume = 4 / 3 * math.pi * radius**3  # 單位：立方公分
volume


# **第 2 部分：** 三角學的一個法則是，對於任何 $x$ 值，$(\cos x)^2 + (\sin x)^2 = 1$。讓我們看看對於特定的 $x$ 值，例如 42，這是否成立。
#
# 建立一個名為 `x` 並賦予這個值的變數。
# 然後使用 `math.cos` 和 `math.sin` 計算 $x$ 的餘弦和正弦，以及它們平方的總和。
#
# 結果應該接近 1。它可能不完全是 1，因為浮點數運算不是精確的——它只是近似正確。

# In[52]: # 譯註：原 In[45] 在我的環境變成 In[52]，不影響程式碼


# 解答

x = 42
math.cos(x)**2 + math.sin(x)**2


# **第 3 部分：** 除了 `pi` 之外，`math` 模組中定義的另一個變數是 `e`，它代表自然對數的底，數學符號寫作 $e$。如果你不熟悉這個值，可以問虛擬助理「什麼是 `math.e`？」現在讓我們用三種方法計算 $e^2$：
#
# * 使用 `math.e` 和次方運算子 (`**`)。
#
# * 使用 `math.pow` 將 `math.e` 提高到 `2` 次方。
#
# * 使用 `math.exp`，它接受一個引數值 $x$，並計算 $e^x$。
#
# 你可能會注意到最後一個結果與前兩個略有不同。
# 試著找出哪一個是正確的。(提示：可以查閱 `math.exp` 的文件或比較它們的精確度)

# In[46]:


# 解答

math.e ** 2


# In[47]:


# 解答

math.pow(math.e, 2)


# In[48]:


# 解答

math.exp(2)


# In[ ]:





# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)