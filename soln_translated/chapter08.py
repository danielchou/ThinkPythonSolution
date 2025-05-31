# 從 chap08.ipynb 轉換而來
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

# # 字串與正規表示式 (Strings and Regular Expressions)
#
# 字串 (String) 跟整數 (integer)、浮點數 (float) 和布林值 (boolean) 不太一樣。字串是一種 **序列 (sequence)**，
# 意思就是它按照特定順序包含多個值。
# 在這一章，我們會學習如何存取組成字串的這些值，並且使用一些處理字串的函數。
#
# 我們也會用到正規表示式 (regular expression)，這是一個強大的工具，可以用來在字串中尋找模式 (pattern)
# 以及執行像是搜尋和取代這類的操作。
#
# 作為練習，你將有機會把這些工具應用到一個叫做 Wordle 的文字遊戲上。

# ## 字串是一個序列 (A string is a sequence)
#
# 字串是由一連串字元 (character) 組成的。一個 **字元** 可以是一個字母（幾乎任何字母系統的字母都可以）、
# 一個數字、一個標點符號，或是空白字元 (white space)。
#
# 你可以用中括號運算子 `[]` 從字串中選取一個字元。
# 下面這個範例陳述式會從 `fruit` 中選取編號為 1 的字元，
# 然後把它指派給變數 `letter`：

fruit = 'banana'
letter = fruit[1]

# 中括號裡面的表達式叫做 **索引 (index)**，因為它 *指出* (indicates) 要選取序列中的哪一個字元。
# 但是，結果可能跟你想的不太一樣喔。

letter

# 索引為 `1` 的字母，實際上是字串的第二個字母。
# 索引是從字串開頭算起的位移量 (offset)，所以第一個字母的位移量是 `0`。

fruit[0]

# 你可以把 `'b'` 想成是 `'banana'` 的第 0 個 (zero-eth) 字母。
#
# 中括號裡的索引可以是一個變數。

i = 1
fruit[i]

# 或者是一個包含變數和運算子的表達式。

fruit[i+1]

# 但是索引的值必須是一個整數——不然你會得到一個 `TypeError`（型別錯誤）。

%%expect TypeError

fruit[1.5]

# 如同我們在第一章看到的，我們可以用內建函數 `len` 來取得字串的長度。

n = len(fruit)
n

# 要取得字串的最後一個字母，你可能會想這樣寫：

%%expect IndexError

fruit[n]

# 但是這樣會造成 `IndexError`（索引錯誤），因為在 `'banana'` 這個字串裡，沒有索引為 6 的字母。
# 因為我們是從 `0` 開始數，所以六個字母的編號是 `0` 到 `5`。
# 要取得最後一個字元，你必須從 `n` 減掉 `1`：

fruit[n-1]

# 不過，有個更簡單的方法。
# 要取得字串的最後一個字母，你可以用負數索引 (negative index)，它是從字串尾巴倒著數回來。

fruit[-1]

# 索引 `-1` 選取的是最後一個字母，`-2` 選取的是倒數第二個，依此类推。

# ## 字串切片 (String slices)
#
# 字串的一個片段叫做 **切片 (slice)**。
# 選取一個切片跟選取一個字元很像。

fruit = 'banana'
fruit[0:3]

# 運算子 `[n:m]` 會回傳字串中從第 `n` 個字元到第 `m` 個字元的片段，
# 其中包含第一個 (第 `n` 個)，但不包含第二個 (第 `m` 個)。
# 這種行為有點違反直覺，但你可以想像索引是指向字元*之間*的位置，像下面這張圖一樣：

from diagram import make_binding, Element, Value

binding = make_binding("fruit", ' b a n a n a ')
elements = [Element(Value(i), None) for i in range(7)]

import matplotlib.pyplot as plt
from diagram import diagram, adjust
from matplotlib.transforms import Bbox

width, height, x, y = [1.35, 0.54, 0.23, 0.39]

ax = diagram(width, height)
bbox = binding.draw(ax, x, y)
bboxes = [bbox]

