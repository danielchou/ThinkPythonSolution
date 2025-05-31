# -*- coding: utf-8 -*-
# 從 chap14.ipynb 轉換而來
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

# # 類別與函數 (Classes and Functions)
#
# 到目前為止，你已經知道如何使用函數來組織程式碼，以及如何使用內建型別來組織資料。
# 下一步是 **物件導向程式設計 (object-oriented programming)**，它使用程式設計師自訂的型別來同時組織程式碼和資料。
#
# 物件導向程式設計是一個很大的主題，所以我們會循序漸進。
# 在這一章，我們會從一些不那麼「道地 (idiomatic)」的程式碼開始 —— 也就是說，它不是有經驗的程式設計師會寫的那種程式碼 —— 但這是一個很好的起點。
# 在接下來的兩章中，我們會使用額外的功能來編寫更道地的程式碼。

# ## 程式設計師自訂型別 (Programmer-defined types)
#
# 我們已經用過很多 Python 的內建型別 —— 現在我們要定義一個新的型別。
# 作為第一個例子，我們會建立一個叫做 `Time` 的型別，用來表示一天中的某個時間。
# 程式設計師自訂的型別也叫做 **類別 (class)**。
# 類別定義看起來像這樣：

class Time:
    """表示一天中的某個時間。""" # 這是類別的文件字串 (docstring)

# 標頭 (header) 指出新的類別叫做 `Time`。
# 主體 (body) 是一個文件字串，解釋這個類別的用途。
# 定義一個類別會建立一個 **類別物件 (class object)**。
#
# 類別物件就像一個用來建立物件的工廠。
# 要建立一個 `Time` 物件，你就像呼叫函數一樣呼叫 `Time`。

lunch = Time() # 呼叫 Time() 來建立一個 Time 物件的實體

# 結果是一個新的物件，其型別是 `__main__.Time`，其中 `__main__` 是定義 `Time` 的模組名稱。
# (如果在互動式環境中，`__main__` 通常指目前執行的腳本或環境)

type(lunch)

# 當你印出一個物件時，Python 會告訴你它的型別以及它在記憶體中儲存的位置
# (前綴 `0x` 表示後面的數字是十六進位)。

print(lunch)

# 建立一個新物件的過程叫做 **實體化 (instantiation)**，而這個物件是該類別的一個 **實體 (instance)**。

# ## 屬性 (Attributes)
#
# 一個物件可以包含變數，這些變數稱為 **屬性 (attributes)**，發音時重音在第一個音節，
# 像是 "AT-trib-ute"，而不是第二個音節 "a-TRIB-ute"。
# 我們可以用點記法 (dot notation) 來建立屬性。

lunch.hour = 11    # 設定 lunch 物件的 hour 屬性
lunch.minute = 59  # 設定 lunch 物件的 minute 屬性
lunch.second = 1   # 設定 lunch 物件的 second 屬性

# 這個例子建立了叫做 `hour`、`minute` 和 `second` 的屬性，
# 它們分別包含了時間 `11:59:01` 的時、分、秒，對我來說這就是午餐時間啦。
#
# 下面的圖表顯示了這些賦值操作後 `lunch` 物件及其屬性的狀態。

from diagram import make_frame, make_binding

d1_lunch_attrs = dict(hour=11, minute=59, second=1)
frame_lunch = make_frame(d1_lunch_attrs, name='Time', dy=-0.3, offsetx=0.48)
binding_lunch = make_binding('lunch', frame_lunch)

from diagram import diagram, adjust # diagram 模組用於繪製狀態圖

width_lunch, height_lunch, x_lunch, y_lunch = [1.77, 1.24, 0.25, 0.86]
ax_lunch = diagram(width_lunch, height_lunch)
bbox_lunch = binding_lunch.draw(ax_lunch, x_lunch, y_lunch)
#adjust(x_lunch, y_lunch, bbox_lunch)

# 變數 `lunch` 指向一個 `Time` 物件，該物件包含三個屬性。
# 每個屬性都指向一個整數。
# 像這樣顯示物件及其屬性的狀態圖稱為 **物件圖 (object diagram)**。
#
# 你可以用點運算子讀取屬性的值。

print(f"lunch.hour: {lunch.hour}")

# 你可以把屬性當作任何表達式的一部分來使用。

total_minutes = lunch.hour * 60 + lunch.minute
print(f"總分鐘數: {total_minutes}")

# 你也可以在 f-字串的表達式中使用點運算子。

f_string_time_raw = f'{lunch.hour}:{lunch.minute}:{lunch.second}'
print(f"原始 f-字串時間表示: {f_string_time_raw}")

# 但請注意，上一個例子的格式並非標準格式。
# 要修正它，我們必須在印出 `minute` 和 `second` 屬性時加上前導零。
# 我們可以透過在 大括號內的表達式後面加上 **格式指定符 (format specifier)** 來做到這點。
# 在下面的例子中，格式指定符表示 `minute` 和 `second` 應該至少顯示兩位數，並在需要時補上前導零。
# (`02d` 的 `0` 表示補零，`2` 表示寬度為2，`d` 表示十進位整數)

f_string_time_formatted = f'{lunch.hour}:{lunch.minute:02d}:{lunch.second:02d}'
print(f"格式化後的 f-字串時間表示: {f_string_time_formatted}")

