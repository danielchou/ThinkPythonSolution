# 從 chap10.ipynb 轉換而來
# 使用 ipynb_to_py.py 腳本自動轉換

# 你可以從以下網站訂購《Think Python 3e》的紙本版和電子書：
# [Bookshop.org](https://bookshop.org/a/98697/9781098155438) 和
# [Amazon](https://www.amazon.com/_/dp/1098155432?smid=ATVPDKIKX0DER&_encoding=UTF8&tag=oreilly20-20&_encoding=UTF8&tag=greenteapre01-20&linkCode=ur2&linkId=e2a529f94920295d27ec8a06e757dc7c&camp=1789&creative=9325).

from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("已下載 " + str(local)) # 把下載訊息也中文化
    return filename

download('https://github.com/AllenDowney/ThinkPython/raw/v3/thinkpython.py');
download('https://github.com/AllenDowney/ThinkPython/raw/v3/diagram.py');

import thinkpython

# # 字典 (Dictionaries)
#
# 這一章要介紹一個叫做字典 (dictionary) 的內建型別。
# 它是 Python 最棒的功能之一 —— 也是許多高效率且優雅演算法的基石。
#
# 我們會用字典來計算一本書中有多少個不重複的單字，以及每個單字出現的次數。
# 在練習題中，我們還會用字典來解決一些文字謎題。

# ## 字典是一種對應 (A dictionary is a mapping)
#
# **字典 (dictionary)** 有點像列表 (list)，但功能更廣泛。
# 在列表中，索引必須是整數；但在字典中，索引幾乎可以是任何型別。
# 舉例來說，假設我們建立一個數字單字的列表，像這樣：

lst = ['zero', 'one', 'two'] # 零、一、二

# 我們可以用整數當作索引來取得對應的單字。

lst[1] # 取得索引為 1 的元素，也就是 'one'

# 但假設我們想反過來，查一個單字來得到對應的整數。
# 用列表做不到這件事，但用字典就可以了。
# 我們先建立一個空字典，然後把它指派給變數 `numbers`。

numbers = {} # 大括號 {} 代表空字典
numbers

# 大括號 `{}` 代表一個空字典。
# 要把項目 (item) 加到字典裡，我們會用方括號 `[]`。

numbers['zero'] = 0 # 把 'zero' 這個鍵 (key) 對應到 0 這個值 (value)

# 這個賦值運算會在字典中加入一個 **項目 (item)**，它代表一個 **鍵 (key)** 和一個 **值 (value)** 之間的關聯。
# 在這個例子中，鍵是字串 `'zero'`，而值是整數 `0`。
# 如果我們顯示這個字典，會看到它包含一個項目，其中鍵和值用冒號 `:` 分隔。

numbers

# 我們可以像這樣加入更多項目。

numbers['one'] = 1
numbers['two'] = 2
numbers

# 現在這個字典包含三個項目了。
#
# 要查詢一個鍵並取得對應的值，我們還是用方括號運算子 `[]`。

numbers['two'] # 查詢鍵 'two' 對應的值

# 如果鍵不在字典裡，我們會得到一個 `KeyError` (鍵錯誤)。

%%expect KeyError
# numbers['three'] # 'three' 這個鍵不在字典裡

# `len()` 函數可以用在字典上；它會回傳項目的數量。

len(numbers)

# 用數學的語言來說，字典代表了一種從鍵到值的 **對應 (mapping)**，所以你也可以說每個鍵 "對應到 (maps to)" 一個值。
# 在這個例子中，每個數字單字都對應到相應的整數。
#
# 下圖顯示了 `numbers` 的狀態圖。
# (狀態圖顯示變數 `numbers` 指向一個字典物件，裡面有 'zero'->0, 'one'->1, 'two'->2 的對應關係)

from diagram import make_dict, Binding, Value

d1 = make_dict(numbers, dy=-0.3, offsetx=0.37)
binding1 = Binding(Value('numbers'), d1)

from diagram import diagram, adjust, Bbox

width, height, x, y = [1.83, 1.24, 0.49, 0.85]
ax = diagram(width, height)
bbox = binding1.draw(ax, x, y)
# adjust(x, y, bbox)

# 字典用一個方框表示，方框外面寫著 "dict"，裡面則是項目。
# 每個項目都用一個鍵和一個指向值的箭頭來表示。
# 引號表示這裡的鍵是字串，而不是變數名稱。

# ## 建立字典 (Creating dictionaries)
#
# 在上一節，我們建立了一個空字典，然後用方括號運算子一個一個地加入項目。
# 其實，我們也可以像這樣一次就把字典建立好。

numbers = {'zero': 0, 'one': 1, 'two': 2}

# 每個項目都包含一個鍵和一個值，用冒號隔開。
# 項目之間用逗號隔開，並且整個字典用大括號包起來。
#
# 建立字典的另一種方法是使用 `dict()` 函數。
# 我們可以像這樣建立一個空字典。

empty = dict()
empty