def draw_elts(x, y, elements):
    for elt in elements:
        bbox = elt.draw(ax, x, y, draw_value=False)
        bboxes.append(bbox)

        x1 = (bbox.xmin + bbox.xmax) / 2
        y1 = bbox.ymax + 0.02
        y2 = y1 + 0.14
        handle = plt.plot([x1, x1], [y1, y2], ':', lw=0.5, color='gray')
        x += 0.105

draw_elts(x + 0.48, y - 0.25, elements)
bbox = Bbox.union(bboxes)
# adjust(x, y, bbox)

# 舉例來說，切片 `[3:6]` 選取的是字母 `ana`，這表示 `6` 作為切片的一部分是合法的，
# 但作為單獨的索引是不合法的。
#
#
# 如果你省略第一個索引，切片會從字串的開頭開始。

fruit[:3]

# 如果你省略第二個索引，切片會一直到字串的結尾：

fruit[3:]

# 如果第一個索引大於或等於第二個索引，結果會是一個 **空字串 (empty string)**，
# 用兩個引號 `""` 表示：

fruit[3:3]

# 空字串不包含任何字元，長度是 0。
#
# 延續這個例子，你覺得 `fruit[:]` 是什麼意思呢？試試看就知道了。

fruit[:]

# ## 字串是不可變的 (Strings are immutable)
#
# 你可能會很想在等號的左邊使用 `[]` 運算子，
# 想要改變字串中的某個字元，像這樣：

%%expect TypeError

greeting = 'Hello, world!'
greeting[0] = 'J'

# 結果是 `TypeError`（型別錯誤）。
# 在錯誤訊息中，"object" (物件) 指的是字串，而 "item" (項目) 指的是我們試圖指派的字元。
# 目前來說，**物件 (object)** 跟值 (value) 是一樣的東西，但我們之後會再 уточнить (refine) 這個定義。
#
# 發生這個錯誤的原因是字串是 **不可變的 (immutable)**，意思是你不能改變一個已經存在的字串。
# 你能做的最好的方法，就是創造一個新的字串，它是原始字串的變形。

new_greeting = 'J' + greeting[1:]
new_greeting

# 這個例子把一個新的第一個字母串接到 `greeting` 的一個切片上。
# 它對原始的字串沒有任何影響。

greeting

# ## 字串比較 (String comparison)
#
# 關係運算子 (relational operators) 也可以用在字串上。要看看兩個字串是否相等，
# 我們可以用 `==` 運算子。

word = 'banana'

if word == 'banana':
    print('沒錯，是香蕉。') # 口語化一點

# 其他的關係運算在按照字母順序排列單字時很有用：

def compare_word(word):
    if word < 'banana':
        print(word, '排在 banana 前面。')
    elif word > 'banana':
        print(word, '排在 banana 後面。')
    else:
        print('沒錯，是 banana。') # 口語化一點

compare_word('apple')

# Python 處理大寫和小寫字母的方式跟人類不太一樣。
# 所有的大寫字母都排在所有的小寫字母前面，所以：

compare_word('Pineapple')

# 為了處理這個問題，我們可以在比較之前，把字串轉換成一個標準格式，例如全部轉成小寫。
# 如果你哪天需要用鳳梨 (Pineapple) 跟人搏鬥，記得這點。 (這句是原文的幽默，保留一下趣味性)

# ## 字串方法 (String methods)
#
# 字串提供了一些方法 (method)，可以執行各種有用的操作。
# 方法跟函數很像——它會接收參數並回傳一個值——但是語法不太一樣。
# 例如，`upper` 方法會接收一個字串，然後回傳一個新的、全部是大寫字母的字串。
#
# 它不是用函數的語法 `upper(word)`，而是用方法的語法 `word.upper()`。

word = 'banana'
new_word = word.upper()
new_word

# 這裡的點運算子 (`.`) 指定了方法的名稱 `upper`，以及要套用這個方法的字串名稱 `word`。
# 空的括號 `()` 表示這個方法不需要任何參數。
#
# 一個方法呼叫 (method call) 被稱為 **調用 (invocation)**；在這個例子中，我們會說我們在 `word` 上調用了 `upper` 方法。

