# -*- coding: utf-8 -*-
# 從 chap15.ipynb 轉換而來
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

# # 類別與方法 (Classes and Methods)
#
# Python 是一種 **物件導向語言 (object-oriented language)** —— 也就是說，它提供了支援物件導向程式設計的功能，
# 物件導向程式設計具有以下定義性特徵：
#
# -   大部分的計算都以對物件的操作來表示。
#
# -   物件通常代表現實世界中的事物，而方法 (method) 通常對應於現實世界中事物互動的方式。
#
# -   程式包含類別 (class) 和方法 (method) 的定義。
#
# 例如，在上一章中，我們定義了一個 `Time` 類別，它對應於人們記錄一天中時間的方式，
# 我們也定義了一些函數，對應於人們處理時間的各種操作。
# 但是，`Time` 類別的定義和後面的函數定義之間並沒有明確的連結。
# 我們可以透過將函數改寫為 **方法 (method)** 來明確這種連結，方法是定義在類別定義內部的。

# ## 定義方法 (Defining methods)
#
# 在上一章，我們定義了一個叫做 `Time` 的類別，並寫了一個叫做 `print_time` 的函數來顯示一天中的時間。

class Time_v0: # 使用 v0 以區分後續版本
    """表示一天中的某個時間。"""

def print_time_v0(time_obj): # 參數改名
    s_time = f'{time_obj.hour:02d}:{time_obj.minute:02d}:{time_obj.second:02d}'
    print(s_time)

# 要讓 `print_time_v0` 成為一個方法，我們只需要把函數定義移到類別定義裡面。
# 注意縮排的改變。
#
# 同時，我們會把參數名稱從 `time_obj` 改成 `self`。
# 這個改變不是必要的，但依照慣例，方法的第一個參數通常命名為 `self`。

class Time: # 這是新的 Time 類別定義，方法將定義在其中
    """表示一天中的某個時間。"""

    def print_time(self): # self 代表物件實體本身
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

# 要呼叫這個方法，你必須傳遞一個 `Time` 物件作為引數 (隱含地傳給 self)。
# 這是我們用來建立 `Time` 物件的函數 (來自上一章)。

# 為了讓這個 Time 類別能被 make_time_v0 使用，make_time_v0 需要知道 Time 類別
# 我們這裡假設 make_time 會使用當前作用域中的 Time 類別
def make_time_v0(hour_val, minute_val, second_val): # 參數改名
    time_instance = Time() # 現在會使用上面定義的 Time 類別
    time_instance.hour = hour_val
    time_instance.minute = minute_val
    time_instance.second = second_val
    return time_instance

# 這是一個 `Time` 實體。

start_time_obj = make_time_v0(9, 40, 0)

# 現在有兩種方式可以呼叫 `print_time`。第一種 (較不常見)
# 的方式是使用函數語法。

print("--- 使用類別名稱呼叫方法 (較不常見) ---")
Time.print_time(start_time_obj) # 把實體 start_time_obj 當作第一個參數 (self) 傳遞

# 在這個版本中，`Time` 是類別的名稱，`print_time` 是方法的名稱，
# 而 `start_time_obj` 作為參數傳遞。
# 第二種 (更道地) 的方式是使用方法語法：

print("--- 使用實體呼叫方法 (常見) ---")
start_time_obj.print_time() # Python 會自動把 start_time_obj 傳給 self

# 在這個版本中，`start_time_obj` 是方法被調用 (invoke) 於其上的物件，
# 這個物件被稱為 **接收者 (receiver)**，
# 這是基於一個比喻：調用一個方法就像是向一個物件發送一條訊息。
#
# 不論使用哪種語法，方法的行為都是相同的。
# 接收者會被指派給第一個參數，所以在方法內部，`self` 指向與 `start_time_obj` 相同的物件。

# ## 另一個方法 (Another method)
#
# 這是上一章的 `time_to_int` 函數。

def time_to_int_v0(time_obj_tti): # 參數改名
    minutes_total = time_obj_tti.hour * 60 + time_obj_tti.minute
    seconds_total = minutes_total * 60 + time_obj_tti.second
    return seconds_total