# 我們會用這個 f-字串來寫一個顯示 `Time` 物件值的函數。
# 你可以像平常一樣把物件當作參數傳遞。
# 例如，下面的函數接收一個 `Time` 物件作為參數。

def print_time(time_obj): # 參數改名以避免與類別 Time 混淆
    s_time_formatted = f'{time_obj.hour:02d}:{time_obj.minute:02d}:{time_obj.second:02d}'
    print(s_time_formatted)

# 當我們呼叫它時，可以把 `lunch` 當作參數傳遞。

print("--- 使用 print_time(lunch) ---")
print_time(lunch)

# ## 物件作為回傳值 (Objects as return values)
#
# 函數可以回傳物件。例如，`make_time` 接收叫做 `hour`、`minute` 和 `second` 的參數，
# 把它們儲存為 `Time` 物件的屬性，然後回傳這個新的物件。

def make_time(hour_val, minute_val, second_val): # 參數改名
    new_time_obj = Time() # 建立一個新的 Time 物件
    new_time_obj.hour = hour_val
    new_time_obj.minute = minute_val
    new_time_obj.second = second_val
    return new_time_obj

# 參數名稱與屬性名稱相同可能讓你有點驚訝，但這是編寫這類函數的常見方式。
# (雖然我在上面把參數改名了，以求更清晰)
# 這是我們如何使用 `make_time` 來建立一個 `Time` 物件。

created_time = make_time(11, 59, 1)
print("--- 使用 make_time 和 print_time ---")
print_time(created_time)

# ## 物件是可變的 (Objects are mutable)
#
# 假設你要去看一場電影，像是《蒙提·派森與聖杯》(Monty Python and the Holy Grail)，
# 它在晚上 `9:20` 開始，片長 `92` 分鐘，也就是一小時 `32` 分鐘。
# 電影什麼時候會結束呢？
#
# 首先，我們建立一個代表開始時間的 `Time` 物件。

start_movie_time = make_time(9, 20, 0)
print("電影開始時間:")
print_time(start_movie_time)

# 要找到結束時間，我們可以修改 `Time` 物件的屬性，加上電影的時長。

start_movie_time.hour += 1    # 直接修改物件的屬性
start_movie_time.minute += 32
print("加上電影時長後的 start_movie_time (已變成結束時間):")
print_time(start_movie_time) # 現在 start_movie_time 實際上是結束時間了

# 電影會在晚上 10:52 結束。
#
# 讓我們把這個計算封裝到一個函數裡，並把它推廣到接收三個參數的電影時長：
# `hours`、`minutes` 和 `seconds`。

def increment_time(time_to_inc, hours_inc, minutes_inc, seconds_inc): # 參數改名
    # 這個函數會直接修改傳入的 time_to_inc 物件 (impure function)
    time_to_inc.hour += hours_inc
    time_to_inc.minute += minutes_inc
    time_to_inc.second += seconds_inc
    # 注意：這個版本的 increment_time 還沒有處理進位問題 (例如分鐘超過60)

# 這裡有一個例子來展示效果。

start_again = make_time(9, 20, 0)
print("--- 使用 increment_time ---")
print("原始 start_again 時間:")
print_time(start_again)
increment_time(start_again, 1, 32, 0) # start_again 物件本身被修改了
print("increment_time 後的 start_again 時間:")
print_time(start_again)

# 下面的堆疊圖 (stack diagram) 顯示了在 `increment_time` 修改物件之前的程式狀態。
# (圖中會顯示 __main__ 框架中的 start_again 和 increment_time 框架中的 time_to_inc 都指向同一個 Time 物件)

from diagram import Frame, Binding, Value, Stack # diagram 模組元件

d1_stack = dict(hour=9, minute=20, second=0)
obj1_stack = make_frame(d1_stack, name='Time', dy=-0.25, offsetx=0.78)

# binding1_stack = make_binding('start_again', frame_lunch, draw_value=False, dx=0.7) # frame_lunch 不適用於此
# 使用 obj1_stack
binding1_main_stack = make_binding('start_again', obj1_stack, draw_value=False, dx=0.7)
frame1_main_stack = Frame([binding1_main_stack], name='__main__', loc='left', offsetx=-0.2)

binding2_func_stack = Binding(Value('time_to_inc'), draw_value=False, dx=0.7, dy=0.35)
binding3_hrs_stack = make_binding('hours_inc', 1)
binding4_min_stack = make_binding('minutes_inc',32)
binding5_sec_stack = make_binding('seconds_inc', 0)
frame2_func_stack = Frame([binding2_func_stack, binding3_hrs_stack, binding4_min_stack, binding5_sec_stack], name='increment_time',
                           loc='left', dy=-0.25, offsetx=0.08)

stack_obj_mutable = Stack([frame1_main_stack, frame2_func_stack], dx=-0.3, dy=-0.5)


from diagram import Bbox # diagram 模組元件