# ## 寫入檔案 (Writing files)
#
# 字串運算子和方法在讀取和寫入文字檔案時很有用。
# 作為例子，我們會處理《德古拉》(Dracula) 這本小說的文本，這是布蘭·斯托克 (Bram Stoker) 的作品，
# 可以從古騰堡計畫 (Project Gutenberg) 取得 (<https://www.gutenberg.org/ebooks/345>)。

import os

if not os.path.exists('pg345.txt'):
    !wget https://www.gutenberg.org/cache/epub/345/pg345.txt

# 我已經把這本書下載成一個叫做 `pg345.txt` 的純文字檔，我們可以像這樣開啟它來讀取：

reader = open('pg345.txt')

# 除了書的本文之外，這個檔案在開頭包含了一些關於書的資訊，在結尾則包含了一些關於授權的資訊。
# 在我們處理文本之前，我們可以藉由找到開頭和結尾那些以 `'***'` 開始的特殊行來移除這些額外的內容。
#
# 下面的函數會接收一行文字，然後檢查它是不是其中一個特殊行。
# 它使用了 `startswith` 方法，這個方法會檢查一個字串是不是以給定的字元序列開頭。

def is_special_line(line):
    return line.startswith('*** ')

# 我們可以用這個函數來遍歷檔案中的每一行，並且只印出那些特殊行。

for line in reader:
    if is_special_line(line):
        print(line.strip()) # strip() 會移除頭尾空白，讓輸出更整潔

# 現在讓我們建立一個新的檔案，叫做 `pg345_cleaned.txt`，裡面只包含書的本文。
# 為了再次遍歷這本書，我們必須重新開啟它來讀取。
# 而且，要寫入一個新的檔案，我們可以開啟它來寫入。

reader = open('pg345.txt')
writer = open('pg345_cleaned.txt', 'w')

# `open` 函數可以接受一個選擇性的參數來指定 "模式 (mode)" —— 在這個例子中，`'w'` 表示我們是以寫入模式開啟檔案。
# 如果檔案不存在，它會被建立；如果檔案已經存在，它的內容會被取代。
#
# 作為第一步，我們會遍歷檔案，直到找到第一個特殊行為止。

for line in reader:
    if is_special_line(line):
        break

# `break` 陳述式會 "跳出 (breaks)" 迴圈 —— 也就是說，它會讓迴圈立刻結束，
# 在我們讀到檔案結尾之前就結束。
#
# 當迴圈結束時，`line` 變數會包含那個讓條件判斷為 `True` (成立) 的特殊行。

line

# 因為 `reader` 會記錄它在檔案中讀到哪裡了，所以我們可以用第二個迴圈從上次離開的地方繼續。
#
# 下面的迴圈會一行一行地讀取檔案剩下的內容。
# 當它找到表示文本結束的特殊行時，它會跳出迴圈。
# 否則，它會把該行寫入到輸出檔案。

for line in reader:
    if is_special_line(line):
        break
    writer.write(line)

# 當這個迴圈結束時，`line` 變數會包含第二個特殊行。

line

# 此時 `reader` 和 `writer` 仍然是開啟的，這表示我們可以繼續從 `reader` 讀取行，
# 或向 `writer` 寫入行。
# 為了表示我們已經完成了，我們可以藉由調用 `close` 方法來關閉這兩個檔案。

reader.close()
writer.close()

# 為了檢查這個過程是否成功，我們可以從我們剛剛建立的新檔案中讀取前幾行。

for line in open('pg345_cleaned.txt'):
    line = line.strip() # 移除頭尾空白
    if len(line) > 0:   # 只印出非空白行
        print(line)
    if line.endswith('Stoker'): # 檢查是否以 'Stoker' 結尾
        break

# `endswith` 方法會檢查一個字串是否以給定的字元序列結尾。

# ## 尋找與取代 (Find and replace)
#
# 在 1901 年的《德古拉》冰島文譯本中，其中一個角色的名字從 "Jonathan" 改成了 "Thomas"。
# 要在英文版中做這個修改，我們可以遍歷這本書，用 `replace` 方法把一個名字換成另一個，
# 然後把結果寫到一個新檔案。
#
# 我們先來計算一下清理過的檔案版本中有多少行。

total = 0
for line in open('pg345_cleaned.txt'):
    total += 1

total

