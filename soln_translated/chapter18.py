# -*- coding: utf-8 -*-
# 從 chap18.ipynb 轉換而來
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

# 這裡有第 17 章的 `Card`、`Deck` 和 `Hand` 類別的版本，
# 我們在本章的一些範例中會用到它們。
# (為了確保這些類別定義在此腳本中可用，我們直接複製過來)

class Card:
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃'] # 中文化花色
    rank_names = [None, 'A', '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit_code, rank_code): # 參數改名
        self.suit = suit_code
        self.rank = rank_code

    def __str__(self):
        rank_name_str = Card.rank_names[self.rank]
        suit_name_str = Card.suit_names[self.suit]
        return f'{suit_name_str}{rank_name_str}' # 符合中文習慣

    # 為了讓 Deck.sort() 能運作，Card 需要比較方法
    def __lt__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return (self.suit, self.rank) < (other.suit, other.rank)


import random

class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list=None): # 參數改名，並允許預設為 None
        if cards_list is None:
            self.cards = Deck.make_cards() # 如果沒提供牌，就建立一副新牌
        else:
            self.cards = cards_list

    def __str__(self):
        res_list_str = [str(card_item) for card_item in self.cards]
        return '\n'.join(res_list_str)

    @staticmethod # 標記為靜態方法
    def make_cards():
        """建立並回傳一副標準的 52 張撲克牌的列表。"""
        cards_deck = []
        for suit_code_deck in range(4):
            for rank_code_deck in range(2, 15): # 2 到 14 (A 為 14)
                card_obj = Card(suit_code_deck, rank_code_deck)
                cards_deck.append(card_obj)
        return cards_deck

    def shuffle(self):
        """隨機打亂牌堆中的牌。"""
        random.shuffle(self.cards)

    def pop_card(self): # 書中用 pop_card，之前用 take_card
        """從牌堆頂部 (列表末端) 移除並回傳一張牌。"""
        if self.cards:
            return self.cards.pop()
        return None

    def add_card(self, card_to_add): # 書中用 add_card，之前用 put_card
        """將一張牌加入到牌堆底部 (列表末端)。"""
        if isinstance(card_to_add, Card):
            self.cards.append(card_to_add)

    def sort(self): # 新增 sort 方法 (如第17章)
        """排序牌堆中的牌。"""
        self.cards.sort()

    def move_cards(self, other_hand_or_deck, num_cards): # 新增 move_cards (如第17章)
        for _ in range(num_cards):
            if not self.cards: break
            card_to_move = self.pop_card()
            if card_to_move:
                other_hand_or_deck.add_card(card_to_move)


class Hand(Deck):
    """表示一手牌。"""
    def __init__(self, label=''): # Hand 的 __init__ 覆寫 Deck 的
        self.label = label
        self.cards = [] # 一手牌開始時是空的

# # Python 額外功能 (Python Extras)
#
# 我寫這本書的目標之一是盡可能少教你 Python 的東西。
# 當有兩種方法可以做某件事時，我會選擇一種，並避免提及另一種。
# 或者有時我會把第二種方法放到練習中。
#
# 現在我想回過頭來看看一些被遺漏掉的好東西。
# Python 提供了許多並非絕對必要的功能 —— 沒有它們你也能寫出好的程式碼 ——
# 但是有了它們，你可以寫出更簡潔、更易讀或更有效率的程式碼，有時三者兼具。

# ## 集合 (Sets)
#
# Python 提供了一個叫做 `set` 的類別，它代表一個不重複元素的集合。
# 要建立一個空集合，我們可以像使用函數一樣使用類別物件。

s1 = set() # 建立一個空集合
print(f"s1 (空集合): {s1}")

# 我們可以用 `add` 方法來加入元素。

s1.add('a')
s1.add('b')
print(f"加入元素後的 s1: {s1}") # 集合元素是無序的

# 或者我們可以傳遞任何種類的序列給 `set()`。

s2 = set('acd') # 從字串建立集合，'a' 'c' 'd'
print(f"s2 (從字串 'acd' 建立): {s2}")

# 一個元素在 `set` 中只能出現一次。
# 如果你加入一個已經存在的元素，它不會有任何效果。

s1.add('a') # 'a' 已經在 s1 中了
print(f"再次加入 'a' 後的 s1: {s1}") # s1 保持不變

# 或者如果你用一個包含重複元素的序列來建立集合，結果只會包含不重複的元素。

set_from_banana = set('banana') # 'b', 'a', 'n'
print(f"set('banana'): {set_from_banana}")

# 本書中的一些練習可以用集合來簡潔且有效率地完成。
# 例如，這裡有一個第十一章練習的解答，它使用字典來檢查序列中是否有任何重複元素。

def has_duplicates_dict_version(t_sequence): # 參數改名
    d_counts = {}
    for x_item in t_sequence:
        # 其實這裡的 d_counts[x_item] = True 就夠了，不需要真的計數
        # 只要 x_item 能當鍵，就可以用來判斷是否出現過
        d_counts[x_item] = True # 把元素當作字典的鍵
    # 如果字典的鍵數少於序列長度，表示有重複 (因為重複的鍵會被覆蓋)
    return len(d_counts) < len(t_sequence)

# 這個版本把 `t_sequence` 的元素當作鍵加入字典，
# 然後檢查鍵的數量是否少於元素的數量。
# 使用集合，我們可以像這樣寫同一個函數。

def has_duplicates_set_version(t_sequence): # 參數改名
    s_unique = set(t_sequence) # 建立集合時會自動去重
    return len(s_unique) < len(t_sequence) # 比較去重後的長度和原始長度

print(f"has_duplicates_set_version('abba'): {has_duplicates_set_version('abba')}") # True

# 一個元素在集合中只能出現一次，所以如果 `t_sequence` 中的元素出現超過一次，
# 集合的大小就會小於 `t_sequence`。
# 如果沒有重複，集合的大小會和 `t_sequence` 相同。
#
# `set` 物件提供了執行集合運算的方法。
# 例如，`union` (聯集) 計算兩個集合的聯集，結果是一個新的集合，
# 包含出現在任一集合中的所有元素。

# s1 是 {'a', 'b'} (或 {'b', 'a'})
# s2 是 {'a', 'c', 'd'} (或其他順序)
union_s1_s2 = s1.union(s2) # {'a', 'b', 'c', 'd'}
print(f"s1.union(s2): {union_s1_s2}")
# 也可以用 | 運算子： s1 | s2

# 一些算術運算子也適用於集合。
# 例如，`-` 運算子執行集合的差集 (set subtraction) —— 結果是一個新的集合，
# 包含所有來自第一個集合但 *不在* 第二個集合中的元素。

diff_s1_minus_s2 = s1 - s2 # s1 中有，但 s2 中沒有的元素 -> {'b'}
print(f"s1 - s2: {diff_s1_minus_s2}")
diff_s2_minus_s1 = s2 - s1 # s2 中有，但 s1 中沒有的元素 -> {'c', 'd'}
print(f"s2 - s1: {diff_s2_minus_s1}")

# 在[第十二章](section_dictionary_subtraction)中，我們用字典來找出文件中出現但不在單字列表中的單字。
# (譯註：section_dictionary_subtraction 指的是書中對應章節的連結)
# 我們用了下面的函數，它接收兩個字典並回傳一個新的字典，
# 其中只包含來自第一個字典但沒有出現在第二個字典中的鍵。

def subtract_dicts(d1, d2): # 書中為 subtract，這裡改名避免與集合的減法混淆
    res_dict_diff = {}
    for key_d1 in d1:
        if key_d1 not in d2:
            res_dict_diff[key_d1] = d1[key_d1] # 保留 d1 中的值
    return res_dict_diff

# 使用集合，我們不需要自己寫這個函數。
# 如果 `word_counter_set_ex` 是一個包含文件中不重複單字的字典 (鍵是單字)，
# 而 `word_list_set_ex` 是一個有效單字的列表，
# 我們可以像這樣計算集合的差集。

# 這個儲存格建立一個小例子，這樣我們就可以執行下面的儲存格而不用載入實際資料
word_counter_set_ex = {'word': 1, 'example': 1, 'test': 1}
word_list_set_ex = ['word', 'test', 'valid']