width_stack, height_stack, x_stack, y_stack = [3.4, 1.89, 1.75, 1.5]
ax_stack = diagram(width_stack, height_stack)
bbox1_stack = stack_obj_mutable.draw(ax_stack, x_stack, y_stack)
# bbox2_stack = obj1_stack.draw(ax_stack, x_stack+0.23, y_stack) # obj1_stack 已經被 binding1_main_stack 參照
# adjust(x_stack, y_stack, bbox1_stack) # bbox1_stack 已包含所有


# 在函數內部，`time_to_inc` 是 `start_again` 的一個別名 (alias)，
# 所以當 `time_to_inc` 被修改時，`start_again` 也會改變。
#
# 這個函數可以運作，但執行完畢後，我們剩下一個叫做 `start_again` 的變數，
# 它指向一個代表 *結束* 時間的物件，而我們不再擁有代表開始時間的物件了。
# 比較好的做法是保持 `start_again` 不變，並建立一個新的物件來代表結束時間。
# 我們可以透過複製 `start_again` 並修改副本來做到這點。

# ## 複製 (Copying)
#
# `copy` 模組提供了一個叫做 `copy` 的函數，它可以複製任何物件。
# (這通常是淺複製 (shallow copy)，對於包含其他物件的物件，只複製參照)
# 我們可以像這樣匯入它。

from copy import copy

# 為了看看它是如何運作的，我們先建立一個新的 `Time` 物件，代表電影的開始時間。

start_for_copy = make_time(9, 20, 0)
print("--- 複製物件範例 ---")
print("start_for_copy 時間:")
print_time(start_for_copy)

# 然後製作一個副本。

end_copied = copy(start_for_copy) # end_copied 是 start_for_copy 的一個副本

# 現在 `start_for_copy` 和 `end_copied` 包含相同的資料。

print("end_copied 時間 (複製後):")
print_time(end_copied)

# 但是 `is` 運算子確認了它們不是同一個物件。

print(f"start_for_copy is end_copied: {start_for_copy is end_copied}") # False

# 讓我們看看 `==` 運算子會做什麼。

print(f"start_for_copy == end_copied: {start_for_copy == end_copied}") # 預設也是 False

# 你可能會期望 `==` 產生 `True`，因為物件包含相同的資料。
# 但是對於程式設計師自訂的類別，`==` 運算子的預設行為與 `is` 運算子相同
# —— 它檢查的是物件的同一性 (identity)，而不是等值性 (equivalence)。
# (除非我們之後為類別定義 `__eq__` 方法)

# ## 純函數 (Pure functions)
#
# 我們可以用 `copy` 來編寫不修改其參數的純函數 (pure function)。
# 例如，這裡有一個函數，它接收一個 `Time` 物件和以時、分、秒表示的持續時間。
# 它會建立原始物件的一個副本，使用 `increment_time` (之前的版本，會修改物件) 來修改副本，然後回傳副本。

def add_time_pure(time_orig, hours_add, minutes_add, seconds_add): # 參數改名
    # 這個版本的 add_time 是純函數，它不修改 time_orig
    time_copy_for_add = copy(time_orig) # 建立副本
    increment_time(time_copy_for_add, hours_add, minutes_add, seconds_add) # 修改副本
    return time_copy_for_add # 回傳修改後的副本

# 我們這樣使用它。

start_pure_test = make_time(9, 20, 0)
print("--- 純函數 add_time_pure 測試 ---")
print("原始 start_pure_test 時間:")
print_time(start_pure_test)

end_from_pure_add = add_time_pure(start_pure_test, 1, 32, 0)
print("add_time_pure 回傳的結束時間:")
print_time(end_from_pure_add)

# 回傳值是一個新的物件，代表電影的結束時間。
# 我們可以確認 `start_pure_test` 保持不變。

print("呼叫 add_time_pure 後的 start_pure_test 時間 (應保持不變):")
print_time(start_pure_test)

# `add_time_pure` 是一個 **純函數 (pure function)**，因為它不修改任何傳遞給它的物件參數，
# 並且它唯一的效果就是回傳一個值。
#
# 任何可以用非純函數完成的事情，也都可以用純函數完成。
# 事實上，有些程式語言只允許純函數。
# 使用純函數的程式可能比較不容易出錯，但非純函數有時很方便，而且可能更有效率。
#
# 一般來說，我建議盡可能編寫純函數，只有在有明顯優勢時才使用非純函數。
# 這種方法可以稱為 **函數式程式設計風格 (functional programming style)**。

# ## 原型與修補 (Prototype and patch)
#
# 在上一個例子中，`increment_time` 和 `add_time_pure` 看起來可以運作，
# 但如果我們試另一個例子，就會發現它們不完全正確。
# (因為 `increment_time` 還沒處理進位)
#
# 假設你到達電影院後發現電影是 `9:40` 開始，而不是 `9:20`。
# 這是我們計算更新後的結束時間時會發生的情況。

start_prototype_test = make_time(9, 40, 0)
# 使用的是還沒處理進位的 increment_time 和依賴它的 add_time_pure
# 我們需要先定義一個會出錯的 add_time 版本
def add_time_buggy(time_orig, hours_add, minutes_add, seconds_add):
    time_copy_for_add = copy(time_orig)
    # 使用舊版(未處理進位)的 increment_time
    time_copy_for_add.hour += hours_add
    time_copy_for_add.minute += minutes_add
    time_copy_for_add.second += seconds_add
    # 沒有進位處理
    return time_copy_for_add