# 我們也可以像這樣複製一個字典。

numbers_copy = dict(numbers) # 建立 numbers 字典的一個副本
numbers_copy

# 在執行會修改字典的操作之前，先建立一個副本通常是很有用的。
# (這樣才不會不小心改到原始的字典)

# ## in 運算子 (The in operator)
#
# `in` 運算子也可以用在字典上；它會告訴你某個東西是否作為字典中的一個 *鍵* 出現。

'one' in numbers # 檢查 'one' 是否是 numbers 字典中的一個鍵

# `in` 運算子 *不會* 檢查某個東西是否作為值出現。

1 in numbers # 檢查 1 是否是 numbers 字典中的一個鍵 (答案是不，1 是值)

# 要查看某個東西是否作為值出現在字典中，你可以使用 `values()` 方法，
# 它會回傳一個包含所有值的序列，然後再使用 `in` 運算子。

1 in numbers.values() # 檢查 1 是否在 numbers 字典的所有值中出現

# Python 字典中的項目儲存在一個 **雜湊表 (hash table)** 中，這是一種組織資料的方式，
# 它有一個很棒的特性：不管字典裡有多少個項目，`in` 運算子所花費的時間都差不多。
# 這使得我們可以寫出一些效率非常高的演算法。

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

# 為了示範，我們會比較兩種演算法來找出單字配對，其中一個單字是另一個的反轉 —— 像是 `stressed` 和 `desserts`。
# 我們先從讀取單字列表開始。

# 確保檔案存在才開啟
word_list_content = ""
if exists('words.txt'):
    word_list_content = open('words.txt', encoding='utf-8').read()
else:
    print("錯誤: words.txt 檔案未找到。請先下載。")

word_list = word_list_content.split() # 分割成單字列表
print(f"單字列表中的單字數量: {len(word_list)}")

# 這是上一章的 `reverse_word` 函數。

def reverse_word(word):
    return ''.join(reversed(word))

# 下面的函數會遍歷列表中的所有單字。
# 對於每個單字，它會反轉字母，然後檢查反轉後的單字是否在單字列表中。

def too_slow():
    count = 0
    if not word_list: # 如果 word_list 是空的，就不用跑了
        print("單字列表是空的，無法執行 too_slow。")
        return 0
    for word in word_list:
        if reverse_word(word) in word_list: # 檢查反轉字是否在列表中
            count += 1
    return count

# 這個函數執行起來要花超過一分鐘。 (在作者的電腦上)
# 問題在於 `in` 運算子會一個一個地檢查列表中的單字，從頭開始。
# 如果它找不到要找的東西 —— 大部分情況都是這樣 —— 它就必須搜尋到列表的最後。

# 要測量一個函數執行多久，我們可以用 `%time`，這是 Jupyter 的「內建魔法指令」之一。
# 這些指令不是 Python 語言的一部分，所以在其他開發環境中可能無法運作。

# %time result_slow = too_slow() # 加上 result_slow 以便查看結果
# print(f"too_slow 找到的相反詞配對數量 (近似值，因為一個詞可能有多個相反詞都在列表裡): {result_slow}")
# (注意：這裡的 count 是指有多少個單字的反轉詞也在列表中，不是指不重複的相反詞配對數)
# (例如 stressed 和 desserts 會讓 count 加 2)

# 而且 `in` 運算子是在迴圈裡面，所以每個單字都會執行一次。
# 因為列表裡有超過 10 萬個單字，而對每個單字我們都要檢查超過 10 萬個單字，
# 所以總比較次數大約是單字數量的平方 —— 差不多是 130 億次。

if word_list: # 避免 word_list 為空時出錯
    print(f"單字數量平方約為: {len(word_list)**2:,}") # 加上千分位分隔符

# 用字典可以讓這個函數快很多。
# 下面的迴圈會建立一個字典，其中包含單字作為鍵。

word_dict = {}
if word_list:
    for word in word_list:
        word_dict[word] = 1 # 值是什麼不重要，這裡用 1 當作佔位符
else:
    print("單字列表是空的，無法建立 word_dict。")

# `word_dict` 中的值都是 `1`，但它們可以是任何東西，因為我們永遠不會去查詢它們
# —— 我們只會用這個字典來檢查一個鍵是否存在。
#
# 現在這是上一個函數的字典版本，它用 `word_dict` 取代了 `word_list`。

def much_faster():
    count = 0
    if not word_dict: # 如果 word_dict 是空的
        print("單字字典是空的，無法執行 much_faster。")
        return 0
    for word in word_dict: # 遍歷字典的鍵 (也就是單字)
        if reverse_word(word) in word_dict: # 檢查反轉字是否是字典的一個鍵
            count += 1
    return count

# 這個函數執行起來不到百分之一秒，所以比上一個版本快了大約 10,000 倍。
# (速度提升的倍數會依電腦效能和資料量而有所不同)