# 把字典的鍵轉成集合，把列表轉成集合，然後相減
set_diff_example = set(word_counter_set_ex.keys()) - set(word_list_set_ex)
# 等同於 set(word_counter_set_ex) - set(word_list_set_ex)
print(f"set(word_counter_ex) - set(word_list_ex): {set_diff_example}") # {'example'}

# 結果是一個集合，包含文件中出現但不在單字列表中的單字。
#
# 關係運算子也適用於集合。
# 例如，`<=` 檢查一個集合是否是另一個集合的子集 (subset)，包含它們相等的可能性。

is_subset1 = set('ab') <= set('abc') # {'a','b'} 是 {'a','b','c'} 的子集
print(f"set('ab') <= set('abc'): {is_subset1}") # True
is_subset2 = set('abd') <= set('abc')
print(f"set('abd') <= set('abc'): {is_subset2}") # False (d 不在裡面)


# 有了這些運算子，我們可以用集合來完成第七章的一些練習。
# 例如，這裡是一個使用迴圈的 `uses_only` 版本。

def uses_only_loop_version(word_uo, available_chars_uo): # 參數改名
    for letter_uo in word_uo:
        if letter_uo not in available_chars_uo:
            return False
    return True

# `uses_only` 檢查 `word_uo` 中的所有字母是否都在 `available_chars_uo` 中。
# 用集合，我們可以像這樣改寫它。

def uses_only_set_version(word_uo_set, available_chars_uo_set): # 參數改名
    # 如果 word_uo_set 中的所有字母都是 available_chars_uo_set 的子集，
    # 表示 word_uo_set 只使用了 available_chars_uo_set 中的字母。
    return set(word_uo_set) <= set(available_chars_uo_set)

# 如果 `word_uo_set` 中的字母是 `available_chars_uo_set` 中字母的子集，
# 這就表示 `word_uo_set` 只使用了 `available_chars_uo_set` 中的字母。
print(f"uses_only_set_version('banana', 'ban'): {uses_only_set_version('banana', 'ban')}") # True
print(f"uses_only_set_version('apple', 'aple'): {uses_only_set_version('apple', 'aple')}") # True (l, e 都在)
print(f"uses_only_set_version('apple', 'aplx'): {uses_only_set_version('apple', 'aplx')}") # False (e不在)

# ## 計數器 (Counters)
#
# `Counter` 像是集合，不同的是如果一個元素出現超過一次，
# `Counter` 會記錄它出現了多少次。
# 如果你熟悉數學上「多重集 (multiset)」的概念，`Counter` 是一種
# 表示多重集的自然方式。
#
# `Counter` 類別定義在一個叫做 `collections` 的模組中，所以你需要匯入它。
# 然後你可以像使用函數一樣使用類別物件，並傳遞一個字串、列表或任何其他種類的序列作為參數。

from collections import Counter # 從 collections 模組匯入 Counter

counter_banana_obj = Counter('banana') # 計算 'banana' 中每個字母的出現次數
print(f"Counter('banana'): {counter_banana_obj}") # Counter({'a': 3, 'n': 2, 'b': 1})

# from collections import Counter # 已匯入
t_tuple_counter = (1, 1, 1, 2, 2, 3)
counter_tuple_obj = Counter(t_tuple_counter) # 計算元組中每個元素的出現次數
print(f"Counter({t_tuple_counter}): {counter_tuple_obj}") # Counter({1: 3, 2: 2, 3: 1})

# `Counter` 物件就像一個字典，它把每個鍵對應到它出現的次數。
# 如同字典，鍵必須是可雜湊的。
#
# 與字典不同的是，如果你存取一個不存在的元素，`Counter` 物件不會引發例外。
# 相反地，它們會回傳 `0`。

print(f"counter_tuple_obj['d'] (d 不存在): {counter_tuple_obj['d']}") # 0
print(f"counter_tuple_obj[4] (4 不存在): {counter_tuple_obj[4]}")   # 0


# 我們可以用 `Counter` 物件來解決第十章的一個練習，
# 該練習要求一個函數接收兩個單字並檢查它們是否為相同字母異序詞 (anagram)
# —— 也就是說，一個字的字母是否可以重新排列成另一個字。
#
# 這裡是用 `Counter` 物件的解答。

def is_anagram_counter(word1_ana_c, word2_ana_c): # 參數改名
    # 如果兩個字的字母計數相同，它們就是相同字母異序詞
    return Counter(word1_ana_c) == Counter(word2_ana_c)

# 如果兩個字是相同字母異序詞，它們包含相同的字母且出現次數也相同，
# 所以它們的 `Counter` 物件是等值的。
print(f"is_anagram_counter('listen', 'silent'): {is_anagram_counter('listen', 'silent')}") # True
print(f"is_anagram_counter('apple', 'apply'): {is_anagram_counter('apple', 'apply')}")   # False

# `Counter` 提供了一個叫做 `most_common` 的方法，它回傳一個 (值, 頻率) 對的列表，
# 按最常見到最不常見的順序排序。

# counter_tuple_obj 是 Counter({1: 3, 2: 2, 3: 1})
most_common_elements = counter_tuple_obj.most_common()
print(f"counter_tuple_obj.most_common(): {most_common_elements}") # [(1, 3), (2, 2), (3, 1)]

# 它們也提供方法和運算子來執行類似集合的操作，
# 包括加法、減法、聯集和交集。
# 例如，`+` 運算子會合併兩個 `Counter` 物件，並建立一個新的 `Counter`，
# 其中包含來自兩者的所有鍵，以及計數的總和。
#
# 我們可以透過建立一個包含 `'bans'` 字母的 `Counter`，
# 並將其與包含 `'banana'` 字母的 `Counter` 相加來測試。
# counter_banana_obj: {'b':1, 'a':3, 'n':2}

counter2_bans = Counter('bans') # {'b':1, 'a':1, 'n':1, 's':1}
sum_of_counters = counter_banana_obj + counter2_bans
# b: 1+1=2, a: 3+1=4, n: 2+1=3, s: 0+1=1
print(f"counter_banana_obj + counter2_bans: {sum_of_counters}")
# Counter({'a': 4, 'n': 3, 'b': 2, 's': 1})

# 你將有機會在本章末尾的練習中探索其他 `Counter` 的操作。

# ## defaultdict (預設字典)
#
# `collections` 模組也提供了 `defaultdict`，它像字典一樣，
# 不同的是如果你存取一個不存在的鍵，它會自動產生一個新的值。
#
# 當你建立一個 `defaultdict` 時，你提供一個用來建立新值的函數。
# 用來建立物件的函數有時被稱為 **工廠 (factory)**。
# 內建的建立列表、集合和其他型別的函數都可以作為工廠使用。
#
# 例如，這裡有一個 `defaultdict`，它在需要時會建立一個新的 `list`。

from collections import defaultdict # 從 collections 匯入 defaultdict

d_default_list = defaultdict(list) # 當鍵不存在時，預設值會是一個新的空列表
print(f"d_default_list (初始): {d_default_list}")

# 注意參數是 `list`，它是一個類別物件，而不是 `list()`，後者是一個建立新列表的函數呼叫。
# 工廠函數只有在我們存取一個不存在的鍵時才會被呼叫。

# 存取一個新鍵 'new key'
# 因為 'new key' 不存在，defaultdict 會呼叫 list() 來建立一個空列表作為預設值
# 並把這個空列表指派給 d_default_list['new key']
# 然後 t_new_list 會得到這個空列表的參照
t_new_list_from_dd = d_default_list['new key']
print(f"存取新鍵後，t_new_list_from_dd: {t_new_list_from_dd}") # []
print(f"存取新鍵後，d_default_list: {d_default_list}") # defaultdict(<class 'list'>, {'new key': []})


# 這個新的列表，我們稱之為 `t_new_list_from_dd`，也被加入了字典中。
# 所以如果我們修改 `t_new_list_from_dd`，這個改變會反映在 `d_default_list` 中：

t_new_list_from_dd.append('new value') # 修改列表
print(f"修改 t_new_list_from_dd 後，d_default_list['new key']: {d_default_list['new key']}") # ['new value']