# 要看看一行文字是否包含 "Jonathan"，我們可以用 `in` 運算子，
# 它會檢查這個字元序列是否出現在該行中的任何地方。

total = 0
for line in open('pg345_cleaned.txt'):
    if 'Jonathan' in line:
        total += 1

total

# 有 199 行包含這個名字，但這還不是它出現的總次數，
# 因為它可能在一行中出現不只一次。
# 要得到總次數，我們可以用 `count` 方法，它會回傳一個序列在字串中出現的次數。

total = 0
for line in open('pg345_cleaned.txt'):
    total += line.count('Jonathan')

total

# 現在我們可以像這樣把 `'Jonathan'` 取代成 `'Thomas'`：

writer = open('pg345_replaced.txt', 'w')

for line in open('pg345_cleaned.txt'):
    line = line.replace('Jonathan', 'Thomas')
    writer.write(line)

# 結果是一個叫做 `pg345_replaced.txt` 的新檔案，裡面是《德古拉》的一個版本，
# 其中 Jonathan Harker 被改名為 Thomas。

total = 0
for line in open('pg345_replaced.txt'):
    total += line.count('Thomas')

total

# ## 正規表示式 (Regular expressions)
#
# 如果我們確切知道要找的是哪個字元序列，我們可以用 `in` 運算子來找它，
# 用 `replace` 方法來取代它。
# 但還有另一個工具，叫做 **正規表示式 (regular expression)**，它也能執行這些操作——而且功能更多。
#
# 為了示範，我會從一個簡單的例子開始，然後慢慢進階。
# 假設，我們又想找出所有包含特定單字的行。
# 換個口味，這次我們來找書中提到主角德古拉伯爵 (Count Dracula) 的地方。
# 這裡有一行提到他：

text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

# 這是我們要用來搜尋的 **模式 (pattern)**。

pattern = 'Dracula'

# 一個叫做 `re` 的模組提供了跟正規表示式相關的函數。
# 我們可以像這樣匯入它，然後用 `search` 函數來檢查模式是否出現在文本中。

import re

result = re.search(pattern, text)
result

# 如果模式出現在文本中，`search` 會回傳一個 `Match` 物件，裡面包含了搜尋的結果。
# 在其他資訊中，它有一個叫做 `string` 的變數，存著被搜尋的文本。

result.string

# 它也提供了一個叫做 `group` 的方法，會回傳文本中符合模式的部分。

result.group()

# 並且它提供了一個叫做 `span` 的方法，會回傳模式在文本中開始和結束的索引位置。

result.span()

# 如果模式沒有出現在文本中，`search` 的回傳值會是 `None`。

result = re.search('Count', text)
print(result)

# 所以我們可以藉由檢查結果是不是 `None` 來判斷搜尋是否成功。

result == None

# 綜合以上，這裡有一個函數，它會遍歷書中的每一行，直到找到符合給定模式的那一行，
# 然後回傳 `Match` 物件。

def find_first(pattern):
    for line in open('pg345_cleaned.txt'):
        result = re.search(pattern, line)
        if result != None: # 或者可以寫 if result:
            return result

# 我們可以用它來找到某個角色第一次被提到的地方。

result = find_first('Harker')
result.string

# 在這個例子中，我們其實不需要用正規表示式——用 `in` 運算子可以更簡單地做到一樣的事。
# 但是正規表示式可以做到 `in` 運算子做不到的事情。
#
# 例如，如果模式包含垂直線字元 `'|'`，它可以符合左邊的序列或右邊的序列。
# 假設我們想找到書中第一次提到 Mina Murray 的地方，但我們不確定她是用名字還是姓氏被提及。
# 我們可以用下面的模式，它可以符合任一個名字。

pattern = 'Mina|Murray'
result = find_first(pattern)
result.string

# 我們可以用像這樣的模式來計算一個角色被任一名字提及了多少次。
# 這裡有一個函數，它會遍歷整本書，並計算符合給定模式的行數。

def count_matches(pattern):
    count = 0
    for line in open('pg345_cleaned.txt'):
        result = re.search(pattern, line)
        if result != None: # 或者 if result:
            count += 1
    return count

# 現在來看看 Mina 被提到了多少次。

