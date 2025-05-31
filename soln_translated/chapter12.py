# 從 chap12.ipynb 轉換而來
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

# # 文本分析與生成 (Text Analysis and Generation)
#
# 到目前為止，我們已經介紹了 Python 的核心資料結構 —— 列表、字典和元組 —— 以及一些使用它們的演算法。
# 在這一章，我們會用它們來探索文本分析和馬可夫生成 (Markov generation)：
#
# * 文本分析是一種描述文件中單字之間統計關係的方法，例如一個單字後面跟著另一個單字的機率，以及
#
# * 馬可夫生成是一種產生新文本的方法，新文本中的單字和片語會與原始文本相似。
#
# 這些演算法與大型語言模型 (Large Language Model, LLM) 的某些部分相似，而 LLM 是聊天機器人的關鍵組成部分。
#
# 我們會先計算一本書中每個單字出現的次數。
# 然後我們會看看成對的單字，並列出每個單字後面可能跟著的單字。
# 我們會製作一個簡單版本的馬可夫生成器，而在練習中，你將有機會製作一個更通用的版本。

# ## 不重複的單字 (Unique words)
#
# 作為文本分析的第一步，讓我們讀一本書 —— 羅伯特·路易斯·史蒂文生 (Robert Louis Stevenson) 的《化身博士》(The Strange Case Of Dr. Jekyll And Mr. Hyde) —— 並計算不重複單字的數量。
# 下載這本書的說明在本章的 notebook 檔案中。

# 下面的儲存格會從古騰堡計畫 (Project Gutenberg) 下載這本書。

download('https://www.gutenberg.org/cache/epub/43/pg43.txt');

# 從古騰堡計畫取得的版本，在開頭包含了關於書的資訊，在結尾則包含了授權資訊。
# 我們會使用第八章的 `clean_file` 函數來移除這些內容，並寫入一個只包含書本本文的「乾淨」檔案。

# 檢查一行是否為特殊行 (例如古騰堡計畫的標頭或註腳標記)
def is_special_line(line):
    return line.strip().startswith('*** ') # 移除頭尾空白後，檢查是否以 '*** ' 開頭

# 清理檔案，移除古騰堡計畫的額外資訊
def clean_file(input_file, output_file):
    try:
        reader = open(input_file, encoding='utf-8')
    except FileNotFoundError:
        print(f"錯誤: 輸入檔案 {input_file} 未找到。")
        return

    writer = open(output_file, 'w', encoding='utf-8') # 寫入也用 utf-8

    # 跳過開頭的版權宣告等等
    for line in reader:
        if is_special_line(line):
            break # 找到第一個特殊行就跳出

    # 寫入書本內容，直到遇到結尾的版權宣告
    for line in reader:
        if is_special_line(line):
            break # 找到第二個特殊行 (結尾標記) 就跳出
        writer.write(line)

    reader.close()
    writer.close()
    print(f"已清理檔案並儲存為: {output_file}")

filename = 'dr_jekyll.txt' # 清理後的檔案名稱

if exists('pg43.txt'):
    clean_file('pg43.txt', filename)
else:
    print(f"錯誤: pg43.txt 未下載，無法進行清理。請先執行 download。")


# 我們會用 `for` 迴圈來讀取檔案中的每一行，並用 `split` 來把每一行分割成單字。
# 然後，為了記錄不重複的單字，我們會把每個單字當作鍵儲存在一個字典裡。

unique_words = {}
if exists(filename): # 確保清理後的檔案存在
    for line in open(filename, encoding='utf-8'):
        seq = line.split() # 預設用空白分割
        for word in seq:
            unique_words[word] = 1 # 值是什麼不重要，用 1 當作佔位符
else:
    print(f"錯誤: {filename} 未找到，無法計算不重複單字。")

print(f"初步計算的不重複單字數量: {len(unique_words)}")

# 字典的長度就是不重複單字的數量 —— 用這種計算方式大約是 `6000` 個。
# 但是如果我們仔細檢查它們，會發現有些並不是有效的單字。
#
# 例如，讓我們看看 `unique_words` 中最長的那些單字。
# 我們可以用 `sorted` 來排序這些單字，並傳遞 `len` 函數作為關鍵字參數，
# 這樣單字就會按長度排序。

if unique_words: # 確保字典不是空的
    longest_initial_words = sorted(unique_words, key=len)[-5:] # 取排序後列表的最後 5 個
    print(f"初步計算中最長的 5 個「單字」: {longest_initial_words}")
else:
    print("unique_words 字典是空的。")

# 切片索引 `[-5:]` 選取了排序後列表的最後 `5` 個元素，也就是最長的單字。
#
# 這個列表包含了一些真正很長的單字，像是 "circumscription" (限制；範圍)，
# 和一些用連字號連接的單字，像是 "chocolate-coloured" (巧克力色的)。
# 但有些最長的「單字」其實是用破折號隔開的兩個字。
# 其他單字則包含了像是句點、驚嘆號和引號之類的標點符號。
#
# 所以，在繼續之前，我們先來處理破折號和其他標點符號。

# ## 標點符號 (Punctuation)
#
# 要識別文本中的單字，我們需要處理兩個問題：
#
# * 當一行中出現破折號 (dash) 時，我們應該把它換成空白 —— 這樣當我們用 `split` 時，單字就會被分開。
#
# * 分割單字後，我們可以用 `strip` 來移除標點符號。
#
# 為了處理第一個問題，我們可以用下面的函數，它接收一個字串，
# 把破折號換成空白，分割字串，然後回傳結果列表。

def split_line(line):
    # 注意：這裡用的是長破折號 '—' (em dash)，不是一般的連字號 '-' (hyphen)
    return line.replace('—', ' ').split()

# 注意 `split_line` 只取代破折號，不取代連字號。
# 這裡有一個例子。

print(f"split_line('coolness—frightened'): {split_line('coolness—frightened')}")

# 現在，要從每個單字的頭尾移除標點符號，我們可以用 `strip`，
# 但我們需要一個被視為標點符號的字元列表。
#
# Python 字串中的字元是 Unicode 編碼，這是一個國際標準，
# 用來表示幾乎所有字母系統的字母、數字、符號、標點符號等等。
# `unicodedata` 模組提供了一個 `category` 函數，可以用來判斷哪些字元是標點符號。
# 給定一個字母，它會回傳一個字串，其中包含該字母所屬類別的資訊。

import unicodedata

print(f"unicodedata.category('A'): {unicodedata.category('A')}")

# `'A'` 的類別字串是 `'Lu'` —— `'L'` 表示它是字母 (Letter)，`'u'` 表示它是大寫 (uppercase)。
#
# `'.'` 的類別字串是 `'Po'` —— `'P'` 表示它是標點符號 (Punctuation)，`'o'` 表示它的子類別是「其他 (other)」。

print(f"unicodedata.category('.'): {unicodedata.category('.')}")