# 如果你在建立一個列表的字典 (dictionary of lists)，使用 `defaultdict` 通常可以寫出更簡單的程式碼。
#
# 在[第十一章](chapter_tuples)的一個練習中，我建立了一個字典，
# 它把一個排序後的字母字串對應到可以用這些字母拼出的單字列表。
# (譯註：chapter_tuples 指的是書中對應章節的連結)
# 例如，字串 `'opst'` 對應到列表 `['opts', 'post', 'pots', 'spot', 'stop', 'tops']`。
# 這是原始的程式碼。

# 為了讓 all_anagrams_orig 能跑，需要 signature 函數
# 假設 signature(word) 是把 word 的字母排序後組成的字串
def signature_s(word_sig): # 參數改名
    return "".join(sorted(word_sig))

def all_anagrams_orig(filename_ana_orig): # 參數改名
    d_anagrams_orig = {}
    try:
        with open(filename_ana_orig, 'r', encoding='utf-8') as f_ana_orig:
            for line_ana_orig in f_ana_orig:
                word_ana_orig = line_ana_orig.strip().lower()
                if not word_ana_orig: continue # 跳過空行
                t_signature_orig = signature_s(word_ana_orig) # 計算簽名 (排序後的字母)
                if t_signature_orig not in d_anagrams_orig:
                    d_anagrams_orig[t_signature_orig] = [word_ana_orig] # 第一次遇到這個簽名
                else:
                    d_anagrams_orig[t_signature_orig].append(word_ana_orig) # 簽名已存在，附加單字
    except FileNotFoundError:
        print(f"錯誤: 檔案 '{filename_ana_orig}' 未找到。")
    return d_anagrams_orig

# 這是使用 `defaultdict` 的更簡單版本。

def all_anagrams_defaultdict(filename_ana_dd): # 參數改名
    d_anagrams_dd = defaultdict(list) # 如果鍵不存在，預設建立一個空列表
    try:
        with open(filename_ana_dd, 'r', encoding='utf-8') as f_ana_dd:
            for line_ana_dd in f_ana_dd:
                word_ana_dd = line_ana_dd.strip().lower()
                if not word_ana_dd: continue
                t_signature_dd = signature_s(word_ana_dd)
                # 不論 t_signature_dd 是否已存在，d_anagrams_dd[t_signature_dd] 都會回傳一個列表
                # (如果是新的，就是 list() 產生的空列表)
                # 然後就可以直接 .append()
                d_anagrams_dd[t_signature_dd].append(word_ana_dd)
    except FileNotFoundError:
        print(f"錯誤: 檔案 '{filename_ana_dd}' 未找到。")
    return d_anagrams_dd

# 在本章末尾的練習中，你將有機會練習使用 `defaultdict` 物件。

# 另一個 defaultdict 的例子
# d_example_dd_key_tuple = defaultdict(list)
# key_example_tuple = ('into', 'the')
# d_example_dd_key_tuple[key_example_tuple].append('woods')
# print(f"d_example_dd_key_tuple: {d_example_dd_key_tuple}")
# defaultdict(<class 'list'>, {('into', 'the'): ['woods']})

# ## 條件表達式 (Conditional expressions)
#
# 條件陳述式 (if-else) 通常用來選擇兩個值中的一個，像這樣：

import math
x_cond_expr = 5

if x_cond_expr > 0:
    y_cond_expr = math.log(x_cond_expr) # 計算 x 的自然對數
else:
    y_cond_expr = float('nan') # nan (Not a Number) 代表無效的浮點數結果

print(f"y_cond_expr (x={x_cond_expr}): {y_cond_expr}")

# 這個陳述式檢查 `x_cond_expr` 是否為正數。如果是，它計算其對數。
# 如果不是，`math.log` 會引發 ValueError。
# 為了避免程式停止，我們產生一個 `NaN`。
#
# 我們可以用 **條件表達式 (conditional expression)** 更簡潔地寫這個陳述式。
# 語法是： value_if_true if condition else value_if_false

y_cond_expr_v2 = math.log(x_cond_expr) if x_cond_expr > 0 else float('nan')

print(f"y_cond_expr_v2 (x={x_cond_expr}): {y_cond_expr_v2}")

# 你幾乎可以像讀英文一樣讀這一行：「`y_cond_expr_v2` 得到 log-`x_cond_expr` 如果 `x_cond_expr` 大於 0；否則它得到 `NaN`」。
#
# 遞迴函數有時可以用條件表達式簡潔地編寫。
# 例如，這裡是一個使用條件 *陳述式* 的 `factorial` (階乘) 版本。

def factorial_if_else(n_fact): # 參數改名
    if n_fact == 0:
        return 1
    else:
        return n_fact * factorial_if_else(n_fact - 1)

# 這裡是一個使用條件 *表達式* 的版本。

def factorial_cond_expr(n_fact_ce): # 參數改名
    return 1 if n_fact_ce == 0 else n_fact_ce * factorial_cond_expr(n_fact_ce - 1)

# 條件表達式的另一個用途是處理選擇性參數。
# 例如，這裡有一個類別定義，其 `__init__` 方法使用條件 *陳述式*
# 來檢查一個具有預設值的參數。
# (這是修正 Kangaroo 類別預設可變參數問題的常用方法)

class Kangaroo_v1: # 版本1，用 if-else
    def __init__(self, name_k_v1, contents_k_v1=None): # 預設值設為 None
        self.name = name_k_v1
        if contents_k_v1 is None: # 如果呼叫時沒提供 contents_k_v1 (或明確傳 None)
            contents_k_v1 = []    # 就建立一個新的空列表
        self.contents = contents_k_v1 # contents 指向新的空列表或傳入的列表

# 這裡是用條件 *表達式* 的版本。

# 這應該在類別定義內部
# class Kangaroo_v2:
#     def __init__(self, name_k_v2, contents_k_v2=None):
#         self.name = name_k_v2
#         self.contents = [] if contents_k_v2 is None else contents_k_v2

# 一般來說，如果兩個分支都只包含單一表達式且沒有其他陳述式，
# 你就可以用條件表達式取代條件陳述式。

# ## 列表推導式 (List comprehensions)
#
# 在之前的章節中，我們看過一些例子，從一個空列表開始，
# 然後使用 `append` 方法一次加入一個元素。
# 例如，假設我們有一個包含電影標題的字串，我們想把所有單字的首字母大寫。

title_movie = 'monty python and the holy grail' # 蒙提派森與聖杯

# 我們可以把它分割成一個字串列表，遍歷這些字串，將它們首字母大寫，然後附加到一個列表中。

t_capitalized_words = []
for word_title in title_movie.split():
    t_capitalized_words.append(word_title.capitalize()) # capitalize() 使首字母大寫，其餘小寫

joined_capitalized_title = ' '.join(t_capitalized_words)
print(f"首字母大寫後的標題: {joined_capitalized_title}")

# 我們可以用 **列表推導式 (list comprehension)** 更簡潔地做同樣的事情：
# 語法： [expression for item in iterable]

t_capitalized_comprehension = [word_c.capitalize() for word_c in title_movie.split()]
joined_capitalized_comprehension = ' '.join(t_capitalized_comprehension)
print(f"使用列表推導式得到的大寫標題: {joined_capitalized_comprehension}")

# 方括號表示我們正在建構一個新的列表。
# 括號內的表達式指定了列表的元素，而 `for` 子句指示了我們正在遍歷哪個序列。
#
# 列表推導式的語法可能看起來有點奇怪，因為迴圈變數 ——
# 在這個例子中是 `word_c` —— 出現在表達式中，卻在其定義之前。
# 但你會習慣的。
#
# 作為另一個例子，在[第九章](section_word_list)中，我們用這個迴圈從檔案讀取單字並將它們附加到列表中。
# (譯註：section_word_list 指的是書中對應章節的連結)

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython2/master/code/words.txt');

word_list_loop = []
if exists('words.txt'):
    for line_wl_loop in open('words.txt', encoding='utf-8'):
        word_wl_loop = line_wl_loop.strip() # 移除頭尾空白 (包括換行符)
        if word_wl_loop: # 確保不是空行
            word_list_loop.append(word_wl_loop)
else:
    print("錯誤: words.txt 未找到。")

print(f"使用迴圈建立的 word_list_loop 長度: {len(word_list_loop)}")

# 這是我們如何把它寫成列表推導式。