# 這是改寫成方法的版本。

# %%add_method_to Time
# 這個 %%add_method_to 是 Jupyter notebook 的魔法指令，在 .py 檔案中無法直接使用。
# 正確的做法是把方法直接定義在 class Time 內部。
# 為了模擬這個效果，我們重新定義 Time 類別並加入這個方法。

class Time: # 重新定義 Time，加入 time_to_int 方法
    """表示一天中的某個時間。"""

    def print_time(self):
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def time_to_int(self): # 新增的方法
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

# 第一行使用了特殊的指令 `%%add_method_to`，它會把一個方法加到先前定義的類別中。
# 這個指令在 Jupyter notebook 中可以運作，但它不是 Python 的一部分，所以在其他環境中無法運作。
# 通常，一個類別的所有方法都定義在類別定義內部，所以它們會與類別同時被定義。
# 但對這本書來說，一次定義一個方法是有幫助的。
#
# 如同上一個例子，方法定義是縮排的，參數名稱是 `self`。
# 除此之外，這個方法與函數是相同的。
# 我們這樣調用它。

# 需要重新建立 start_time_obj，因為 Time 類別被重新定義了
start_time_obj_redef = make_time_v0(9, 40, 0) # make_time_v0 現在會用新的 Time 類別
seconds_total_val = start_time_obj_redef.time_to_int()
print(f"start_time_obj_redef.time_to_int() 的結果: {seconds_total_val}")

# 通常我們說「呼叫 (call)」一個函數，和「調用 (invoke)」一個方法，但它們意思相同。

# ## 靜態方法 (Static methods)
#
# 再舉一個例子，讓我們看看 `int_to_time` 函數。
# 這是上一章的版本。

def int_to_time_v0(total_seconds_itt): # 參數改名
    # make_time_v0 在此仍可使用，它會建立一個 (目前最新定義的) Time 實體
    minutes_itt, second_itt = divmod(total_seconds_itt, 60)
    hour_itt, minute_itt = divmod(minutes_itt, 60)
    return make_time_v0(hour_itt, minute_itt, second_itt)

# 這個函數接收 `total_seconds_itt` 作為參數，並回傳一個新的 `Time` 物件。
# 如果我們把它轉換成 `Time` 類別的一個方法，我們就必須在一個 `Time` 物件上調用它。
# 但是如果我們正試圖建立一個新的 `Time` 物件，我們應該在什麼物件上調用它呢？
#
# 我們可以用 **靜態方法 (static method)** 來解決這個先有雞還是先有蛋的問題，
# 靜態方法是一種不需要類別實體就能被調用的方法。
# 這是我們如何把這個函數改寫成靜態方法。

# 再次重新定義 Time 類別以加入靜態方法
class Time:
    """表示一天中的某個時間。"""

    def print_time(self):
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    # 靜態方法通常用 @staticmethod 裝飾器標註，但書中此處還沒教到
    # 這裡我們先按照書中不加 self 的方式定義，並透過類別名呼叫
    def int_to_time(total_seconds_static): # 沒有 self 參數
        # 靜態方法內部不能直接用 self.attribute
        # 它通常是作為一個工具函數，與類別相關，但不需要實體狀態
        # make_time_v0 仍然可以呼叫，它會建立一個新的 Time 實體
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        # 由於 make_time_v0 會實例化 Time()，這裡的 Time() 指的是目前定義的這個 Time 類別
        return make_time_v0(hour_static, minute_static, second_static)


# 因為它是靜態方法，所以它沒有 `self` 作為參數。
# 要調用它，我們使用 `Time`，也就是類別物件本身。

start_time_from_static = Time.int_to_time(34800) # 34800 秒 = 9 小時 40 分鐘

# 結果是一個代表 9:40 的新物件。

print("--- 測試靜態方法 Time.int_to_time ---")
start_time_from_static.print_time()

# 現在我們有了 `Time.int_to_time` (作為靜態方法)，
# 我們可以用它來把 `add_time` 寫成一個方法。
# 這是上一章的函數版本。