# 我們可以透過檢查類別以 `'P'` 開頭的字元，來找出書中的標點符號。
# 下面的迴圈會把不重複的標點符號儲存在一個字典裡。

punc_marks = {}
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for char_in_line in line:
            category_of_char = unicodedata.category(char_in_line)
            if category_of_char.startswith('P'): # 如果類別是 P 開頭 (標點符號)
                punc_marks[char_in_line] = 1
else:
    print(f"錯誤: {filename} 未找到，無法收集標點符號。")


# 要建立一個標點符號列表 (字串形式)，我們可以把字典的鍵串接起來。

punctuation = ''.join(punc_marks.keys()) # .keys() 可省略，直接遍歷字典也是遍歷鍵
print(f"書中收集到的標點符號: {punctuation}")
# 為了讓 strip 更有效，我們可能還想手動加入一些常見的標點，以防 unicodedata 沒有完全涵蓋
# 或者，使用 string.punctuation 可能是更標準的方法，但書中用了 unicodedata
import string as py_string_module
standard_punctuation = py_string_module.punctuation
print(f"Python 標準標點符號 (string.punctuation): {standard_punctuation}")
# 這裡我們還是依照書中邏輯，使用從文本收集到的 punctuation


# 現在我們知道書中有哪些字元是標點符號了，
# 我們可以寫一個函數，它接收一個單字，移除頭尾的標點符號，並轉換成小寫。

def clean_word(word_to_clean):
    # 使用從文本收集到的 punctuation 進行移除
    return word_to_clean.strip(punctuation).lower()

# 這裡有一個例子。

print(f"clean_word('“Behold!”'): {clean_word('“Behold!”')}") # Behold (看啊！)

# 因為 `strip` 會移除頭尾的字元，所以它不會動到用連字號連接的單字。

print(f"clean_word('pocket-handkerchief'): {clean_word('pocket-handkerchief')}") # pocket-handkerchief (口袋手帕)

# 現在這裡有一個迴圈，它使用 `split_line` 和 `clean_word` 來識別書中不重複的單字。

unique_words2 = {}
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_from_split in split_line(line): # split_line 處理破折號並分割
            cleaned_word_item = clean_word(word_from_split) # 清理標點並轉小寫
            if cleaned_word_item: # 確保清理後不是空字串
                unique_words2[cleaned_word_item] = 1
else:
    print(f"錯誤: {filename} 未找到，無法重新計算不重複單字。")

print(f"清理後的不重複單字數量: {len(unique_words2)}")

# 用這種更嚴格的單字定義，不重複的單字大約有 4000 個。
# 我們可以確認最長單字的列表已經被清理乾淨了。

if unique_words2:
    longest_cleaned_words = sorted(unique_words2, key=len)[-5:]
    print(f"清理後最長的 5 個單字: {longest_cleaned_words}")
else:
    print("unique_words2 字典是空的。")


# 現在讓我們看看每個單字被使用了多少次。

# ## 單字頻率 (Word frequencies)
#
# 下面的迴圈會計算每個不重複單字的頻率。

word_counter = {}
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_from_split_freq in split_line(line):
            cleaned_word_freq = clean_word(word_from_split_freq)
            if cleaned_word_freq: # 確保不是空字串
                if cleaned_word_freq not in word_counter:
                    word_counter[cleaned_word_freq] = 1 # 第一次看到，計數為 1
                else:
                    word_counter[cleaned_word_freq] += 1 # 之前看過了，計數加 1
else:
    print(f"錯誤: {filename} 未找到，無法計算單字頻率。")

# 我們第一次看到一個單字時，把它的頻率初始化為 `1`。如果之後又看到同一個單字，就把它的頻率加一。
#
# 要看看哪些單字最常出現，我們可以用 `items()` 從 `word_counter` 中取得鍵值對，
# 然後按鍵值對的第二個元素 (也就是頻率) 來排序。
# 首先我們定義一個選取第二個元素的函數。

def second_element(t_tuple_freq): # 參數改名以避免混淆
    return t_tuple_freq[1] # 回傳元組的第二個元素 (頻率)

# 現在我們可以用 `sorted` 搭配兩個關鍵字參數：
#
# * `key=second_element` 表示項目會根據單字的頻率來排序。
#
# * `reverse=True` 表示項目會反向排序，最常出現的單字排在最前面。

sorted_word_items = []
if word_counter:
    sorted_word_items = sorted(word_counter.items(), key=second_element, reverse=True)
else:
    print("word_counter 是空的，無法排序。")

# 這裡是最常出現的五個單字。

print("\n--- 最常出現的 5 個單字 ---")
if sorted_word_items:
    for word_item_freq, freq_val in sorted_word_items[:5]: # 取前 5 個
        print(f"{freq_val}\t{word_item_freq}") # \t 是定位字元 (tab)
else:
    print("無法顯示最常見單字，因為列表是空的。")

# 在下一節，我們會把這個迴圈封裝到一個函數裡。
# 我們也會用它來示範一個新功能 —— 選擇性參數 (optional parameters)。

# ## 選擇性參數 (Optional parameters)
#
# 我們用過一些接收選擇性參數的內建函數。
# 例如，`round()` 接收一個叫做 `ndigits` 的選擇性參數，用來指定要保留的小數位數。

print(f"\nround(3.141592653589793, ndigits=3): {round(3.141592653589793, ndigits=3)}")

# 不只是內建函數 —— 我們也可以寫出帶有選擇性參數的函數。
# 例如，下面的函數接收兩個參數，`word_counter_func` 和 `num`。

def print_most_common(word_counter_func, num=5): # num=5 表示 num 的預設值是 5
    if not word_counter_func:
        print("傳入的 word_counter 是空的。")
        return

    items_to_sort = sorted(word_counter_func.items(), key=second_element, reverse=True)
    print(f"\n--- 最常出現的 {num} 個單字 ---")
    for word_p, freq_p in items_to_sort[:num]:
        print(f"{freq_p}\t{word_p}")

# 第二個參數看起來像一個賦值陳述式，但它不是 —— 它是一個選擇性參數。
#
# 如果你用一個引數呼叫這個函數，`num` 就會得到 **預設值 (default value)**，也就是 `5`。

print_most_common(word_counter) # 呼叫時只給一個引數

# 如果你用兩個引數呼叫這個函數，第二個引數就會被指派給 `num`，而不是使用預設值。

print_most_common(word_counter, 3) # 呼叫時給兩個引數，num 會是 3

# 在那種情況下，我們會說選擇性引數 **覆寫 (overrides)** 了預設值。
#
# 如果一個函數同時有必要參數 (required parameter) 和選擇性參數，
# 所有的必要參數都必須在前面，後面才是選擇性參數。

%%expect SyntaxError
# def bad_function(n=5, word_counter_req): # 錯誤：選擇性參數不能在必要參數前面
#     return None

