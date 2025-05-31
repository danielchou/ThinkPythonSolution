# 從 chap11.ipynb 轉換而來
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

# # 元組 (Tuples)
#
# 這一章要介紹另一種內建型別：元組 (tuple)，然後會展示列表 (list)、字典 (dictionary) 和元組如何協同運作。
# 內容還包括元組賦值 (tuple assignment) 以及一個對應可變長度參數列表函數很有用的功能：打包 (packing) 和解包 (unpacking) 運算子。
#
# 在練習題中，我們會使用元組，以及列表和字典，來解決更多的文字謎題並實作高效率的演算法。
#
# 附註： "tuple" 有兩種發音方式。
# 有些人唸 "tuh-ple"，聽起來像 "supple"。
# 但在程式設計的領域，大多數人唸 "too-ple"，聽起來像 "quadruple"。
# (中文通常直接唸「元組」ㄩㄢˊ ㄗㄨˇ)

# ## 元組就像列表 (Tuples are like lists)
#
# 元組 (tuple) 是一個值的序列。這些值可以是任何型別，並且由整數索引，所以元組和列表非常相似。
# 重要的差別在於元組是不可變的 (immutable)。
#
# 要建立一個元組，你可以寫下一串用逗號分隔的值。

t = 'l', 'u', 'p', 'i', 'n' # Lupin (羽扇豆；羅蘋，一個角色名)
type(t) # 檢查 t 的型別

# 雖然不是必要的，但通常會用括號把元組包起來。

t = ('l', 'u', 'p', 'i', 'n')
type(t)

# 要建立一個只包含單一元素的元組，你必須在最後加上一個逗號。

t1 = 'p', # 注意這個逗號！
type(t1)

# 括號裡只有一個值並不是元組。(它只是一個被括號包起來的值)

t2 = ('p') # 這只是一個字串 'p'
type(t2)

# 另一種建立元組的方法是使用內建函數 `tuple()`。如果不給任何參數，
# 它會建立一個空元組。

t = tuple()
t

# 如果參數是一個序列 (字串、列表或元組)，結果會是一個包含該序列元素的元組。

t = tuple('lupin') # 把字串 'lupin' 轉換成元組
t

# 因為 `tuple` 是一個內建函數的名稱，所以你應該避免用它來當作變數名稱。
# (不然你會把內建函數蓋掉！)
#
# 大多數列表運算子也可以用在元組上。
# 例如，方括號運算子 `[]` 可以索引一個元素。

t[0] # 取得元組 t 的第一個元素

# 而切片運算子 `[:]` 可以選取一個範圍的元素。

t[1:3] # 選取索引 1 到索引 3 (不包含 3) 的元素

# `+` 運算子可以串接元組。

tuple('lup') + ('i', 'n')

# 而 `*` 運算子可以將一個元組重複指定的次數。

tuple('spam') * 2 # 'spam' 是一個常用的範例字串

# `sorted()` 函數可以用在元組上 —— 但結果會是一個列表，而不是元組。

sorted_list_from_tuple = sorted(t)
print(sorted_list_from_tuple)
type(sorted_list_from_tuple)

# `reversed()` 函數也可以用在元組上。

reversed_obj_from_tuple = reversed(t)
print(reversed_obj_from_tuple) # 這會印出一個 reversed 物件的描述

# 結果是一個 `reversed` 物件，我們可以把它轉換成列表或元組。

tuple(reversed(t))

# 從目前的例子看來，元組似乎跟列表沒什麼兩樣。

# ## 但是元組是不可變的 (But tuples are immutable)
#
# 如果你試著用方括號運算子修改元組，你會得到一個 `TypeError` (型別錯誤)。

%%expect TypeError
# t[0] = 'L' # 元組是不可變的，不能修改元素

# 而且元組沒有那些會修改列表的方法，像是 `append` 和 `remove`。

%%expect AttributeError
# t.remove('l') # 元組沒有 remove 方法

# 回想一下，「屬性 (attribute)」是與物件相關聯的變數或方法 —— 這個錯誤訊息表示元組沒有叫做 `remove` 的方法。
#
# 因為元組是不可變的，所以它們是可雜湊的 (hashable)，這表示它們可以被用作字典中的鍵。
# 例如，下面的字典包含兩個元組作為鍵，它們對應到整數。

d = {}
d[1, 2] = 3 # (1, 2) 是一個元組鍵，不需要額外的括號
d[3, 4] = 7
print(d)

# 我們可以像這樣在字典中查詢一個元組：

d[1, 2]

# 或者如果我們有一個變數指向一個元組，我們可以用它作為鍵。

t_key = (3, 4)
d[t_key]

# 元組也可以作為字典中的值。

t_value = tuple('abc')
d_with_tuple_value = {'key': t_value}
d_with_tuple_value

# ## 元組賦值 (Tuple assignment)
#
# 你可以把一個變數元組放在賦值運算子的左邊，一個值元組放在右邊。

a, b = 1, 2 # 這等同於 (a, b) = (1, 2)

# 值會從左到右依序指派給變數 —— 在這個例子中，`a` 得到值 `1`，`b` 得到值 `2`。
# 我們可以像這樣顯示結果：

a, b

# 更一般地說，如果賦值運算子的左邊是一個元組，右邊可以是任何種類的序列 —— 字串、列表或元組。
# 例如，要把一個電子郵件地址分割成使用者名稱和網域名稱，你可以這樣寫：

email = 'monty@python.org' # monty python (蒙提·派森，一個英國喜劇團體)
username, domain = email.split('@') # split('@') 會回傳一個列表

# `split` 的回傳值是一個包含兩個元素的列表 —— 第一個元素被指派給 `username`，第二個被指派給 `domain`。

username, domain

# 左邊的變數數量和右邊的值的數量必須相同 —— 否則你會得到一個 `ValueError` (值錯誤)。

%%expect ValueError
# a, b = 1, 2, 3 # 左邊兩個變數，右邊三個值，數量不符

# 如果你想交換兩個變數的值，元組賦值非常有用。
# 用傳統的賦值方法，你必須使用一個暫存變數，像這樣：

# 假設 a 和 b 的初始值
a_orig = 5
b_orig = 10
print(f"交換前: a_orig = {a_orig}, b_orig = {b_orig}")
temp = a_orig
a_orig = b_orig
b_orig = temp
print(f"傳統交換後: a_orig = {a_orig}, b_orig = {b_orig}")