word_list_comprehension = []
if exists('words.txt'):
    # [line.strip() for line in open('words.txt') if line.strip()] # 也可以加入 if 來過濾空行
    word_list_comprehension = [line_comp.strip() for line_comp in open('words.txt', encoding='utf-8')]
    # 上面的版本可能會包含因 strip() 後變成的空字串 (如果原檔案有空行)
    # 更安全的版本：
    # word_list_comprehension = [word for line in open('words.txt') if (word := line.strip())] # Python 3.8+ 海象運算子
    # 或者兩步：
    # lines = [line.strip() for line in open('words.txt')]
    # word_list_comprehension = [word for word in lines if word]
else:
    print("錯誤: words.txt 未找到。")


print(f"使用列表推導式建立的 word_list_comprehension 長度: {len(word_list_comprehension)}")
# 為了與迴圈版本一致 (排除空字串)，可以這樣寫：
if exists('words.txt'):
    word_list_comp_filtered = [
        word.strip() for word in open('words.txt', encoding='utf-8') if word.strip()
    ]
    print(f"過濾空行後的列表推導式 word_list_comp_filtered 長度: {len(word_list_comp_filtered)}")


# 列表推導式也可以有一個 `if` 子句，用來決定哪些元素會被包含在列表中。
# 例如，這裡有一個我們在[第十章](section_palindrome_list)中用來建立
# `word_list_comprehension` (或 `word_list_loop`) 中所有回文單字列表的 `for` 迴圈。
# (譯註：section_palindrome_list 指的是書中對應章節的連結)

def is_palindrome(word_pal): # 參數改名
    # 簡單的回文檢查 (忽略大小寫和非字母可能更好，但這裡照書中)
    return word_pal == word_pal[::-1] # 用切片反轉字串

palindromes_loop = []
# 使用之前建立的 word_list_loop 或 word_list_comp_filtered
# 假設 word_list_comp_filtered 是我們想要的
if 'word_list_comp_filtered' in globals() and word_list_comp_filtered:
    source_list_for_pal = word_list_comp_filtered
elif 'word_list_loop' in globals() and word_list_loop:
    source_list_for_pal = word_list_loop
else:
    source_list_for_pal = []
    print("警告: 沒有可用的單字列表來尋找回文。")


for word_pal_loop in source_list_for_pal:
    if is_palindrome(word_pal_loop):
        palindromes_loop.append(word_pal_loop)

print(f"使用迴圈找到的回文 (前10個): {palindromes_loop[:10]}")

# 這是我們如何用列表推導式做同樣的事情。
# [expression for item in iterable if condition]

palindromes_comprehension = [
    word_pal_comp for word_pal_comp in source_list_for_pal if is_palindrome(word_pal_comp)
]

print(f"使用列表推導式找到的回文 (前10個): {palindromes_comprehension[:10]}")

# 當列表推導式作為函數的參數時，我們通常可以省略方括號。
# 例如，假設我們想把 $1 / 2^n$ (n 從 0 到 9) 的值加總起來。
# 我們可以像這樣使用列表推導式。

sum_list_comp = sum([1/2**n_lc for n_lc in range(10)]) # 建立一個列表然後加總
print(f"sum([1/2**n for n in range(10)]): {sum_list_comp}")

# 或者我們可以像這樣省略方括號。

sum_gen_expr = sum(1/2**n_ge for n_ge in range(10)) # 這裡是一個生成器表達式
print(f"sum(1/2**n for n in range(10)): {sum_gen_expr}")

# 在這個例子中，參數嚴格來說是一個 **生成器表達式 (generator expression)**，
# 而不是列表推導式，它實際上並不會建立一個列表。
# 但除此之外，行為是相同的。(生成器會逐個產生值，更節省記憶體)
#
# 列表推導式和生成器表達式很簡潔且易讀，至少對於簡單的表達式是這樣。
# 而且它們通常比等效的 for 迴圈更快，有時快很多。
# 所以如果你因為我之前沒提到它們而生我的氣，我能理解。
#
# 但是，為我辯護一下，列表推導式比較難除錯，因為你不能在迴圈裡面放 print 陳述式。
# 我建議只有在計算足夠簡單，你很有可能一次就寫對的情況下才使用它們。
# 或者考慮先寫並除錯一個 `for` 迴圈，然後再把它轉換成列表推導式。

# ## `any` 和 `all`
#
# Python 提供了一個內建函數 `any`，它接收一個布林值序列並回傳 `True`
# 如果序列中有任何一個值是 `True`。

print(f"any([False, False, True]): {any([False, False, True])}") # True
print(f"any([False, False, False]): {any([False, False, False])}") # False

# `any` 經常與生成器表達式一起使用。

# 檢查 'monty' 中是否有字母 't'
has_t_in_monty = any(letter_char == 't' for letter_char in 'monty')
print(f"any(letter == 't' for letter in 'monty'): {has_t_in_monty}") # True

# 這個例子不太有用，因為它做的事情和 `in` 運算子一樣。
# ('t' in 'monty')
# 但是我們可以用 `any` 來為[第七章](chapter_search)的一些練習編寫簡潔的解答。
# (譯註：chapter_search 指的是書中對應章節的連結)
# 例如，我們可以像這樣寫 `uses_none` (檢查單字是否完全不使用禁用字母)。

def uses_none_any(word_un, forbidden_un): # 參數改名
    """檢查單字是否完全不使用禁用字母。"""
    # 如果 word_un 中的任何一個字母出現在 forbidden_un 中，
    # 那麼 (letter in forbidden_un for letter in word_un) 就會有 True，any() 就是 True。
    # 所以，如果 any() 是 True，表示「有用到了禁用字母」，所以 uses_none 應該是 False。
    # 因此需要用 not any(...)
    return not any(letter_un in forbidden_un.lower() for letter_un in word_un.lower())


print(f"uses_none_any('banana', 'xyz'): {uses_none_any('banana', 'xyz')}") # True

print(f"uses_none_any('apple', 'efg'): {uses_none_any('apple', 'efg')}") # False (因為 e 在 apple 也在 efg)

# 這個函數遍歷 `word_un` 中的字母，並檢查是否有任何字母在 `forbidden_un` 中。
# 使用 `any` 搭配生成器表達式效率很高，因為如果它找到一個 `True` 值，
# 它會立刻停止，所以不需要遍歷整個序列。
#
# Python 提供了另一個內建函數 `all`，如果序列中的每個元素都是 `True`，它就回傳 `True`。
# 我們可以用它來寫一個簡潔版本的 `uses_all` (檢查單字是否使用了所有必要字母)。

def uses_all_all(word_ua, required_ua): # 參數改名
    """檢查單字是否使用了所有必要字母。"""
    # 對於 required_ua 中的每個字母，檢查它是否在 word_ua 中。
    # 如果所有必要字母都在 word_ua 中，all() 就會回傳 True。
    return all(letter_req in word_ua.lower() for letter_req in required_ua.lower())

print(f"uses_all_all('banana', 'ban'): {uses_all_all('banana', 'ban')}") # True

print(f"uses_all_all('apple', 'api'): {uses_all_all('apple', 'api')}") # False (i 不在 apple)
print(f"uses_all_all('apple', 'aple'): {uses_all_all('apple', 'aple')}") # True

# 使用 `any` 和 `all` 的表達式可以很簡潔、有效率且易讀。

# ## 具名元組 (Named tuples)
#
# `collections` 模組提供了一個叫做 `namedtuple` 的函數，可以用來建立簡單的類別。
# 例如，[第十六章](section_create_point)中的 `Point` 物件只有兩個屬性 `x` 和 `y`。
# (譯註：section_create_point 指的是書中對應章節的連結)
# 這是我們定義它的方式。

class Point_v0_nt: # 版本0，傳統類別定義
    """表示一個二維空間中的點。"""
    def __init__(self, x_nt0, y_nt0): # 參數改名
        self.x = x_nt0
        self.y = y_nt0
    def __str__(self):
        return f'({self.x}, {self.y})' # 書中用 (x, y) 格式

# 這麼多程式碼只為了傳達少量資訊。
# `namedtuple` 提供了一種更簡潔的方式來定義像這樣的類別。

from collections import namedtuple # 從 collections 匯入 namedtuple