# ## 字典相減 (Dictionary subtraction)
#
# 假設我們想對一本書進行拼字檢查 —— 也就是找出可能拼錯的單字列表。
# 一種方法是找出書中出現但沒有出現在有效單字列表中的單字。
# 在之前的章節中，我們用過一個被認為在像 Scrabble (拼字遊戲) 這樣的文字遊戲中有效的單字列表。
# 現在我們用這個列表來對羅伯特·路易斯·史蒂文生的作品進行拼字檢查。
#
# 我們可以把這個問題想成集合的相減 —— 也就是說，我們想找出所有來自一個集合 (書中的單字)
# 但不在另一個集合 (列表中的單字) 的單字。

# 下面的儲存格會下載單字列表 (words.txt)。

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

# 如同我們之前做過的，我們可以讀取 `words.txt` 的內容並把它分割成一個字串列表。

word_list_valid = []
if exists('words.txt'):
    word_list_valid = open('words.txt', encoding='utf-8').read().split()
else:
    print("錯誤: words.txt 未找到，無法建立有效單字字典。")


# 然後我們會把這些單字當作鍵儲存在一個字典裡，這樣我們就可以用 `in` 運算子
# 快速檢查一個單字是否有效。

valid_words = {}
if word_list_valid:
    for word_v in word_list_valid:
        valid_words[word_v] = 1 # 值不重要
else:
    print("word_list_valid 是空的。")


# 現在，要識別出現在書中但不在單字列表中的單字，
# 我們會用 `subtract` 函數，它接收兩個字典作為參數，
# 並回傳一個新的字典，其中包含所有來自第一個字典但不在第二個字典中的鍵。

def subtract(d1, d2):
    res_diff_dict = {}
    for key_d1 in d1:
        if key_d1 not in d2: # 如果 d1 的鍵不在 d2 中
            res_diff_dict[key_d1] = d1[key_d1] # 就把這個鍵和它在 d1 中的值加入結果字典
    return res_diff_dict

# 我們這樣使用它：

diff_book_vs_valid = {}
if word_counter and valid_words:
    diff_book_vs_valid = subtract(word_counter, valid_words) # 書中單字 - 有效單字列表
else:
    print("word_counter 或 valid_words 是空的，無法執行相減。")


# 要取得可能拼錯的單字樣本，我們可以印出 `diff_book_vs_valid` 中最常見的那些字。

print_most_common(diff_book_vs_valid)

# 最常見的「拼錯」單字大多是名字和一些單字母縮寫
# (Mr. Utterson 是 Dr. Jekyll 的朋友和律師)。
#
# 如果我們選出只出現一次的單字，它們更有可能是真正的拼寫錯誤。
# 我們可以透過遍歷項目並建立一個頻率為 `1` 的單字列表來做到這點。

singletons = [] # 只出現一次的「拼錯」字
if diff_book_vs_valid:
    for word_s, freq_s in diff_book_vs_valid.items():
        if freq_s == 1:
            singletons.append(word_s)
else:
    print("diff_book_vs_valid 是空的。")


# 這是列表的最後幾個元素。

print(f"只出現一次的「拼錯」字 (最後 5 個): {singletons[-5:]}")

# 它們大部分是有效的單字，只是不在我們的單字列表 (words.txt) 中。
# 但是 `'reindue'` 看起來像是 `'reinduce'` (重新引導；使再發生) 的拼寫錯誤，所以至少我們找到了一個真正的錯誤。

# ## 隨機數 (Random numbers)
#
# 作為馬可夫文本生成的一步，接下來我們會從 `word_counter` 中選擇一個隨機的單字序列。
# 但首先我們來談談隨機性。
#
# 給定相同的輸入，大多數電腦程式都是 **決定性的 (deterministic)**，這表示它們每次都會產生相同的輸出。
# 決定性通常是件好事，因為我們期望相同的計算會產生相同的結果。
# 不過，對於某些應用程式，我們希望電腦是不可預測的。
# 遊戲是一個例子，但還有更多。
#
# 讓程式真正具有非決定性結果是很困難的，但有一些方法可以假裝做到。
# 一種是使用產生 **偽隨機 (pseudorandom)** 數的演算法。
# 偽隨機數並非真正的隨機，因為它們是由決定性的計算產生的，
# 但僅僅看這些數字，幾乎不可能把它們與真正的隨機數區分開來。
#
# `random` 模組提供了產生偽隨機數的函數 —— 從現在開始我會簡稱它們為「隨機數」。
# 我們可以像這樣匯入它。

import random

# 這個儲存格會初始化隨機數產生器，
# 這樣每次執行 notebook 時它都會產生相同的序列。
# (這對於重現結果和除錯很有用)
random.seed(4) # 使用一個固定的種子

# `random` 模組提供了一個叫做 `choice` 的函數，它可以從一個列表中隨機選擇一個元素，
# 每個元素被選擇的機率都相同。

t_random_list = [1, 2, 3]
print(f"random.choice({t_random_list}): {random.choice(t_random_list)}")

# 如果你再次呼叫這個函數，你可能會再次得到相同的元素，或者得到不同的元素。

print(f"再次 random.choice({t_random_list}): {random.choice(t_random_list)}")

# 長期來看，我們期望每個元素被選擇的次數大致相同。
#
# 如果你對字典使用 `choice`，你會得到一個 `KeyError`。
# (因為 `choice` 期望的是一個序列，例如列表，而不是映射)

%%expect KeyError
# if word_counter: # 避免 word_counter 為空時出錯
#    random.choice(word_counter)

# 要隨機選擇一個鍵，你必須先把鍵放到一個列表中，然後再呼叫 `choice`。

random_key_from_wc = ""
if word_counter:
    words_from_counter_keys = list(word_counter.keys()) # 或者直接 list(word_counter)
    if words_from_counter_keys: # 確保列表不是空的
        random_key_from_wc = random.choice(words_from_counter_keys)
print(f"從 word_counter 隨機選一個鍵: {random_key_from_wc}")


# 如果我們產生一個隨機的單字序列，它看起來沒什麼意義。

print("\n--- 隨機選擇的 6 個單字 (等機率) ---")
if word_counter:
    words_for_random_seq = list(word_counter)
    if words_for_random_seq:
        for i in range(6):
            word_rand_eq = random.choice(words_for_random_seq)
            print(word_rand_eq, end=' ')
        print() # 換行
    else:
        print("word_counter 的鍵列表是空的。")
else:
    print("word_counter 是空的。")

# 部分問題在於我們沒有考慮到有些單字比其他單字更常見。
# 如果我們用不同的「權重 (weights)」來選擇單字，讓某些單字被選擇的頻率更高，結果會更好。
#
# 如果我們使用 `word_counter` 中的值 (頻率) 作為權重，
# 每個單字被選擇的機率就會取決於它的頻率。