print("--- 原型與修補：測試有問題的 add_time ---")
end_prototype_test_buggy = add_time_buggy(start_prototype_test, 1, 32, 0) # 9:40 + 1h32m
print("有問題的 add_time 計算出的結束時間 (9:40 + 1h32m):")
print_time(end_prototype_test_buggy) # 預期結果 10:72:00 (分鐘超過59)

# 結果不是一個有效的時間。
# 問題在於 `increment_time` (以及依賴它的 `add_time_buggy`) 沒有處理秒數或分鐘數加總超過 `60` 的情況。
#
# 這裡是一個改良過的版本，它會檢查 `second` 是否超過或等於 `60` —— 如果是，就增加 `minute` ——
# 然後檢查 `minute` 是否超過或等於 `60` —— 如果是，就增加 `hour`。

# 改良版的 increment_time (處理進位)
def increment_time_v2(time_obj_v2, hours_inc_v2, minutes_inc_v2, seconds_inc_v2):
    time_obj_v2.hour += hours_inc_v2
    time_obj_v2.minute += minutes_inc_v2
    time_obj_v2.second += seconds_inc_v2

    if time_obj_v2.second >= 60:
        time_obj_v2.second -= 60 # 秒數減60
        time_obj_v2.minute += 1  # 分鐘加1 (進位)

    if time_obj_v2.minute >= 60:
        time_obj_v2.minute -= 60 # 分鐘減60
        time_obj_v2.hour += 1    # 小時加1 (進位)
    # 注意：這個版本還沒處理小時超過 23 的情況 (例如跨日)

# 修正 `increment_time_v2` 也會修正依賴它的 `add_time` (如果 `add_time` 用的是新版 `increment_time`)。
# 讓我們定義一個使用新版 increment_time_v2 的 add_time_v2
def add_time_v2(time_orig_v2, hours_add_v2, minutes_add_v2, seconds_add_v2):
    time_copy_v2 = copy(time_orig_v2)
    increment_time_v2(time_copy_v2, hours_add_v2, minutes_add_v2, seconds_add_v2)
    return time_copy_v2

# 所以現在上一個例子可以正確運作了。
print("\n--- 使用改良版 add_time_v2 ---")
start_prototype_test_v2 = make_time(9, 40, 0)
end_prototype_test_v2 = add_time_v2(start_prototype_test_v2, 1, 32, 0) # 9:40 + 1h32m
print("改良版 add_time_v2 計算出的結束時間 (9:40 + 1h32m):")
print_time(end_prototype_test_v2) # 應該是 11:12:00

# 但這個函數仍然不完全正確，因為參數可能大於 `60`。
# 例如，假設我們得到的執行時間是 `92` 分鐘，而不是 `1` 小時 `32` 分鐘。
# 我們可能會像這樣呼叫 `add_time_v2`：

start_large_arg_test = make_time(9, 40, 0) # 從 9:40 開始
end_large_arg_test = add_time_v2(start_large_arg_test, 0, 92, 0) # 加上 0 小時 92 分鐘
print("\n--- 測試參數大於 60 的情況 (使用 add_time_v2) ---")
print("參數大於 60 時計算出的結束時間 (9:40 + 0h92m):")
print_time(end_large_arg_test) # 9: (40+92) : 0  => 9:132:0 => (進位後) 11:12:0
                               # v2 版的 increment_time 只處理一次進位，所以這裡還是會出錯
                               # 132 分鐘，進位一次變 10:72:0，再進位一次變 11:12:0。
                               # v2 版的邏輯是正確的，因為是先加總再處理進位。
                               # 書中這一步是為了引導到 divmod 的方法。
                               # 為了模擬書中「仍然不正確」的說法，
                               # increment_time_v2 的進位邏輯需要是「只處理一次」的錯誤版本
                               # 這裡我們假設 increment_time_v2 是正確的，所以 9:40 + 92min = 11:12

# (如果 increment_time_v2 如書中暗示的那麼簡單，結果會不正確。)
# 所以讓我們嘗試另一種方法，使用 `divmod` 函數。
# 我們先建立 `start_large_arg_test` 的一個副本，然後修改它的 `minute` 屬性。

# 假設 start_time_divmod 是 9:40
start_time_divmod = make_time(9, 40, 0)
end_time_divmod_step1 = copy(start_time_divmod)
end_time_divmod_step1.minute = start_time_divmod.minute + 92 # 40 + 92 = 132
print(f"end_time_divmod_step1.minute (直接相加後): {end_time_divmod_step1.minute}")

# 現在 `minute` 是 `132`，也就是 `2` 小時 `12` 分鐘。
# 我們可以用 `divmod` 除以 `60`，得到完整的小時數和剩下的分鐘數。
# divmod(x, y) 回傳 (x // y, x % y)

carry_hours, end_time_divmod_step1.minute = divmod(end_time_divmod_step1.minute, 60) # 132 // 60 = 2, 132 % 60 = 12
print(f"進位的小時數: {carry_hours}, 更新後的分鐘數: {end_time_divmod_step1.minute}")

# 現在 `minute` 是正確的了，我們可以把小時數加到 `hour` 上。