# 為了避免名稱衝突和使用正確的 time_to_int / int_to_time 版本，
# 我們需要確保 add_time_v0 使用的是全域函數版本
def add_time_v0(time_obj_add_v0, hours_add_v0, minutes_add_v0, seconds_add_v0): # 參數改名
    # 這裡的 time_to_int 和 int_to_time 應該是之前定義的全域函數
    # 但為了讓範例在此處能跑，我們假設它們存在或重新定義
    # 假設 time_to_int_v0 和 int_to_time_v0 是可用的全域函數
    duration_time_obj_v0 = make_time_v0(hours_add_v0, minutes_add_v0, seconds_add_v0)
    total_seconds_add_v0 = time_to_int_v0(time_obj_add_v0) + time_to_int_v0(duration_time_obj_v0)
    return int_to_time_v0(total_seconds_add_v0)

# 這是改寫成方法的版本。

# 再次重新定義 Time 類別以加入 add_time 方法
class Time:
    """表示一天中的某個時間。"""

    def print_time(self):
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    # 假設 make_time_v0 在此作用域仍可訪問，並且它會建立目前這個 Time 類別的實體
    # 靜態方法 int_to_time
    def int_to_time(total_seconds_static):
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        return make_time_v0(hour_static, minute_static, second_static)

    # 新增的 add_time 實體方法
    def add_time(self, hours_add_m, minutes_add_m, seconds_add_m): # 參數改名
        # duration 可以用 make_time_v0 建立一個 Time 實體
        duration_time_obj_m = make_time_v0(hours_add_m, minutes_add_m, seconds_add_m)
        # self.time_to_int() 會呼叫目前 Time 類別的 time_to_int 方法
        # duration_time_obj_m.time_to_int() 也是
        total_seconds_add_m = self.time_to_int() + duration_time_obj_m.time_to_int()
        # Time.int_to_time() 會呼叫目前 Time 類別的靜態方法 int_to_time
        return Time.int_to_time(total_seconds_add_m)


# `add_time` 有 `self` 作為參數，因為它不是靜態方法。
# 它是一個普通的方法 —— 也稱為 **實體方法 (instance method)**。
# 要調用它，我們需要一個 `Time` 實體。

# 重新建立 start_time_obj_redef2，使用包含所有方法的 Time 類別
start_time_obj_redef2 = make_time_v0(9, 40, 0)
end_time_from_method = start_time_obj_redef2.add_time(1, 32, 0) # 9:40 + 1h32m = 11:12
print("--- 測試實體方法 add_time ---")
end_time_from_method.print_time()

# ## 比較 Time 物件 (Comparing Time objects)
#
# 再舉一個例子，讓我們把 `is_after` 寫成一個方法。
# 這是 `is_after` 函數，它是上一章一個練習的解答。

def is_after_v0(t1_after_v0, t2_after_v0): # 參數改名
    # 假設 time_to_int_v0 是可用的全域函數
    return time_to_int_v0(t1_after_v0) > time_to_int_v0(t2_after_v0)

# 這是它作為方法的版本。

# 再次重新定義 Time 類別以加入 is_after 方法
class Time:
    """表示一天中的某個時間。"""

    def print_time(self):
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    def int_to_time(total_seconds_static):
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        return make_time_v0(hour_static, minute_static, second_static)

    def add_time(self, hours_add_m, minutes_add_m, seconds_add_m):
        duration_time_obj_m = make_time_v0(hours_add_m, minutes_add_m, seconds_add_m)
        total_seconds_add_m = self.time_to_int() + duration_time_obj_m.time_to_int()
        return Time.int_to_time(total_seconds_add_m)

    # 新增的 is_after 實體方法
    def is_after(self, other_time_obj): # 參數改名
        # self.time_to_int() 和 other_time_obj.time_to_int() 都會呼叫實體方法
        return self.time_to_int() > other_time_obj.time_to_int()


# 因為我們要比較兩個物件，而第一個參數是 `self`，
# 所以我們把第二個參數叫做 `other_time_obj` (書中為 `other`)。
# 要使用這個方法，我們必須在一個物件上調用它，並把另一個物件作為參數傳遞。

# 重新建立實體，使用包含所有方法的 Time 類別
start_compare = make_time_v0(9, 40, 0) # 09:40:00
end_compare = make_time_v0(11, 12, 0)   # 11:12:00 (由 9:40 + 1h32m 得到)