# 使用 namedtuple 建立一個 Point 類別
# 第一個參數是類別名稱 ('Point')
# 第二個參數是屬性名稱的列表 (或用空格/逗號分隔的字串)
Point_NT = namedtuple('Point_NT_Class', ['x', 'y']) # 類別名稱設為 Point_NT_Class 以區分
                                                 # 通常類別名就是 'Point'

# 第一個參數是你想要建立的類別的名稱。
# 第二個參數是 `Point_NT` 物件應該具有的屬性列表。
# 結果是一個類別物件，這就是為什麼它被指派給一個大寫開頭的變數名稱。
#
# 用 `namedtuple` 建立的類別提供了一個 `__init__` 方法，
# 它會將值指派給屬性，還有一個 `__str__` 方法，用易讀的形式顯示物件。
# 所以我們可以像這樣建立和顯示一個 `Point_NT` 物件。

p_namedtuple = Point_NT(1, 2) # 像普通類別一樣實體化
print(f"具名元組 p_namedtuple: {p_namedtuple}") # __str__ 預設格式類似 Point_NT_Class(x=1, y=2)

# `Point_NT` 也提供了一個 `__eq__` 方法，檢查兩個 `Point_NT` 物件是否等值
# —— 也就是說，它們的屬性是否相同。

print(f"p_namedtuple == Point_NT(1, 2): {p_namedtuple == Point_NT(1, 2)}") # True
print(f"p_namedtuple == Point_NT(1, 3): {p_namedtuple == Point_NT(1, 3)}") # False

# 你可以用名稱或索引來存取具名元組的元素。

print(f"p_namedtuple.x: {p_namedtuple.x}, p_namedtuple.y: {p_namedtuple.y}")

print(f"p_namedtuple[0]: {p_namedtuple[0]}, p_namedtuple[1]: {p_namedtuple[1]}") # 像元組一樣用索引

# 你也可以把具名元組當作普通元組來處理，例如在這個賦值中。

x_nt_unpack, y_nt_unpack = p_namedtuple # 解包到變數
print(f"解包後: x_nt_unpack={x_nt_unpack}, y_nt_unpack={y_nt_unpack}")

# 但是 `namedtuple` 物件是不可變的。
# 屬性初始化後就不能更改了。

%%expect TypeError # 因為具名元組繼承自元組，元組是不可變的
# p_namedtuple[0] = 3 # TypeError: 'Point_NT_Class' object does not support item assignment

%%expect AttributeError # 屬性也不能直接賦值修改
# p_namedtuple.x = 3 # AttributeError: can't set attribute

# `namedtuple` 提供了一種快速定義簡單類別的方法。
# 缺點是簡單的類別不一定總是保持簡單。
# 你稍後可能會決定想為具名元組新增方法。
# 在那種情況下，你可以定義一個繼承自具名元組的新類別。

class Pointier_NT(Point_NT): # Pointier_NT 繼承自用 namedtuple 建立的 Point_NT
    """這個類別繼承自 Point_NT。可以新增額外方法。"""
    def distance_from_origin(self):
        return math.sqrt(self.x**2 + self.y**2)

# 或者到那時你可以換回傳統的類別定義。
pointy_nt = Pointier_NT(3,4)
print(f"Pointier_NT 物件: {pointy_nt}")
print(f"  離原點距離: {pointy_nt.distance_from_origin()}")


# ## 打包關鍵字引數 (Packing keyword arguments)
#
# 在[第十一章](section_argument_pack)中，我們寫了一個把其引數打包到一個元組中的函數。
# (譯註：section_argument_pack 指的是書中對應章節的連結)

def mean_args_only(*args_mean): # *args_mean 會收集所有位置引數
    if not args_mean: return 0.0
    return sum(args_mean) / len(args_mean)

# 你可以用任意數量的位置引數呼叫這個函數。

print(f"mean_args_only(1, 2, 3): {mean_args_only(1, 2, 3)}")

# 但是 `*` 運算子不會打包關鍵字引數。
# 所以用關鍵字引數呼叫這個函數會導致錯誤。

%%expect TypeError
# mean_args_only(1, 2, start=3) # TypeError: mean_args_only() got an unexpected keyword argument 'start'

# 要打包關鍵字引數，我們可以用 `**` 運算子：
# (`**kwargs` 會把所有未被其他參數捕獲的關鍵字引數收集到一個字典中)

def mean_with_kwargs(*args_kw, **kwargs_kw): # 參數改名
    print(f"kwargs_kw 字典: {kwargs_kw}") # kwargs_kw 會是一個字典
    if not args_kw: return 0.0
    return sum(args_kw) / len(args_kw)

# 關鍵字打包參數可以有任何名稱，但 `kwargs` (keyword arguments 的縮寫) 是慣用法。
# 結果是一個從關鍵字對應到值的字典。

print(f"mean_with_kwargs(1, 2, start=3): {mean_with_kwargs(1, 2, start=3)}")
# 輸出會先印出 kwargs_kw 字典: {'start': 3}
# 然後回傳 (1+2)/2 = 1.5 (因為 start=3 被 kwargs_kw 接收，沒有傳給 sum)

# 在這個例子中，`kwargs_kw` 的值被印出來了，但除此之外它沒有其他作用。
#
# 但是 `**` 運算子也可以在引數列表中用來解包一個字典。
# 例如，這裡有一個 `mean` 的版本，它打包它收到的任何關鍵字引數，
# 然後再把它們解包作為關鍵字引數傳遞給 `sum` 函數。
# (`sum` 函數可以接受一個 `start` 關鍵字參數)

def mean_unpack_kwargs(*args_ukw, **kwargs_ukw): # 參數改名
    if not args_ukw:
        # 如果沒有位置引數，但有 start，則結果是 start
        return kwargs_ukw.get('start', 0.0)
    # 把 kwargs_ukw 解包傳給 sum
    # sum(iterable, /, start=0) -> number
    return sum(args_ukw, **kwargs_ukw) / len(args_ukw)
    # 如果 kwargs_ukw 是 {'start': 3}，那麼 sum(args_ukw, **kwargs_ukw)
    # 就等同於 sum(args_ukw, start=3)

# 現在如果我們用 `start` 作為關鍵字引數呼叫 `mean_unpack_kwargs`，它會被傳遞給 `sum`，
# `sum` 會用它作為加總的起始點。
# 在下面的例子中，`start=3` 會在計算平均值之前把 `3` 加到總和中，
# 所以總和是 `1+2+3 = 6`，結果是 `6 / 2 = 3.0` (因為有兩個位置引數)。
# (等等，sum(iterable, start) 是 start + sum(iterable)，然後再除以 len(iterable))
# 所以是 ( (1+2) + 3 ) / 2 = (3+3)/2 = 6/2 = 3.0。

print(f"mean_unpack_kwargs(1, 2, start=3): {mean_unpack_kwargs(1, 2, start=3)}")

# 作為另一個例子，如果我們有一個包含鍵 `x` 和 `y` 的字典，
# 我們可以用解包運算子來建立一個 `Point_NT` 物件。
# Point_NT = namedtuple('Point_NT_Class', ['x', 'y'])

d_for_point_unpack = dict(x=1, y=2)
point_from_unpack = Point_NT(**d_for_point_unpack) # 等同於 Point_NT(x=1, y=2)
print(f"從解包字典建立的 Point_NT: {point_from_unpack}")

# 如果沒有解包運算子，`d_for_point_unpack` 會被視為單一的位置引數，
# 所以它會被指派給 `x`，然後我們會得到一個 `TypeError`，因為沒有第二個引數可以指派給 `y`。

%%expect TypeError
# d_for_point_error = dict(x=1, y=2)
# Point_NT(d_for_point_error) # TypeError: Point_NT_Class.__new__() missing 1 required positional argument: 'y'

# 當你處理具有大量關鍵字引數的函數時，
# 建立並傳遞指定常用選項的字典通常很有用。

def pack_and_print_kwargs(**kwargs_pap): # 參數改名
    print(f"打包的關鍵字引數: {kwargs_pap}")

pack_and_print_kwargs(a=1, b=2) # kwargs_pap 會是 {'a': 1, 'b': 2}

# ## 除錯 (Debugging)
#
# 在之前的章節中，我們用 `doctest` 來測試函數。
# 例如，這裡有一個叫做 `add` 的函數，它接收兩個數字並回傳它們的和。
# 它包含一個 doctest 來檢查 `2 + 2` 是否為 `4`。