# 那樣可行，但用元組賦值，我們可以不用暫存變數就做到同樣的事情。

# 重新設定 a 和 b
a_swap = 5
b_swap = 10
print(f"交換前: a_swap = {a_swap}, b_swap = {b_swap}")
a_swap, b_swap = b_swap, a_swap # 元組賦值交換
print(f"元組賦值交換後: a_swap = {a_swap}, b_swap = {b_swap}")


# 這之所以可行，是因為右邊的所有表達式都會在任何賦值發生之前先被評估。
#
# 我們也可以在 `for` 陳述式中使用元組賦值。
# 例如，要遍歷字典中的項目 (item)，我們可以用 `items()` 方法。

d_items_example = {'one': 1, 'two': 2}

print("\n--- 使用元組賦值遍歷字典項目 (方法一) ---")
for item_tuple in d_items_example.items(): # items() 回傳 (鍵, 值) 元組的序列
    key_from_item, value_from_item = item_tuple # 把元組解包到兩個變數
    print(key_from_item, '->', value_from_item)

# 迴圈每跑一次，`item_tuple` 就會被指派一個包含鍵和對應值的元組。
#
# 我們可以把這個迴圈寫得更簡潔，像這樣：

print("\n--- 使用元組賦值遍歷字典項目 (方法二，更簡潔) ---")
for key_direct, value_direct in d_items_example.items(): # 直接在 for 後面解包
    print(key_direct, '->', value_direct)

# 迴圈每跑一次，一個鍵和對應的值就會直接被指派給 `key_direct` 和 `value_direct`。

# ## 元組作為回傳值 (Tuples as return values)
#
# 嚴格來說，一個函數只能回傳一個值，但如果那個值是一個元組，
# 效果就跟回傳多個值一樣。
# 例如，如果你想把兩個整數相除並計算商和餘數，
# 分別計算 `x//y` 和 `x%y` 效率不高。最好是一次把它們都算出來。
#
# 內建函數 `divmod` 接收兩個參數，並回傳一個包含兩個值的元組：商和餘數。

divmod_result = divmod(7, 3)
print(divmod_result)

# 我們可以用元組賦值把元組的元素儲存到兩個變數中。

quotient, remainder = divmod(7, 3)
print(f"商: {quotient}")

print(f"餘數: {remainder}")

# 這裡有一個回傳元組的函數範例。

def min_max(t_sequence): # 參數改名以避免與之前的變數 t 混淆
    return min(t_sequence), max(t_sequence) # 回傳一個包含最小值和最大值的元組

# `max` 和 `min` 是內建函數，它們會找出序列中最大和最小的元素。
# `min_max` 會同時計算這兩個值，並回傳一個包含兩個值的元組。

min_max_result = min_max([2, 4, 1, 3])
print(min_max_result)

# 我們可以像這樣把結果指派給變數：

low, high = min_max([2, 4, 1, 3])
print(f"最小值: {low}, 最大值: {high}")

# ## 引數打包 (Argument packing)
#
# 函數可以接收可變數量的引數 (argument)。
# 一個以 `*` 運算子開頭的參數名稱會把引數 **打包 (packs)** 到一個元組中。
# 例如，下面的函數接收任意數量的引數，並計算它們的算術平均數
# —— 也就是它們的總和除以引數的數量。

def mean(*args): # *args 會把所有傳入的引數收集到一個叫做 args 的元組裡
    if not args: # 處理沒有引數的情況
        return 0.0 # 或者可以引發一個錯誤
    return sum(args) / len(args)

# 參數名稱可以隨你喜歡，但 `args` 是慣用法。
# (args 是 arguments 的縮寫)
# 我們可以像這樣呼叫這個函數：

mean_result1 = mean(1, 2, 3)
print(f"mean(1, 2, 3) = {mean_result1}")
mean_result2 = mean(10, 20, 30, 40, 50)
print(f"mean(10, 20, 30, 40, 50) = {mean_result2}")

# 如果你有一個值的序列，並且想把它們作為多個引數傳遞給一個函數，
# 你可以用 `*` 運算子來 **解包 (unpack)** 這個元組 (或列表、字串等序列)。
# 例如，`divmod` 函數剛好需要兩個引數 —— 如果你傳遞一個元組作為參數，你會得到錯誤。

%%expect TypeError
# t_for_divmod = (7, 3)
# divmod(t_for_divmod) # 這樣是把一個元組當作單一引數傳遞

# 即使元組包含兩個元素，它仍然只算是一個單一的引數。
# 但是如果你解包這個元組，它就會被視為兩個引數。

t_for_divmod = (7, 3)
divmod_unpacked_result = divmod(*t_for_divmod) # *t_for_divmod 會把元組解成 divmod(7, 3)
print(f"divmod(*{t_for_divmod}) = {divmod_unpacked_result}")

# 如果你想調整現有函數的行為，打包和解包功能會很有用。
# 例如，這個函數接收任意數量的引數，移除最小值和最大值，然後計算其餘值的平均數。

def trimmed_mean(*args):
    if len(args) < 3: # 如果少於3個數，移除最大最小後就沒了或只剩一個
        print("警告: trimmed_mean 需要至少3個引數才能有效運作。")
        # 可以選擇回傳 None, 0, 或引發錯誤
        if not args: return 0.0
        if len(args) == 1: return args[0]
        if len(args) == 2: return sum(args)/2 # 或者 undefined
        return float('nan') # Not a Number

    low_val, high_val = min_max(args) # 找出最小值和最大值
    trimmed = list(args) # 把 args 元組轉成列表才能用 remove
    trimmed.remove(low_val) # 移除最小值
    trimmed.remove(high_val) # 移除最大值
    if not trimmed: # 如果移除後變空了 (例如 [1,1,1] 移除後可能空)
        # 這種情況應該在前面 len(args) < 3 時處理掉
        # 但為了安全起見
        return 0.0
    return mean(*trimmed) # 解包列表，把元素當作個別引數傳給 mean

# 首先它使用 `min_max` 找到最小和最大的元素。
# 然後它把 `args` 轉換成列表，這樣才能使用 `remove` 方法。
# (注意：如果最小值或最大值有多個，`remove` 只會移除第一個遇到的)
# 最後它解包這個列表，這樣元素就會作為獨立的引數傳遞給 `mean`，而不是作為單一的列表。
#
# 這裡有一個例子顯示效果。

print(f"mean(1, 2, 3, 10) = {mean(1, 2, 3, 10)}") # (1+2+3+10)/4 = 16/4 = 4.0