# 一般來說，在列表中尋找一個元素所需的時間與列表的長度成正比。
# 而在字典中尋找一個鍵所需的時間幾乎是固定的 —— 不管有多少個項目。

# %time result_fast = much_faster()
# print(f"much_faster 找到的相反詞配對數量 (近似值): {result_fast}")

# ## 計數器集合 (A collection of counters)
#
# 假設給你一個字串，你想要計算每個字母出現的次數。
# 字典是完成這項工作的好工具。
# 我們先從一個空字典開始。

counter = {}

# 當我們遍歷字串中的字母時，假設我們第一次看到字母 `'a'`。
# 我們可以像這樣把它加到字典裡。

counter['a'] = 1

# 值 `1` 表示我們看到這個字母一次。
# 之後，如果我們又看到同一個字母，我們可以像這樣把計數器加一。

counter['a'] += 1 # 等同於 counter['a'] = counter['a'] + 1

# 現在 `'a'` 對應的值是 `2`，因為我們看到這個字母兩次了。

counter

# 下面的函數使用這些功能來計算一個字串中每個字母出現的次數。

def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter: # 如果字母還沒在計數器裡
            counter[letter] = 1   # 就把它加進去，計數為 1
        else:                     # 如果字母已經在裡面了
            counter[letter] += 1  # 就把它的計數加 1
    return counter

# 迴圈每跑一次，如果 `letter` 不在字典中，我們就建立一個新的項目，鍵是 `letter`，值是 `1`。
# 如果 `letter` 已經在字典中了，我們就把 `letter` 對應的值加一。
#
# 這裡有一個例子。

counter_bronto = value_counts('brontosaurus') # brontosaurus (雷龍)
counter_bronto

# `counter_bronto` 中的項目顯示字母 `'b'` 出現一次，`'r'` 出現兩次，依此類推。

# ## 迴圈和字典 (Looping and dictionaries)
#
# 如果你在 `for` 陳述式中使用一個字典，它會遍歷字典的鍵。
# 為了示範，我們來建立一個計算 `'banana'` 中字母出現次數的字典。

counter_banana = value_counts('banana')
counter_banana

# 下面的迴圈會印出鍵，也就是字母。

for key in counter_banana:
    print(key)

# 要印出值，我們可以用 `values()` 方法。

for value in counter_banana.values():
    print(value)

# 要同時印出鍵和值，我們可以遍歷鍵，然後查詢對應的值。

for key in counter_banana:
    value = counter_banana[key]
    print(key, value)

# 在下一章，我們會看到一個更簡潔的方法來做同樣的事情。
# (提示：`items()` 方法)

# ## 列表和字典 (Lists and dictionaries)
#
# 你可以把列表當作字典中的值。
# 例如，這裡有一個字典，它把數字 `4` 對應到一個包含四個字母的列表。

d = {4: ['r', 'o', 'u', 's']}
d

# 但是你不能把列表當作字典中的鍵。
# 如果我們試著這樣做，會發生以下情況。

%%expect TypeError
# letters_as_key = list('abcd')
# d[letters_as_key] = 4 # 列表是可變的，不能當作鍵

# 我之前提到字典使用雜湊表，這表示鍵必須是 **可雜湊的 (hashable)**。
#
# **雜湊 (hash)** 是一個函數，它接收一個值 (任何種類的)，然後回傳一個整數。
# 字典使用這些整數，也就是雜湊值，來儲存和查詢鍵。
#
# 這個系統只有在鍵是不可變的 (immutable)，所以它的雜湊值永遠相同的情況下才能運作。
# 但是如果一個鍵是可變的，它的雜湊值可能會改變，字典就無法正常運作了。
# 這就是為什麼鍵必須是可雜湊的，以及為什麼像列表這樣的可變型別不能當作鍵。
#
# 因為字典本身也是可變的，所以它們也不能被用作鍵。
# 但是它們 *可以* 被用作值。

# ## 累加列表 (Accumulating a list)
#
# 對於許多程式設計任務來說，在建立另一個列表或字典的同時遍歷一個列表或字典是很有用的。
# 作為例子，我們會遍歷 `word_dict` 中的單字，並建立一個回文 (palindromes) 列表
# —— 也就是正讀和反讀都一樣的字，像是 "noon" 和 "rotator"。
#
# 在上一章，其中一個練習要求你寫一個檢查單字是否為回文的函數。
# 這裡有一個使用 `reverse_word` 的解答。

def is_palindrome(word):
    """檢查一個字是否為回文。"""
    return reverse_word(word) == word

# 如果我們遍歷 `word_dict` 中的單字，我們可以像這樣計算回文的數量。

count_pal = 0

if word_dict: # 確保 word_dict 不是空的
    for word_in_dict in word_dict: # 遍歷字典的鍵 (單字)
        if is_palindrome(word_in_dict):
            count_pal +=1
else:
    print("單字字典是空的，無法計算回文。")

print(f"回文的數量: {count_pal}")

