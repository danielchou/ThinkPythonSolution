# Python 語法速查表 - 第 17 章：類別與方法

## 物件導向的方法
```python
# 傳統函式寫法
def print_time(time):
    print(f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}")

# 物件導向方法寫法
class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def print_time(self):
        print(f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}")

# 使用方式比較
time = Time(9, 45, 0)
print_time(time)  # 傳統函式呼叫
time.print_time() # 物件導向方法呼叫
```

## 方法的類型
```python
class Example:
    count = 0  # 類別變數
    
    def __init__(self, value):
        self.value = value  # 實例變數
        Example.count += 1
    
    # 實例方法：第一個參數是 self
    def instance_method(self):
        return f"實例方法，值為 {self.value}"
    
    # 類別方法：第一個參數是 cls
    @classmethod
    def class_method(cls):
        return f"類別方法，計數為 {cls.count}"
    
    # 靜態方法：沒有特定的第一個參數
    @staticmethod
    def static_method(x, y):
        return x + y

# 使用各種方法
e = Example(42)
print(e.instance_method())  # 實例方法，值為 42
print(Example.class_method())  # 類別方法，計數為 1
print(Example.static_method(10, 20))  # 30
```

## 運算符重載
```python
class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
    
    def __add__(self, other):
        """加法運算符 +"""
        seconds = self.time_to_int() + other.time_to_int()
        return int_to_time(seconds)
    
    def __sub__(self, other):
        """減法運算符 -"""
        seconds = self.time_to_int() - other.time_to_int()
        return int_to_time(seconds)
    
    def __eq__(self, other):
        """等於運算符 =="""
        return (self.hour == other.hour and
                self.minute == other.minute and
                self.second == other.second)
    
    def __lt__(self, other):
        """小於運算符 <"""
        t1 = (self.hour, self.minute, self.second)
        t2 = (other.hour, other.minute, other.second)
        return t1 < t2
    
    # 其他比較運算符會自動根據 __eq__ 和 __lt__ 生成
    
    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

def int_to_time(seconds):
    time = Time()
    minutes, time.second = divmod(seconds, 60)
    time.hour, time.minute = divmod(minutes, 60)
    return time

# 使用運算符
t1 = Time(9, 45, 0)
t2 = Time(1, 30, 0)
print(t1 + t2)  # 11:15:00
print(t1 - t2)  # 08:15:00
print(t1 == t2)  # False
print(t1 < t2)   # False
```

## 類型基於方法
```python
# 鴨子型別：如果它走路像鴨子、叫聲像鴨子，那麼它就是鴨子
class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def __add__(self, other):
        if hasattr(other, 'time_to_int'):
            # 如果 other 有 time_to_int 方法，就視為 Time 物件
            return self.add_time(other)
        else:
            # 否則嘗試將 other 視為秒數
            return self.increment(other)
    
    def add_time(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return int_to_time(seconds)
    
    def increment(self, seconds):
        seconds += self.time_to_int()
        return int_to_time(seconds)
    
    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

# 另一個具有相容方法的類別
class TimeSpan:
    def __init__(self, seconds):
        self.seconds = seconds
    
    def time_to_int(self):
        return self.seconds

# 使用鴨子型別
t1 = Time(1, 30, 0)
t2 = TimeSpan(3600)  # 1小時的秒數
print(t1 + t2)  # 可以相加，因為 TimeSpan 有 time_to_int 方法
```

## 多態
```python
class Shape:
    def area(self):
        pass  # 抽象方法，由子類實現

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

# 多態函式
def print_area(shape):
    print(f"面積: {shape.area()}")

# 使用多態
shapes = [Rectangle(5, 10), Circle(7)]
for shape in shapes:
    print_area(shape)  # 根據實際類型調用不同的 area 方法
```

## 介面與協議
```python
# Python 中的介面是非正式的，通常通過抽象基類或協議來實現
from abc import ABC, abstractmethod

# 使用抽象基類定義介面
class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

# 實現介面
class Circle(Drawable):
    def __init__(self, radius):
        self.radius = radius
    
    def draw(self):
        print(f"繪製半徑為 {self.radius} 的圓")

# 使用協議（Python 3.8+）
from typing import Protocol

class Printable(Protocol):
    def print_out(self) -> None:
        ...

class Document:
    def print_out(self) -> None:
        print("列印文件")

# 檢查類型是否符合協議
def is_printable(obj: Printable) -> bool:
    return hasattr(obj, 'print_out') and callable(obj.print_out)

doc = Document()
print(is_printable(doc))  # True
```

## 繼承與組合
```python
# 繼承
class Vehicle:
    def __init__(self, color):
        self.color = color
    
    def move(self):
        print("移動中...")

class Car(Vehicle):
    def __init__(self, color, brand):
        super().__init__(color)  # 調用父類的初始化方法
        self.brand = brand
    
    def move(self):
        print("開車中...")
        super().move()  # 調用父類的方法

# 組合
class Engine:
    def start(self):
        print("引擎啟動")
    
    def stop(self):
        print("引擎停止")

class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand
        self.engine = Engine()  # 組合
    
    def start(self):
        print(f"{self.color} {self.brand} 車輛啟動")
        self.engine.start()  # 委託給組合物件
```

## 方法解析順序 (MRO)
```python
# 多重繼承中的方法解析順序
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()

class C(A):
    def method(self):
        print("C.method")
        super().method()

class D(B, C):
    def method(self):
        print("D.method")
        super().method()

# 查看方法解析順序
print(D.__mro__)  # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# 調用方法
d = D()
d.method()
# 輸出:
# D.method
# B.method
# C.method
# A.method
```

## 屬性裝飾器
```python
class Person:
    def __init__(self, name, age=0):
        self._name = name
        self._age = age
    
    # 使用 property 裝飾器
    @property
    def name(self):
        """獲取姓名"""
        return self._name
    
    @name.setter
    def name(self, value):
        """設置姓名"""
        if not isinstance(value, str):
            raise TypeError("姓名必須是字串")
        self._name = value
    
    @property
    def age(self):
        """獲取年齡"""
        return self._age
    
    @age.setter
    def age(self, value):
        """設置年齡"""
        if not isinstance(value, int):
            raise TypeError("年齡必須是整數")
        if value < 0:
            raise ValueError("年齡不能為負數")
        self._age = value
    
    # 只讀屬性
    @property
    def is_adult(self):
        """判斷是否成年"""
        return self._age >= 18

# 使用屬性
person = Person("Alice", 25)
print(person.name)  # Alice
print(person.is_adult)  # True

person.name = "Bob"  # 使用 setter
person.age = 17  # 使用 setter
print(person.name)  # Bob
print(person.is_adult)  # False

# 錯誤示例
# person.is_adult = True  # 錯誤：只讀屬性不能設置
# person.age = -5  # 錯誤：年齡不能為負數
```