print(f"trimmed_mean(1, 2, 3, 10) = {trimmed_mean(1, 2, 3, 10)}") # 移除 1 和 10，剩下 (2+3)/2 = 2.5

# 這種「修剪後 (trimmed)」的平均值被用於一些有主觀評分的運動項目中 —— 像是跳水和體操 ——
# 以減少某位評審分數與其他人差異過大的影響。

# ## Zip
#
# 元組對於遍歷兩個序列的元素並對相應元素執行操作非常有用。
# 例如，假設兩隊進行了七場系列賽，我們把他們的得分記錄在兩個列表中，每隊一個。

scores1 = [1, 2, 4, 5, 1, 5, 2]
scores2 = [5, 5, 2, 2, 5, 2, 3]

# 讓我們看看每隊贏了幾場比賽。
# 我們會使用 `zip`，它是一個內建函數，接收兩個或多個序列，
# 並回傳一個 **zip 物件 (zip object)**，之所以這麼稱呼是因為它會像拉鍊的齒一樣把序列的元素配對起來。

zip_object = zip(scores1, scores2)
print(zip_object) # 這會印出一個 zip 物件的描述

# 我們可以用 zip 物件來成對地遍歷序列中的值。

print("\n--- zip 物件遍歷 ---")
for pair in zip(scores1, scores2): # zip 會在最短的序列結束時停止
     print(pair)

# 迴圈每跑一次，`pair` 就會被指派一個包含得分的元組。
# 所以我們可以把得分指派給變數，並計算第一隊的勝場數，像這樣：

wins_team1 = 0
for team1_score, team2_score in zip(scores1, scores2):
    if team1_score > team2_score:
        wins_team1 += 1

print(f"第一隊贏了 {wins_team1} 場比賽。")

# 可惜的是，第一隊只贏了三場比賽，輸掉了系列賽。
#
# 如果你有兩個列表，並且想要一個包含配對的列表，你可以使用 `zip` 和 `list`。

list_of_pairs = list(zip(scores1, scores2))
print(f"得分配對列表: {list_of_pairs}")

# 結果是一個元組的列表，所以我們可以像這樣取得最後一場比賽的結果：

last_game_scores = list_of_pairs[-1]
print(f"最後一場比賽的得分: {last_game_scores}")

# 如果你有一個鍵的列表和一個值的列表，你可以用 `zip` 和 `dict` 來建立一個字典。
# 例如，這裡展示了如何建立一個把每個字母對應到它在字母表中位置的字典。

letters_alphabet = 'abcdefghijklmnopqrstuvwxyz'
numbers_indices = range(len(letters_alphabet)) # 0 到 25 的數字序列
letter_map_alphabet = dict(zip(letters_alphabet, numbers_indices))
# print(letter_map_alphabet) # 印出來會很長，這裡只印部分

# 現在我們可以查詢一個字母並得到它在字母表中的索引。

print(f"字母 'a' 的索引: {letter_map_alphabet['a']}")
print(f"字母 'z' 的索引: {letter_map_alphabet['z']}")

# 在這個對應中，`'a'` 的索引是 `0`，`'z'` 的索引是 `25`。
#
# 如果你需要同時遍歷序列的元素和它們的索引，你可以使用內建函數 `enumerate`。

enumerate_obj = enumerate('abc')
print(enumerate_obj) # 這會印出一個 enumerate 物件的描述

# 結果是一個 **enumerate 物件 (enumerate object)**，它可以遍歷一個成對的序列，
# 其中每一對包含一個索引 (從 0 開始) 和來自給定序列的一個元素。

print("\n--- enumerate 物件遍歷 ---")
for index, element in enumerate('abc'):
    print(index, element)

# ## 比較和排序 (Comparing and Sorting)
#
# 關係運算子 (像是 `<`、`>`、`==` 等) 可以用在元組和其他序列上。
# 例如，如果你對元組使用 `<` 運算子，它會從每個序列的第一個元素開始比較。
# 如果它們相等，它會繼續比較下一對元素，依此類推，直到找到一對不相同的元素。

print( (0, 1, 2) < (0, 3, 4) ) # True，因為 1 < 3

# 後續的元素不會被考慮 —— 即使它們非常大。

print( (0, 1, 2000000) < (0, 3, 4) ) # 仍然是 True，因為比較在第二個元素就決定了 (1 < 3)

# 這種比較元組的方式對於排序元組列表，或者找出最小值或最大值非常有用。
# 作為例子，讓我們找出一個單字中出現最多次的字母。
# 在上一章，我們寫了 `value_counts`，它接收一個字串並回傳一個字典，
# 該字典把每個字母對應到它出現的次數。

# 重新定義 value_counts 以確保在本章節可用
def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter

# 這是字串 `'banana'` 的結果。

counter_banana_sort = value_counts('banana')
print(f"value_counts('banana'): {counter_banana_sort}")

# 只有三個項目，我們可以輕易看出出現最多次的字母是 `'a'`，它出現了三次。
# 但如果項目更多，自動排序它們會很有用。
#
# 我們可以像這樣從 `counter_banana_sort` 中取得項目 (items)。

items_from_counter = counter_banana_sort.items() # .items() 回傳一個 dict_items 物件
print(f"counter.items(): {items_from_counter}")

# 結果是一個 `dict_items` 物件，它的行為類似一個元組的列表，所以我們可以像這樣排序它。

sorted_items_default = sorted(items_from_counter) # 預設按鍵 (元組的第一個元素) 排序
print(f"sorted(items) (預設): {sorted_items_default}")

# 預設行為是使用每個元組的第一個元素來排序列表，並使用第二個元素來打破平手 (break ties)。
# (更準確地說，如果第一個元素相同，則比較第二個元素，依此類推)
#
# 然而，要找出計數最高的項目，我們希望使用第二個元素 (計數值) 來排序列表。
# 我們可以寫一個函數，它接收一個元組並回傳第二個元素。

def second_element(t_tuple): # 參數改名
    return t_tuple[1] # 回傳元組的第二個元素 (索引為1)

# 然後我們可以把這個函數作為一個叫做 `key` 的選擇性參數傳遞給 `sorted`，
# 這表示應該使用這個函數來計算每個項目的 **排序鍵 (sort key)**。

sorted_items_by_value = sorted(items_from_counter, key=second_element)
print(f"sorted(items, key=second_element): {sorted_items_by_value}")