# 到目前為止，這個模式我們已經很熟悉了。
#
# * 迴圈開始前，`count_pal` 初始化為 `0`。
#
# * 迴圈內部，如果 `word_in_dict` 是回文，我們就把 `count_pal` 加一。
#
# * 當迴圈結束時，`count_pal` 就包含了回文的總數。
#
# 我們可以用類似的模式來建立一個回文列表。

palindromes = [] # 初始化一個空列表來存放回文

if word_dict:
    for word_in_dict in word_dict:
        if is_palindrome(word_in_dict):
            palindromes.append(word_in_dict) # 如果是回文，就加到列表中
else:
    print("單字字典是空的，無法建立回文列表。")

print(f"找到的前 10 個回文: {palindromes[:10]}") # 印出前 10 個

# 它是這樣運作的：
#
# * 迴圈開始前，`palindromes` 初始化為一個空列表。
#
# * 迴圈內部，如果 `word_in_dict` 是回文，我們就把它附加到 `palindromes` 的尾巴。
#
# * 當迴圈結束時，`palindromes` 就是一個包含所有回文的列表。
#
# 在這個迴圈中，`palindromes` 被用作一個 **累加器 (accumulator)**，這是一個在計算過程中收集或累加資料的變數。
#
# 現在假設我們只想選出包含七個或更多字母的回文。
# 我們可以遍歷 `palindromes` 列表，並建立一個只包含長回文的新列表。

long_palindromes = []

if palindromes: # 確保 palindromes 列表不是空的
    for word_pal in palindromes:
        if len(word_pal) >= 7:
            long_palindromes.append(word_pal)
else:
    print("回文列表是空的，無法篩選長回文。")

print(f"長度大於等於 7 的回文: {long_palindromes}")

# 像這樣遍歷一個列表，選取某些元素並忽略其他元素，稱為 **篩選 (filtering)**。

# ## 備忘錄 (Memos)
#
# 如果你執行過[第六章](section_fibonacci)的 `fibonacci` 函數，你可能注意到你提供的參數越大，函數執行的時間就越長。
# (譯註：section_fibonacci 指的是書中對應章節的連結，這裡無法直接點擊)

def fibonacci(n): # 原始的遞迴費氏數列函數
    if n == 0:
        return 0
    
    if n == 1:
        return 1

    return fibonacci(n-1) + fibonacci(n-2)

# 而且，執行時間增加得非常快。
# 要了解原因，請看下圖，它顯示了 `fibonacci` 函數在 `n=4` 時的 **呼叫圖 (call graph)**：
# (呼叫圖顯示了函數如何互相呼叫，以及重複的計算)

from diagram import make_binding, Frame, Arrow

bindings_fib = [make_binding('n', i) for i in range(5)]
frames_fib = [Frame([binding]) for binding in bindings_fib]

arrowprops = dict(arrowstyle="-", color='gray', alpha=0.5, ls='-', lw=0.5)

def left_arrow(ax, bbox1, bbox2):
    x = bbox1.xmin + 0.1
    y = bbox1.ymin
    dx = bbox2.xmax - x - 0.1
    dy = bbox2.ymax - y
    arrow = Arrow(dx=dx, dy=dy, arrowprops=arrowprops)
    return arrow.draw(ax, x, y)

def right_arrow(ax, bbox1, bbox2):
    x = bbox1.xmax - 0.1
    y = bbox1.ymin
    dx = bbox2.xmin - x + 0.1
    dy = bbox2.ymax - y
    arrow = Arrow(dx=dx, dy=dy, arrowprops=arrowprops)
    return arrow.draw(ax, x, y)

from diagram import diagram, adjust, Bbox

width_fib, height_fib, x_fib, y_fib = [4.94, 2.16, -1.03, 1.91]
ax_fib = diagram(width_fib, height_fib)

dx_fib = 0.6
dy_fib = 0.55

bboxes_fib = []
bboxes_fib.append(frames_fib[4].draw(ax_fib, x_fib+6*dx_fib, y_fib)) # fib(4)

bboxes_fib.append(frames_fib[3].draw(ax_fib, x_fib+4*dx_fib, y_fib-dy_fib)) # fib(3)
bboxes_fib.append(frames_fib[2].draw(ax_fib, x_fib+8*dx_fib, y_fib-dy_fib)) # fib(2)

bboxes_fib.append(frames_fib[2].draw(ax_fib, x_fib+3*dx_fib, y_fib-2*dy_fib)) # fib(2) from fib(3)
bboxes_fib.append(frames_fib[1].draw(ax_fib, x_fib+5*dx_fib, y_fib-2*dy_fib)) # fib(1) from fib(3)
bboxes_fib.append(frames_fib[1].draw(ax_fib, x_fib+7*dx_fib, y_fib-2*dy_fib)) # fib(1) from fib(2)
bboxes_fib.append(frames_fib[0].draw(ax_fib, x_fib+9*dx_fib, y_fib-2*dy_fib)) # fib(0) from fib(2)