print("--- 測試實體方法 is_after ---")
result_is_after = end_compare.is_after(start_compare) # 11:12 is after 09:40 ?
print(f"end_compare.is_after(start_compare): {result_is_after}") # True

# 這種語法的一個好處是它幾乎可以像問句一樣閱讀：
# 「`end_compare` 是在 `start_compare` 之後嗎？」

# ## __str__ 方法 (The __str__ method)
#
# 當你寫一個方法時，你可以選擇幾乎任何你想要的名字。
# 然而，有些名字有特殊的意義。
# 例如，如果一個物件有一個叫做 `__str__` 的方法，Python 會用這個方法把物件轉換成字串。
# 例如，這裡是一個 Time 物件的 `__str__` 方法。
# (注意：前後各兩個底線，稱為 "dunder" 方法，dunder 是 double underscore 的縮寫)

# 再次重新定義 Time 類別以加入 __str__ 方法
class Time:
    """表示一天中的某個時間。"""

    def print_time(self): # 雖然有了 __str__，print_time 仍然可以保留
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    def int_to_time(total_seconds_static):
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        return make_time_v0(hour_static, minute_static, second_static)

    def add_time(self, hours_add_m, minutes_add_m, seconds_add_m):
        duration_time_obj_m = make_time_v0(hours_add_m, minutes_add_m, seconds_add_m)
        total_seconds_add_m = self.time_to_int() + duration_time_obj_m.time_to_int()
        return Time.int_to_time(total_seconds_add_m)

    def is_after(self, other_time_obj):
        return self.time_to_int() > other_time_obj.time_to_int()

    # 新增的 __str__ 特殊方法
    def __str__(self): # __str__ 必須回傳一個字串
        s_time_str = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        return s_time_str


# 這個方法類似於上一章的 `print_time`，只是它回傳字串而不是印出字串。
#
# 你可以用通常的方式調用這個方法。

# 重新建立實體，使用包含 __str__ 的 Time 類別
end_str_test = make_time_v0(11, 12, 0)
str_representation = end_str_test.__str__()
print(f"end_str_test.__str__(): {str_representation}")

# 但 Python 也可以為你調用它。
# 如果你使用內建函數 `str()` 來把 `Time` 物件轉換成字串，
# Python 會使用 `Time` 類別中的 `__str__` 方法。

str_from_builtin = str(end_str_test)
print(f"str(end_str_test): {str_from_builtin}")

# 如果你印出一個 `Time` 物件，它也會做同樣的事情。
# (print 函數內部會嘗試呼叫物件的 __str__ 方法)

print("--- print(end_str_test) 會自動呼叫 __str__ ---")
print(end_str_test)

# 像 `__str__` 這樣的方法稱為 **特殊方法 (special methods)**。
# 你可以透過它們的名字以兩個底線開頭和結尾來識別它們。

# ## __init__ 方法 (The __init__ method)
#
# 特殊方法中最特別的是 `__init__`，之所以這麼稱呼是因為它會初始化 (initialize)
# 一個新物件的屬性。
# `Time` 類別的 `__init__` 方法可能看起來像這樣：
# (`__init__` 類似於其他語言中的建構子 (constructor))