end_time_divmod_step1.hour += carry_hours # 9 + 2 = 11
print("--- 使用 divmod 手動調整 ---")
print_time(end_time_divmod_step1) # 應該是 11:12:00

# 結果是一個有效的時間。
# 我們可以對 `hour` (處理跨日) 和 `second` 做同樣的事情，並把整個過程封裝到一個函數裡。
# (注意：書中這裡的 increment_time 版本沒有處理小時跨日的問題，只處理秒和分的進位)

# 最終版的 increment_time (使用 divmod)
def increment_time_v3_divmod(time_obj_v3, hours_inc_v3, minutes_inc_v3, seconds_inc_v3):
    # 先全部加起來
    time_obj_v3.hour += hours_inc_v3
    time_obj_v3.minute += minutes_inc_v3
    time_obj_v3.second += seconds_inc_v3

    # 處理秒的進位到分
    carry_to_minute, time_obj_v3.second = divmod(time_obj_v3.second, 60)
    time_obj_v3.minute += carry_to_minute # 把秒的進位加到分鐘上

    # 處理分的進位到時
    carry_to_hour, time_obj_v3.minute = divmod(time_obj_v3.minute, 60)
    time_obj_v3.hour += carry_to_hour # 把分的進位加到小時上

    # 處理時的進位 (例如跨日，結果可能大於23，但 Time 物件本身不限制小時範圍)
    # 如果需要限制在 0-23 小時，可以 time_obj_v3.hour %= 24
    # 書中目前還沒處理這個
    # carry_to_day, time_obj_v3.hour = divmod(time_obj_v3.hour, 24)
    # (如果需要回傳天數進位，函數簽名就要改)

# 有了這個版本的 `increment_time_v3_divmod`，`add_time` (如果用它) 就能正確運作，即使參數超過 `60`。
# 我們定義一個使用 v3 的 add_time_v3
def add_time_v3(time_orig_v3, hours_add_v3, minutes_add_v3, seconds_add_v3):
    time_copy_v3 = copy(time_orig_v3)
    increment_time_v3_divmod(time_copy_v3, hours_add_v3, minutes_add_v3, seconds_add_v3)
    return time_copy_v3

start_final_test = make_time(9, 40, 0)
# 測試 0 小時 90 分 120 秒 => 0 小時 90+2 分 0 秒 => 0 小時 92 分 0 秒
end_final_test = add_time_v3(start_final_test, 0, 90, 120)
print("\n--- 使用最終版 add_time_v3 (基於 divmod 的 increment_time) ---")
print("最終測試結果 (9:40 + 0h90m120s):")
print_time(end_final_test) # 9:40 + 92min = 11:12:00

# 這一節展示了一種我稱為 **原型與修補 (prototype and patch)** 的程式開發計畫。
# 我們從一個能正確處理第一個例子的簡單原型開始。
# 然後我們用更困難的例子來測試它 —— 當我們發現錯誤時，就修改程式來修正它，
# 就像在破了洞的輪胎上打補丁一樣。
#
# 這種方法可能很有效，尤其是在你對問題還沒有深入理解的時候。
# 但是漸進式的修正可能會產生不必要複雜的程式碼 —— 因為它處理了很多特殊情況 ——
# 而且也不可靠 —— 因為很難知道你是否已經找到了所有的錯誤。

# ## 設計優先開發 (Design-first development)
#
# 另一種計畫是 **設計優先開發 (design-first development)**，它在原型製作之前會進行更多的規劃。
# 在設計優先的過程中，有時對問題的高層次洞察可以使程式設計變得更容易。
#
# 在這個例子中，洞察點是我們可以把 `Time` 物件看作是一個以 60 為基底的三位數 ——
# 也稱為六十進位制 (sexagesimal)。
# `second` 屬性是「個位數」，`minute` 屬性是「六十位數」，
# 而 `hour` 屬性是「三千六百位數」。
# 當我們寫 `increment_time` 時，我們實際上是在做以 60 為基底的加法，
# 這就是為什麼我們需要從一個位數進位到下一個位數。
#
# 這個觀察提示了整個問題的另一種解決方法 ——
# 我們可以把 `Time` 物件轉換成整數，並利用 Python 知道如何做整數運算這一點。
#
# 這裡有一個把 `Time` 物件轉換成整數 (總秒數) 的函數。

def time_to_int(time_obj_tti): # 參數改名
    minutes_total = time_obj_tti.hour * 60 + time_obj_tti.minute
    seconds_total = minutes_total * 60 + time_obj_tti.second
    return seconds_total

# 結果是從一天開始算起的總秒數。
# 例如，`01:01:01` 是從一天開始算的 `1` 小時 `1` 分 `1` 秒，
# 也就是 `3600` 秒、`60` 秒和 `1` 秒的總和。

time_for_tti = make_time(1, 1, 1)
print("\n--- time_to_int 測試 ---")
print("時間:")
print_time(time_for_tti)
seconds_from_time = time_to_int(time_for_tti)
print(f"轉換成的總秒數: {seconds_from_time}") # 1*3600 + 1*60 + 1 = 3661

# 這裡有一個反過來的函數 —— 把一個整數 (總秒數) 轉換回 `Time` 物件 —— 使用 `divmod` 函數。