# 排序鍵決定了列表中項目的順序。
# 計數最低的字母會先出現，計數最高的字母最後出現。
# 所以我們可以像這樣找到出現最多次的字母。

most_common_item = sorted_items_by_value[-1] # 取排序後列表的最後一個元素
print(f"出現最多次的項目 (字母, 次數): {most_common_item}")

# 如果我們只想找到最大值，就不需要排序整個列表。
# 我們可以用 `max` 函數，它也接受 `key` 作為選擇性參數。

max_item_by_value = max(items_from_counter, key=second_element)
print(f"max(items, key=second_element): {max_item_by_value}")

# 要找到計數最低的字母，我們可以用 `min` 函數以同樣的方式處理。
min_item_by_value = min(items_from_counter, key=second_element)
print(f"min(items, key=second_element): {min_item_by_value}")


# ## 反轉字典 (Inverting a dictionary)
#
# 假設你想反轉一個字典，以便你可以查詢一個值並得到對應的鍵。
# 例如，如果你有一個單字計數器，它把每個單字對應到它出現的次數，
# 你可以建立一個字典，它把整數 (次數) 對應到出現該次數的單字列表。
#
# 但有一個問題 —— 字典中的鍵必須是唯一的，但值不必。
# 例如，在單字計數器中，可能有很多單字具有相同的計數。
#
# 所以，反轉字典的一種方法是建立一個新的字典，其中值是來自原始字典的鍵的列表。
# 作為例子，讓我們計算 `'parrot'` (鸚鵡) 中的字母。

d_parrot_counts =  value_counts('parrot')
print(f"value_counts('parrot'): {d_parrot_counts}")

# 如果我們反轉這個字典，結果應該是 `{1: ['p', 'a', 'o', 't'], 2: ['r']}` (列表內元素順序可能不同)，
# 這表示出現一次的字母是 `'p'`、`'a'`、`'o'` 和 `'t'`，出現兩次的字母是 `'r'`。
#
# 下面的函數接收一個字典並回傳其反轉版本作為一個新的字典。

def invert_dict(d_to_invert): # 參數改名
    new_inverted_dict = {}
    for key_orig, value_orig in d_to_invert.items():
        if value_orig not in new_inverted_dict: # 如果這個值還沒成為新字典的鍵
            new_inverted_dict[value_orig] = [key_orig] # 就用這個值當鍵，並建立一個只包含目前鍵的列表
        else: # 如果這個值已經是新字典的鍵了
            new_inverted_dict[value_orig].append(key_orig) # 就把目前的鍵加到對應的列表中
    return new_inverted_dict

# `for` 陳述式遍歷 `d_to_invert` 中的鍵和值。
# 如果值還沒在新字典中，它就會被加入，並與一個只包含單一元素的列表相關聯。
# 否則，它會被附加到現有的列表中。
#
# 我們可以像這樣測試它：

inverted_parrot_dict = invert_dict(d_parrot_counts)
# 為了讓比較結果一致，我們可以對列表內的值排序
for key_inv in inverted_parrot_dict:
    inverted_parrot_dict[key_inv].sort()
print(f"invert_dict(d_parrot_counts): {inverted_parrot_dict}")


# 我們得到了預期的結果。
#
# 這是我們看到的第一個字典中的值是列表的例子。
# 我們將會看到更多！

# ## 除錯 (Debugging)
#
# 列表、字典和元組都是 **資料結構 (data structures)**。
# 在這一章，我們開始看到複合資料結構，像是元組的列表，
# 或者是包含元組作為鍵、列表作為值的字典。
# 複合資料結構很有用，但也容易因為資料結構的型別、大小或結構錯誤而導致錯誤。
# 例如，如果一個函數期望得到一個整數列表，而你給了它一個普通的整數
# (不在列表中)，它可能無法運作。
#
# 為了幫助除錯這類錯誤，我寫了一個叫做 `structshape` 的模組，
# 它提供了一個也叫做 `structshape` 的函數，該函數接收任何種類的資料結構作為參數，
# 並回傳一個總結其結構的字串。
# 你可以從以下網址下載它：
# <https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py>。

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py');

# 我們可以像這樣匯入它。

try:
    from structshape import structshape
except ImportError:
    print("錯誤: structshape.py 未找到或無法匯入。請確保已下載並在 Python 路徑中。")
    # 定義一個假的 structshape 以免後續程式碼出錯
    def structshape(data):
        return f"structshape無法使用，傳入的資料型別為: {type(data)}"


# 這裡有一個簡單列表的例子。

t_struct_list = [1, 2, 3]
print(structshape(t_struct_list))

# 這裡是一個列表的列表。

t2_list_of_lists = [[1,2], [3,4], [5,6]]
print(structshape(t2_list_of_lists))

# 如果列表的元素型別不同，`structshape` 會按型別將它們分組。

t3_mixed_types = [1, 2, 3, 4.0, '5', '6', [7], [8], 9]
print(structshape(t3_mixed_types))

# 這裡是一個元組的列表。

s_for_zip = 'abc'
t_for_zip_struct = [1,2,3] # 確保 t_for_zip_struct 與 s_for_zip 長度一致或更長
lt_list_of_tuples = list(zip(t_for_zip_struct, s_for_zip))
print(structshape(lt_list_of_tuples))

# 這裡是一個包含三個項目的字典，它們把整數對應到字串。

d_struct_example = dict(lt_list_of_tuples)
print(structshape(d_struct_example))

# 如果你難以追蹤你的資料結構，`structshape` 可以幫上忙。

# ## 詞彙表 (Glossary)
#
# **打包 (pack):**
#  將多個引數收集到一個元組中。
#
# **解包 (unpack):**
#  將元組 (或其他序列) 視為多個引數。
#
# **zip 物件 (zip object):**
#  呼叫內建函數 `zip` 的結果，可以用來遍歷一個元組序列。
#
# **enumerate 物件 (enumerate object):**
#  呼叫內建函數 `enumerate` 的結果，可以用來遍歷一個元組序列 (包含索引和元素)。
#
# **排序鍵 (sort key):**
#  一個值，或是一個計算出值的函數，用來排序一個集合中的元素。
#
# **資料結構 (data structure):**
#  值的集合，以某種方式組織起來以便有效地執行某些操作。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 本章的練習可能比前幾章的練習更難，所以我鼓勵你向虛擬助理尋求幫助。
# 當你提出更困難的問題時，你可能會發現答案在第一次嘗試時並不正確，
# 所以這是一個練習撰寫好的提示 (prompt) 並接著提出好的修正意見的機會。
#
# 你可以考慮的一個策略是，把大問題分解成可以用簡單函數解決的小塊。
# 請虛擬助理編寫這些函數並測試它們。
# 然後，一旦它們可以運作了，再請求解決原始問題的方案。
#
# 對於下面的一些練習，我會提出關於使用哪些資料結構和演算法的建議。
# 你在解決問題時可能會覺得這些建議很有用，但它們也是很好的提示，可以傳達給虛擬助理。