# 最終版本的 Time 類別，包含 __init__ 和其他方法
class Time:
    """表示一天中的某個時間。"""

    def __init__(self, hour_init=0, minute_init=0, second_init=0): # 參數改名並加上預設值
        # __init__ 方法不應該回傳任何東西 (除了隱含的 None)
        # 它的工作是設定 self 的屬性
        self.hour = hour_init
        self.minute = minute_init
        self.second = second_init

    def print_time(self): # 為了與書中一致，保留 (雖然有了 __str__，直接 print 就好)
        s_time = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s_time)

    def __str__(self):
        s_time_str = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        return s_time_str

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    # 靜態方法 int_to_time，用來從秒數建立 Time 物件
    # 為了讓它能建立目前這個 Time 類別的實體，它應該使用 cls (類別本身)
    # 或者，如果 make_time_v0 不再需要，可以直接在靜態方法中實例化
    @staticmethod # 標準的靜態方法標記法 (雖然書中此處還沒教)
    def int_to_time(total_seconds_static):
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        # 直接用 Time() 呼叫 __init__ 來建立實體
        return Time(hour_static, minute_static, second_static)

    def add_time(self, hours_add_m, minutes_add_m, seconds_add_m):
        # 建立一個代表時長的 Time 物件
        duration_time_obj_m = Time(hours_add_m, minutes_add_m, seconds_add_m) # 使用 __init__
        total_seconds_add_m = self.time_to_int() + duration_time_obj_m.time_to_int()
        return Time.int_to_time(total_seconds_add_m) # 使用靜態方法

    def is_after(self, other_time_obj):
        if not isinstance(other_time_obj, Time): # 檢查 other_time_obj 是否為 Time 實體
            return NotImplemented # 表示無法比較
        return self.time_to_int() > other_time_obj.time_to_int()


# 現在當我們實體化一個 `Time` 物件時，Python 會調用 `__init__`，並傳遞引數。
# 所以我們可以同時建立物件並初始化其屬性。

time_with_init = Time(9, 40, 0) # 呼叫 Time() 時，引數會傳給 __init__
print("--- 使用 __init__ 建立 Time 物件 ---")
print(time_with_init) # print 會用 __str__

# 在這個例子中，參數是選擇性的，所以如果你呼叫 `Time` 時不帶任何引數，
# 你會得到預設值。

time_default_init = Time() # 使用 __init__ 的預設值 (0, 0, 0)
print(time_default_init)

# 如果你提供一個引數，它會覆寫 `hour_init`：

time_one_arg_init = Time(9) # hour=9, minute=0, second=0
print(time_one_arg_init)

# 如果你提供兩個引數，它們會覆寫 `hour_init` 和 `minute_init`。

time_two_args_init = Time(9, 45) # hour=9, minute=45, second=0
print(time_two_args_init)

# 如果你提供三個引數，它們會覆寫所有三個預設值。
#
# 當我寫一個新的類別時，我幾乎總是從寫 `__init__` 開始，它讓建立物件更容易，
# 然後寫 `__str__`，它對於除錯很有用。

# ## 運算子重載 (Operator overloading)
#
# 透過定義其他特殊方法，你可以指定運算子對程式設計師自訂型別的行為。
# 例如，如果你為 `Time` 類別定義一個叫做 `__add__` 的方法，
# 你就可以在 Time 物件上使用 `+` 運算子。
#
# 這裡有一個 `__add__` 方法。
# (注意：這個 __add__ 的邏輯是把兩個時間點當作持續時間來相加，
#  結果可能是一個超過 24 小時的時間，然後再轉換回 Time 物件。
#  這與之前 add_time(self, hours, minutes, seconds) 的語義不同，
#  後者是時間點加上一個時長。)

# 再次重新定義 Time 類別以加入 __add__ 方法
class Time:
    """表示一天中的某個時間。"""

    def __init__(self, hour_init=0, minute_init=0, second_init=0):
        self.hour = hour_init
        self.minute = minute_init
        self.second = second_init

    def __str__(self):
        s_time_str = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        return s_time_str

    def time_to_int(self):
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total

    @staticmethod
    def int_to_time(total_seconds_static):
        minutes_static, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static, 60)
        # 如果要處理天數，這裡需要調整
        # hour_static %= 24 # 例如，只保留 0-23 小時
        return Time(hour_static, minute_static, second_static)

    # __add__ 方法讓你可以用 t1 + t2
    def __add__(self, other_time_add):
        if not isinstance(other_time_add, Time):
            # 如果 other_time_add 不是 Time 物件，可以引發 TypeError 或回傳 NotImplemented
            return NotImplemented # 表示這個操作對這些型別未定義

        # 把兩個 Time 物件都轉換成總秒數，相加，然後再轉換回 Time 物件
        total_seconds_sum_add = self.time_to_int() + other_time_add.time_to_int()
        return Time.int_to_time(total_seconds_sum_add)
        # 注意：這樣的加法意義是把兩個「時間點」當作「時長」來加。
        # 例如 01:00:00 + 02:00:00 = 03:00:00。
        # 如果是時間點加時長，other_time_add 應該是一個時長，而不是另一個時間點。
        # 書中此處的例子是把兩個 Time 物件相加。

    # is_after (為了完整性，從前面複製過來)
    def is_after(self, other_time_obj):
        if not isinstance(other_time_obj, Time):
            return NotImplemented
        return self.time_to_int() > other_time_obj.time_to_int()


