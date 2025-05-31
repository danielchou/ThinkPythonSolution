# chap08_完整版.py

# -----------------------------------------------------------------------------
# Jupyter Notebook 元資訊 (保留供參考，在 .py 檔中無實際作用)
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---
# -----------------------------------------------------------------------------

# 你可以從 [Bookshop.org](https://bookshop.org/a/98697/9781098155438) 和
# [Amazon](https://www.amazon.com/_/dp/1098155432?smid=ATVPDKIKX0DER&_encoding=UTF8&tag=oreilly20-20&_encoding=UTF8&tag=greenteapre01-20&linkCode=ur2&linkId=e2a529f94920295d27ec8a06e757dc7c&camp=1789&creative=9325)
# 訂購《Think Python 3e》的實體書和電子書版本。

# -----------------------------------------------------------------------------
# 下載輔助函數及檔案 (原筆記本中的輔助工具)
# -----------------------------------------------------------------------------
from os.path import basename, exists
import os # 為了 os.path.exists 和檔案操作
import re # 為了正規表示式

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        try:
            local, _ = urlretrieve(url, filename)
            print("下載了 " + str(local))
        except Exception as e:
            print(f"下載 {filename} 失敗: {e}")
            print(f"請手動從 {url} 下載並放到與此腳本相同的目錄。")
    else:
        print(f"檔案 {filename} 已存在，跳過下載。")
    return filename

# --- 筆記本中下載的輔助檔案 ---
# 如果需要 thinkpython.py 和 diagram.py，可以取消以下註解來下載
# print("準備下載 thinkpython.py...")
# download('https://github.com/AllenDowney/ThinkPython/raw/v3/thinkpython.py')
# print("準備下載 diagram.py...")
# download('https://github.com/AllenDowney/ThinkPython/raw/v3/diagram.py')
# import thinkpython # 如果下載了 thinkpython.py 才能匯入

# --- 練習中會用到的檔案 ---
# words.txt (Wordle練習)
WORDS_TXT_URL = 'https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt'
WORDS_TXT_FILE = 'words.txt'
# print(f"準備下載 {WORDS_TXT_FILE}...")
# download(WORDS_TXT_URL)

# pg345.txt (Dracula - 德古拉)
DRACULA_URL = 'https://www.gutenberg.org/cache/epub/345/pg345.txt'
DRACULA_FILE = 'pg345.txt'
DRACULA_CLEANED_FILE = 'pg345_cleaned.txt'
DRACULA_REPLACED_FILE = 'pg345_replaced.txt'
# print(f"準備下載 {DRACULA_FILE}...")
# download(DRACULA_URL)

# pg1184.txt (The Count of Monte Cristo - 基督山恩仇記)
MONTECRISTO_URL = 'https://www.gutenberg.org/cache/epub/1184/pg1184.txt'
MONTECRISTO_FILE = 'pg1184.txt'
MONTECRISTO_CLEANED_FILE = 'pg1184_cleaned.txt'
# print(f"準備下載 {MONTECRISTO_FILE}...")
# download(MONTECRISTO_URL)

# -----------------------------------------------------------------------------
# 章節內容開始
# -----------------------------------------------------------------------------

# 字串與正規表示式

# 字串不像整數、浮點數和布林值那樣。字串是一種**序列（sequence）**，意思是它按照特定的順序包含多個值。
# 在本章中，我們將學習如何存取構成字串的那些值，並且會使用一些處理字串的函數。
#
# 我們還會用到正規表示式，這是一種非常強大的工具，可以用來在字串中尋找特定的模式（pattern），以及執行像是搜尋和取代這類的操作。
#
# 在練習部分，你將有機會把這些工具應用到一個叫做 Wordle 的文字遊戲上。

print("\n--- 字串是一種序列 ---")


# ## 字串是一種序列
#
# 字串是由一連串字元組成的序列。**字元（character）**可以是一個字母（幾乎可以是任何語言的字母）、一個數字、一個標點符號，或是空白字元。
#
# 你可以使用方括號運算子 `[]` 從字串中選取出某個字元。
# 下面這個範例敘述，會從 `fruit`（水果）這個字串中選取出編號為 1 的字元，
# 然後把它賦值（assign）給 `letter`（字母）這個變數：

fruit = 'banana' # 水果 = '香蕉'
letter = fruit[1]  # 字母 = 水果[1]
print(f"fruit = '{fruit}'")
print(f"letter = fruit[1] -> '{letter}'")

# 方括號裡面的那個表達式叫做**索引（index）**，因為它*指示*了要選取序列中的哪一個字元。
# 不過，結果可能跟你想的不太一樣喔。
# 索引為 `1` 的字母，實際上是字串的第二個字母。
# 這是因為索引是從字串的開頭算起的**偏移量（offset）**，所以第一個字母的偏移量是 `0`。
print(f"fruit[0] -> '{fruit[0]}'")

# 你可以把 `'b'` 想成是 `'banana'` 的第 0 個字母——發音可以想成「第零個」。
#
# 方括號裡的索引也可以是一個變數。
i = 1
print(f"i = {i}, fruit[i] -> '{fruit[i]}'")

# 或者是一個包含變數和運算子的表達式。
print(f"fruit[i+1] -> '{fruit[i+1]}'")

# 但是索引的值必須是整數——不然的話，你會得到一個 `TypeError`（型別錯誤）。
# # 下面這行程式碼會產生 TypeError，因為索引不能是小數
# try:
#     fruit[1.5]
# except TypeError as e:
#     print(f"fruit[1.5] 產生錯誤: {e}")

# 如同我們在第一章看到的，我們可以使用內建函數 `len` 來取得字串的長度。
n = len(fruit)
print(f"n = len(fruit) -> {n}")