def add_ddt(a_ddt, b_ddt): # 參數改名
    '''將兩個數字相加。

    >>> add_ddt(2, 2)
    4
    '''
    return a_ddt + b_ddt

# 這個函數接收一個函數物件並執行其 doctests。

from doctest import run_docstring_examples

def run_doctests_ddt(func_ddt): # 參數改名
    print(f"--- 執行 {func_ddt.__name__} 的 doctests ---")
    run_docstring_examples(func_ddt, globals(), name=func_ddt.__name__)

# 所以我們可以像這樣測試 `add_ddt`。

run_doctests_ddt(add_ddt) # 沒有輸出表示通過

# 沒有輸出，表示所有測試都通過了。
#
# Python 提供了另一個執行自動化測試的工具，叫做 `unittest`。
# 它使用起來稍微複雜一些，但這裡有一個例子。

from unittest import TestCase # 從 unittest 模組匯入 TestCase 類別

class TestExample(TestCase): # 定義一個測試類別，繼承自 TestCase

    def test_add(self): # 測試方法的名稱必須以 test_ 開頭
        result_test_add = add_ddt(2, 2)
        self.assertEqual(result_test_add, 4) # assertEqual 檢查兩個值是否相等

# 首先我們匯入 `TestCase`，它是 `unittest` 模組中的一個類別。
# 要使用它，我們必須定義一個繼承自 `TestCase` 的新類別，並提供至少一個測試方法。
# 測試方法的名稱必須以 `test` 開頭，並且應該指明它測試哪個函數。
#
# 在這個例子中，`test_add` 透過呼叫 `add_ddt`、儲存結果，並調用 `assertEqual`
# (從 `TestCase` 繼承而來) 來測試 `add_ddt` 函數。
# `assertEqual` 接收兩個參數並檢查它們是否相等。
#
# 為了執行這個測試方法，我們必須執行 `unittest` 中一個叫做 `main` 的函數，
# 並提供幾個關鍵字引數。
# 下面的函數展示了細節 —— 如果你好奇，可以請虛擬助理解釋它是如何運作的。

import unittest

def run_unittest_custom(): # 函數改名
    # unittest.main() 通常用於從命令列執行測試。
    # 在 notebook 或腳本中執行時，需要一些調整。
    # argv=[''] 模擬沒有命令列參數。
    # exit=False 防止 unittest.main 試圖結束程式 (這在 notebook 中會有問題)。
    # verbosity=0 設置為靜默模式 (只顯示錯誤和摘要)
    # verbosity=1 預設模式
    # verbosity=2 更詳細的輸出
    print("--- 執行 unittest ---")
    # 為了能在 notebook 中執行並看到結果，我們通常會用 TextTestRunner
    # 但書中用 unittest.main，我們照做並處理其輸出
    # 由於 %%add_method_to TestExample 後 TestExample 類別被修改，
    # unittest.main() 會自動發現並執行其中的 test_* 方法。
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # 從 TestExample 類別中載入測試
    suite.addTests(loader.loadTestsFromTestCase(TestExample))
    # 建立一個 runner
    runner = unittest.TextTestRunner(verbosity=1) # verbosity=1 可以看到點
    result_unittest = runner.run(suite)
    print(f"Unittest 執行結果: Ran {result_unittest.testsRun} tests. "
          f"Errors: {len(result_unittest.errors)}. "
          f"Failures: {len(result_unittest.failures)}.")


# `run_unittest_custom` 不接收 `TestExample` 作為參數 —— 相反地，
# 它 (或 unittest.main 的機制) 會搜尋繼承自 `TestCase` 的類別。
# 然後它會搜尋以 `test` 開頭的方法並執行它們。
# 這個過程稱為 **測試發現 (test discovery)**。
#
# 這是我們呼叫 `run_unittest_custom` 時發生的情況。

run_unittest_custom() # 應該會找到並執行 TestExample.test_add

# `unittest.main` (或我們的 runner) 會報告它執行的測試數量和結果。
# 在這個例子中，`OK` (或沒有錯誤/失敗) 表示測試通過了。
#
# 為了看看測試失敗時會發生什麼，我們在 `TestExample` 中加入一個不正確的測試方法。

# %%add_method_to TestExample
# 再次定義 TestExample 以加入錯誤的測試
class TestExample(TestCase):
    def test_add(self):
        result = add_ddt(2, 2)
        self.assertEqual(result, 4) # 正確的測試

    def test_add_broken(self): # 新增一個會失敗的測試
        result = add_ddt(2, 2) # 2+2 = 4
        self.assertEqual(result, 100) # 但我們期望是 100 (這會失敗)

# 這是我們執行測試時發生的情況。

run_unittest_custom() # 現在會執行兩個測試，其中一個會失敗

# 報告會包含失敗的測試方法以及顯示錯誤位置的錯誤訊息。
# 摘要會指出執行了兩個測試，其中一個失敗了。
#
# 在下面的練習中，我會建議一些你可以用來向虛擬助理詢問更多關於 `unittest` 資訊的提示。

# ## 詞彙表 (Glossary)
#
# **工廠 (factory):**
#  一個用來建立物件的函數，通常作為參數傳遞給另一個函數。
#
# **條件表達式 (conditional expression):**
#  一種使用條件來選擇兩個值之一的表達式。
#
# **列表推導式 (list comprehension):**
#  一種遍歷序列並建立列表的簡潔方式。
#
# **生成器表達式 (generator expression):**
#  與列表推導式類似，只是它不建立列表 (而是逐個產生值)。
#
# **測試發現 (test discovery):**
#  一個用來尋找並執行測試的過程。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 本章中有幾個主題你可能想進一步了解。
#
# * 「Python 的 set (集合) 類別有哪些方法和運算子？」
#
# * 「Python 的 Counter (計數器) 類別有哪些方法和運算子？」
#
# * 「Python 的列表推導式和生成器表達式有什麼區別？」
#
# * 「什麼時候應該用 Python 的 `namedtuple` 而不是定義一個新的類別？」
#
# * 「打包和解包關鍵字引數有哪些用途？」
#
# * 「`unittest` 是如何進行測試發現的？」
#
# * 「除了 `assertEqual` 之外，`unittest.TestCase` 中最常用的方法有哪些？」
#
# * 「`doctest` 和 `unittest` 各有哪些優缺點？」
#
# 對於下面的練習，可以考慮請虛擬助理幫忙，但一如往常，記得測試結果。

# ### 練習
#
# 第七章的一個練習要求一個叫做 `uses_none` 的函數，它接收一個單字和一個禁用字母的字串，
# 如果單字沒有使用任何禁用字母，則回傳 `True`。這是一個解答。

def uses_none_loop_v2(word_un_v2, forbidden_un_v2): # 參數改名
    for letter_un_v2 in word_un_v2.lower(): # 轉小寫以忽略大小寫
        if letter_un_v2 in forbidden_un_v2.lower():
            return False
    return True

# 編寫一個使用集合運算而不是 `for` 迴圈的這個函數的版本。
# 提示：問問虛擬助理：「如何計算 Python 集合的交集 (intersection)？」
# (交集可以用 & 運算子，或 intersection() 方法)

# 你可以用這個大綱開始。

def uses_none_set_starter(word, forbidden): # 書中原始名稱
    """檢查單字是否完全不使用禁用字母。

    >>> uses_none_set_starter('banana', 'xyz')
    True
    >>> uses_none_set_starter('apple', 'efg') # e is in both
    False
    >>> uses_none_set_starter('', 'abc') # 空字串不包含任何字母
    True
    """
    return False # 預留位置

# 解答

def uses_none_set(word_un_set, forbidden_un_set): # 參數改名
    """檢查單字是否完全不使用禁用字母 (使用集合)。

    >>> uses_none_set('banana', 'xyz')
    True
    >>> uses_none_set('apple', 'efg')
    False
    >>> uses_none_set('', 'abc')
    True
    >>> uses_none_set('ZEBRA', 'a') # 測試大小寫
    False
    """
    word_char_set = set(word_un_set.lower()) # 單字中的字母集合 (小寫)
    forbidden_char_set = set(forbidden_un_set.lower()) # 禁用字母集合 (小寫)

    # 如果兩個集合的交集是空的，表示單字中沒有任何禁用字母
    # word_char_set.isdisjoint(forbidden_char_set) 也可以
    return len(word_char_set.intersection(forbidden_char_set)) == 0
    # 或者 return not (word_char_set & forbidden_char_set)