# 我們可以像這樣使用它。

start_op_ov = Time(9, 40, 0) # 09:40:00
duration_op_ov = Time(1, 32, 0) # 01:32:00 (代表一個時長)
print("--- 測試運算子重載 __add__ ---")
# 這裡 start_op_ov + duration_op_ov 會呼叫 start_op_ov.__add__(duration_op_ov)
end_op_ov = start_op_ov + duration_op_ov
print(f"{start_op_ov} + {duration_op_ov} = {end_op_ov}") # (9*3600+40*60) + (1*3600+32*60) = 34800 + 5520 = 40320
                                                     # 40320 秒 = 11 小時 12 分 0 秒 => 11:12:00


# 當我們執行這三行程式碼時，發生了很多事情：
#
# * 當我們實體化一個 `Time` 物件時，會調用 `__init__` 方法。
#
# * 當我們對 `Time` 物件使用 `+` 運算子時，會調用它的 `__add__` 方法。
#
# * 當我們印出一個 `Time` 物件時，會調用它的 `__str__` 方法。
#
# 改變一個運算子的行為，使其適用於程式設計師自訂的型別，稱為 **運算子重載 (operator overloading)**。
# 對於每個運算子，像是 `+`，都有一個對應的特殊方法，像是 `__add__`。

# ## 除錯 (Debugging)
#
# 如果 `minute` 和 `second` 的值介於 `0` 和 `60` 之間 (包含 `0` 但不包含 `60`)，
# 並且 `hour` 是正數 (或非負數，取決於定義)，則 `Time` 物件是有效的。
# 此外，`hour` 和 `minute` 應該是整數值，但我們可能允許 `second` 有小數部分。
# 像這樣的需求稱為 **不變量 (invariants)**，因為它們應該總是為真。
# 換句話說，如果它們不為真，就表示出了問題。
#
# 編寫檢查不變量的程式碼可以幫助偵測錯誤並找出原因。
# 例如，你可能有一個像 `is_valid` 這樣的方法，它接收一個 Time 物件，
# 如果它違反了不變量，就回傳 `False`。

# 再次重新定義 Time 類別以加入 is_valid 方法
class Time:
    """表示一天中的某個時間。"""

    def __init__(self, hour_init=0, minute_init=0, second_init=0):
        self.hour = hour_init
        self.minute = minute_init
        self.second = second_init
        # 可以在 __init__ 中就檢查不變量
        # if not self.is_valid():
        #     raise ValueError("無效的時間值傳給建構子")


    def __str__(self):
        # 允許 second 是浮點數，但顯示時可以格式化
        # 為了簡單，假設 second 也是整數或能被 :02d 處理
        return f'{self.hour:02d}:{self.minute:02d}:{int(self.second):02d}'


    def time_to_int(self):
        # 假設 second 是數字 (可以是浮點數)
        minutes_total = self.hour * 60 + self.minute
        seconds_total = minutes_total * 60 + self.second
        return seconds_total # 結果可能是浮點數

    @staticmethod
    def int_to_time(total_seconds_static):
        # total_seconds_static 可能是浮點數
        minutes_static_total, second_static = divmod(total_seconds_static, 60)
        hour_static, minute_static = divmod(minutes_static_total, 60)
        # 結果的時和分是整數，秒可能是浮點數
        return Time(int(hour_static), int(minute_static), second_static)


    def __add__(self, other_time_add):
        if not isinstance(other_time_add, Time):
            return NotImplemented
        total_seconds_sum_add = self.time_to_int() + other_time_add.time_to_int()
        return Time.int_to_time(total_seconds_sum_add)

    # 新增的 is_valid 實體方法
    def is_valid(self):
        # 假設 hour 應為非負整數
        if not (isinstance(self.hour, int) and self.hour >= 0):
            # print(f"Hour 無效: {self.hour}")
            return False
        # minute 應為 0-59 的整數
        if not (isinstance(self.minute, int) and 0 <= self.minute < 60):
            # print(f"Minute 無效: {self.minute}")
            return False
        # second 應為 0-59.99... 的數字 (允許浮點數)
        if not (isinstance(self.second, (int, float)) and 0 <= self.second < 60):
            # print(f"Second 無效: {self.second}")
            return False
        return True

    # is_after 方法，加入 assert 檢查
    def is_after(self, other_time_obj):
        # assert 語句：如果條件為 False，會引發 AssertionError
        # 可以在開發和測試階段幫助發現問題
        assert self.is_valid(), 'self (第一個時間) 不是一個有效的 Time 物件'
        assert isinstance(other_time_obj, Time), 'other (第二個時間) 必須是 Time 物件'
        assert other_time_obj.is_valid(), 'other (第二個時間) 不是一個有效的 Time 物件'
        return self.time_to_int() > other_time_obj.time_to_int()