# 要取得字串的最後一個字母，你Might會想這樣寫：
# # 下面這行程式碼會產生 IndexError，因為索引超出範圍了
# try:
#     fruit[n]
# except IndexError as e:
#     print(f"fruit[n] (fruit[6]) 產生錯誤: {e}")

# 但這樣會導致 `IndexError`（索引錯誤），因為在 `'banana'` 這個字串中，沒有索引為 6 的字母。因為我們是從 `0` 開始計數的，所以六個字母的編號是從 `0` 到 `5`。要取得最後一個字元，你必須從 `n` 減去 `1`：
print(f"fruit[n-1] -> '{fruit[n-1]}'")

# 不過，有個更簡單的方法。
# 要取得字串中的最後一個字母，你可以使用負數索引，它是從字串的末尾往前數。
print(f"fruit[-1] -> '{fruit[-1]}'")
# 索引 `-1` 會選取最後一個字母，`-2` 會選取倒數第二個字母，依此类推。

print("\n--- 字串切片 (String slices) ---")
# ## 字串切片 (String slices)
#
# 字串的一小段叫做**切片（slice）**。
# 選取切片跟選取字元很像。
fruit = 'banana'
print(f"fruit[0:3] -> '{fruit[0:3]}'")

# 運算子 `[n:m]` 會傳回字串中從第 `n` 個字元到第 `m` 個字元的部分，**包含**第一個（第 `n` 個），但**不包含**第二個（第 `m` 個）。
# 這行為有點違反直覺，但你可以想像索引是指向字元*之間*的位置。

# 例如，切片 `[3:6]` 會選取字母 `ana`，這表示 `6` 作為切片的一部分是合法的，但作為索引（`fruit[6]`）是不合法的。
print(f"fruit[3:6] -> '{fruit[3:6]}'")

# 如果你省略第一個索引，切片會從字串的開頭開始。
print(f"fruit[:3] -> '{fruit[:3]}'")

# 如果你省略第二個索引，切片會一直到字串的結尾：
print(f"fruit[3:] -> '{fruit[3:]}'")

# 如果第一個索引大於或等於第二個索引，結果會是一個**空字串（empty string）**，用兩個引號表示：
print(f"fruit[3:3] -> '{fruit[3:3]}'")

# 空字串不包含任何字元，長度為 0。
#
# 延續這個例子，你覺得 `fruit[:]` 是什麼意思呢？試試看就知道。
print(f"fruit[:] -> '{fruit[:]}'") # 結果會是整個 'banana' 字串

print("\n--- 字串是不可變的 (Strings are immutable) ---")
# ## 字串是不可變的 (Strings are immutable)
#
# 有時候我們會想用 `[]` 運算子在賦值的左邊，想要改變字串中的某個字元，像這樣：
greeting = 'Hello, world!'
# # 下面這行程式碼會產生 TypeError，因為字串是不可變的
# try:
#     greeting[0] = 'J'
# except TypeError as e:
#     print(f"greeting[0] = 'J' 產生錯誤: {e}")

# 結果是 `TypeError`（型別錯誤）。
# 在錯誤訊息中，「object」指的是字串，而「item」是我們試圖賦值的那個字元。
# 目前為止，**物件（object）**跟值（value）是同一樣東西，但我們之後會更精確地定義它。
#
# 發生這個錯誤的原因是，字串是**不可變的（immutable）**，這表示你不能改變一個已經存在的字串。
# 你能做的最好的方法是，創造一個新的字串，它是原始字串的一個變形。
new_greeting = 'J' + greeting[1:]
print(f"Original greeting: '{greeting}'")
print(f"New greeting: '{new_greeting}'")

# 這個例子把一個新的第一個字母，跟 `greeting` 從第二個字元開始的切片串接起來。
# 它對原始的字串 `greeting` 沒有任何影響。
print(f"Original greeting after creating new_greeting: '{greeting}'")

print("\n--- 字串比較 (String comparison) ---")
# ## 字串比較 (String comparison)
#
# 關係運算子（像是 `==`, `<`, `>`）可以用在字串上。要看看兩個字串是否相等，我們可以用 `==` 運算子。
word = 'banana'
if word == 'banana':
    print('沒錯，是香蕉。')

# 其他的關係運算，對於把單字按字母順序排列很有用：
def compare_word(word_to_compare): # 比較單字
    if word_to_compare < 'banana':
        print(f"'{word_to_compare}' 在 banana（香蕉）前面。")
    elif word_to_compare > 'banana':
        print(f"'{word_to_compare}' 在 banana（香蕉）後面。")
    else:
        print('沒錯，是香蕉。')

compare_word('apple') # 比較 'apple'（蘋果）

# Python 處理大寫和小寫字母的方式跟人類不太一樣。所有的大寫字母都排在所有的小寫字母前面，所以：
compare_word('Pineapple') # 比較 'Pineapple'（鳳梨）

# 要解決這個問題，我們可以在比較之前，把字串轉換成一種標準格式，例如全部轉成小寫。
# (例如: word_to_compare.lower() < 'banana')

print("\n--- 字串方法 (String methods) ---")
# ## 字串方法 (String methods)
#
# 字串提供了一些**方法（methods）**，可以執行各種有用的操作。
# 方法跟函數很像——它接受參數並傳回一個值——但是語法不太一樣。
# 例如，`upper` 方法會接受一個字串，然後傳回一個新的、所有字母都變成大寫的字串。
#
# 它不是用函數的語法 `upper(word)`，而是用方法的語法 `word.upper()`。
word = 'banana'
new_word = word.upper() # 把 'banana' 轉成大寫
print(f"word.upper() -> '{new_word}'")