# ### 練習
#
# 在本章我說過，元組可以用作字典中的鍵，因為它們是可雜湊的，
# 而它們之所以可雜湊，是因為它們是不可變的。
# 但這並不總是對的。
#
# 如果一個元組包含一個可變的值，像是列表或字典，
# 那麼這個元組就不再是可雜湊的，因為它包含了不可雜湊的元素。
# 作為例子，這裡有一個包含兩個整數列表的元組。

list0_ex = [1, 2, 3]
list1_ex = [4, 5]

t_mutable_content = (list0_ex, list1_ex)
print(f"原始元組 t_mutable_content: {t_mutable_content}")

# 寫一行程式碼，將值 `6` 附加到 `t_mutable_content` 中第二個列表的末尾。
# 如果你顯示 `t_mutable_content`，結果應該是 `([1, 2, 3], [4, 5, 6])`。

# 解答:
t_mutable_content[1].append(6) # 元組本身不可變，但它包含的列表是可變的
print(f"修改後元組 t_mutable_content: {t_mutable_content}")

# 試著建立一個把 `t_mutable_content` 對應到一個字串的字典，並確認你會得到一個 `TypeError`。

%%expect TypeError
# d_error_test = {t_mutable_content: '這個元組包含兩個列表'}
# (因為 t_mutable_content 包含可變的列表，所以 t_mutable_content 不可雜湊)

# 想了解更多關於這個主題的資訊，可以問問虛擬助理：「Python 的元組總是可雜湊的嗎？」

# ### 練習
#
# 在本章中，我們建立了一個把每個字母對應到它在字母表中索引的字典。

letters_alpha = 'abcdefghijklmnopqrstuvwxyz'
numbers_alpha_indices = range(len(letters_alpha))
letter_map_alpha_ex = dict(zip(letters_alpha, numbers_alpha_indices))

# 例如，`'a'` 的索引是 `0`。

print(f"\n--- 凱撒密碼練習 ---")
print(f"letter_map_alpha_ex['a']: {letter_map_alpha_ex['a']}")

# 要反過來做，我們可以用列表索引 (這裡 `letters_alpha` 是字串，行為類似列表)。
# 例如，索引 `1` 的字母是 `'b'`。

print(f"letters_alpha[1]: {letters_alpha[1]}")

# 我們可以用 `letter_map_alpha_ex` 和 `letters_alpha` 來使用凱撒密碼 (Caesar cipher) 編碼和解碼單字。
#
# 凱撒密碼是一種弱加密形式，它將每個字母在字母表中移動固定的位置數，
# 如有必要則從頭開始循環。例如，`'a'` 移動 2 位是 `'c'`，`'z'` 移動 1 位是 `'a'`。
#
# 寫一個叫做 `shift_word` 的函數，它接收一個字串和一個整數作為參數，
# 並回傳一個新的字串，其中包含來自原字串的字母被移動了指定位置數。
#
# 為了測試你的函數，請確認 "cheer" 移動 7 位是 "jolly"，"melon" 移動 16 位是 "cubed"。
#
# 提示：使用模數運算子 `%` 來從 `'z'` 循環回 `'a'`。
# 遍歷單字的字母，移動每一個字母，然後把結果附加到一個字母列表中。
# 然後使用 `join` 把字母串接成一個字串。

# 你可以用這個大綱開始。

def shift_word_starter(word, n): # 改名避免與解答衝突
    """將 `word` 的字母移動 `n` 個位置。

    >>> shift_word_starter('cheer', 7)
    'jolly'
    >>> shift_word_starter('melon', 16)
    'cubed'
    """
    return None # 你的程式碼會取代這裡

# 解答

def shift_word(word, n_shift): # 參數改名
    """將 `word` 的字母移動 `n_shift` 個位置。

    >>> shift_word('cheer', 7)
    'jolly'
    >>> shift_word('melon', 16)
    'cubed'
    >>> shift_word('zebra', 1) # 測試循環
    'afcsb'
    >>> shift_word('apple', -1) # 測試負數移動
    'zooqd'
    """
    shifted_letters_list = []
    num_letters = 26 # 字母表中的字母數量
    for letter_char in word:
        if letter_char in letter_map_alpha_ex: # 只處理字母表中的字母
            original_index = letter_map_alpha_ex[letter_char]
            new_index = (original_index + n_shift) % num_letters
            # 處理負數 n_shift 後的 new_index 可能仍為負的情況 (如果 Python 的 % 結果是負的)
            # 在 Python 中, a % n 的結果符號與 n 相同，所以如果 n_shift 是大的負數，
            # (original_index + n_shift) 可能是負的，
            # (original_index + n_shift) % num_letters 的結果可能是 -num_letters 到 -1 之間。
            # 例如 (-1) % 26 在 Python 中是 25。所以通常是正確的。
            # 但為了更明確，可以寫成 (original_index + n_shift % num_letters + num_letters) % num_letters
            # 或者直接用 (original_index + n_shift) % num_letters 就好，因為 Python 的 % 行為通常符合需求。
            shifted_letters_list.append(letters_alpha[new_index])
        else:
            shifted_letters_list.append(letter_char) # 非字母字元保持不變
    return ''.join(shifted_letters_list)

print(f"shift_word('cheer', 7): {shift_word('cheer', 7)}")

print(f"shift_word('melon', 16): {shift_word('melon', 16)}")

# 你可以用 `doctest` 來測試你的函數。

from doctest import run_docstring_examples

def run_doctests(func):
    print(f"--- 執行 {func.__name__} 的 doctests ---")
    run_docstring_examples(func, globals(), name=func.__name__)

run_doctests(shift_word)

# ### 練習
#
# 寫一個叫做 `most_frequent_letters` 的函數，它接收一個字串，
# 並按頻率遞減的順序列印字母。
#
# 要按遞減順序獲取項目，你可以使用 `reversed` 搭配 `sorted`，
# 或者你可以將 `reverse=True` 作為關鍵字參數傳遞給 `sorted`。