weights_from_wc_values = []
if word_counter:
    weights_from_wc_values = list(word_counter.values()) # 取得所有頻率作為權重
# print(f"前 10 個權重: {weights_from_wc_values[:10]}")


# `random` 模組提供了另一個叫做 `choices` 的函數 (注意是複數 s)，
# 它可以接收 `weights` 作為選擇性參數。

# 確保 words_from_counter_keys 和 weights_from_wc_values 長度一致且非空
random_word_weighted = ""
if word_counter and words_from_counter_keys and weights_from_wc_values and len(words_from_counter_keys) == len(weights_from_wc_values):
    # random.choices 回傳一個列表，即使 k=1
    chosen_list = random.choices(words_from_counter_keys, weights=weights_from_wc_values)
    if chosen_list:
        random_word_weighted = chosen_list[0]
print(f"按權重隨機選擇一個單字: {random_word_weighted}")


# 它還接收另一個選擇性參數 `k`，用來指定要選擇的單字數量。

random_words_weighted_k6 = []
if word_counter and words_from_counter_keys and weights_from_wc_values and len(words_from_counter_keys) == len(weights_from_wc_values):
    random_words_weighted_k6 = random.choices(words_from_counter_keys, weights=weights_from_wc_values, k=6)
print(f"按權重隨機選擇 6 個單字: {random_words_weighted_k6}")


# 結果是一個字串列表，我們可以把它們串接成看起來更像句子的東西。

if random_words_weighted_k6:
    print(f"串接後的隨機加權單字: {' '.join(random_words_weighted_k6)}")

# 如果你從書中隨機選擇單字，你會對詞彙有所了解，
# 但一連串隨機的單字很少能構成有意義的句子，因為連續的單字之間沒有關聯。
# 例如，在一個真實的句子中，你期望像 "the" 這樣的冠詞後面會跟著一個形容詞或名詞，
# 而不太可能是一個動詞或副詞。
# 所以下一步是看看這些單字之間的關係。

# ## 二元組 (Bigrams)
#
# 現在我們不再一次只看一個單字，而是看看兩個單字的序列，這稱為 **二元組 (bigrams)**。
# 三個單字的序列稱為 **三元組 (trigram)**，而某個未指定數量的單字序列稱為 **n-元組 (n-gram)**。
#
# 讓我們寫一個程式來找出書中所有的二元組以及每個二元組出現的次數。
# 為了儲存結果，我們會使用一個字典，其中：
#
# * 鍵是代表二元組的字串元組，而且
#
# * 值是代表頻率的整數。
#
# 我們稱它為 `bigram_counter`。

bigram_counter = {}

# 下面的函數接收一個包含兩個字串的列表作為參數。
# 首先它把這兩個字串做成一個元組，這個元組可以用作字典的鍵。
# 然後它把這個鍵加入到 `bigram_counter` 中 (如果不存在的話)，或者增加其頻率 (如果已存在)。

def count_bigram(bigram_list_input): # 參數改名
    key_tuple_bigram = tuple(bigram_list_input) # 把列表轉成元組作為鍵
    if key_tuple_bigram not in bigram_counter:
        bigram_counter[key_tuple_bigram] = 1
    else:
        bigram_counter[key_tuple_bigram] += 1

# 當我們遍歷這本書時，我們必須記錄每一對連續的單字。
# 所以如果我們看到序列 "man is not truly one" (人並非真正單一)，
# 我們會加入二元組 "man is"、"is not"、"not truly" 等等。
#
# 為了記錄這些二元組，我們會使用一個叫做 `window` (窗格) 的列表，
# 因為它就像一個滑過書頁的窗格，一次只顯示兩個單字。
# 一開始，`window` 是空的。

window = [] # 用來儲存滑動的二元組窗格

# 我們會用下面的函數來一次處理一個單字。

def process_word_for_bigram(word_input_pb): # 參數改名
    window.append(word_input_pb) # 把目前的單字加入窗格

    if len(window) == 2: # 如果窗格裡有兩個單字了 (形成一個二元組)
        count_bigram(window) # 就計算這個二元組的頻率
        window.pop(0) # 然後把窗格裡的第一個單字移掉，準備接收下一個字

# 第一次呼叫這個函數時，它會把給定的單字附加到 `window`。
# 因為窗格裡只有一個單字，所以還沒有二元組，函數就結束了。
#
# 第二次呼叫時 —— 以及之後的每一次 —— 它會把第二個單字附加到 `window`。
# 因為窗格裡有兩個單字了，它會呼叫 `count_bigram` 來記錄每個二元組出現的次數。
# 然後它用 `pop` 來移除窗格中的第一個單字。
#
# 下面的程式會遍歷書中的單字並一次處理一個。

bigram_counter = {} # 重設 bigram_counter
window = []         # 重設 window
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_in_line_bg in split_line(line): # split_line 處理破折號並分割
            cleaned_word_bg = clean_word(word_in_line_bg) # 清理標點並轉小寫
            if cleaned_word_bg: # 確保不是空字串
                process_word_for_bigram(cleaned_word_bg)
else:
    print(f"錯誤: {filename} 未找到，無法計算二元組頻率。")


# 結果是一個字典，它把每個二元組對應到它出現的次數。
# 我們可以用 `print_most_common` 來看看最常見的二元組。
# (需要確保 print_most_common 和 second_element 在此可用)

if bigram_counter:
    print_most_common(bigram_counter) # 使用之前定義的 print_most_common
else:
    print("bigram_counter 是空的。")

# 看看這些結果，我們可以大致了解哪些單字對最可能一起出現。
# 我們也可以用這些結果來產生隨機文本，像這樣。

random.seed(0) # 重設隨機種子以保持一致性

random_bigrams_generated = []
if bigram_counter:
    bigrams_list_from_counter = list(bigram_counter.keys()) # 取得所有二元組 (鍵)
    weights_for_bigrams = list(bigram_counter.values())   # 取得它們的頻率 (值) 作為權重
    if bigrams_list_from_counter and weights_for_bigrams and len(bigrams_list_from_counter) == len(weights_for_bigrams):
        random_bigrams_generated = random.choices(bigrams_list_from_counter, weights=weights_for_bigrams, k=6)
else:
    print("bigram_counter 是空的，無法產生隨機二元組。")

# `bigrams_list_from_counter` 是書中出現的二元組的列表。
# `weights_for_bigrams` 是它們的頻率列表，所以 `random_bigrams_generated` 是一個樣本，
# 其中一個二元組被選擇的機率與其頻率成正比。
#
# 這是結果。

print("\n--- 隨機生成的二元組序列 ---")
if random_bigrams_generated:
    for pair_bg_gen in random_bigrams_generated:
        print(' '.join(pair_bg_gen), end='; ') # 用分號隔開，並在結尾加空白
    print() # 換行
else:
    print("未能生成隨機二元組。")


# 這種產生文本的方式比隨機選擇單字要好一些，但仍然不太通順。