# 這裡使用點運算子 `.` 來指定方法的名稱 `upper`，以及要套用這個方法的字串名稱 `word`。
# 空的括號 `()` 表示這個方法不接受任何參數。
#
# 呼叫一個方法稱為**調用（invocation）**；在這個例子中，我們會說我們在 `word` 這個字串上調用了 `upper` 方法。

# -----------------------------------------------------------------------------
# 檔案操作相關函數定義
# -----------------------------------------------------------------------------
def is_special_line(line): # 檢查是不是特殊行 (用於清理古騰堡計畫檔案)
    return line.startswith('*** ')

def clean_project_gutenberg_file(input_filename, output_filename):
    """ 清理古騰堡計畫的檔案，移除開頭結尾的輔助資訊。 """
    if not os.path.exists(input_filename):
        print(f"錯誤: clean_project_gutenberg_file - 輸入檔案 {input_filename} 不存在。")
        return False
    try:
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as reader:
            # 跳過開頭的版權資訊
            for line in reader:
                if is_special_line(line):
                    break # 找到第一個標記，跳出

            # 開始寫入正文
            with open(output_filename, 'w', encoding='utf-8') as writer:
                for line in reader:
                    if is_special_line(line):
                        break # 找到第二個標記，表示正文結束
                    writer.write(line)
        print(f"檔案 {input_filename} 已清理並存為 {output_filename}")
        return True
    except Exception as e:
        print(f"清理檔案 {input_filename} 時發生錯誤: {e}")
        return False

print("\n--- 寫入檔案 (Writing files) ---")
# ## 寫入檔案 (Writing files)
#
# 字串運算子和方法對於讀取和寫入文字檔案很有用。
# 作為範例，我們將處理《德古拉》（*Dracula*）的文本，這是布拉姆·斯托克（Bram Stoker）的小說，可以從古騰堡計畫（Project Gutenberg）取得。

# 下載並清理德古拉檔案 (如果尚未進行)
if not os.path.exists(DRACULA_CLEANED_FILE):
    if not os.path.exists(DRACULA_FILE):
        print(f"正在下載 {DRACULA_FILE}...")
        download(DRACULA_URL)
    if os.path.exists(DRACULA_FILE):
        print(f"正在清理 {DRACULA_FILE} 存到 {DRACULA_CLEANED_FILE}...")
        clean_project_gutenberg_file(DRACULA_FILE, DRACULA_CLEANED_FILE)
    else:
        print(f"{DRACULA_FILE} 不存在，無法進行清理。")

if os.path.exists(DRACULA_CLEANED_FILE):
    print(f"\n使用已清理的檔案: {DRACULA_CLEANED_FILE}")
    # 我已經把這本書下載成一個叫做 `pg345.txt` 的純文字檔案，我們可以像這樣打開它來讀取：
    # (現在我們用清理過的 DRACULA_CLEANED_FILE)
    try:
        with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as reader:
            # 除了書的文本之外，這個檔案在開頭包含了一些關於書的資訊，在結尾則包含了一些關於授權的資訊。
            # 在我們處理文本之前，我們可以藉由找到開頭和結尾那些以 `'***'` 開頭的特殊行來移除這些額外的材料。
            # (這一步驟已由 clean_project_gutenberg_file 完成)

            # 我們可以用 is_special_line 函數來遍歷檔案中的每一行，並且只印出那些特殊行。
            # (因為已經清理過，所以 DRACULA_CLEANED_FILE 中不應該再有特殊行)
            print(f"\n在 {DRACULA_CLEANED_FILE} 中尋找特殊行 (應該找不到):")
            found_special = False
            for line_num, line_content in enumerate(reader):
                if is_special_line(line_content):
                    print(f"在第 {line_num+1} 行找到特殊行: {line_content.strip()}")
                    found_special = True
            if not found_special:
                print("未在清理過的檔案中找到特殊行。")
            reader.seek(0) # 重置讀取指標到檔案開頭

            # 檢查清理後的檔案開頭幾行
            print(f"\n{DRACULA_CLEANED_FILE} 的前幾行內容:")
            for i in range(5):
                line = reader.readline()
                if not line: break
                print(line.strip())
    except FileNotFoundError:
        print(f"{DRACULA_CLEANED_FILE} 找不到，無法繼續此範例。")
    except Exception as e:
        print(f"讀取 {DRACULA_CLEANED_FILE} 時發生錯誤: {e}")
else:
    print(f"{DRACULA_CLEANED_FILE} 不存在，跳過檔案寫入範例的詳細演示。")