# 你可以用這個函數大綱開始。

def most_frequent_letters_starter(string_input): # 改名避免與解答衝突
    return None # 你的程式碼會取代這裡

# 解答

def most_frequent_letters(string_input):
    # 確保 value_counts 和 second_element 在此作用域可用
    # value_counts 之前已定義，second_element 也在前面定義過
    letter_counts = value_counts(string_input)
    # items() 取得 (鍵, 值) 對
    # key=second_element 表示按值 (元組的第二個元素，即計數) 排序
    # reverse=True 表示遞減排序
    sorted_letter_pairs = sorted(letter_counts.items(), key=second_element, reverse=True)
    print(f"字串 '{string_input[:20]}{'...' if len(string_input)>20 else ''}' 中字母按頻率遞減排序:")
    for letter_item, count_item in sorted_letter_pairs:
        print(f"{letter_item}: {count_item}")

# 用這個例子來測試你的函數。

print("\n--- 測試 most_frequent_letters ---")
most_frequent_letters('brontosaurus')

# 一旦你的函數可以運作，你可以用下面的程式碼來印出《德古拉》(Dracula) 中最常見的字母，
# 我們可以從古騰堡計畫下載它。

download('https://www.gutenberg.org/cache/epub/345/pg345.txt');

dracula_string = ""
if exists('pg345.txt'):
    dracula_string = open('pg345.txt', encoding='utf-8').read().lower() # 轉小寫以統一計數
    # 也可以只計算字母
    # import string as py_string
    # dracula_string_letters_only = ''.join(filter(str.isalpha, dracula_string))
    # most_frequent_letters(dracula_string_letters_only)
    most_frequent_letters(dracula_string)

else:
    print("錯誤: pg345.txt 未找到，無法分析。")


# 根據 Zim 的《密碼與秘密寫作》(Codes and Secret Writing)，
# 英文中按頻率遞減排序的字母序列以 "ETAONRISH" 開始。
# 這個序列與《德古拉》的結果相比如何？
# (觀察上面印出的結果來比較)

# ### 練習
#
# 在之前的練習中，我們透過排序兩個字串中的字母並檢查排序後的字母是否相同，
# 來測試兩個字串是否為相同字母異序詞 (anagram)。
# 現在讓我們把問題弄得更有挑戰性一點。
#
# 我們要寫一個程式，它接收一個單字列表，並印出所有互為相同字母異序詞的單字集合。
# 輸出可能看起來像這樣 (只是範例，實際輸出會依 word_list 而定)：
#
#     ['deltas', 'desalt', 'lasted', 'salted', 'slated', 'staled']
#     ['retainers', 'ternaries']
#     ['generating', 'greatening']
#     ['resmelts', 'smelters', 'termless']
#
# 提示：對於單字列表中的每個單字，將其字母排序並重新組合成一個字串。
# 建立一個字典，將這個排序後的字串對應到一個包含其所有相同字母異序詞的單字列表。

# 下面的儲存格會下載 `words.txt` 並將單字讀入一個列表。

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

word_list_anagram = []
if exists('words.txt'):
    word_list_anagram = open('words.txt', encoding='utf-8').read().split()
else:
    print("錯誤: words.txt 未找到，無法進行相同字母異序詞分析。")


# 這是我們之前用過的 `sort_word` 函數。

def sort_word(word_input): # 參數改名
    return ''.join(sorted(word_input))

# 解答
print("\n--- 找出所有相同字母異序詞的集合 ---")
anagram_dict = {}
if word_list_anagram:
    for current_word in word_list_anagram:
        sorted_key = sort_word(current_word) # 用排序後的字串當作鍵
        if sorted_key not in anagram_dict:
            anagram_dict[sorted_key] = [current_word] # 如果鍵不存在，建立新列表
        else:
            anagram_dict[sorted_key].append(current_word) # 如果鍵已存在，將單字加入列表
else:
    print("單字列表是空的。")

# 印出所有包含多於一個單字 (即有相同字母異序詞) 的集合
anagram_sets_count = 0
for sorted_signature, anagram_group in anagram_dict.items():
    if len(anagram_group) > 1:
        print(anagram_group)
        anagram_sets_count +=1
        if anagram_sets_count > 10 and len(word_list_anagram) > 1000 : # 避免印太多，只印前幾組
            print("... (還有更多)")
            break
if anagram_sets_count == 0 and word_list_anagram:
    print("沒有找到任何相同字母異序詞的集合。")


# 要找到最長的相同字母異序詞列表，你可以使用下面的函數，
# 它接收一個鍵值對，其中鍵是一個字串，值是一個單字列表。
# 它回傳列表的長度。

def value_length(pair_input): # 參數改名
    key_item, value_list = pair_input
    return len(value_list)

# 我們可以用這個函數作為排序鍵來找到最長的相同字母異序詞列表。

print("\n--- 最長的 10 組相同字母異序詞 (按組內單字數量排序) ---")
if anagram_dict:
    # .items() 將字典轉成 (鍵, 值) 元組的列表
    # key=value_length 表示按每個元組的值 (即相同字母異序詞列表的長度) 來排序
    anagram_items_sorted_by_length = sorted(anagram_dict.items(), key=value_length)
    # 印出最長的 10 組 (如果有的話)
    for key_s, value_s_list in anagram_items_sorted_by_length[-10:]: # 取最後10個 (最長的)
        if len(value_s_list) > 1: # 確保是真的異序詞組
            print(value_s_list)
else:
    print("相同字母異序詞字典是空的。")


# 如果你想知道哪些是最長的、且具有相同字母異序詞的單字，
# 你可以用下面的迴圈來印出其中一些。

print("\n--- 最長的且有相同字母異序詞的單字 (按單字本身長度) ---")
longest_word_len_with_anagrams = 0 # 初始化為一個合理的小值，或第一個找到的長度

# 先找出所有有異序詞的組，並記錄它們原始單字的長度
anagram_groups_with_word_len = []
if anagram_dict:
    for key_al, value_al_list in anagram_dict.items():
        if len(value_al_list) > 1: # 確保是異序詞組
            # 假設組內單字長度都一樣 (因為它們是異序詞)
            word_len_in_group = len(value_al_list[0])
            anagram_groups_with_word_len.append((word_len_in_group, value_al_list))

    # 按單字長度排序 (降序)
    anagram_groups_with_word_len.sort(key=lambda x: x[0], reverse=True)

    # 印出前幾個最長單字的異序詞組
    printed_longest_count = 0
    for length, group in anagram_groups_with_word_len:
        if printed_longest_count < 5: # 印出前 5 組最長的
            print(f"長度 {length}: {group}")
            printed_longest_count += 1
        else:
            break
    if not anagram_groups_with_word_len:
        print("沒有找到任何有相同字母異序詞的單字組。")