# ## 馬可夫分析 (Markov analysis)
#
# 我們可以用馬可夫鏈文本分析 (Markov chain text analysis) 做得更好，
# 這種方法會計算文本中每個單字後面可能跟著的單字列表。
# 作為例子，我們來分析蒙提·派森歌曲《半隻小蜜蜂艾瑞克》(Eric, the Half a Bee) 的歌詞：
# (Eric, the Half a Bee 是一首荒謬的歌曲，關於一隻只有一半的蜜蜂)

song = """
Half a bee, philosophically,
Must, ipso facto, half not be.
But half the bee has got to be
Vis a vis, its entity. D'you see?
"""
# ipso facto: 拉丁語，意思是「事實本身就證明了」
# Vis a vis: 法語，意思是「相對於；關於」
# entity: 實體
# D'you see?: 你明白嗎？

# 為了儲存結果，我們會使用一個字典，它把每個單字對應到其後繼單字的列表。

successor_map = {} # 後繼詞對照表

# 作為例子，我們先從歌曲的前兩個單字開始。

first_song_word = 'half'
second_song_word = 'a'

# 如果第一個單字不在 `successor_map` 中，我們必須新增一個項目，
# 把第一個單字對應到一個只包含第二個單字的列表。

successor_map[first_song_word] = [second_song_word]
print(f"加入 ('half', 'a') 後的 successor_map: {successor_map}")

# 如果第一個單字已經在字典中了，我們可以查詢它以取得目前為止看到的後繼詞列表，
# 然後把新的後繼詞附加到列表中。

first_song_word_again = 'half' # 假設又遇到 'half'
second_song_word_next = 'not'  # 這次後面是 'not'

if first_song_word_again in successor_map: # 確保鍵存在
    successor_map[first_song_word_again].append(second_song_word_next)
else:
    successor_map[first_song_word_again] = [second_song_word_next]
print(f"再次加入 'half' 的後繼詞後的 successor_map: {successor_map}")


# 下面的函數封裝了這些步驟。

def add_bigram_to_successor_map(bigram_input_smap): # 參數改名
    first_word_smap, second_word_smap = bigram_input_smap # 解包二元組

    if first_word_smap not in successor_map:
        successor_map[first_word_smap] = [second_word_smap] # 第一次遇到 first_word_smap
    else:
        successor_map[first_word_smap].append(second_word_smap) # first_word_smap 已存在，附加後繼詞

# 如果同一個二元組出現多次，第二個單字就會被多次加入到列表中。
# 透過這種方式，`successor_map` 記錄了每個後繼詞出現的次數。
# (這隱含地包含了頻率信息，因為重複的後繼詞會讓它在列表中出現多次，被 random.choice 選中的機率就更高)
#
# 如同上一節，我們會用一個叫做 `window` 的列表來儲存連續的單字對。
# 我們會用下面的函數來一次處理一個單字。

# 這個函數名與 In[105] 的 process_word_for_bigram 作用類似，但呼叫的是 add_bigram_to_successor_map
def process_word_for_successor_map(word_input_sm): # 參數改名
    window.append(word_input_sm)

    if len(window) == 2: # 形成二元組
        add_bigram_to_successor_map(window) # 加入到後繼詞對照表
        window.pop(0) # 滑動窗格

# 我們這樣用它來處理歌曲中的單字。

successor_map = {} # 重設
window = []        # 重設

# 處理歌曲文本
song_words = []
# 預處理歌曲文本：移除標點，轉小寫，分割
# 這裡用更簡單的方式處理，因為歌詞比較規律
import re
for line_song in song.splitlines(): # 按行分割
    if not line_song.strip(): continue # 跳過空行
    # 移除行首尾標點，轉小寫
    cleaned_line_song = re.sub(r"[^\w\s']", '', line_song).lower() # 保留單引號 (像 d'you)
    song_words.extend(cleaned_line_song.split())

for word_from_song in song_words:
    # clean_word 在這裡是為了處理像 d'you 這樣的詞，但可能 song_words 已經夠乾淨了
    # cleaned_song_word = clean_word(word_from_song) # clean_word 可能會移除 '
    # 為了保留 d'you, vis-a-vis (雖然前面說不處理連字號，但歌詞中可能有)
    # 我們可以假設 song_words 已經是清理過的單字列表
    if word_from_song: # 確保不是空字串
        process_word_for_successor_map(word_from_song)

# 這是結果。

print(f"\n歌曲 'Eric, the Half a Bee' 的 successor_map:")
# 為了讓輸出更可讀，可以逐項印出
for pred_word, succ_list in successor_map.items():
    print(f"'{pred_word}': {succ_list}")


# 單字 `'half'` 後面可以跟著 `'a'`、`'not'` 或 `'the'`。
# 單字 `'a'` 後面可以跟著 `'bee'` 或 `'vis'`。
# 大部分其他單字只出現一次，所以它們後面只跟著一個單字。
#
# 現在我們來分析這本書。

successor_map = {} # 重設
window = []        # 重設

if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_in_line_sm_book in split_line(line):
            cleaned_word_sm_book = clean_word(word_in_line_sm_book)
            if cleaned_word_sm_book:
                process_word_for_successor_map(cleaned_word_sm_book)
else:
    print(f"錯誤: {filename} 未找到，無法建立書籍的 successor_map。")


# 我們可以查詢任何單字，並找到它後面可能跟著的單字。

# 我用這個儲存格來找一個有很多可能後繼詞，並且至少有一個重複單字的前導詞。
# (這是作者的筆記)
def has_duplicates_list(t_list_dup): # 檢查列表是否有重複元素
    return len(set(t_list_dup)) < len(t_list_dup)

print("\n--- 尋找 successor_map 中有趣的例子 ---")
found_example_key = None
if successor_map:
    for key_sm_ex, value_sm_list_ex in successor_map.items():
        if len(value_sm_list_ex) >= 5 and has_duplicates_list(value_sm_list_ex): # 例如至少5個後繼詞且有重複
            print(f"找到一個例子: 前導詞 '{key_sm_ex}', 後繼詞列表: {value_sm_list_ex}")
            found_example_key = key_sm_ex
            break # 找到一個就停
    if not found_example_key:
        print("未找到符合條件的有趣例子，隨便選一個。")
        # 如果找不到，就從 successor_map 中隨便選一個非空的
        for key_sm_ex, value_sm_list_ex in successor_map.items():
            if value_sm_list_ex:
                found_example_key = key_sm_ex
                break
else:
    print("successor_map 是空的。")


if found_example_key and successor_map:
    print(f"單字 '{found_example_key}' 的後繼詞列表: {successor_map.get(found_example_key, [])}")
elif successor_map.get('going'): # 如果上面沒找到，試試書中用的 'going'
     print(f"單字 'going' 的後繼詞列表: {successor_map['going']}")