print("\n--- 尋找與取代 (Find and replace) ---")
# ## 尋找與取代 (Find and replace)
#
# 在1901年的冰島文版《德古拉》翻譯中，其中一個角色的名字從「Jonathan」改成了「Thomas」。
# 要在英文版中做出這個改變，我們可以遍歷這本書，使用 `replace` 方法把一個名字換成另一個，然後把結果寫到一個新檔案裡。
if os.path.exists(DRACULA_CLEANED_FILE):
    # 我們先來計算清理過的檔案版本中有多少行。
    total_lines = 0
    with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as reader:
        for line in reader:
            total_lines += 1
    print(f"{DRACULA_CLEANED_FILE} 總共有 {total_lines} 行。")

    # 要查看一行是否包含「Jonathan」，我們可以使用 `in` 運算子，它會檢查這個字元序列是否出現在該行的任何地方。
    lines_with_jonathan = 0
    with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as reader:
        for line in reader:
            if 'Jonathan' in line:
                lines_with_jonathan += 1
    print(f"包含 'Jonathan' 的行數: {lines_with_jonathan}")

    # 有 199 行包含這個名字，但這不完全是它出現的總次數，因為它可能在一行中出現多次。
    # 要得到總次數，我們可以使用 `count` 方法，它會傳回一個序列在字串中出現的次數。
    total_jonathan_occurrences = 0
    with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as reader:
        for line in reader:
            total_jonathan_occurrences += line.count('Jonathan')
    print(f"'Jonathan' 出現的總次數: {total_jonathan_occurrences}")

    # 現在我們可以像這樣把 `'Jonathan'` 取代成 `'Thomas'`：
    try:
        with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as reader, \
             open(DRACULA_REPLACED_FILE, 'w', encoding='utf-8') as writer:
            for line in reader:
                modified_line = line.replace('Jonathan', 'Thomas')
                writer.write(modified_line)
        print(f"已將 'Jonathan' 取代為 'Thomas' 並存入 {DRACULA_REPLACED_FILE}")

        # 驗證取代是否成功
        total_thomas_occurrences_in_replaced = 0
        with open(DRACULA_REPLACED_FILE, 'r', encoding='utf-8', errors='ignore') as reader:
            for line in reader:
                total_thomas_occurrences_in_replaced += line.count('Thomas')
        print(f"在 {DRACULA_REPLACED_FILE} 中 'Thomas' 出現的總次數: {total_thomas_occurrences_in_replaced}")
    except Exception as e:
        print(f"取代 'Jonathan' 時發生錯誤: {e}")
else:
    print(f"{DRACULA_CLEANED_FILE} 不存在，跳過尋找與取代範例。")


print("\n--- 正規表示式 (Regular expressions) ---")
# ## 正規表示式 (Regular expressions)
#
# 如果我們確切知道要找什麼樣的字元序列，我們可以用 `in` 運算子來找它，用 `replace` 方法來取代它。
# 但還有另一個工具，叫做**正規表示式（regular expression）**，它也能執行這些操作——而且能做的更多。
#
# 為了示範，我會從一個簡單的例子開始，然後慢慢進階。
# 假設，我們又想找出所有包含特定單字的行。
# 換個例子，讓我們找找書中提到主角德古拉伯爵（Count Dracula）的地方。
# 這裡有一行提到了他。
text_example = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."
print(f"示範文本: '{text_example}'")

# 這是我們將用來搜尋的**模式（pattern）**。
pattern_example = 'Dracula'
print(f"示範模式: '{pattern_example}'")

# 有一個叫做 `re` 的模組提供了與正規表示式相關的函數。
# 我們可以像這樣匯入它，然後使用 `search` 函數來檢查模式是否出現在文本中。
# (import re 已在檔案開頭)
result_re_search = re.search(pattern_example, text_example)
print(f"re.search('{pattern_example}', text_example) 的結果: {result_re_search}")

# 如果模式出現在文本中，`search` 會傳回一個 `Match` 物件，裡面包含了搜尋的結果。
# 在其他資訊中，它有一個名為 `string` 的變數，包含了被搜尋的文本。
if result_re_search:
    print(f"Match 物件的 .string 屬性: {result_re_search.string}")
    # 它還提供了一個叫做 `group` 的方法，會傳回文本中符合模式的部分。
    print(f"Match 物件的 .group() 方法: {result_re_search.group()}")
    # 並且它提供了一個叫做 `span` 的方法，會傳回模式在文本中開始和結束的索引位置。
    print(f"Match 物件的 .span() 方法: {result_re_search.span()}")

# 如果模式沒有出現在文本中，`search` 傳回的值會是 `None`。
result_re_search_none = re.search('Count', text_example)
print(f"re.search('Count', text_example) 的結果: {result_re_search_none}")

# 所以我們可以藉由檢查結果是否為 `None` 來判斷搜尋是否成功。
print(f"result_re_search_none == None -> {result_re_search_none == None}")

# 綜合以上，這裡有一個函數，它會遍歷書中的每一行，直到找到符合給定模式的那一行，然後傳回 `Match` 物件。
def find_first_match_in_file(pattern_to_find, filename):
    if not os.path.exists(filename):
        print(f"錯誤: find_first_match_in_file - 檔案 {filename} 不存在。")
        return None
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line_content in f:
                match_result = re.search(pattern_to_find, line_content)
                if match_result:
                    return match_result # 傳回第一個 Match 物件
    except Exception as e:
        print(f"在 {filename} 中尋找 '{pattern_to_find}' 時發生錯誤: {e}")
    return None # 如果找不到或發生錯誤