bboxes_fib.append(frames_fib[1].draw(ax_fib, x_fib+2*dx_fib, y_fib-3*dy_fib)) # fib(1) from fib(2)
bboxes_fib.append(frames_fib[0].draw(ax_fib, x_fib+4*dx_fib, y_fib-3*dy_fib)) # fib(0) from fib(2)

left_arrow(ax_fib, bboxes_fib[0], bboxes_fib[1]) # 4 -> 3
left_arrow(ax_fib, bboxes_fib[1], bboxes_fib[3]) # 3 -> 2
left_arrow(ax_fib, bboxes_fib[3], bboxes_fib[7]) # 2 -> 1
left_arrow(ax_fib, bboxes_fib[2], bboxes_fib[5]) # 2 (right branch) -> 1

right_arrow(ax_fib, bboxes_fib[0], bboxes_fib[2]) # 4 -> 2
right_arrow(ax_fib, bboxes_fib[1], bboxes_fib[4]) # 3 -> 1
right_arrow(ax_fib, bboxes_fib[2], bboxes_fib[6]) # 2 (right branch) -> 0
right_arrow(ax_fib, bboxes_fib[3], bboxes_fib[8]) # 2 (left branch) -> 0

bbox_fib_union = Bbox.union(bboxes_fib)
# adjust(x_fib, y_fib, bbox_fib_union)

# 呼叫圖顯示了一組函數框架 (function frame)，以及連接每個框架到它所呼叫函數框架的線條。
# 在圖的頂部，`fibonacci(4)` 呼叫了 `fibonacci(3)` 和 `fibonacci(2)`。
# 接著，`fibonacci(3)` 呼叫了 `fibonacci(2)` 和 `fibonacci(1)`。依此類推。
#
# 數數看 `fibonacci(0)` 和 `fibonacci(1)` 被呼叫了多少次。
# 這是一個解決問題的低效率方法，而且隨著參數變大，情況會變得更糟。
#
# 一個解決方法是把已經計算過的值記錄下來，儲存在一個字典裡。
# 一個先前計算過並儲存起來供以後使用的值，稱為 **備忘錄 (memo)**。
# 這裡是一個「備忘錄化」的 `fibonacci` 版本：

known = {0:0, 1:1} # 用一個字典來儲存已知的費氏數

def fibonacci_memo(n):
    if n in known: # 如果 n 已經在備忘錄裡了
        return known[n] # 直接回傳儲存的值

    # 如果 n 不在備忘錄裡，就計算它
    res = fibonacci_memo(n-1) + fibonacci_memo(n-2)
    known[n] = res # 把新算出來的值存到備忘錄裡
    return res

# `known` 是一個字典，用來記錄我們已經知道的費氏數。
# 它一開始有兩個項目：`0` 對應到 `0`，`1` 對應到 `1`。
#
# 每當 `fibonacci_memo` 被呼叫時，它會檢查 `known`。
# 如果結果已經在那裡了，它就可以立刻回傳。
# 否則，它就必須計算新的值，把它加到字典裡，然後回傳它。
#
# 比較這兩個函數，`fibonacci(40)` 大約需要 30 秒才能執行完畢。 (在作者的電腦上)
# `fibonacci_memo(40)` 大約只需要 30 微秒 (microsecond)，所以快了一百萬倍。
# 在本章的 notebook 檔案中，你會看到這些測量數據是怎麼來的。

# print("計算 fibonacci(40)...")
# %time result_fib_40 = fibonacci(40)
# print(f"fibonacci(40) = {result_fib_40}")

print("計算 fibonacci_memo(40)...")
%time result_fib_memo_40 = fibonacci_memo(40)
print(f"fibonacci_memo(40) = {result_fib_memo_40}")

# ## 除錯 (Debugging)
#
# 當你處理越來越大的資料集時，用印出訊息然後手動檢查輸出的方式來除錯可能會變得很麻煩。
# 以下是一些針對大型資料集除錯的建議：
#
# 1.  縮小輸入規模：如果可能的話，減少資料集的規模。例如，如果程式讀取一個文字檔，
#     可以先從前 10 行開始，或者用你能找到的最小範例開始。你可以直接編輯檔案本身，
#     或者 (更好的方法是) 修改程式，讓它只讀取前 `n` 行。
#
#     如果發生錯誤，你可以把 `n` 減少到發生錯誤的最小值。
#     當你找到並修正錯誤後，可以逐漸增加 `n` 的值。

# 2. 檢查摘要和型別：與其印出並檢查整個資料集，不如考慮印出資料的摘要 —— 例如，
#     字典中的項目數量，或數字列表的總和。
#
#     執行期錯誤的一個常見原因是值的型別不正確。要除錯這類錯誤，
#     通常只需要印出值的型別就夠了。

