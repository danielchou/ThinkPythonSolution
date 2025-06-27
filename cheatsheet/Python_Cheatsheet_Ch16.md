# Python 語法速查表 - 第 16 章：類別與函式

## 時間類別範例
```python
class Time:
    """表示一天中的時間。
    屬性：hour, minute, second
    """
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def __str__(self):
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    def print_time(self):
        print(str(self))
    
    def time_to_int(self):
        """將時間轉換為秒數"""
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds
    
    def int_to_time(seconds):
        """將秒數轉換為 Time 物件"""
        time = Time()
        minutes, time.second = divmod(seconds, 60)
        time.hour, time.minute = divmod(minutes, 60)
        return time
    
    def add_time(self, other):
        """將兩個時間相加"""
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)
    
    def __add__(self, other):
        """重載 + 運算符"""
        if isinstance(other, Time):
            return self.add_time(other)
        else:
            return NotImplemented
```

## 純函式與修改器
```python
# 純函式：不修改傳入的參數
def add_time(t1, t2):
    sum = Time()
    sum.hour = t1.hour + t2.hour
    sum.minute = t1.minute + t2.minute
    sum.second = t1.second + t2.second
    
    if sum.second >= 60:
        sum.second -= 60
        sum.minute += 1
    
    if sum.minute >= 60:
        sum.minute -= 60
        sum.hour += 1
    
    return sum

# 修改器：修改傳入的參數
def increment(time, seconds):
    time.second += seconds
    
    if time.second >= 60:
        time.second -= 60
        time.minute += 1
    
    if time.minute >= 60:
        time.minute -= 60
        time.hour += 1
```

## 原型開發與規劃開發
```python
# 原型開發：先實現基本功能，再逐步改進
def add_time_simple(t1, t2):
    sum = Time()
    sum.hour = t1.hour + t2.hour
    sum.minute = t1.minute + t2.minute
    sum.second = t1.second + t2.second
    return sum  # 可能需要處理進位

# 規劃開發：設計更完善的解決方案
def add_time_planned(t1, t2):
    # 轉換為秒數
    seconds1 = t1.hour * 3600 + t1.minute * 60 + t1.second
    seconds2 = t2.hour * 3600 + t2.minute * 60 + t2.second
    total_seconds = seconds1 + seconds2
    
    # 轉換回時、分、秒
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # 創建新的 Time 物件
    sum_time = Time(hours, minutes, seconds)
    return sum_time
```

## 調試技巧
```python
# 使用 print 語句
def debug_time():
    t = Time(12, 59, 30)
    print(f'原始時間: {t}')
    t.minute += 1
    print(f'加一分鐘後: {t}')

# 使用 assert 語句
def add_time_with_assert(t1, t2):
    seconds = t1.time_to_int() + t2.time_to_int()
    result = Time.int_to_time(seconds)
    
    # 驗證結果
    assert 0 <= result.hour < 24
    assert 0 <= result.minute < 60
    assert 0 <= result.second < 60
    
    return result

# 使用單元測試
import unittest

class TestTime(unittest.TestCase):
    def test_add_time(self):
        t1 = Time(1, 30, 0)
        t2 = Time(2, 40, 0)
        result = t1.add_time(t2)
        self.assertEqual(result.hour, 4)
        self.assertEqual(result.minute, 10)
        self.assertEqual(result.second, 0)
```

## 介面與實現
```python
class Time:
    """介面：Time 類別提供的方法和屬性
    - 建構函式：__init__(hour, minute, second)
    - 字串表示：__str__()
    - 時間轉換：time_to_int(), int_to_time()
    - 時間運算：add_time(), __add__()
    """
    
    def __init__(self, hour=0, minute=0, second=0):
        """實現：初始化 Time 物件"""
        # 檢查輸入值的有效性
        if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
            raise ValueError('Hour, minute, and second must be valid.')
        self.hour = hour
        self.minute = minute
        self.second = second
    
    # 其他方法實現...
```

## 多態與鴨子型別
```python
# 多態：不同類別實現相同的方法
class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def __str__(self):
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'

class Date:
    def __init__(self, year=0, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self):
        return f'{self.year:04d}-{self.month:02d}-{self.day:02d}'

# 鴨子型別：如果它走路像鴨子、叫聲像鴨子，那麼它就是鴨子
def print_object(obj):
    print(str(obj))  # 只要物件有 __str__ 方法就可以使用

# 使用多態
time = Time(12, 30, 0)
date = Date(2023, 5, 15)
print_object(time)  # 12:30:00
print_object(date)  # 2023-05-15
```

## 類別方法與靜態方法
```python
class Time:
    @staticmethod
    def is_valid_time(hour, minute, second):
        """靜態方法：檢查時間是否有效"""
        return 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60
    
    @classmethod
    def from_string(cls, time_str):
        """類別方法：從字串創建 Time 物件"""
        hour, minute, second = map(int, time_str.split(':'))
        if cls.is_valid_time(hour, minute, second):
            return cls(hour, minute, second)
        else:
            raise ValueError('Invalid time string')
    
    def __init__(self, hour=0, minute=0, second=0):
        if not Time.is_valid_time(hour, minute, second):
            raise ValueError('Invalid time')
        self.hour = hour
        self.minute = minute
        self.second = second

# 使用類別方法和靜態方法
valid = Time.is_valid_time(12, 30, 0)  # True
time = Time.from_string('12:30:00')    # 創建 Time 物件
```

## 函式式編程與類別
```python
# 使用函式式編程
def time_to_int(time):
    return time.hour * 3600 + time.minute * 60 + time.second

def int_to_time(seconds):
    time = Time()
    minutes, time.second = divmod(seconds, 60)
    time.hour, time.minute = divmod(minutes, 60)
    return time

def add_times(t1, t2):
    seconds = time_to_int(t1) + time_to_int(t2)
    return int_to_time(seconds)

# 使用類別方法
class Time:
    def time_to_int(self):
        return self.hour * 3600 + self.minute * 60 + self.second
    
    @staticmethod
    def int_to_time(seconds):
        time = Time()
        minutes, time.second = divmod(seconds, 60)
        time.hour, time.minute = divmod(minutes, 60)
        return time
    
    def add_time(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)
```