else:
    print("找不到 'going' 或其他範例的後繼詞。")


# 在這個後繼詞列表中，注意到單字 `'to'` 出現了三次 —— 其他後繼詞只出現一次。
# (這取決於上面找到的 found_example_key，如果是 'going'，'to' 的確常出現)

# ## 生成文本 (Generating text)
#
# 我們可以用上一節的結果來產生新的文本，
# 新文本中連續單字之間的關係會與原始文本相同。
# 它是這樣運作的：
#
# * 從文本中出現的任何一個單字開始，我們查詢它可能的後繼詞，並隨機選擇一個。
#
# * 然後，使用選擇的單字，我們查詢它可能的後繼詞，並隨機選擇一個。
#
# 我們可以重複這個過程來產生任意數量的單字。
# 作為例子，讓我們從單字 `'although'` (雖然) 開始。
# 這是它後面可能跟著的單字。

start_word_gen = 'although'
successors_for_although = []
if successor_map and start_word_gen in successor_map:
    successors_for_although = successor_map[start_word_gen]
print(f"單字 '{start_word_gen}' 的後繼詞: {successors_for_although}")

# 這個儲存格會初始化隨機數產生器，
# 這樣每次執行這個 notebook 時，它都會從序列的同一個點開始。
random.seed(2)

# 我們可以用 `choice` 從列表中等機率地選擇。

next_word_gen = ""
current_word_for_gen = start_word_gen # 假設從 'although' 開始
print("\n--- 馬可夫鏈文本生成 (以 bigram 為基礎) ---")
if successor_map and current_word_for_gen in successor_map:
    successors_list_gen = successor_map[current_word_for_gen]
    if successors_list_gen: # 確保後繼詞列表不是空的
        next_word_gen = random.choice(successors_list_gen)
print(f"從 '{current_word_for_gen}' 的後繼詞中隨機選一個: {next_word_gen}")
current_word_for_gen = next_word_gen # 更新目前的單字
else:
    print(f"無法從 '{current_word_for_gen}' 開始生成，它不在 successor_map 中或沒有後繼詞。")
    # 如果無法開始，可以嘗試從一個隨機的有效鍵開始
    if successor_map:
        valid_start_keys = [k for k,v in successor_map.items() if v] # 找有後繼詞的鍵
        if valid_start_keys:
            current_word_for_gen = random.choice(valid_start_keys)
            print(f"改從隨機選擇的 '{current_word_for_gen}' 開始。")
        else:
            current_word_for_gen = None # 標記無法生成
            print("successor_map 中沒有任何單字有後繼詞，無法生成文本。")



# 如果同一個單字在列表中出現多次，它就更有可能被選中。
# (因為 `random.choice` 是等機率從列表中選，列表元素多自然機率高)
#
# 重複這些步驟，我們可以用下面的迴圈來產生一個更長的序列。

generated_text_list = []
if current_word_for_gen and successor_map : # 確保可以開始生成
    generated_text_list.append(current_word_for_gen) # 把第一個選出的字也加進去
    for i in range(20): # 生成 20 個字
        if current_word_for_gen in successor_map and successor_map[current_word_for_gen]:
            successors_loop = successor_map[current_word_for_gen]
            current_word_for_gen = random.choice(successors_loop)
            generated_text_list.append(current_word_for_gen)
        else:
            # 如果目前的單字沒有後繼詞 (例如到了文本結尾的字，或者 map 不完整)
            # 就可以停止，或者從一個新的隨機字開始
            print(f"\n(單字 '{current_word_for_gen}' 沒有後繼詞，停止生成。)")
            break
    print(" ".join(generated_text_list))
else:
    print("無法生成文本。")


# 結果聽起來更像真實的句子，但仍然不太通順。
#
# 我們可以用 `successor_map` 中使用多於一個單字作為鍵來做得更好。
# 例如，我們可以建立一個字典，它把每個二元組 —— 或三元組 —— 對應到其後繼單字的列表。
# 作為練習，你將有機會實作這種分析，並看看結果如何。

# ## 除錯 (Debugging)
#
# 到目前為止，我們寫的程式越來越龐大，你可能會發現花在除錯上的時間越來越多。
# 如果你卡在一個困難的 bug 上，這裡有一些可以嘗試的方法：
#
# * 閱讀 (Reading)：仔細檢查你的程式碼，把它唸給自己聽，確認它寫的是你真正想表達的意思。
#
# * 執行 (Running)：透過修改和執行不同版本來進行實驗。通常如果在程式的正確位置顯示正確的資訊，問題就會變得很明顯，但有時你必須建立一些輔助性的程式碼 (scaffolding)。
#
# * 思考 (Ruminating)：花點時間思考！這是哪種類型的錯誤：語法錯誤、執行期錯誤，還是語義錯誤？你能從錯誤訊息或程式的輸出中得到什麼資訊？什麼樣的錯誤可能會導致你看到的問題？在你發現問題之前，你最後修改了什麼？
#
# * 小黃鴨除錯法 (Rubberducking)：如果你向別人解釋問題，有時在問完問題之前你就會找到答案。通常你不需要另一個人；你可以只對著一隻橡皮鴨說話。這就是著名策略「小黃鴨除錯法」的由來。我可不是在開玩笑 —— 請看 <https://en.wikipedia.org/wiki/Rubber_duck_debugging>。
#
# * 退回 (Retreating)：有時候，最好的做法是退一步 —— 復原最近的修改 —— 直到你回到一個可以運作的程式版本。然後你可以開始重新建構。
#
# * 休息 (Resting)：如果你讓大腦休息一下，有時它會自己幫你找到問題。

# 初學程式設計的人有時會卡在其中一項活動而忘記其他項。每項活動都有其失敗模式。
#
# 例如，如果問題是打字錯誤，閱讀程式碼是有效的，但如果問題是概念上的誤解，那就不行了。
# 如果你不了解你的程式在做什麼，即使你看 100 次也可能永遠看不到錯誤，因為錯誤在你的腦海裡。
#
# 進行實驗可能有效，尤其是當你進行小型、簡單的測試時。
# 但是如果你不思考或不閱讀程式碼就進行實驗，可能需要很長時間才能弄清楚發生了什麼事。
#
# 你必須花時間思考。除錯就像一門實驗科學。你至少應該對問題是什麼有一個假設。
# 如果有兩種或多種可能性，試著想一個可以排除其中一種的測試。

# 但即使是最好的除錯技巧，如果錯誤太多，或者你試圖修復的程式碼太大太複雜，
# 也可能會失敗。有時最好的選擇是退回，簡化程式，直到你回到可以運作的狀態。
#
# 初學者通常不願意退回，因為他們無法忍受刪除一行程式碼 (即使它是錯的)。
# 如果這樣能讓你感覺好一點，可以在開始精簡程式碼之前，先把你的程式複製到另一個檔案。
# 然後你可以一次一點地把片段複製回來。
#
# 找到一個困難的 bug 需要閱讀、執行、思考、退回，有時還需要休息。
# 如果你卡在其中一項活動，試試其他的。