# 3. 編寫自我檢查程式碼：有時候你可以寫程式碼來自動檢查錯誤。例如，
#     如果你在計算一個數字列表的平均值，你可以檢查結果是否
#     大於列表中的最大元素或小於最小元素。這叫做「合理性檢查 (sanity check)」，
#     因為它可以偵測到「不合理 (insane)」的結果。
#
#     另一種檢查是比較兩種不同計算方式的結果，看看它們是否一致。
#     這叫做「一致性檢查 (consistency check)」。

# 4. 格式化輸出：格式化除錯輸出可以讓你更容易發現錯誤。我們在[第六章](section_debugging_factorial)
#     看過一個例子。另一個你可能會覺得有用的工具是 `pprint` 模組，它提供了一個
#     `pprint` 函數，可以用更易讀的方式顯示內建型別 (`pprint` 是 "pretty print" 的縮寫，意思是很漂亮的印出)。
#
#     再次強調，你花在建立輔助工具 (scaffolding) 上的時間，可以減少你花在除錯上的時間。

# ## 詞彙表 (Glossary)
#
# **字典 (dictionary):**
#  一個包含鍵值對 (key-value pair)，也稱為項目 (item) 的物件。
#
# **項目 (item):**
#  在字典中，鍵值對的另一個名稱。
#
# **鍵 (key):**
#  在字典中作為鍵值對第一部分出現的物件。
#
# **值 (value):**
#  在字典中作為鍵值對第二部分出現的物件。這比我們之前使用「值」這個詞的意義更具體。
#
# **對應 (mapping):**
#   一種關係，其中一個集合的每個元素都對應到另一個集合的一個元素。
#
# **雜湊表 (hash table):**
#  一種鍵值對的集合，其組織方式讓我們可以有效地查詢一個鍵並找到它的值。
#
# **可雜湊的 (hashable):**
#  像整數、浮點數和字串這樣的不可變型別是可雜湊的。
#  像列表和字典這樣的可變型別則不是。
#
# **雜湊函數 (hash function):**
#  一個接收物件並計算出一個整數的函數，這個整數被用來在雜湊表中定位一個鍵。
#
# **累加器 (accumulator):**
#  在迴圈中用來加總或累加結果的變數。
#
# **篩選 (filtering):**
#  遍歷一個序列並選取或忽略某些元素的過程。
#
# **呼叫圖 (call graph):**
#  一個圖表，顯示程式執行期間建立的每個框架，以及從每個呼叫者到每個被呼叫者的箭頭。
#
# **備忘錄 (memo):**
#  一個儲存起來的計算結果，用來避免未來不必要的重複計算。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問助理 (Ask an assistant)
#
# 在這一章，我說過字典中的鍵必須是可雜湊的，並且簡短解釋了原因。如果你想知道更多細節，可以問問虛擬助理：「為什麼 Python 字典中的鍵必須是可雜湊的？」
#
# 在[前面的一個小節](section_dictionary_in_operator)中，我們把一個單字列表儲存為字典的鍵，這樣我們就可以使用 `in` 運算子的有效率版本。
# 我們也可以用 `set` (集合) 來做同樣的事情，它是另一種內建的資料型別。
# 問問虛擬助理：「我要如何從一個字串列表建立 Python 集合，並檢查一個字串是否是集合的元素？」
# (譯註：section_dictionary_in_operator 指的是書中對應章節的連結)

# ### 練習
#
# 字典有一個叫做 `get` 的方法，它接收一個鍵和一個預設值。
# 如果鍵出現在字典中，`get` 會回傳對應的值；否則它會回傳預設值。
# 例如，這裡有一個字典，它把字串中的字母對應到它們出現的次數。

counter_get_example = value_counts('brontosaurus') # 使用之前定義的 value_counts

# 如果我們查詢一個出現在單字中的字母，`get` 會回傳它出現的次數。

counter_get_example.get('b', 0) # 查詢 'b'，如果沒有就回傳 0

# 如果我們查詢一個沒有出現的字母，我們會得到預設值 `0`。

counter_get_example.get('c', 0) # 查詢 'c'，'c' 不在裡面，所以回傳預設值 0

# 請使用 `get` 方法來寫一個更簡潔的 `value_counts` 版本。
# 你應該能夠去掉 `if` 陳述式。

# 解答:
def value_counts_concise(string):
    counter = {}
    for letter in string:
        counter[letter] = counter.get(letter, 0) + 1 # 如果 letter 不在，get 回傳 0，所以 0+1=1
                                                       # 如果 letter 在，get 回傳目前計數，再加 1
    return counter

# 測試 concise 版本
print("\n--- 測試 value_counts_concise ---")
counter_concise_test = value_counts_concise('banana')
print(f"value_counts_concise('banana'): {counter_concise_test}")
counter_concise_bronto = value_counts_concise('brontosaurus')
print(f"value_counts_concise('brontosaurus'): {counter_concise_bronto}")


# ### 練習
#
# 你能想到最長的、每個字母只出現一次的單字是什麼？
# 讓我們看看能不能找到比 `unpredictably` (無法預測地) 更長的。
# (unpredictably 長度 14，字母不重複)
#
# 寫一個叫做 `has_duplicates` 的函數，它接收一個序列 (像是列表或字串) 作為參數，
# 如果序列中有任何元素出現超過一次，就回傳 `True`。