else:
    print("相同字母異序詞字典是空的。")


# ### 練習
#
# 寫一個叫做 `word_distance` 的函數，它接收兩個相同長度的單字，
# 並回傳這兩個單字在多少個位置上的字母不同。
#
# 提示：使用 `zip` 來遍歷單字的相應字母。

# 這裡有一個包含 doctests 的函數大綱，你可以用來檢查你的函數。

def word_distance_starter(word1, word2): # 改名避免與解答衝突
    """計算兩個單字在多少個位置上不同。

    >>> word_distance_starter("hello", "hxllo")
    1
    >>> word_distance_starter("ample", "apply")
    2
    >>> word_distance_starter("kitten", "mutton") # k!=m, i!=u, e!=o -> 3
    3
    """
    return None # 你的程式碼會取代這裡

# 解答

def word_distance(word1, word2):
    """計算兩個單字在多少個位置上不同。

    >>> word_distance("hello", "hxllo")
    1
    >>> word_distance("ample", "apply")
    2
    >>> word_distance("kitten", "mutton")
    3
    >>> word_distance("same", "same")
    0
    """
    # 斷言 (assert) 確保兩個單字長度相同，如果不符合條件程式會終止並報錯
    assert len(word1) == len(word2), "輸入的兩個單字長度必須相同"

    difference_count = 0
    for char1, char2 in zip(word1, word2): # zip 會成對遍歷
        if char1 != char2:
            difference_count += 1

    return difference_count

# from doctest import run_docstring_examples # 已在前面匯入過

# def run_doctests(func): # 已在前面定義過
#     run_docstring_examples(func, globals(), name=func.__name__)

print("\n--- 測試 word_distance ---")
run_doctests(word_distance)

# ### 練習
#
# 「換位 (Metathesis)」是指單字中字母的調換。
# 如果你可以透過交換兩個字母將一個單字轉換成另一個單字，
# 那麼這兩個單字就構成一個「換位對 (metathesis pair)」，例如 `converse` 和 `conserve`。
# (c-o-n-v-e-r-s-e, c-o-n-s-e-r-v-e，v/s 和 r/e 的位置不同，但這裡的例子是交換 v 和 s)
# (更準確的例子: `observe` 和 `obverse` 交換 s, v)
# (再一個例子: `teacher` 和 `cheater`，交換 t 和 c)
#
# 寫一個程式，找出單字列表中的所有換位對。
#
# 提示：換位對中的單字必須互為相同字母異序詞。
#
# 來源：這個練習的靈感來自 <http://puzzlers.org> 的一個例子。

# 解答
print("\n--- 找出換位對 (長度 >= 10，且差異為 2) ---")
metathesis_pair_count = 0
if anagram_dict: # 確保 anagram_dict 已建立
    for anagram_key, anagrams_list in anagram_dict.items():
        # 我們只需要檢查同一個相同字母異序詞組內的單字
        if len(anagrams_list) > 1: # 必須至少有兩個單字才可能形成配對
            # 為了避免重複配對 (word1, word2) 和 (word2, word1)
            # 以及一個字和自己比較，我們可以用索引來遍歷
            for i in range(len(anagrams_list)):
                for j in range(i + 1, len(anagrams_list)): # j 從 i+1 開始
                    word1_meta = anagrams_list[i]
                    word2_meta = anagrams_list[j]

                    # 題目要求「交換兩個字母」，所以 word_distance 應該是 2
                    # 並且，為了讓例子更有趣，我們可以加上長度限制
                    if len(word1_meta) >= 10 and word_distance(word1_meta, word2_meta) == 2:
                        print(word1_meta, word2_meta)
                        metathesis_pair_count += 1
                        if metathesis_pair_count > 10 and len(word_list_anagram) > 1000: # 避免印太多
                            print("... (還有更多)")
                            # 用 break 只能跳出一層迴圈，若要完全停止可以設 flag
                            break
                if metathesis_pair_count > 10 and len(word_list_anagram) > 1000:
                    break
        if metathesis_pair_count > 10 and len(word_list_anagram) > 1000:
            break
    if metathesis_pair_count == 0:
        print("沒有找到符合條件的換位對。")
else:
    print("相同字母異序詞字典是空的，無法尋找換位對。")


# ### 練習
#
# 這是一個書中沒有的額外練習。
# 它比本章的其他練習更具挑戰性，所以你可能需要向虛擬助理尋求幫助，
# 或者在閱讀更多章節後再回來做。
#
# 這裡有另一個 Car Talk Puzzler (汽車談話謎題)
# (<http://www.cartalk.com/content/puzzlers>):
#
# > 哪個是最長的英文單字，當你逐一移除它的字母時，它仍然是一個有效的英文單字？
# >
# > 現在，字母可以從兩端或中間移除，但你不能重新排列任何字母。
# > 每次你去掉一個字母，你都會得到另一個英文單字。如果你這樣做，
# > 你最終會得到一個字母，而那個字母本身也是一個英文單字——在字典中可以找到的。
# > 我想知道最長的單字是什麼，它有多少個字母？
# >
# > 我給你一個簡單的例子：Sprite (雪碧；小精靈)。好嗎？你從 sprite 開始，
# > 去掉一個字母，從單字內部去掉一個，把 r 去掉，剩下 spite (怨恨)，
# > 然後我們把尾巴的 e 去掉，剩下 spit (吐痰)，我們把 s 去掉，
# > 剩下 pit (坑)，然後是 it (它)，最後是 I (我)。
#
# 寫一個程式來找出所有可以這樣被縮減的單字，然後找出最長的那一個。
#
# 這個練習比大多數練習都難一點，所以這裡有一些建議：
#
# 1.  你可能需要寫一個函數，它接收一個單字並計算出一個列表，
#     其中包含所有可以透過移除一個字母形成的單字。這些是該單字的「子字 (children)」。
#
# 2.  遞迴地說，如果一個單字的任何子字是可縮減的，那麼該單字就是可縮減的。
#     作為基礎情況 (base case)，你可以認為空字串是可縮減的。
#
# 3.  我們一直使用的單字列表不包含單字母單字。所以你可能需要加入 "I" 和 "a"。
#
# 4.  為了提高程式的效能，你可能需要將已知可縮減的單字備忘錄化 (memoize)。