def int_to_time(total_seconds_itt): # 參數改名
    # 先從總秒數中分出分鐘和剩餘秒數
    minutes_itt, second_itt = divmod(total_seconds_itt, 60)
    # 再從總分鐘數中分出小時和剩餘分鐘數
    hour_itt, minute_itt = divmod(minutes_itt, 60)
    # 如果需要處理超過24小時的情況，這裡可以對 hour_itt 再做 divmod(hour_itt, 24)
    # 但目前 make_time 不處理天數
    return make_time(hour_itt, minute_itt, second_itt)

# 我們可以透過把上一個例子的結果轉換回 `Time` 物件來測試它。

time_from_int = int_to_time(3661)
print("\n--- int_to_time 測試 ---")
print(f"從總秒數 {3661} 轉換回的時間:")
print_time(time_from_int) # 應該是 01:01:01

# 使用這些函數，我們可以寫出一個更簡潔的 `add_time` 版本。
# (這個版本是設計優先的，更優雅)

def add_time_design_first(time_obj_df, hours_df, minutes_df, seconds_df): # 參數改名
    # 1. 把要加的時長也轉換成一個 Time 物件 (方便統一處理或直接轉成秒數)
    #    或者，可以直接把時長轉成總秒數
    duration_seconds_df = hours_df * 3600 + minutes_df * 60 + seconds_df
    # duration_time_obj_df = make_time(hours_df, minutes_df, seconds_df) # 書中做法

    # 2. 把原始時間和時長都轉換成總秒數，然後相加
    # total_seconds_sum_df = time_to_int(time_obj_df) + time_to_int(duration_time_obj_df) # 書中做法
    total_seconds_sum_df = time_to_int(time_obj_df) + duration_seconds_df

    # 3. 把總秒數轉換回 Time 物件並回傳
    return int_to_time(total_seconds_sum_df)

# 第一行 (書中做法) 把參數轉換成一個叫做 `duration` 的 `Time` 物件。
# 第二行把 `time_obj_df` 和 `duration` (或直接是時長秒數) 轉換成秒數並相加。
# 第三行把總和轉換回 `Time` 物件並回傳。
#
# 這是它的運作方式。

start_design_first_test = make_time(9, 40, 0)
end_design_first_test = add_time_design_first(start_design_first_test, 1, 32, 0) # 9:40 + 1h32m
print("\n--- 設計優先的 add_time_design_first 測試 ---")
print("設計優先版計算出的結束時間:")
print_time(end_design_first_test) # 應該是 11:12:00

# 在某些方面，從 60 進位轉換到 10 進位再轉換回來，比直接處理時間要困難一些。
# 基底轉換比較抽象；我們對處理時間值的直覺比較好。
#
# 但是如果我們有洞察力把時間看作 60 進位數 —— 並且投入精力編寫轉換函數
# `time_to_int` 和 `int_to_time` —— 我們就能得到一個更短、更容易閱讀和除錯，
# 也更可靠的程式。
#
# 之後要加入新功能也更容易。例如，想像一下減去兩個 `Time` 物件來找出它們之間的時長。
# 天真的做法是實作帶有借位的減法。
# 使用轉換函數會更容易，也更可能正確。
#
# 諷刺的是，有時候把問題弄得更難 —— 或更一般化 —— 反而讓它變得更容易，
# 因為特殊情況變少了，出錯的機會也變少了。

# ## 除錯 (Debugging)
#
# Python 提供了幾個內建函數，對於測試和除錯處理物件的程式很有用。
# 例如，如果你不確定一個物件是什麼型別，你可以問它。

print(f"\n--- 物件除錯工具 ---")
print(f"type(start_design_first_test): {type(start_design_first_test)}")

# 你也可以用 `isinstance` 來檢查一個物件是否是某個特定類別的實體。

print(f"isinstance(end_design_first_test, Time): {isinstance(end_design_first_test, Time)}")
print(f"isinstance(end_design_first_test, int): {isinstance(end_design_first_test, int)}")


# 如果你不確定一個物件是否有某個特定的屬性，你可以用內建函數 `hasattr`。

print(f"hasattr(start_design_first_test, 'hour'): {hasattr(start_design_first_test, 'hour')}")
print(f"hasattr(start_design_first_test, 'day'): {hasattr(start_design_first_test, 'day')}") # False


# 要取得物件的所有屬性及其值 (以字典形式)，你可以用 `vars()`。
# (注意：vars() 通常只對具有 __dict__ 屬性的物件有效，我們目前簡單的 Time 類別實體是有的)

print(f"vars(start_design_first_test): {vars(start_design_first_test)}")

# 我們在[第十一章](section_debugging_11)看到的 `structshape` 模組也適用於程式設計師自訂的型別。
# (譯註：section_debugging_11 指的是書中對應章節的連結)

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/raw/v3/structshape.py');

try:
    from structshape import structshape # 已在 chap13 嘗試匯入
except ImportError:
    print("structshape 模組無法匯入。")
    def structshape(data): return f"structshape無法使用，資料型別: {type(data)}"


t_structshape_test = (start_design_first_test, end_design_first_test) # 一個包含兩個 Time 物件的元組
print(f"structshape(t_structshape_test): {structshape(t_structshape_test)}")