# 為了讓你開始，這裡有一個包含 doctests 的函數大綱。

def has_duplicates_starter(t): # 改名避免與解答衝突
    """檢查序列中是否有任何元素出現超過一次。

    >>> has_duplicates_starter('banana')
    True
    >>> has_duplicates_starter('ambidextrously') # 左右開弓地 (長度 14，字母不重複)
    False
    >>> has_duplicates_starter([1, 2, 2])
    True
    >>> has_duplicates_starter([1, 2, 3])
    False
    """
    return None # 你的程式碼會取代這裡

# 解答

def has_duplicates(t):
    """檢查序列中是否有任何元素出現超過一次。

    >>> has_duplicates('banana')
    True
    >>> has_duplicates('ambidextrously')
    False
    >>> has_duplicates([1, 2, 2])
    True
    >>> has_duplicates([1, 2, 3])
    False
    """
    # 方法一: 使用字典來計數或標記
    # d = {}
    # for x in t:
    #     if x in d:
    #         return True # 發現重複
    #     d[x] = True
    # return False # 沒有重複

    # 方法二: 比較原長度和轉換成 set 後的長度 (set 會自動去重)
    return len(t) != len(set(t))

    # 書中解答的邏輯是：
    # d = {}
    # for x in t:
    #     d[x] = True # 把元素當鍵存入，值不重要
    # # 如果有重複元素，加入字典時鍵會被覆蓋，所以字典長度會小於原序列長度
    # return len(d) < len(t)


# 你可以用 `doctest` 來測試你的函數。

from doctest import run_docstring_examples

def run_doctests(func):
    print(f"--- 執行 {func.__name__} 的 doctests ---")
    run_docstring_examples(func, globals(), name=func.__name__)

run_doctests(has_duplicates)

# 你可以用這個迴圈來找出沒有重複字母的最長單字。
# (這裡用的是 word_list，不是 word_dict，因為我們要檢查原始單字)

no_repeats_words = []
longest_no_repeat_word = ""

print("\n--- 找出沒有重複字母的長單字 (長度 > 12) ---")
if word_list: # 確保 word_list 已載入
    for word_from_list in word_list:
        if not has_duplicates(word_from_list):
            if len(word_from_list) > 12: # 先找長度大於12的
                no_repeats_words.append(word_from_list)
            if len(word_from_list) > len(longest_no_repeat_word):
                longest_no_repeat_word = word_from_list

    print(f"長度大於 12 且無重複字母的單字 (部分): {no_repeats_words[:10]}") # 印出前10個
    print(f"找到的最長無重複字母單字是: '{longest_no_repeat_word}' (長度: {len(longest_no_repeat_word)})")
    # 書中找到的是 'uncopyrightable' 和 'ambidextrously' (長度15)
    # 'dermatoglyphics' (指紋學，長度15)
    # 'misunderstandingly' (誤解地，長度18，但有重複s,n,d,i,y)
    # 'globefish-sucker' (16, 但有 hyphen)
else:
    print("單字列表是空的，無法搜尋。")


# ### 練習
#
# 寫一個叫做 `find_repeats` 的函數，它接收一個字典作為參數，
# 這個字典把每個鍵對應到一個計數器，就像 `value_counts` 的結果一樣。
# 它應該遍歷這個字典，並回傳一個包含計數大於 `1` 的所有鍵的列表。
# 你可以用下面的大綱開始。

def find_repeats_starter(counter): # 改名避免與解答衝突
    """建立一個值大於 1 的所有鍵的列表。

    counter: 一個把鍵對應到計數的字典

    回傳: 鍵的列表
    """
    return [] # 你的程式碼會取代這裡

# 解答

def find_repeats(counter_dict): # 參數名改為 counter_dict 以示區別
    """建立一個值大於 1 的所有鍵的列表。

    counter_dict: 一個把鍵對應到計數的字典

    回傳: 鍵的列表
    """
    repeats_list = []
    # 遍歷字典的鍵值對 (items)
    for key, count_val in counter_dict.items():
        if count_val > 1:
            repeats_list.append(key)
    return repeats_list

# 你可以用下面的例子來測試你的程式碼。
# 首先，我們建立一個把字母對應到計數的字典。

counter1_repeats_test = value_counts('banana')
print(f"\n--- 測試 find_repeats ---")
print(f"counter1_repeats_test ('banana'): {counter1_repeats_test}")

# `find_repeats` 的結果應該是 `['a', 'n']` (順序可能不同，因為字典無序)。

repeats_result1 = find_repeats(counter1_repeats_test)
print(f"find_repeats(counter1_repeats_test) 的結果: {sorted(repeats_result1)}") # 排序以方便比較

# 這裡有另一個從數字列表開始的例子。
# 結果應該是 `[1, 2]` (順序可能不同)。