count_matches('Mina|Murray')

# 特殊字元 `'^'` 符合字串的開頭，所以我們可以找到以給定模式開頭的行。

result = find_first('^Dracula')
result.string

# 而特殊字元 `'$'` 符合字串的結尾，所以我們可以找到以給定模式結尾的行
# (忽略結尾的換行符號)。

result = find_first('Harker$')
result.string

# ## 字串替換 (String substitution)
#
# 布蘭·斯托克出生於愛爾蘭，當《德古拉》於 1897 年出版時，他住在英國。
# 所以我們預期他會使用像是 "centre" 和 "colour" 這樣的英式拼法。
# 要檢查的話，我們可以用下面的模式，它可以符合 "centre" 或美式拼法的 "center"。

pattern = 'cent(er|re)'

# 在這個模式中，括號包住了垂直線所作用的部分。
# 所以這個模式符合以 `'cent'` 開頭，並以 `'er'` 或 `'re'` 結尾的序列。

result = find_first(pattern)
result.string

# 如同預期的，他用了英式拼法。
#
# 我們也可以檢查他是否用了 "colour" 的英式拼法。
# 下面的模式用了特殊字元 `'?'`，表示前一個字元是可選的。

pattern = 'colou?r'

# 這個模式符合有 `'u'` 的 "colour" 或沒有 `'u'` 的 "color"。

result = find_first(pattern)
line = result.string
line

# 再次，如同預期的，他用了英式拼法。
#
# 現在假設我們想製作一個使用美式拼法的書本版本。
# 我們可以用 `re` 模組中的 `sub` 函數，它會執行 **字串替換 (string substitution)**。

re.sub(pattern, 'color', line)

# 第一個參數是我們要尋找和取代的模式，第二個是我們要取代成的內容，
# 第三個是我們要搜尋的字串。
# 在結果中，你可以看到 "colour" 已經被取代成 "color" 了。

# 我用這個函數來搜尋作為範例的句子

def all_matches(pattern):
    for line in open('pg345_cleaned.txt'):
        result = re.search(pattern, line)
        if result:
            print(line.strip())

# 這是我用的模式 (它用了一些我們還沒看過的功能)

names = r'(?<!\.\s)[A-Z][a-zA-Z]+' # r'' 表示 raw string, 處理反斜線時很有用

all_matches(names)

# ## 除錯 (Debugging)
#
# 當你在讀寫檔案時，除錯可能會有點棘手。
# 如果你在 Jupyter Notebook 中工作，你可以用 **shell 指令** 來幫忙。
# 例如，要顯示檔案的前幾行，你可以用 `!head` 指令，像這樣：

!head pg345_cleaned.txt

# 開頭的驚嘆號 `!` 表示這是一個 shell 指令，它不是 Python 的一部分。
# 要顯示最後幾行，你可以用 `!tail`。

!tail pg345_cleaned.txt

# 當你處理大型檔案時，除錯可能會很困難，因為輸出的內容可能太多，沒辦法用手動檢查。
# 一個好的除錯策略是先從檔案的一部分開始，讓程式可以運作，然後再用整個檔案來執行它。
#
# 要製作一個包含較大檔案一部分的小檔案，我們可以再次使用 `!head` 搭配重新導向運算子 `>`，
# 它表示結果應該被寫入檔案，而不是顯示出來。

!head pg345_cleaned.txt > pg345_cleaned_10_lines.txt

# 預設情況下，`!head` 會讀取前 10 行，但它可以接受一個選擇性的參數來指定要讀取的行數。

!head -100 pg345_cleaned.txt > pg345_cleaned_100_lines.txt

# 這個 shell 指令會從 `pg345_cleaned.txt` 讀取前 100 行，然後把它們寫到一個叫做 `pg345_cleaned_100_lines.txt` 的檔案裡。
#
# 注意：shell 指令 `!head` 和 `!tail` 並不是在所有作業系統上都可用。
# 如果它們在你的系統上不能用，我們可以用 Python 寫出類似的函數。
# 請看本章末尾的第一個練習題的建議。