# from doctest import run_docstring_examples # 已匯入
# def run_doctests(func): # 已定義

print(f"\n--- 測試 uses_none_set ---")
run_doctests_ddt(uses_none_set) # 使用之前為 ddt 命名的 run_doctests_ddt

# ### 練習
#
# Scrabble (拼字遊戲) 是一種棋盤遊戲，目標是使用字母牌來拼出單字。
# 例如，如果我們有字母牌 `T`、`A`、`B`、`L`、`E`，
# 我們可以用這些牌的一部分來拼出 `BELT` 和 `LATE` ——
# 但我們拼不出 `BEET`，因為我們沒有兩個 `E`。
#
# 編寫一個函數，它接收一串字母牌和一個單字，
# 並檢查這些字母牌是否能拼出該單字，要考慮每個字母出現的次數。
# (提示：使用 Counter)

# 你可以用下面的大綱開始。

def can_spell_starter(available_letters_cs, target_word_cs): # 參數改名
    """檢查 available_letters_cs 是否能拼出 target_word_cs。

    >>> can_spell_starter('table', 'belt') # t,a,b,l,e 可以拼出 b,e,l,t
    True
    >>> can_spell_starter('table', 'late') # t,a,b,l,e 可以拼出 l,a,t,e
    True
    >>> can_spell_starter('table', 'beet') # t,a,b,l,e 沒有兩個 e
    False
    >>> can_spell_starter('banana', 'bandana') # banana 少一個 d, 多一個 n
    False
    >>> can_spell_starter('applepie', 'apple')
    True
    """
    return False # 預留位置

# 解答
# from collections import Counter # 已在前面匯入過

def can_spell_counter(available_letters_csc, target_word_csc): # 參數改名
    """檢查 available_letters_csc 是否能拼出 target_word_csc (使用 Counter)。

    >>> can_spell_counter('table', 'belt')
    True
    >>> can_spell_counter('table', 'late')
    True
    >>> can_spell_counter('table', 'beet')
    False
    >>> can_spell_counter('banana', 'bandana')
    False
    >>> can_spell_counter('applepie', 'apple')
    True
    >>> can_spell_counter('aabbc', 'abac') # 測試重複字母
    True
    """
    # Counter(target_word_csc) <= Counter(available_letters_csc)
    # 這個比較的意思是：對於 target_word_csc 中的每個字母，
    # 它在 available_letters_csc 中的計數必須大於或等於它在 target_word_csc 中的計數。
    # 這正是我們需要的「是否能拼出」。
    # Counter 的比較 (<=, >=, <, >) 是逐個元素比較的。
    # A <= B if for all x in A, A[x] <= B[x].
    
    # Counter 減法： c1 - c2 只保留 c1 中計數大於 c2 的元素。
    # 如果 (Counter(word) - Counter(letters)) 是空的 (或者所有元素的計數都 <= 0)，
    # 則表示 letters 可以拼出 word。

    counter_word = Counter(target_word_csc.lower())
    counter_letters = Counter(available_letters_csc.lower())

    # 檢查 target_word 中的每個字母，其數量是否不超過 available_letters 中的數量
    for char_cs, count_cs_needed in counter_word.items():
        if counter_letters[char_cs] < count_cs_needed: # available_letters 中該字母不夠用
            return False
    return True
    # 書中解答更簡潔： return Counter(word) <= Counter(letters)
    # 但這依賴於 Counter 的特定比較行為，如果 Counter A 比 Counter B 多了 B 沒有的鍵，
    # 則 A <= B 可能是 False。
    # 例如 Counter('aab') <= Counter('aa') 是 False。
    # 我們要的是 word 的每個字母，letters 裡都要夠。
    # 所以上面的 for 迴圈邏輯是正確的。


print(f"\n--- 測試 can_spell_counter ---")
run_doctests_ddt(can_spell_counter)

# ### 練習
#
# 在[第十七章](chapter_inheritance)的一個練習中，我對 `has_straightflush` 的解答
# 使用了下面的方法，它把一手 `PokerHand` 按花色分割成四手牌的列表，
# 每手牌只包含相同花色的牌。
# (譯註：chapter_inheritance 指的是書中對應章節的連結)

# 這應該是 PokerHand 的一個方法
# class PokerHand_For_Partition_Orig(Hand): # 假設 PokerHand 已定義
#     def partition_original(self): # 方法改名以區分
#         """將手牌按花色分成四手牌 (PokerHand 物件) 的列表。"""
#         hands_by_suit_po = []
#         for i_suit_po in range(4): # 0 到 3 代表四種花色
#             # 每次都建立新的 PokerHand 實體
#             hands_by_suit_po.append(PokerHand_For_Partition_Orig(label=f'Suit {Card.suit_names[i_suit_po]}'))
#
#         for card_po in self.cards:
#             # add_card 是從 Deck/Hand 繼承來的
#             hands_by_suit_po[card_po.suit].add_card(card_po)
#
#         return hands_by_suit_po

# 用 `defaultdict` 編寫這個函數的簡化版本。
# (目標是改寫 PokerHand 的 partition 方法)

# 這裡是大綱，PokerHand 類別和你要修改的 partition_dd 方法。
# (為了能在這裡執行，我們需要 Card, Deck, Hand 的定義，已在檔案開頭提供)

class PokerHand_For_Partition_DD(Hand): # 新類別名以測試
    """表示一手撲克牌 (用於 defaultdict partition 練習)。"""
    def __init__(self, label=''): # 確保 __init__ 與 Hand 一致或自訂
        super().__init__(label) # 呼叫父類別 Hand 的 __init__

    def add_card(self, card): # 確保 PokerHand 有 add_card (從 Deck/Hand 繼承)
        super().add_card(card)

    def partition_with_defaultdict(self): # 方法改名
        """使用 defaultdict 將手牌按花色分割。
        回傳一個 (花色代碼 -> PokerHand 物件) 的 defaultdict。
        """
        # 預設工廠是 PokerHand，這樣當我們存取一個新的花色代碼時，
        # 會自動為該花色建立一個新的 PokerHand 物件。
        # PokerHand() 會呼叫 PokerHand 的 __init__。
        # 如果 PokerHand 的 __init__ 需要 label，這裡的 lambda 可能需要調整。
        # 假設 PokerHand('') 是有效的。
        d_partition_dd = defaultdict(PokerHand_For_Partition_DD) # lambda: PokerHand_For_Partition_DD()

        for card_pdd in self.cards:
            # d_partition_dd[card_pdd.suit] 會：
            # 1. 如果 card_pdd.suit (花色代碼) 還不是鍵，就呼叫 PokerHand() 建立一個新手牌
            #    並將其設為該鍵的值。
            # 2. 回傳該鍵對應的 PokerHand 物件。
            # 然後我們就可以對這個 PokerHand 物件呼叫 add_card。
            d_partition_dd[card_pdd.suit].add_card(card_pdd)
            # 如果 PokerHand 的 __init__ 需要 label，可以這樣：
            # if card_pdd.suit not in d_partition_dd:
            #     d_partition_dd[card_pdd.suit] = PokerHand_For_Partition_DD(label=f'Suit {Card.suit_names[card_pdd.suit]}')
            # d_partition_dd[card_pdd.suit].add_card(card_pdd)
            # 但 defaultdict 的優點就是避免這個 if not in。
            # 如果 PokerHand('') 可行，那麼 defaultdict(PokerHand) 就行。
            # 如果 PokerHand 的 __init__ 有 label='' 預設值，那麼 PokerHand() 是可以的。
            # 我們在上面定義 PokerHand_For_Partition_DD 時，__init__ 確實有 label=''

        return d_partition_dd

# (上面是書中解答的翻譯，實際上 partition 方法應該在 PokerHand 類別內部)

# 為了測試你的程式碼，我們先建立一副牌並洗牌。
print(f"\n--- PokerHand partition (defaultdict) 測試 ---")
cards_deck_ph_test = Deck.make_cards()
deck_ph_test = Deck(cards_deck_ph_test)
deck_ph_test.shuffle()