if os.path.exists(DRACULA_CLEANED_FILE):
    # 我們可以用它來尋找某個角色第一次被提到的地方。
    first_harker_match = find_first_match_in_file('Harker', DRACULA_CLEANED_FILE)
    if first_harker_match:
        print(f"\n在 {DRACULA_CLEANED_FILE} 中第一次提到 'Harker' 的行: {first_harker_match.string.strip()}")

    # 在這個例子中，我們其實不需要用正規表示式——用 `in` 運算子可以更簡單地做到同樣的事情。
    # 但是正規表示式可以做到 `in` 運算子做不到的事情。
    #
    # 例如，如果模式包含垂直線字元 `'|'`，它可以匹配左邊的序列**或**右邊的序列。
    # 假設我們想找到書中第一次提到 Mina Murray 的地方，但我們不確定她是先被提到姓還是名。
    # 我們可以使用下面的模式，它可以匹配任何一個名字。
    pattern_mina_murray = 'Mina|Murray'
    first_mina_murray_match = find_first_match_in_file(pattern_mina_murray, DRACULA_CLEANED_FILE)
    if first_mina_murray_match:
        print(f"第一次提到 '{pattern_mina_murray}' 的行: {first_mina_murray_match.string.strip()}")
        print(f"實際匹配到的內容: {first_mina_murray_match.group()}")


    # 我們可以用這樣的模式來看看一個角色被任一名字提到了多少次。
    # 這裡有一個函數，它會遍歷整本書，並計算符合給定模式的行數。
    def count_matching_lines_in_file(pattern_to_count, filename):
        if not os.path.exists(filename):
            print(f"錯誤: count_matching_lines_in_file - 檔案 {filename} 不存在。")
            return 0
        count = 0
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_content in f:
                    if re.search(pattern_to_count, line_content):
                        count += 1
        except Exception as e:
            print(f"在 {filename} 中計數 '{pattern_to_count}' 時發生錯誤: {e}")
        return count

    # 現在來看看 Mina 被提到了多少次 (在多少行中出現)。
    mina_murray_line_count = count_matching_lines_in_file(pattern_mina_murray, DRACULA_CLEANED_FILE)
    print(f"包含 'Mina' 或 'Murray' 的行數: {mina_murray_line_count}")

    # 特殊字元 `'^'` 會匹配字串的開頭，所以我們可以找到以給定模式開頭的行。
    first_dracula_start_match = find_first_match_in_file('^Dracula', DRACULA_CLEANED_FILE)
    if first_dracula_start_match:
        print(f"第一行以 'Dracula' 開頭的內容: {first_dracula_start_match.string.strip()}")

    # 而特殊字元 `'$'` 會匹配字串的結尾，所以我們可以找到以給定模式結尾的行（忽略結尾的換行符號）。
    # 為了讓 $ 能正確作用於字串內容而非包含換行符的整行，通常會先 strip()
    # 或者在正規表示式中使用 re.MULTILINE 配合 ^ 和 $ (但此處 search 是逐行處理)
    # 此處的 find_first_match_in_file 是逐行 search，所以 $ 會作用在該行內容的結尾 (換行符之前)
    first_harker_end_match = find_first_match_in_file('Harker$', DRACULA_CLEANED_FILE)
    if first_harker_end_match:
         # .string 會是整行，包含換行符。 .group() 才是匹配到的內容。
        print(f"第一行以 'Harker' 結尾的內容: {first_harker_end_match.string.strip()}")

else:
    print(f"{DRACULA_CLEANED_FILE} 不存在，跳過正規表示式檔案操作範例。")

print("\n--- 字串取代 (String substitution with re.sub) ---")
# ## 字串取代 (String substitution)
#
# 布拉姆·斯托克出生於愛爾蘭，當《德古拉》於1897年出版時，他住在英國。
# 所以我們預期他會使用英式拼法的單字，像是 "centre"（中心）和 "colour"（顏色）。
# 為了確認，我們可以使用下面的模式，它可以匹配 "centre" 或美式拼法的 "center"。
pattern_center = 'cent(er|re)' # 模式：匹配 'center' 或 'centre'
# 在這個模式中，括號 `()` 包住了垂直線 `|` 適用的部分。
# 所以這個模式會匹配以 `'cent'` 開頭，並以 `'er'` 或 `'re'` 結尾的序列。

if os.path.exists(DRACULA_CLEANED_FILE):
    first_center_match = find_first_match_in_file(pattern_center, DRACULA_CLEANED_FILE)
    if first_center_match:
        print(f"\n找到符合 '{pattern_center}' 的行: {first_center_match.string.strip()}")
        print(f"實際匹配: {first_center_match.group()}")

    # 我們也可以檢查他是否用了英式拼法的 "colour"。
    # 下面的模式使用了特殊字元 `'?'`，它表示前一個字元是**可選的**（optional），可有可無。
    pattern_colour = 'colou?r' # 模式：'u' 是可選的，所以可以匹配 'color' 或 'colour'
    # 這個模式可以匹配有 `'u'` 的 "colour" 或沒有 `'u'` 的 "color"。
    first_colour_match = find_first_match_in_file(pattern_colour, DRACULA_CLEANED_FILE)
    if first_colour_match:
        line_with_colour = first_colour_match.string
        print(f"找到符合 '{pattern_colour}' 的行: {line_with_colour.strip()}")
        print(f"實際匹配: {first_colour_match.group()}")

        # 現在假設我們想出版一本使用美式拼法的書。
        # 我們可以使用 `re` 模組中的 `sub` 函數，它可以做**字串取代（string substitution）**。
        american_spelling_line = re.sub(pattern_colour, 'color', line_with_colour)
        print(f"用 re.sub 將 '{pattern_colour}' 取代為 'color' 後: {american_spelling_line.strip()}")
        # 第一個參數是我們要尋找並取代的模式，第二個是我們想要取代成的內容，第三個是我們要搜尋的字串。
        # 在結果中，你可以看到 "colour" 已經被取代成了 "color"。
else:
    print(f"{DRACULA_CLEANED_FILE} 不存在，跳過 re.sub 範例。")