# ## 詞彙表 (Glossary)
#
# **序列 (sequence):**
#  一個有序的值的集合，其中每個值都由一個整數索引來識別。
#
# **字元 (character):**
#  字串的一個元素，包含字母、數字和符號。
#
# **索引 (index):**
#  一個整數值，用來選取序列中的一個項目，例如字串中的一個字元。在 Python 中，索引從 `0` 開始。
#
# **切片 (slice):**
#  字串的一部分，由一個索引範圍指定。
#
# **空字串 (empty string):**
#  一個不包含任何字元且長度為 `0` 的字串。
#
# **物件 (object):**
#  變數可以參照的東西。一個物件有它的型別和值。
#
# **不可變的 (immutable):**
#  如果一個物件的元素不能被改變，那麼這個物件就是不可變的。
#
# **調用 (invocation):**
#  一個呼叫方法的表達式——或表達式的一部分。
#
# **正規表示式 (regular expression):**
#  一個定義搜尋模式的字元序列。
#
# **模式 (pattern):**
#  一個規則，指定一個字串必須符合哪些要求才能構成匹配。
#
# **字串替換 (string substitution):**
#  將一個字串或字串的一部分取代成另一個字串。
#
# **shell 指令 (shell command):**
#  shell 語言中的一個陳述式，shell 語言是一種用來與作業系統互動的語言。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 在這一章，我們只稍微碰觸了正規表示式能做到的事情的表面。
# 為了了解它有哪些可能性，可以問問虛擬助理：「Python 正規表示式中最常用的特殊字元有哪些？」
#
# 你也可以要求它提供符合特定種類字串的模式。
# 例如，試著問問：
#
# * 寫一個 Python 正規表示式，可以符合帶有連字號的 10 位數電話號碼。
#
# * 寫一個 Python 正規表示式，可以符合包含門牌號碼和街道名稱，後面接著 `ST` 或 `AVE` 的街道地址。
#
# * 寫一個 Python 正規表示式，可以符合包含任何常見稱謂 (如 `Mr` 或 `Mrs`)，後面跟著任意數量以大寫字母開頭的名字 (名字之間可能有用連字號連接) 的全名。
#
# 如果你想看更複雜的東西，試著要求一個可以符合任何合法 URL 的正規表示式。
#
# 正規表示式常常在引號前面加上字母 `r`，表示它是一個 "raw string" (原始字串)。
# 想知道更多資訊，可以問問虛擬助理：「Python 中的 raw string 是什麼意思？」

from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)

# ### 練習
#
# 試著寫一個函數，做跟 shell 指令 `!head` 一樣的事情。
# 它應該接收三個參數：要讀取的檔案名稱、要讀取的行數，以及要把這些行寫入的檔案名稱。
# 如果第三個參數是 `None`，它應該顯示這些行，而不是把它們寫到檔案裡。
#
# 可以考慮請虛擬助理幫忙，但如果你這麼做，告訴它不要使用 `with` 陳述式或 `try` 陳述式。

# 解答

def head(input_file, num_lines=10, output_file=None):
    reader = open(input_file, 'r') # 'r' 表示讀取模式

    if output_file is not None:
        writer = open(output_file, 'w') # 'w' 表示寫入模式

    for i in range(num_lines):
        line = reader.readline() # 一次讀一行

        if not line: # 如果讀到檔案結尾，readline() 會回傳空字串
            break

        if output_file is not None:
            writer.write(line)
        else:
            print(line, end='') # end='' 避免 print 自動加上多餘的換行

    reader.close()
    if output_file is not None:
        writer.close()

# 你可以用下面的例子來測試你的函數。

head('pg345_cleaned.txt', 10)

head('pg345_cleaned.txt', 100, 'pg345_cleaned_100_lines.txt')

!tail pg345_cleaned_100_lines.txt