# 解答
print("\n--- Car Talk Puzzler: 可縮減單字 ---")

# 確保 word_list_anagram (或任何你選擇使用的完整單字列表) 已載入
# 並且建立一個 word_dict 方便快速查找
word_dict_reducible = {}
if word_list_anagram:
    for w in word_list_anagram:
        word_dict_reducible[w] = 1
else:
    # 如果 word_list_anagram 是空的，嘗試從 words.txt 重新載入
    if exists('words.txt'):
        temp_list = open('words.txt', encoding='utf-8').read().split()
        for w_temp in temp_list:
            word_dict_reducible[w_temp] = 1
    else:
        print("錯誤: words.txt 未找到，無法進行可縮減單字分析。")

# 加入單字母單字和空字串
for single_char_word in ['a', 'i', '']: # 空字串作為遞迴的基礎
    word_dict_reducible[single_char_word] = 1


def children(word_input_child):
    """回傳所有可以透過移除一個字母形成的有效單字的列表。

    word_input_child: 字串

    回傳: 字串列表
    """
    res_children = []
    for i_child in range(len(word_input_child)):
        child_word = word_input_child[:i_child] + word_input_child[i_child+1:]
        if child_word in word_dict_reducible: # 檢查是否是有效單字
            res_children.append(child_word)
    return res_children

# 解答

"""memo_reducible 是一個字典，它把每個已知可縮減的單字
對應到其可縮減子字的列表。
它從空字串開始。"""

memo_reducible = {}
memo_reducible[''] = [''] # 基礎情況：空字串是可縮減的，它的子字是它自己 (或一個代表終點的標記)


def reduce_word(word_input_reduce):
    """如果 word_input_reduce 是可縮減的，回傳其可縮減子字的列表。

    同時在 memo_reducible 字典中新增一個項目。

    一個字串是可縮減的，如果它至少有一個子字是可縮減的。
    空字串也是可縮減的。

    word_input_reduce: 字串
    """
    # 如果已經檢查過這個單字，回傳答案
    if word_input_reduce in memo_reducible:
        return memo_reducible[word_input_reduce]

    # 檢查每個子字，並建立一個可縮減子字的列表
    res_reducible_children = []
    for child_candidate in children(word_input_reduce): # children() 會回傳有效的子單字
        # 遞迴檢查子字是否可縮減
        # reduce_word(child_candidate) 回傳的是該子字的可縮減路徑 (的下一個)
        # 如果 reduce_word(child_candidate) 回傳非空列表，表示 child_candidate 可縮減
        if reduce_word(child_candidate): # 這裡的條件是 reduce_word 回傳的列表不為空
            res_reducible_children.append(child_candidate) # 把這個可縮減的子字加入結果

    # 備忘錄化並回傳結果
    # 如果 res_reducible_children 是空的，表示這個字不可縮減 (到空字串)
    # 除非它本身就是 '' (已在 memo_reducible[''] 處理)
    memo_reducible[word_input_reduce] = res_reducible_children
    return res_reducible_children

# 解答

def print_trail(word_input_trail):
    """印出將此單字縮減為空字串的單字序列。

    如果有多種選擇，它會選擇第一個。

    word_input_trail: 字串
    """
    if len(word_input_trail) == 0: # 到達空字串，結束遞迴
        print("-> ''") # 標示結束
        return
    print(word_input_trail, end=' ')
    reducible_children_trail = reduce_word(word_input_trail)
    if reducible_children_trail: # 如果有可縮減的路徑
        print_trail(reducible_children_trail[0]) # 選擇第一條路徑繼續
    else: # 理論上，如果 word_input_trail 是從 all_reducible 來的，這裡不該發生
        print("(無法再縮減)")


# 解答

def all_reducible():
    """檢查 word_dict_reducible 中的所有單字；回傳一個可縮減單字的列表。
    """
    res_all_reducible = []
    if not word_dict_reducible:
        print("word_dict_reducible 是空的，無法找出可縮減單字。")
        return res_all_reducible

    # 為了讓進度可見，可以加個計數器
    total_words_to_check = len(word_dict_reducible)
    checked_count = 0
    print_interval = total_words_to_check // 100 + 1 # 每 1% 印一次

    for word_check in word_dict_reducible:
        # if checked_count % print_interval == 0:
        #     print(f"正在檢查可縮減單字... 進度: {checked_count}/{total_words_to_check} ({checked_count*100/total_words_to_check:.0f}%)")
        
        # 我們只對長度大於1的字有興趣，因為 'a' 和 'i' 已經是單字母了
        if len(word_check) <= 1 and word_check != '': # a, i 可以直接縮減到 ''
             if reduce_word(word_check): # 確保它們能縮到 ''
                res_all_reducible.append(word_check)
        elif len(word_check) > 1:
            # reduce_word 會回傳一個列表，如果列表不空，表示 word_check 可縮減
            if reduce_word(word_check):
                res_all_reducible.append(word_check)
        checked_count += 1
    # print("可縮減單字檢查完成。")
    return res_all_reducible

# 解答 (執行的主體部分)

# 重新填充 word_dict_reducible，因為之前的 word_dict 可能被其他練習修改
# (如果是在同一個 notebook session 中，變數會共享)
# 或者確保 word_dict_reducible 在此處被正確初始化
# (已在 In[205] 的開頭處理)

if word_dict_reducible:
    # 找出可縮減的單字並按長度排序
    print("開始尋找所有可縮減單字 (這可能需要一些時間)...")
    reducible_words_found = all_reducible()
    print(f"共找到 {len(reducible_words_found)} 個可縮減單字。")

    if reducible_words_found:
        sorted_reducible_words = sorted(reducible_words_found, key=len)

        # 印出最長的10個 (如果少於10個就全印)
        print("\n最長的幾個可縮減單字及其縮減路徑:")
        num_to_print = min(10, len(sorted_reducible_words))
        for word_to_print_trail in sorted_reducible_words[-num_to_print:]: # 取最後 num_to_print 個
            print_trail(word_to_print_trail)
            # print('') # print_trail 裡面會換行
    else:
        print("沒有找到任何可縮減單字。")
else:
    print("word_dict_reducible 是空的，無法執行主要解答部分。")


# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)