# 然後建立一個 `PokerHand_For_Partition_DD` 並加入七張牌。

random_hand_ph_test = PokerHand_For_Partition_DD('隨機手牌') # 使用新類別

if hasattr(deck_ph_test, 'move_cards'): # 確保 Deck 有 move_cards
    deck_ph_test.move_cards(random_hand_ph_test, 7) # 發7張牌
else: # 手動發牌
    for _ in range(7):
        c = deck_ph_test.pop_card()
        if c: random_hand_ph_test.add_card(c)

print("隨機產生的7張手牌:")
print(random_hand_ph_test)


# 如果你調用 `partition_with_defaultdict` 並印出結果，
# 每手牌應該只包含一種花色的牌。

hand_dict_partitioned = random_hand_ph_test.partition_with_defaultdict()
print("\n按花色分割後的手牌 (使用 defaultdict):")
if hand_dict_partitioned:
    for suit_code_hdp, hand_obj_hdp in sorted(hand_dict_partitioned.items()): # 按花色代碼排序印出
        print(f"--- 花色: {Card.suit_names[suit_code_hdp]} ---")
        print(hand_obj_hdp)
        print()
else:
    print("分割結果為空。")


# ### 練習
#
# 這是第十一章計算費氏數列的函數。

def fibonacci_orig(n_fib_orig): # 參數改名
    if n_fib_orig == 0:
        return 0
    if n_fib_orig == 1:
        return 1
    return fibonacci_orig(n_fib_orig - 1) + fibonacci_orig(n_fib_orig - 2)

# 用一個包含兩個條件表達式 (一個巢狀在另一個裡面) 的單一 return 陳述式改寫這個函數。

# 解答

def fibonacci_cond_expr_nested(n_fib_cen): # 參數改名
    # value_if_true if condition else value_if_false
    return 0 if n_fib_cen == 0 else \
           (1 if n_fib_cen == 1 else \
            fibonacci_cond_expr_nested(n_fib_cen - 1) + fibonacci_cond_expr_nested(n_fib_cen - 2))

print(f"\n--- 費氏數列 (巢狀條件表達式) ---")
print(f"fibonacci_cond_expr_nested(10): {fibonacci_cond_expr_nested(10)}")    # 55

print(f"fibonacci_cond_expr_nested(20): {fibonacci_cond_expr_nested(20)}")    # 6765

# ### 練習
# 下面是一個遞迴計算二項式係數 (binomial coefficient) 的函數。
# (二項式係數 C(n,k) 或 "n 取 k"，表示從 n 個不同項目中取出 k 個項目的組合數)

def binomial_coeff_orig(n_bc_orig, k_bc_orig): # 參數改名
    """計算二項式係數 "n 取 k"。

    n_bc_orig: 試驗次數 (總項目數)
    k_bc_orig: 成功次數 (選取項目數)

    回傳: 整數
    """
    # 基礎情況：
    if k_bc_orig == 0: # 從 n 個取 0 個，只有 1 種方法 (都不取)
        return 1
    if n_bc_orig == 0: # 從 0 個取 k 個 (k>0)，有 0 種方法
                       # (如果 k 也是 0，則上面已回傳 1)
        return 0
    # (如果 k > n，也應該是 0，但遞迴會處理這個)

    # 遞迴關係： C(n,k) = C(n-1, k) + C(n-1, k-1)
    # C(n-1, k)：不選第n個項目，從剩下n-1個中選k個
    # C(n-1, k-1)：選了第n個項目，從剩下n-1個中選k-1個
    return binomial_coeff_orig(n_bc_orig - 1, k_bc_orig) + \
           binomial_coeff_orig(n_bc_orig - 1, k_bc_orig - 1)

# 用巢狀條件表達式改寫函數主體。
#
# 這個函數不是很有效率，因為它會重複計算相同的值。
# 如[第十章](section_memos)所述，將其備忘錄化 (memoize) 以使其更有效率。
# (譯註：section_memos 指的是書中對應章節的連結)

# 解答
# 備忘錄 (cache) 作為預設參數，只建立一次
_binomial_coeff_cache = {} # 使用底線開頭的全域變數作為快取

def binomial_coeff_memo_cond_expr(n_bc_mce, k_bc_mce): # 參數改名
    """計算二項式係數 "n 取 k" (使用備忘錄和條件表達式)。"""
    # global _binomial_coeff_cache # 如果要在函數內修改全域變數本身 (例如賦值給它) 才需要
                                # 但這裡只是修改字典內容，所以不需要 global

    if (n_bc_mce, k_bc_mce) in _binomial_coeff_cache: # 檢查是否已在快取中
        return _binomial_coeff_cache[(n_bc_mce, k_bc_mce)]

    # 巢狀條件表達式
    # if k == 0: res = 1
    # else: (if n == 0: res = 0 else: res = rec1 + rec2)
    result_bc_mce = \
        1 if k_bc_mce == 0 else \
        (0 if n_bc_mce == 0 else \
         (binomial_coeff_memo_cond_expr(n_bc_mce - 1, k_bc_mce) + \
          binomial_coeff_memo_cond_expr(n_bc_mce - 1, k_bc_mce - 1)))
    
    # 處理 k > n 的情況，結果應為 0
    if k_bc_mce > n_bc_mce and k_bc_mce != 0 : # k=0 時結果是 1
        result_bc_mce = 0
    
    # 如果 n < 0 或 k < 0，也應該處理，但題目沒要求
    # if n_bc_mce < 0 or k_bc_mce < 0 : result_bc_mce = 0


    _binomial_coeff_cache[(n_bc_mce, k_bc_mce)] = result_bc_mce # 存入快取
    return result_bc_mce

# 清除快取以便重複測試 (如果需要的話)
def clear_binomial_cache():
    global _binomial_coeff_cache
    _binomial_coeff_cache = {}


print(f"\n--- 二項式係數 (備忘錄 + 巢狀條件表達式) ---")
clear_binomial_cache() # 確保快取是空的
print(f"binomial_coeff_memo_cond_expr(10, 4): {binomial_coeff_memo_cond_expr(10, 4)}")    # 210
clear_binomial_cache()
print(f"binomial_coeff_memo_cond_expr(20, 10): {binomial_coeff_memo_cond_expr(20, 10)}") # 184756
clear_binomial_cache()
print(f"binomial_coeff_memo_cond_expr(5, 6): {binomial_coeff_memo_cond_expr(5, 6)}")    # 0 (k > n)


# ### 練習
#
# 這是[第十七章](section_print_deck)中 `Deck` 類別的 `__str__` 方法。
# (譯註：section_print_deck 指的是書中對應章節的連結)

# %%add_method_to Deck
#     def __str__(self): # 這是迴圈版本
#         res_list_deck_str_loop = []
#         for card_deck_str_loop in self.cards:
#             res_list_deck_str_loop.append(str(card_deck_str_loop))
#         return '\n'.join(res_list_deck_str_loop)

# 用列表推導式或生成器表達式編寫這個方法的更簡潔版本。

# %%add_method_to Deck
# 我們在 In[72] 的 Deck 定義中已經用了列表推導式/生成器表達式
# class Deck:
#     ...
#     def __str__(self):
#         return '\n'.join(str(card_item) for card_item in self.cards) # 這是生成器表達式
#         # 或者列表推導式: return '\n'.join([str(card_item) for card_item in self.cards])

# 你可以用這個例子來測試你的解答。
# (Deck 的 __str__ 已在前面更新為使用生成器表達式的版本)

print(f"\n--- Deck __str__ (使用生成器表達式) 測試 ---")
cards_deck_str_test = Deck.make_cards()
deck_str_test = Deck(cards_deck_str_test)
# print(deck_str_test) # 會印出52張牌，很長
print("Deck __str__ 測試 (只印前3張和總數):")
if deck_str_test.cards:
    temp_deck_first_3 = Deck(deck_str_test.cards[:3])
    print(temp_deck_first_3)
    print(f"... (共 {len(deck_str_test.cards)} 張牌)")
else:
    print("(空牌堆)")

(這個 cell 在原始 .py 中是空的)
(這個 cell 在原始 .py 中是參考連結)