# 然後，在每個方法的開頭，你可以檢查參數以確保它們是有效的。

# is_after 方法已在上面 Time 類別的最新定義中加入了 assert

# `assert` 陳述式會評估後面的表達式。如果結果是 `True`，它什麼也不做；
# 如果結果是 `False`，它會引發一個 `AssertionError`。
# 這裡有一個例子。

start_assert_test = Time(9, 40, 0) # 有效時間
duration_invalid = Time(minute=132) # 建立一個無效時間 (minute=132)
print(f"start_assert_test: {start_assert_test}, is_valid: {start_assert_test.is_valid()}")
print(f"duration_invalid: {duration_invalid}, is_valid: {duration_invalid.is_valid()}") # False

%%expect AssertionError
# 現在呼叫 is_after，其中一個參數是無效的
# start_assert_test.is_after(duration_invalid)
# 上面的 is_after 實現中，other.is_valid() 會是 False，所以 assert 會失敗

# `assert` 陳述式很有用，因為它們區分了處理正常情況的程式碼和檢查錯誤的程式碼。
# (在生產環境中，assert 可能會被優化掉，所以不應該用來處理預期會發生的錯誤，
#  而是用來檢查程式設計師的假設是否成立。)

# ## 詞彙表 (Glossary)
#
# **物件導向語言 (object-oriented language):**
#  一種提供功能來支援物件導向程式設計的語言，特別是使用者自訂型別。
#
# **方法 (method):**
#  一個定義在類別定義內部，並在該類別的實體上調用的函數。
#
# **接收者 (receiver):**
#  方法被調用於其上的物件。
#
# **靜態方法 (static method):**
#  一個可以不需要物件作為接收者就能被調用的方法。
#
# **實體方法 (instance method):**
#  一個必須有一個物件作為接收者才能被調用的方法。
#
# **特殊方法 (special method):**
#  一種改變運算子和某些函數與物件運作方式的方法 (通常名稱前後有雙底線)。
#
# **運算子重載 (operator overloading):**
#  使用特殊方法來改變運算子與使用者自訂型別運作方式的過程。
#
# **不變量 (invariant):**
#  在程式執行期間應該總是為真的條件。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 想了解更多關於靜態方法的資訊，可以問問虛擬助理：
#
# * 「實體方法和靜態方法有什麼區別？」
#
# * 「為什麼靜態方法被稱為靜態的？」
#
# 如果你請虛擬助理產生一個靜態方法，結果可能會以 `@staticmethod` 開頭，
# 這是一個「裝飾器 (decorator)」，用來表示它是一個靜態方法。
# 本書沒有涵蓋裝飾器，但如果你好奇，可以向虛擬助理詢問更多資訊。
#
# 在本章中，我們把幾個函數改寫成了方法。
# 虛擬助理通常很擅長這類程式碼轉換。
# 作為例子，把下面的函數貼到虛擬助理中，然後問它：「請把這個函數改寫成 `Time` 類別的一個方法。」
# (注意：虛擬助理可能會產生包含 `__init__` 的完整類別定義，而不只是單獨的方法)