# ### 練習
#
# "Wordle" 是一個線上文字遊戲，目標是在六次或更少次的嘗試內猜出一個五個字母的單字。
# 每次嘗試都必須是一個被認可的單字，不包含專有名詞。
# 每次嘗試後，你會得到關於你猜的字母中有哪些出現在目標單字中，以及哪些位置正確的資訊。
#
# 例如，假設目標單字是 `MOWER`，而你猜了 `TRIED`。
# 你會知道 `E` 在單字中且位置正確，`R` 在單字中但位置不正確，
# 而 `T`、`I` 和 `D` 則不在單字中。
#
# 換個例子，假設你已經猜了 `SPADE` 和 `CLERK` 這兩個字，
# 並且你得知 `E` 在目標單字中，但不在這兩個字裡 `E` 出現的位置，
# 而且其他字母 (S, P, A, D, C, L, R, K) 都不在目標單字中。
# 在單字列表裡，有多少個字可能是目標單字呢？
# 寫一個叫做 `check_word` 的函數，它接收一個五個字母的單字，
# 並根據這些猜測來檢查它是否可能是目標單字。

# 解答

def check_word(word):
    # 條件1: 目標字必須包含 'e'
    if 'e' not in word:
        return False

    # 條件2: 'e' 不在 SPADE 的第3個位置 (索引2) 也不在 CLERK 的第5個位置 (索引4)
    # 也就是說，目標字的 'e' 不能在索引 2 或索引 4 的位置
    if word[2] == 'e' or word[4] == 'e':
        return False

    # 條件3: 目標字不能包含 SPADCLRK 這些字母中的任何一個
    if uses_any(word, 'spadclrk'): # uses_any 會檢查 word 是否用了 letters 中的任一字母
        return False

    # 如果以上檢查都通過了，這個字就可能是目標字
    return True

# 你可以用上一章的任何函數，像是 `uses_any`。

def uses_any(word, letters):
    for letter in word.lower(): # 轉成小寫來比較，避免大小寫問題
        if letter in letters.lower():
            return True
    return False

# 你可以用下面的迴圈來測試你的函數。

print("--- Wordle 第一次篩選 ---")
count = 0
for line in open('words.txt'):
    word = line.strip()
    if len(word) == 5 and check_word(word):
        print(word)
        count += 1
print(f"符合條件的字總共有: {count} 個")


# ### 練習
#
# 延續上一個練習，假設你猜了 `TOTEM` 這個字，
# 然後得知 `E` *仍然* 不在正確的位置，但是 `M` 的位置是正確的。
# 那還剩下多少個可能的字呢？

# 解答

def check_word2(word):
    # 首先，它必須通過第一次的檢查
    if not check_word(word):
        return False

    # 條件4: 'E' 不在 TOTEM 的第4個位置 (索引3)
    if word[3] == 'e':
        return False

    # 條件5: 'M' 在 TOTEM 的第5個位置 (索引4) 是正確的
    #         而且，TOTEM 的 T 和 O 都不在目標字中 (這點已由 check_word 裡面的 spadclrk 處理了一部分，
    #         但 't' 和 'o' 需要額外加入排除列表，如果它們在第一次猜測後被確認為不存在。
    #         不過題目只說 M 位置正確，E 位置不對。我們先假設 T 和 O 的資訊還未知或已被之前的排除涵蓋)
    #         這裡，最重要的是 M 必須在最後一個位置
    if word[4] != 'm':
        return False
    
    # 條件6: TOTEM 的 T 和 O 不在目標字中
    # 根據第一次猜測 SPADE 和 CLERK，我們知道 S,P,A,D,C,L,R,K 不在。
    # 猜了 TOTEM 後，如果 T 和 O 也不在，那就要排除它們。
    # 題目暗示 "E 仍然不在正確位置，但 M 是"，通常 Wordle 會標示出不在的字母。
    # 所以我們假設 T 和 O 也不在。
    if uses_any(word, 'to'): # 排除 't' 和 'o'
        return False

    return True

# 解答 (執行迴圈)
print("--- Wordle 第二次篩選 ---")
count2 = 0
for line in open('words.txt'):
    word = line.strip()
    if len(word) == 5 and check_word2(word):
        print(word)
        count2 +=1
print(f"符合條件的字總共有: {count2} 個")