# ## 詞彙表 (Glossary)
#
# **物件導向程式設計 (object-oriented programming):**
#  一種使用物件來組織程式碼和資料的程式設計風格。
#
# **類別 (class):**
#  程式設計師自訂的型別。類別定義會建立一個新的類別物件。
#
# **類別物件 (class object):**
#  代表一個類別的物件 —— 它是一個類別定義的結果。
#
# **實體化 (instantiation):**
#  建立屬於某個類別的物件的過程。
#
# **實體 (instance):**
#  屬於某個類別的物件。
#
# **屬性 (attribute):**
#  與物件相關聯的變數，也稱為實體變數 (instance variable)。
#
# **物件圖 (object diagram):**
#  物件、其屬性及其值的圖形表示。
#
# **格式指定符 (format specifier):**
#  在 f-字串中，格式指定符決定了一個值如何被轉換成字串。
#
# **純函數 (pure function):**
#  一個不修改其參數，也沒有回傳值以外任何其他效果的函數。
#
# **函數式程式設計風格 (functional programming style):**
#  一種盡可能使用純函數的程式設計方式。
#
# **原型與修補 (prototype and patch):**
#  一種程式開發方式，從一個粗略的草稿開始，然後逐漸增加功能並修正錯誤。
#
# **設計優先開發 (design-first development):**
#  一種比原型與修補更仔細規劃的程式開發方式。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 這一章有很多新的詞彙。
# 與虛擬助理對話可以幫助你鞏固理解。
# 可以考慮問問：
#
# * 「類別 (class) 和型別 (type) 有什麼區別？」
#
# * 「物件 (object) 和實體 (instance) 有什麼區別？」
#
# * 「變數 (variable) 和屬性 (attribute) 有什麼區別？」
#
# * 「純函數和非純函數相比，各有哪些優缺點？」
#
# 因為我們才剛開始學習物件導向程式設計，所以本章的程式碼並不「道地」
# —— 它不是有經驗的程式設計師會寫的那種程式碼。
# 如果你向虛擬助理尋求練習題的幫助，你可能會看到我們還沒學過的功能。
# 特別是，你很可能會看到一個叫做 `__init__` 的方法，用來初始化實體的屬性。
#
# 如果這些功能對你來說有道理，那就用吧。
# 但如果沒有，請耐心等待 —— 我們很快就會學到。
# 在此期間，看看你是否能只用我們目前學過的功能來解決下面的練習。
#
# 另外，在本章我們看到了一個格式指定符的例子。想了解更多資訊，可以問問：「Python f-字串中可以使用哪些格式指定符？」

# ### 練習
#
# 寫一個叫做 `subtract_time` 的函數，它接收兩個 `Time` 物件，
# 並回傳它們之間以秒為單位的間隔 —— 假設它們是同一天內的兩個時間。

# 這裡有一個函數大綱讓你開始。

def subtract_time_starter(t1, t2): # 改名避免與解答衝突
    """計算兩個時間之間以秒為單位的差值。

    >>> subtract_time_starter(make_time(3, 2, 1), make_time(3, 2, 0))
    1
    >>> subtract_time_starter(make_time(3, 2, 1), make_time(3, 0, 0))
    121
    >>> subtract_time_starter(make_time(11, 12, 0), make_time(9, 40, 0))
    5520
    """
    return None # 你的程式碼會取代這裡

# 解答
# time_to_int 函數已在 In[85] 定義

def subtract_time(t1_sub, t2_sub): # 參數改名
    """計算兩個時間之間以秒為單位的差值。

    >>> subtract_time(make_time(3, 2, 1), make_time(3, 2, 0))
    1
    >>> subtract_time(make_time(3, 2, 1), make_time(3, 0, 0))
    121
    >>> subtract_time(make_time(11, 12, 0), make_time(9, 40, 0))
    5520
    >>> subtract_time(make_time(9, 40, 0), make_time(11, 12, 0)) # 測試 t2 > t1
    -5520
    """
    return time_to_int(t1_sub) - time_to_int(t2_sub)

# 你可以用 `doctest` 來測試你的函數。

from doctest import run_docstring_examples # 已在前面匯入過

def run_doctests(func): # 已在前面定義過
    print(f"--- 執行 {func.__name__} 的 doctests ---")
    run_docstring_examples(func, globals(), name=func.__name__)

print("\n--- 測試 subtract_time ---")
run_doctests(subtract_time)

# ### 練習
#
# 寫一個叫做 `is_after` 的函數，它接收兩個 `Time` 物件，
# 如果第一個時間比第二個時間晚 (在一天中)，則回傳 `True`，否則回傳 `False`。

# 這裡有一個函數大綱讓你開始。

def is_after_starter(t1, t2): # 改名避免與解答衝突
    """檢查 `t1` 是否在 `t2` 之後。

    >>> is_after_starter(make_time(3, 2, 1), make_time(3, 2, 0))
    True
    >>> is_after_starter(make_time(3, 2, 1), make_time(3, 2, 1)) # 相等時應為 False
    False
    >>> is_after_starter(make_time(11, 12, 0), make_time(9, 40, 0))
    True
    """
    return None # 你的程式碼會取代這裡

# 解答