# ## 詞彙表 (Glossary)
#
# **預設值 (default value):**
#  如果沒有提供引數，指派給參數的值。
#
# **覆寫 (override):**
#  用引數取代預設值。
#
# **決定性的 (deterministic):**
#  一個決定性的程式在每次執行時，給定相同的輸入，都會做相同的事情。
#
# **偽隨機 (pseudorandom):**
#  一個偽隨機數序列看起來是隨機的，但它是由一個決定性的程式產生的。
#
# **二元組 (bigram):**
#  兩個元素的序列，通常是單字。
#
# **三元組 (trigram):**
#  三個元素的序列。
#
# **n-元組 (n-gram):**
#  一個未指定元素數量的序列。
#
# **小黃鴨除錯法 (rubber duck debugging):**
#  一種透過向一個無生命的物體大聲解釋問題來進行除錯的方法。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 在 `add_bigram_to_successor_map` (原書為 `add_bigram`) 中，`if` 陳述式會根據鍵是否已在字典中，
# 來建立一個新的列表或將元素附加到現有的列表中。

# 為了演示 setdefault，我們需要一個空的 successor_map
successor_map_setdefault_example = {}
def add_bigram_original_for_setdefault(bigram_input): # 這是書中原始的 add_bigram 邏輯
    first, second = bigram_input
    global successor_map_setdefault_example # 確保修改的是外面的字典

    if first not in successor_map_setdefault_example:
        successor_map_setdefault_example[first] = [second]
    else:
        successor_map_setdefault_example[first].append(second)

add_bigram_original_for_setdefault(('half', 'a'))
add_bigram_original_for_setdefault(('half', 'not'))
print(f"使用原始 if/else 的 successor_map: {successor_map_setdefault_example}")


# 字典提供了一個叫做 `setdefault` 的方法，我們可以用它來更簡潔地做同樣的事情。
# 問問虛擬助理它是如何運作的，或者把 `add_bigram_original_for_setdefault` (原書為 `add_word`，但這裡的上下文是 bigram)
# 複製到虛擬助理中並問：「你能用 `setdefault` 重寫這個嗎？」
#
# 這裡是用 setdefault 的版本：
successor_map_setdefault_example_v2 = {}
def add_bigram_with_setdefault(bigram_input):
    first, second = bigram_input
    global successor_map_setdefault_example_v2
    # setdefault(key, default_value)
    # 如果 key 不在字典中，它會插入 key 並將其值設為 default_value，然後回傳 default_value。
    # 如果 key 已經在字典中，它只會回傳 key 對應的目前值，不做任何改變。
    # 所以，successor_map_setdefault_example_v2.setdefault(first, [])
    # 會確保 first 存在於字典中，並且其值是一個列表 (如果不存在就設為空列表)。
    # 然後 .append(second) 就可以安全地使用了。
    successor_map_setdefault_example_v2.setdefault(first, []).append(second)

add_bigram_with_setdefault(('half', 'a'))
add_bigram_with_setdefault(('half', 'not'))
print(f"使用 setdefault 的 successor_map: {successor_map_setdefault_example_v2}")


# 在本章中，我們實作了馬可夫鏈文本分析和生成。
# 如果你好奇，可以向虛擬助理詢問更多關於這個主題的資訊。
# 你可能會學到的一件事是，虛擬助理使用的演算法在很多方面與此相似 —— 但在重要方面也有所不同。
# 問問虛擬助理：「像 GPT 這樣的大型語言模型和馬可夫鏈文本分析之間有什麼區別？」

# ### 練習
#
# 寫一個函數，計算每個三元組 (三個單字的序列) 出現的次數。
# 如果你用《化身博士》的文本測試你的函數，你應該會發現最常見的三元組是 "said the lawyer" (律師說)。
#
# 提示：寫一個叫做 `count_trigram` 的函數，它類似於 `count_bigram`。
# 然後寫一個叫做 `process_word_trigram` 的函數，它類似於 `process_word_for_bigram` (原書為 `process_word_bigram`)。

# 解答
trigram_counter = {} # 全域變數來儲存三元組計數

def count_trigram(trigram_list_input): # 參數改名
    key_tuple_trigram = tuple(trigram_list_input) # 用元組當鍵

    if key_tuple_trigram not in trigram_counter:
        trigram_counter[key_tuple_trigram] = 1
    else:
        trigram_counter[key_tuple_trigram] += 1

# 解答
# window 應該是全域的，或者作為參數傳遞
# 這裡假設 window 是全域的，並在執行前重設

def process_word_for_trigram_count(word_input_tc): # 參數改名
    # 假設 window 是在此函數外部定義和管理的
    window.append(word_input_tc)

    if len(window) == 3: # 形成三元組
        count_trigram(window) # 計算這個三元組
        window.pop(0) # 滑動窗格

# 你可以用下面的迴圈來讀取書本並處理單字。

trigram_counter = {} # 重設計數器
window = []        # 重設窗格

print("\n--- 計算三元組頻率 ---")
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_in_line_tg in split_line(line):
            cleaned_word_tg = clean_word(word_in_line_tg)
            if cleaned_word_tg:
                process_word_for_trigram_count(cleaned_word_tg)
else:
    print(f"錯誤: {filename} 未找到，無法計算三元組。")


# 然後使用 `print_most_common` 來找出書中最常見的三元組。

if trigram_counter:
    print_most_common(trigram_counter)
else:
    print("trigram_counter 是空的。")


# ### 練習
#
# 現在讓我們實作馬可夫鏈文本分析，其中每個二元組對應到一個可能的後繼詞列表。
#
# 從 `add_bigram_to_successor_map` (原書為 `add_bigram`) 開始，寫一個叫做 `add_trigram_to_successor_map` (原書為 `add_trigram`) 的函數，
# 它接收一個包含三個單字的列表，並在 `successor_map` (這裡的 `successor_map` 鍵將是二元組) 中
# 新增或更新一個項目，使用前兩個單字作為鍵，第三個單字作為可能的後繼詞。

# 解答
# successor_map 將是全域的，鍵是二元組 (word1, word2)，值是 [word3_successor1, word3_successor2, ...]
# successor_map_trigram_key = {} # 用新名字以區分

def add_trigram_key_to_successor_map(trigram_list_input_sm): # 參數改名
    # 假設 successor_map_trigram_key 是全域的
    # global successor_map_trigram_key # 如果在函數內部賦值給全域名稱本身，才需要 global
                                    # 但這裡只是修改其內容，所以不需要

    if len(trigram_list_input_sm) != 3:
        print("錯誤: add_trigram_key_to_successor_map 需要一個包含三個單字的列表。")
        return

    first_tgk, second_tgk, third_successor_tgk = trigram_list_input_sm
    key_bigram_tgk = (first_tgk, second_tgk) # 用前兩個字當鍵

    if key_bigram_tgk not in successor_map_trigram_key: # successor_map_trigram_key 是練習的目標字典
        successor_map_trigram_key[key_bigram_tgk] = [third_successor_tgk]
    else:
        successor_map_trigram_key[key_bigram_tgk].append(third_successor_tgk)