counter2_repeats_test = value_counts([1, 2, 3, 2, 1])
print(f"counter2_repeats_test ([1, 2, 3, 2, 1]): {counter2_repeats_test}")
repeats_result2 = find_repeats(counter2_repeats_test)
print(f"find_repeats(counter2_repeats_test) 的結果: {sorted(repeats_result2)}") # 排序以方便比較

# ### 練習
#
# 假設你用兩個不同的單字執行 `value_counts`，並把結果儲存在兩個字典中。

counter1_add = value_counts('brontosaurus')
counter2_add = value_counts('apatosaurus') # apatosaurus (迷惑龍)
print(f"\n--- 測試 add_counters ---")
print(f"counter1_add ('brontosaurus'): {counter1_add}")
print(f"counter2_add ('apatosaurus'): {counter2_add}")

# 每個字典都把一組字母對應到它們出現的次數。
# 寫一個叫做 `add_counters` 的函數，它接收兩個像這樣的字典，
# 並回傳一個新的字典，其中包含所有字母以及它們在任一個單字中出現的總次數。
#
# 這個問題有很多種解法。
# 一旦你有了一個可以運作的解法，可以考慮問問虛擬助理不同的解法。

# 解答

def add_counters(counter_a, counter_b):
    # 從 counter_a 建立一個副本開始，這樣才不會修改到原始的 counter_a
    result_counter = dict(counter_a)

    # 遍歷 counter_b
    for letter, count_val_b in counter_b.items():
        # 使用 get 來取得 result_counter 中 letter 的現有計數 (如果沒有就是 0)
        # 然後加上 counter_b 中 letter 的計數
        result_counter[letter] = result_counter.get(letter, 0) + count_val_b
    return result_counter

# 解答 (執行)
added_result = add_counters(counter1_add, counter2_add)
print(f"add_counters 的結果: {added_result}")

# ### 練習
#
# 如果一個單字可以透過取其交錯字母來分割成兩個單字，那麼它就是一個「交錯 (interlocking)」字。
# 例如，"schooled" (受過教育的) 是一個交錯字，因為它可以分割成 "shoe" (鞋子) 和 "cold" (冷的)。
#
# 要從一個字串中選取交錯的字母，你可以使用有三個部分 (開始、停止、步長) 的切片運算子。
#
# 在下面的切片中，第一個部分是 `0`，所以我們從第一個字母開始。
# 第二個部分是 `None`，表示我們應該一直到字串的結尾。
# 第三個部分是 `2`，所以我們選取的字母之間有兩個步長 (即每隔一個取一個)。

word_interlock_example = 'schooled'
first_half = word_interlock_example[0:None:2] # 從索引0開始，每隔2個取一個
print(f"\n--- 測試交錯字 ---")
print(f"'{word_interlock_example}' 的第一個交錯部分: {first_half}")

# 與其提供 `None` 作為第二個部分，我們也可以完全省略它來達到相同的效果。
# 例如，下面的切片選取交錯的字母，從第二個字母開始。

second_half = word_interlock_example[1::2] # 從索引1開始，每隔2個取一個 (到結尾)
print(f"'{word_interlock_example}' 的第二個交錯部分: {second_half}")

# 寫一個叫做 `is_interlocking` 的函數，它接收一個單字作為參數，
# 如果它可以分割成兩個交錯的單字 (且這兩個分割出來的字都在 `word_dict` 中)，就回傳 `True`。

# 解答

def is_interlocking(word_to_check):
    # 這裡假設 word_dict 已經被建立了
    if not word_dict:
        # print("警告: word_dict 未建立，is_interlocking 可能無法正常運作。")
        # 為了讓 doctest 或獨立測試能跑，如果 word_dict 不存在，可以暫時用一個小的
        # 模擬 word_dict，或者讓它在 word_list 上查找，但會比較慢。
        # 這裡為了符合題目情境，我們假設 word_dict 存在。
        # 如果 word_dict 為空，那麼 in word_dict 永遠是 False。
        pass

    first = word_to_check[0::2]
    second = word_to_check[1::2]
    return first in word_dict and second in word_dict

# 你可以用下面的迴圈來找出單字列表中的交錯字。
# (這裡用的是 word_list，因為我們要檢查的 word 是從 word_list 來的原始字串)

print("\n--- 找出交錯字 (長度 >= 8) ---")
interlocking_count = 0
if word_list and word_dict: # 確保兩者都已載入
    for word_from_list_interlock in word_list:
        if len(word_from_list_interlock) >= 8 and is_interlocking(word_from_list_interlock):
            first_part = word_from_list_interlock[0::2]
            second_part = word_from_list_interlock[1::2]
            print(word_from_list_interlock, first_part, second_part)
            interlocking_count += 1
    if interlocking_count == 0:
        print("沒有找到符合條件的交錯字。")
else:
    print("單字列表或字典未載入，無法搜尋交錯字。")

# (這個儲存格是空的，保留)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)