# 這是上一章的 subtract_time 函數 (假設 time_to_int_v0 是全域可用的)
def subtract_time_v0_for_va(t1_va, t2_va): # 參數改名
    # 為了讓這個函數獨立運作，我們需要 time_to_int_v0
    # 假設它已經定義
    # return time_to_int_v0(t1_va) - time_to_int_v0(t2_va)
    # 為了能在這裡執行，我們用 Time 類別的方法版本 (如果有 Time 實體的話)
    # 或者我們可以把 time_to_int_v0 複製到這裡
    if hasattr(t1_va, 'time_to_int') and hasattr(t2_va, 'time_to_int'):
        return t1_va.time_to_int() - t2_va.time_to_int()
    else:
        print("警告: subtract_time_v0_for_va 的參數可能不是具有 time_to_int 方法的物件。")
        return None # 或引發錯誤


# ### 練習
#
# 在上一章中，一系列練習要求你編寫一個 `Date` 類別和幾個處理 `Date` 物件的函數。
# 現在讓我們練習把那些函數改寫成方法。
#
# 1. 編寫一個 `Date` 類別的定義，用來表示一個日期 —— 也就是年、月、日。
#
# 2. 編寫一個 `__init__` 方法，它接收 `year`、`month` 和 `day` 作為參數，並將這些參數指派給屬性。建立一個代表 1933 年 6 月 22 日的物件。
#
# 3. 編寫一個 `__str__` 方法，它使用 f-字串來格式化屬性並回傳結果。如果你用你建立的 `Date` 物件來測試它，結果應該是 `1933-06-22`。
#
# 4. 編寫一個叫做 `is_after` 的方法，它接收兩個 `Date` 物件 (其中一個是 `self`) 並回傳 `True` 如果第一個 (self) 在第二個 (other) 之後。建立一個代表 1933 年 9 月 17 日的第二個物件，並檢查它是否在第一個物件之後。
#
# 提示：你可能會發現編寫一個叫做 `to_tuple` 的方法很有用，它回傳一個包含 `Date` 物件年、月、日屬性 (按此順序) 的元組。

# 解答

class Date:
    """表示一個日期，包含年、月、日。"""

    def __init__(self, year_dt, month_dt, day_dt): # 參數改名
        # 可以在這裡加入對日期有效性的檢查，例如月份 1-12，日期對應月份有效等
        # 為了簡化，我們先假設輸入是有效的
        self.year = year_dt
        self.month = month_dt
        self.day = day_dt

    def __str__(self): # 參數通常命名為 self，即使書中 Date 的 __str__ 用了 date
                       # 為了與慣例一致，這裡用 self
        return f'{self.year}-{self.month:02d}-{self.day:02d}'

    def to_tuple(self):
        """回傳一個 (年, 月, 日) 的元組。"""
        return (self.year, self.month, self.day)

    def is_after(self, other_date_obj): # 參數改名
        """檢查 self 是否在 other_date_obj 之後。"""
        if not isinstance(other_date_obj, Date):
            return NotImplemented # 或引發 TypeError
        return self.to_tuple() > other_date_obj.to_tuple()

# 你可以用這些例子來測試你的解答。

birthday1_date_ex = Date(1933, 6, 22)
print("\n--- Date 類別練習測試 ---")
print(f"birthday1_date_ex (使用 __str__): {birthday1_date_ex}")

birthday2_date_ex = Date(1933, 9, 17)
print(f"birthday2_date_ex (使用 __str__): {birthday2_date_ex}")

# birthday1_date_ex (06-22) is after birthday2_date_ex (09-17) ?
result_after_date1 = birthday1_date_ex.is_after(birthday2_date_ex)
print(f"birthday1_date_ex.is_after(birthday2_date_ex): {result_after_date1}")  # 應該是 False

# birthday2_date_ex (09-17) is after birthday1_date_ex (06-22) ?
result_after_date2 = birthday2_date_ex.is_after(birthday1_date_ex)
print(f"birthday2_date_ex.is_after(birthday1_date_ex): {result_after_date2}")  # 應該是 True

# (這個儲存格是空的)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)