print("\n--- 除錯 (Debugging) ---")
# ## 除錯 (Debugging)
#
# 當你在讀寫檔案時，除錯可能會有點棘手。
# 如果你在 Jupyter Notebook 環境中工作，你可以使用**shell 指令**來幫忙。
# 例如，要顯示檔案的前幾行，你可以用 `!head` 指令，像這樣：
# `!head pg345_cleaned.txt` (這是在 Jupyter Notebook 或終端機中執行的 shell 指令)
# Python 中可以用檔案讀取的前N行來模擬：
print(f"模擬 'head' 指令顯示 {DRACULA_CLEANED_FILE} 的前3行:")
if os.path.exists(DRACULA_CLEANED_FILE):
    try:
        with open(DRACULA_CLEANED_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for _ in range(3):
                line = f.readline()
                if not line: break
                print(line.strip())
    except Exception as e:
        print(f"模擬 head 時發生錯誤: {e}")
else:
    print(f"{DRACULA_CLEANED_FILE} 不存在。")


# 開頭的驚嘆號 `!` 表示這是一個 shell 指令，它不是 Python 的一部分。
# 要顯示最後幾行，你可以用 `!tail`。
# `!tail pg345_cleaned.txt` (shell 指令)

# 當你處理大型檔案時，除錯可能會很困難，因為輸出的內容可能太多，無法手動檢查。
# 一個好的除錯策略是，先從檔案的一小部分開始，讓程式可以正確運作，然後再用整個檔案去執行它。
#
# 要建立一個包含較大檔案一部分內容的小檔案，我們可以再次使用 `!head` 搭配重新導向運算子 `>`，
# 它表示結果應該被寫入檔案，而不是顯示出來。
# `!head pg345_cleaned.txt > pg345_cleaned_10_lines.txt` (shell 指令)
#
# 預設情況下，`!head` 會讀取前 10 行，但它可以接受一個可選的參數，來指示要讀取的行數。
# `!head -100 pg345_cleaned.txt > pg345_cleaned_100_lines.txt` (shell 指令)
#
# 這個 shell 指令會從 `pg345_cleaned.txt` 讀取前 100 行，並把它們寫入一個叫做 `pg345_cleaned_100_lines.txt` 的檔案。
#
# 注意：shell 指令 `!head` 和 `!tail` 並非在所有作業系統上都可用。
# 如果它們在你的系統上無法運作，我們可以用 Python 寫出類似的函數。
# 請參考本章末尾的第一個練習的建議。


# -----------------------------------------------------------------------------
# ## 詞彙表 (Glossary)
# -----------------------------------------------------------------------------
# **sequence (序列):**
#   一個有序的值的集合，其中每個值都由一個整數索引來識別。
#
# **character (字元):**
#   字串的一個元素，包括字母、數字和符號。
#
# **index (索引):**
#   一個整數值，用來選取序列中的一個項目，例如字串中的一個字元。在 Python 中，索引從 `0` 開始。
#
# **slice (切片):**
#   字串的一部分，由一個索引範圍指定。
#
# **empty string (空字串):**
#   一個不包含任何字元且長度為 `0` 的字串。
#
# **object (物件):**
#   變數可以參考（指向）的東西。一個物件有它的型別和值。
#
# **immutable (不可變的):**
#   如果一個物件的元素不能被改變，那麼這個物件就是不可變的。
#
# **invocation (調用):**
#   一個表達式——或表達式的一部分——它呼叫了一個方法。
#
# **regular expression (正規表示式):**
#   一個定義搜尋模式的字元序列。
#
# **pattern (模式):**
#   一個規則，指定了一個字串必須滿足什麼樣的要求才算是符合（match）。
#
# **string substitution (字串取代):**
#   將一個字串，或字串的一部分，用另一個字串取代。
#
# **shell command (shell 指令):**
#   shell 語言中的一個陳述式，shell 語言是用來與作業系統互動的語言。

# -----------------------------------------------------------------------------
# ## 練習 (Exercises)
# -----------------------------------------------------------------------------
print("\n\n--- 練習 ---")

# Jupyter Notebook 中的 %xmode Verbose 指令，用於更詳細的錯誤追蹤。
# 在 .py 腳本中無直接對應，Python 預設會提供 traceback。

# ### 問問虛擬助理 (此為文字說明，非程式碼)
#
# 在本章中，我們只稍微談到了正規表示式能做什麼。
# 為了了解它還有哪些可能性，可以問問虛擬助理：「Python 正規表示式中最常用的特殊字元有哪些？」
#
# 你也可以請它幫你寫一個符合特定字串種類的模式。
# 例如，試著問問：
#
# *   寫一個 Python 正規表示式，用來匹配帶有連字號的 10 位數電話號碼。
# *   寫一個 Python 正規表示式，用來匹配包含號碼和街道名稱，後面跟著 `ST` 或 `AVE` 的街道地址。
# *   寫一個 Python 正規表示式，用來匹配一個完整的姓名，包含任何常見的稱謂（如 `Mr` 或 `Mrs`），後面跟著任意數量以大寫字母開頭的名字，名字之間可能帶有連字號。
#
# 如果你想看更複雜的，試著問問看匹配任何合法 URL 的正規表示式。
#
# 正規表示式通常在引號前面會有一個字母 `r`，表示它是一個「原始字串（raw string）」。
# 想知道更多資訊，可以問問虛擬助理：「Python 中的原始字串是什麼？」

print("\n--- 練習 1: 實作 head 函數 ---")
# ### 練習
#
# 試試看你能不能寫一個函數，做到跟 shell 指令 `!head` 一樣的事情。
# 它應該接受以下參數：要讀取的檔案名稱、要讀取的行數，以及要把這些行寫入的檔案名稱。
# 如果第三個參數是 `None`，它應該直接顯示這些行，而不是把它們寫入檔案。
#
# 可以考慮請虛擬助理幫忙，但如果你這樣做，告訴它不要使用 `with` 陳述式或 `try` 陳述式。
# (譯註：`with` 和 `try` 是比較進階的語法，這裡的練習希望你用目前學到的基礎語法來完成。)
# (下方解答已使用 with 和 try-except 以求穩健)

def head_exercise_solution(input_file_path, num_lines_to_read=10, output_file_path=None):
    """
    讀取輸入檔案的前 num_lines 行。
    如果 output_file_path 不是 None，就將這些行寫入 output_file_path。
    否則，將這些行印到螢幕上。
    """
    if not os.path.exists(input_file_path):
        print(f"錯誤: head - 輸入檔案 {input_file_path} 不存在。")
        return

    try:
        reader = open(input_file_path, 'r', encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"打開輸入檔案 {input_file_path} 失敗: {e}")
        return

    writer_obj = None
    if output_file_path is not None:
        try:
            writer_obj = open(output_file_path, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打開輸出檔案 {output_file_path} 失敗: {e}")
            reader.close()
            return

    try:
        for _ in range(num_lines_to_read):
            line_content = reader.readline()
            if not line_content: # 如果讀不到東西 (例如檔案行數不夠)
                break

            if writer_obj is not None:
                writer_obj.write(line_content)
            else:
                print(line_content, end='') # end='' 是為了避免多一個換行
    except Exception as e:
        print(f"讀取/寫入時發生錯誤: {e}")
    finally:
        reader.close()
        if writer_obj is not None:
            writer_obj.close()

# 測試 head 函數
if os.path.exists(DRACULA_CLEANED_FILE):
    print(f"\n測試 head_exercise_solution (印出 {DRACULA_CLEANED_FILE} 前3行到螢幕):")
    head_exercise_solution(DRACULA_CLEANED_FILE, 3)

    temp_head_output_file = 'temp_head_output.txt'
    print(f"\n測試 head_exercise_solution (將 {DRACULA_CLEANED_FILE} 前5行寫入 {temp_head_output_file}):")
    head_exercise_solution(DRACULA_CLEANED_FILE, 5, temp_head_output_file)
    if os.path.exists(temp_head_output_file):
        print(f"{temp_head_output_file} 已產生。內容:")
        with open(temp_head_output_file, 'r', encoding='utf-8') as f_temp:
            print(f_temp.read())
        # os.remove(temp_head_output_file) # 清理臨時檔案
    else:
        print(f"{temp_head_output_file} 未產生。")
else:
    print(f"{DRACULA_CLEANED_FILE} 不存在，無法測試 head_exercise_solution。")


print("\n--- 練習 2 & 3: Wordle 遊戲邏輯 ---")
# ### 練習 (Wordle)
#
# "Wordle" 是一個線上的文字遊戲，目標是在六次或更少次的嘗試中猜出一個五個字母的單字。
# 每次嘗試都必須是一個被認可的單字，不包含專有名詞。
# 每次嘗試後，你會得到關於你猜的字母中，哪些出現在目標單字裡，以及哪些位置正確的資訊。
#
# 例如，假設目標單字是 `MOWER`，而你猜了 `TRIED`。
# 你會知道 `E` 在目標單字中且位置正確，`R` 在目標單字中但位置不正確，而 `T`、`I` 和 `D` 都不在目標單字中。
#
# 另一個例子，假設你已經猜了 `SPADE` 和 `CLERK` 這兩個字，並且你知道 `E` 在目標單字中，但不在這兩個猜測中的位置，而且其他猜過的字母（S,P,A,D,C,L,R,K）都不在目標單字中。
# 在單字列表裡，有多少個單字可能是目標單字呢？
# 寫一個叫做 `check_word` 的函數，它接受一個五個字母的單字，並根據這些猜測來檢查它是否可能是目標單字。

# 你可以使用前一章的任何函數，像是 `uses_any`。
def uses_any(word_to_check, letters_to_check):
    """
    檢查 word_to_check 中是否包含 letters_to_check 中的任何一個字母。
    """
    for letter_in_word in word_to_check.lower(): # 把 word 轉小寫，然後一個個字母檢查
        if letter_in_word in letters_to_check.lower(): # 如果這個字母也在 letters (也轉小寫) 裡面
            return True # 就代表找到了，傳回 True
    return False # 如果整個迴圈跑完都沒找到，傳回 False

def check_word_wordle1(word_candidate):
    # 條件1: 'e' 必須在單字中
    if 'e' not in word_candidate:
        return False

    # 條件2: 'e' 不能在 SPADE 的 'E' 位置 (索引2) 或 CLERK 的 'E' 位置 (索引4)
    # fruit[2] 是第三個字母，fruit[4] 是第五個字母
    if len(word_candidate) == 5: # 確保長度為5才進行索引
        if word_candidate[2] == 'e' or word_candidate[4] == 'e':
            return False
    else: # 如果長度不為5，直接不符合
        return False

    # 條件3: 單字中不能包含 's', 'p', 'a', 'd', 'c', 'l', 'r', 'k' 這些字母
    if uses_any(word_candidate, 'spadclrk'):
        return False

    # 如果以上條件都通過，代表這個單字可能是答案
    return True

if os.path.exists(WORDS_TXT_FILE):
    print("\nWordle 練習 1: SPADE, CLERK 後的可能字")
    possible_words_count1 = 0
    with open(WORDS_TXT_FILE, 'r') as f_words:
        for line in f_words:
            word_from_list = line.strip().lower() # Wordle 通常不分大小寫，且無前後空白
            if len(word_from_list) == 5 and check_word_wordle1(word_from_list):
                # print(word_from_list) # 印出符合的字太多，註解掉
                possible_words_count1 += 1
    print(f"第一輪 (SPADE, CLERK) 後，符合條件的五字母單字總共有：{possible_words_count1} 個")
else:
    print(f"{WORDS_TXT_FILE} 檔案不存在，無法執行 Wordle 練習 1。")


# ### 練習 (Wordle 續)
#
# 延續上一個練習，假設你猜了 `TOTEM` 這個字，然後得知 `E` *仍然*不在正確的位置，但是 `M` 的位置是正確的。那還剩下多少個可能的單字呢？
# (譯註：`TOTEM` 的 `E` 在索引3，`M` 在索引4)

def check_word_wordle2(word_candidate):
    # 條件1: 必須先通過 check_word_wordle1 的所有檢查
    if not check_word_wordle1(word_candidate):
        return False

    # 假設 word_candidate 長度必為5 (因為 check_word_wordle1 會檢查)
    # 條件2: 'e' 不能在 TOTEM 的 'E' 位置 (索引3)
    if word_candidate[3] == 'e':
        return False

    # 條件3: 'm' 必須在 TOTEM 的 'M' 位置 (索引4)
    if word_candidate[4] != 'm':
        return False

    # 條件4: 't' 和 'o' 不在目標字中 (因為 TOTEM 中 T 和 O 沒亮燈，假設它們是灰色)
    # 這個假設基於 Wordle 的常見玩法：如果字母不在字中，則為灰色。
    if uses_any(word_candidate, 'to'):
        return False

    # 如果以上條件都通過
    return True

if os.path.exists(WORDS_TXT_FILE):
    print("\nWordle 練習 2: 再猜 TOTEM 後的可能字")
    possible_words_count2 = 0
    with open(WORDS_TXT_FILE, 'r') as f_words:
        for line in f_words:
            word_from_list = line.strip().lower()
            if len(word_from_list) == 5 and check_word_wordle2(word_from_list):
                print(f"找到可能單字: {word_from_list}") # 這次結果應該不多，可以印出
                possible_words_count2 += 1
    print(f"第二輪 (再猜 TOTEM) 後，符合條件的五字母單字總共有：{possible_words_count2} 個")
else:
    print(f"{WORDS_TXT_FILE} 檔案不存在，無法執行 Wordle 練習 2。")


print("\n--- 練習 4: 《基督山恩仇記》中 'pale' 相關詞計數 ---")
# ### 練習
#
# 《基督山恩仇記》（*The Count of Monte Cristo*）是亞歷山大·仲馬（Alexandre Dumas）的一部被視為經典的小說。
# 然而，在這本書的英文譯本序言中，作家安伯托·艾可（Umberto Eco）坦承他覺得這本書是「有史以來寫得最糟糕的小說之一」。
#
# 他特別提到，書中「無恥地重複使用相同的形容詞」，並特別指出「書中角色要嘛不寒
# 栗（shudder），要嘛臉色蒼白（turn pale）」的次數。
#
# 為了看看他的批評是否有道理，讓我們來計算一下包含任何形式的 `pale` 這個字的行數，包括 `pale`、`pales`、`paled` 和 `paleness`，以及相關的字 `pallor`。
# 使用一個正規表示式來匹配這些字中的任何一個。
# 作為額外的挑戰，確保它不會匹配到其他字，像是 `impale`——你可能需要請虛擬助理幫忙。

# 下載並清理基督山恩仇記檔案 (如果尚未進行)
if not os.path.exists(MONTECRISTO_CLEANED_FILE):
    if not os.path.exists(MONTECRISTO_FILE):
        print(f"正在下載 {MONTECRISTO_FILE}...")
        download(MONTECRISTO_URL)
    if os.path.exists(MONTECRISTO_FILE):
        print(f"正在清理 {MONTECRISTO_FILE} 存到 {MONTECRISTO_CLEANED_FILE}...")
        clean_project_gutenberg_file(MONTECRISTO_FILE, MONTECRISTO_CLEANED_FILE)
    else:
        print(f"{MONTECRISTO_FILE} 不存在，無法進行清理。")


def count_matching_lines_regex(pattern_str, filename, ignore_case=True):
    """計算指定檔案中，符合正規表示式模式的行數。"""
    if not os.path.exists(filename):
        print(f"錯誤: count_matching_lines_regex - 檔案 {filename} 找不到。")
        return 0
    count = 0
    try:
        flags = re.IGNORECASE if ignore_case else 0
        compiled_pattern = re.compile(pattern_str, flags) # 編譯模式以提高效率
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line_content in f:
                if compiled_pattern.search(line_content):
                    count += 1
    except Exception as e:
        print(f"在 {filename} 中用模式 '{pattern_str}' 計數時發生錯誤: {e}")
    return count

if os.path.exists(MONTECRISTO_CLEANED_FILE):
    # 解法1: 只用了本章學到的功能 (可能匹配到 impale)
    # (pale|pales|paled|paleness|pallor)
    # 為了讓它更有彈性，我們用 re.IGNORECASE 來忽略大小寫 (已在函數中處理)
    pattern_pale1 = r'(pale|pales|paled|paleness|pallor)'
    num_matches_pale1 = count_matching_lines_regex(pattern_pale1, MONTECRISTO_CLEANED_FILE)
    print(f"使用模式 '{pattern_pale1}' (可能匹配到 'impale' 等)，符合的行數：{num_matches_pale1}")

    # 解法2: 使用了特殊序列 \b 來匹配單字的邊界
    # \b 是零寬度斷言，匹配單字字元(\w)和非單字字元(\W)之間的位置。
    # 引號前的 r 表示這個模式是一個原始字串 (raw string)。
    pattern_pale2 = r'\b(pale|pales|paled|paleness|pallor)\b'
    num_matches_pale2 = count_matching_lines_regex(pattern_pale2, MONTECRISTO_CLEANED_FILE)
    print(f"使用模式 '{pattern_pale2}' (使用字詞邊界 \\b)，符合的行數：{num_matches_pale2}")
    # 根據這個計數，這些詞在書中出現了相當多次，艾可先生的觀點可能有道理。
else:
    print(f"{MONTECRISTO_CLEANED_FILE} 不存在，無法執行 'pale' 計數練習。")


# -----------------------------------------------------------------------------
# 版權與授權資訊
# -----------------------------------------------------------------------------
# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# Code license: [MIT License](https://mit-license.org/)
#
# Text license: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

print("\n--- 腳本結束 ---")