# ### 練習
#
# 《基督山恩仇記》(The Count of Monte Cristo) 是大仲馬 (Alexandre Dumas) 的一部經典小說。
# 然而，在這本書的英文譯本序言中，作家安伯托·艾可 (Umberto Eco) 坦承他覺得這本書是
# "有史以來寫得最差的小說之一"。
#
# 他特別提到，書中 "恬不知恥地重複使用相同的形容詞"，
# 並特別指出書中角色 "要嘛渾身發抖 (shudder)，要嘛臉色蒼白 (turn pale)" 的次數。
#
# 為了看看他的抱怨是否有道理，讓我們來計算一下包含任何形式 `pale` (蒼白) 這個字的行數，
# 包括 `pale`、`pales`、`paled` 和 `paleness`，以及相關的字 `pallor` (蒼白；灰土色)。
# 請使用一個單一的正規表示式來符合這些字中的任何一個。
# 作為額外的挑戰，確保它不會符合其他字，像是 `impale` (刺穿) —— 你可能需要請虛擬助理幫忙。

# 下面的儲存格會從古騰堡計畫下載這本書 (<https://www.gutenberg.org/ebooks/1184>)。

import os

if not os.path.exists('pg1184.txt'):
    !wget https://www.gutenberg.org/cache/epub/1184/pg1184.txt

# 下面的儲存格執行一個函數，它會讀取古騰堡計畫的檔案，
# 並寫入一個只包含書本本文、不含額外書籍資訊的檔案。

def clean_file(input_file, output_file):
    reader = open(input_file, encoding='utf-8') # 加上 encoding='utf-8' 以免讀取問題
    writer = open(output_file, 'w', encoding='utf-8') # 寫入也用 utf-8

    # 跳過開頭的版權宣告等等
    for line in reader:
        if is_special_line(line): # is_special_line 之前定義過了
            break

    # 寫入書本內容，直到遇到結尾的版權宣告
    for line in reader:
        if is_special_line(line):
            break
        writer.write(line)

    reader.close()
    writer.close()

if not os.path.exists('pg1184_cleaned.txt'): # 避免重複清理
    clean_file('pg1184.txt', 'pg1184_cleaned.txt')

# 解答 (count_matches 函數已在前面定義過，這裡直接使用)

# 解答

# 這個解法只用了本章看過的正規表示式功能，
# 但它也會符合包含這些字串的字，例如 "impale"。
# 我們把它定義為 count_matches_original 以便比較
def count_matches_original(pattern, filename='pg1184_cleaned.txt'):
    count = 0
    # 確保檔案存在
    if not os.path.exists(filename):
        print(f"錯誤: 檔案 {filename} 不存在。")
        return 0
        
    for line in open(filename, encoding='utf-8'):
        result = re.search(pattern, line, re.IGNORECASE) # 加上 re.IGNORECASE 忽略大小寫
        if result != None:
            count += 1
    return count

pattern_original = '(pale|pales|paled|paleness|pallor)'
matches_original = count_matches_original(pattern_original)
print(f"使用 '{pattern_original}' (會匹配到 impale 等字) 找到 {matches_original} 行。")


# 解答

# 這個解法使用了特殊序列 `\b` 來符合單字邊界 (word boundary)，
# 它可以是任何種類的空白字元或標點符號。
# 引號前的 `r` 表示這個模式是一個原始字串 (raw string)，
# 因為模式中包含了特殊序列，所以需要用原始字串。
# 我們把它定義為 count_matches_boundary 以便比較
def count_matches_boundary(pattern, filename='pg1184_cleaned.txt'):
    count = 0
    # 確保檔案存在
    if not os.path.exists(filename):
        print(f"錯誤: 檔案 {filename} 不存在。")
        return 0

    for line in open(filename, encoding='utf-8'):
        result = re.search(pattern, line, re.IGNORECASE) # 加上 re.IGNORECASE 忽略大小寫
        if result != None:
            count += 1
    return count

pattern_boundary = r'\b(pale|pales|paled|paleness|pallor)\b'
matches_boundary = count_matches_boundary(pattern_boundary)
print(f"使用 '{pattern_boundary}' (使用單字邊界) 找到 {matches_boundary} 行。")

# 根據這個精確的計數，這些字出現在書中的 `223` 行 (使用 `\b` 的結果，如果你的 words.txt 和 pg1184.txt 與作者相同)，
# 所以艾可先生的抱怨可能有點道理。
# (注意：實際數字可能會因檔案版本、清理方式或正規表示式細微差異而略有不同)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)