# 這是 `process_word_for_trigram_count` (原書 `process_word_trigram`) 的一個版本，它呼叫 `add_trigram_key_to_successor_map`。
# (注意：書中的 `process_word_trigram` 在 In[159] 是用來計數的，這裡則是用來建立後繼詞對照表)
# 我們需要一個新的 process_word 函數

def process_word_for_trigram_key_successor_map(word_input_tgksm): # 參數改名
    # 假設 window 和 successor_map_trigram_key 是全域的
    window.append(word_input_tgksm)

    if len(window) == 3: # 形成三元組
        add_trigram_key_to_successor_map(window) # 加入到 (二元組 -> 後繼詞) 的對照表
        window.pop(0) # 滑動窗格

# 你可以用下面的迴圈來測試你的函數與 "Eric, the Half a Bee" 的歌詞。

successor_map_trigram_key = {} # 重設
window = []                    # 重設

print("\n--- 使用三元組 (前兩字為鍵) 建立歌曲的 successor_map ---")
# song_words 之前已處理好
if song_words:
    for word_from_song_tgksm in song_words:
        if word_from_song_tgksm:
            process_word_for_trigram_key_successor_map(word_from_song_tgksm)
else:
    print("song_words 是空的。")


# 如果你的函數運作正常，前導詞 `('half', 'a')` 應該對應到一個只包含元素 `'bee'` 的列表。
# 事實上，碰巧的是，這首歌中的每個二元組 (作為鍵) 都只出現一次，
# 所以 `successor_map_trigram_key` 中的所有值都只有一個元素。

if successor_map_trigram_key:
    for key_tgk_song, val_tgk_song_list in successor_map_trigram_key.items():
        print(f"{key_tgk_song}: {val_tgk_song_list}")
else:
    print("successor_map_trigram_key (歌曲) 是空的。")


# 你可以用下面的迴圈來測試你的函數與書中的單字。

successor_map_trigram_key = {} # 重設
window = []                    # 重設

print("\n--- 使用三元組 (前兩字為鍵) 建立書籍的 successor_map ---")
if exists(filename):
    for line in open(filename, encoding='utf-8'):
        for word_in_line_tgksm_book in split_line(line):
            cleaned_word_tgksm_book = clean_word(word_in_line_tgksm_book)
            if cleaned_word_tgksm_book:
                process_word_for_trigram_key_successor_map(cleaned_word_tgksm_book)
    print(f"建立完成，successor_map_trigram_key 中有 {len(successor_map_trigram_key)} 個項目。")
    # 隨便印幾個看看
    count_printed_tgksm_book = 0
    for k_tgksm, v_tgksm_list in successor_map_trigram_key.items():
        print(f"{k_tgksm}: {v_tgksm_list}")
        count_printed_tgksm_book +=1
        if count_printed_tgksm_book >= 5: break # 只印 5 個
else:
    print(f"錯誤: {filename} 未找到。")


# 在下一個練習中，你將使用這些結果來產生新的隨機文本。

# ### 練習
#
# 在這個練習中，我們假設 `successor_map_trigram_key` 是一個字典，
# 它把每個二元組對應到其後繼單字的列表。

# 這個儲存格會初始化隨機數產生器，
# 這樣每次執行這個 notebook 時，它都會從序列的同一個點開始。
random.seed(3)

# 要產生隨機文本，我們先從 `successor_map_trigram_key` 中隨機選擇一個鍵 (二元組)。

start_bigram_for_gen_tgk = None
if successor_map_trigram_key:
    # 確保只選擇有後繼詞的鍵
    valid_start_bigrams_tgk = [k_tgk for k_tgk, v_list_tgk in successor_map_trigram_key.items() if v_list_tgk]
    if valid_start_bigrams_tgk:
        start_bigram_for_gen_tgk = random.choice(valid_start_bigrams_tgk)
print(f"隨機選擇的起始二元組 (用於三元組生成): {start_bigram_for_gen_tgk}")


# 現在寫一個迴圈，依照以下步驟產生 50 個以上的單字：
#
# 1. 在 `successor_map_trigram_key` 中，查詢可以跟在 `start_bigram_for_gen_tgk` (目前的二元組) 後面的單字列表。
#
# 2. 從中隨機選擇一個並印出來 (或加入到生成文本列表中)。
#
# 3. 為了下一次迭代，建立一個新的二元組，它包含 `start_bigram_for_gen_tgk` 的第二個單字和剛才選擇的後繼詞。
#
# 例如，如果我們從二元組 `('doubted', 'if')` 開始，並選擇 `'from'` 作為其後繼詞，
# 那麼下一個二元組就是 `('if', 'from')`。

# 解答
print("\n--- 馬可夫鏈文本生成 (以 trigram/二元組鍵 為基礎) ---")
generated_text_tgk_list = []
current_bigram_for_gen = start_bigram_for_gen_tgk

if current_bigram_for_gen and successor_map_trigram_key:
    # 先把起始二元組的兩個字加進去
    generated_text_tgk_list.extend(list(current_bigram_for_gen))

    for i in range(50): # 生成 50 個「新」的字
        if current_bigram_for_gen in successor_map_trigram_key and successor_map_trigram_key[current_bigram_for_gen]:
            possible_successors_tgk = successor_map_trigram_key[current_bigram_for_gen]
            chosen_next_word_tgk = random.choice(possible_successors_tgk)
            generated_text_tgk_list.append(chosen_next_word_tgk)

            # 更新目前的二元組
            # 新的二元組是 (舊二元組的第二個字, 剛選出的字)
            current_bigram_for_gen = (current_bigram_for_gen[1], chosen_next_word_tgk)
        else:
            print(f"\n(二元組 '{current_bigram_for_gen}' 沒有後繼詞或不在 map 中，停止生成。)")
            break
    print(" ".join(generated_text_tgk_list))
else:
    print("無法開始生成文本 (起始二元組無效或 map 為空)。")


# 如果一切運作正常，你應該會發現生成的文本在風格上與原始文本可辨識地相似，
# 並且某些片語是有意義的，但文本可能會從一個主題跳到另一個主題。
#
# 作為一個額外練習，修改你最後兩個練習的解答，
# 使用三元組作為 `successor_map` 中的鍵 (即 (w1, w2, w3) -> [w4, ...])，
# 看看它對結果有什麼影響。
# (這會需要一個長度為 4 的窗格)

# (這個儲存格是空的，保留給可能的額外練習)

# (這個儲存格是空的)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)