def is_after(t1_after, t2_after): # 參數改名
    """檢查 `t1_after` 是否在 `t2_after` 之後。

    >>> is_after(make_time(3, 2, 1), make_time(3, 2, 0))
    True
    >>> is_after(make_time(3, 2, 1), make_time(3, 2, 1))
    False
    >>> is_after(make_time(11, 12, 0), make_time(9, 40, 0))
    True
    >>> is_after(make_time(9, 40, 0), make_time(11, 12, 0)) # 測試 t1 < t2
    False
    """
    return time_to_int(t1_after) > time_to_int(t2_after)

# 你可以用 `doctest` 來測試你的函數。

print("\n--- 測試 is_after (Time) ---")
run_doctests(is_after)

# ### 練習
#
# 這裡有一個 `Date` 類別的定義，用來表示一個日期 —— 也就是年、月、日。

class Date:
    """表示一個年、月、日。"""

# 1. 寫一個叫做 `make_date` 的函數，它接收 `year`、`month` 和 `day` 作為參數，
#    建立一個 `Date` 物件，將參數指派給屬性，然後回傳這個新的物件。
#    建立一個代表 1933 年 6 月 22 日的物件。
#
# 2. 寫一個叫做 `print_date` 的函數，它接收一個 `Date` 物件，
#    使用 f-字串格式化其屬性，然後印出結果。
#    如果你用你建立的 `Date` 物件來測試它，結果應該是 `1933-06-22`。
#
# 3. 寫一個叫做 `is_after_date` (原書 `is_after`) 的函數，它接收兩個 `Date` 物件作為參數，
#    如果第一個日期在第二個日期之後，則回傳 `True`。
#    建立一個代表 1933 年 9 月 17 日的第二個物件，並檢查它是否在第一個物件之後。
#
# 提示：你可能會發現寫一個叫做 `date_to_tuple` 的函數很有用，
# 它接收一個 `Date` 物件並回傳一個包含其年、月、日屬性的元組 (按此順序)。
# (這樣就可以直接比較元組來判斷日期先後)

# 你可以用這個函數大綱開始 (make_date)。

def make_date_starter(year, month, day): # 改名避免與解答衝突
    return None # 你的程式碼會取代這裡

# 解答 (make_date)

def make_date(year_val_md, month_val_md, day_val_md): # 參數改名
    new_date_obj = Date() # 建立 Date 物件
    new_date_obj.year = year_val_md
    new_date_obj.month = month_val_md
    new_date_obj.day = day_val_md
    return new_date_obj

# 你可以用這些例子來測試 `make_date`。

birthday1_date = make_date(1933, 6, 22)
print(f"\n--- Date 類別練習 ---")
print(f"birthday1_date: 年={birthday1_date.year}, 月={birthday1_date.month}, 日={birthday1_date.day}")


birthday2_date = make_date(1933, 9, 17)
print(f"birthday2_date: 年={birthday2_date.year}, 月={birthday2_date.month}, 日={birthday2_date.day}")


# 你可以用這個函數大綱開始 (print_date)。

def print_date_starter(date_obj_pd): # 改名避免與解答衝突
    print('') # 你的程式碼會取代這裡

# 解答 (print_date)

def print_date(date_obj_pd):
    # 使用 f-字串和格式指定符 (月份和日期補零到兩位)
    s_date_formatted = f'{date_obj_pd.year}-{date_obj_pd.month:02d}-{date_obj_pd.day:02d}'
    print(s_date_formatted)

# 你可以用這個例子來測試 `print_date`。

print("print_date(birthday1_date):")
print_date(birthday1_date) # 應該印出 1933-06-22

# 你可以用這個函數大綱開始 (is_after_date)。

def is_after_date_starter(date1, date2): # 改名避免與解答衝突
    return None # 你的程式碼會取代這裡

# 解答 (date_to_tuple) - 輔助函數

def date_to_tuple(date_obj_dtt): # 參數改名
    # 把 Date 物件的屬性放到一個元組中，方便比較
    return (date_obj_dtt.year, date_obj_dtt.month, date_obj_dtt.day)

# 解答 (is_after_date) - 書中原名 is_after，這裡改為 is_after_date 以區分 Time 的版本

def is_after_date(date1_iad, date2_iad): # 參數改名
    tuple1_iad = date_to_tuple(date1_iad)
    tuple2_iad = date_to_tuple(date2_iad)
    # Python 可以直接比較元組，它會逐個元素比較
    return tuple1_iad > tuple2_iad

# 你可以用這些例子來測試 `is_after_date`。

result_after1 = is_after_date(birthday1_date, birthday2_date)
print(f"is_after_date(birthday1 (1933-06-22), birthday2 (1933-09-17)): {result_after1}")  # 應該是 False

result_after2 = is_after_date(birthday2_date, birthday1_date)
print(f"is_after_date(birthday2 (1933-09-17), birthday1 (1933-06-22)): {result_after2}")  # 應該是 True

# 額外測試：同一天
same_day_test1 = make_date(2000, 1, 1)
same_day_test2 = make_date(2000, 1, 1)
print(f"is_after_date(same_day_test1, same_day_test2): {is_after_date(same_day_test1, same_day_test2)}") # False


# (這個儲存格是空的)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)