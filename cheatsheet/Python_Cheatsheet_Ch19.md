# Python 語法速查表 - 第 19 章：特殊方法

## 基本特殊方法
```python
class Point:
    def __init__(self, x=0, y=0):
        """初始化方法，創建物件時調用"""
        self.x = x
        self.y = y
    
    def __str__(self):
        """字串表示方法，用於 str() 和 print()"""
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        """官方字串表示方法，用於 repr() 和互動式環境"""
        return f"Point({self.x}, {self.y})"
    
    def __bool__(self):
        """布林值方法，用於 bool() 和條件判斷"""
        return self.x != 0 or self.y != 0

# 使用基本特殊方法
p = Point(3, 4)
print(str(p))    # (3, 4)
print(repr(p))   # Point(3, 4)
print(bool(p))   # True
print(bool(Point()))  # False
```

## 比較特殊方法
```python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """等於運算符 =="""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        """不等於運算符 !="""
        return not (self == other)
    
    def __lt__(self, other):
        """小於運算符 <"""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x < other.x or (self.x == other.x and self.y < other.y)
    
    def __le__(self, other):
        """小於等於運算符 <="""
        return self < other or self == other
    
    def __gt__(self, other):
        """大於運算符 >"""
        return not (self <= other)
    
    def __ge__(self, other):
        """大於等於運算符 >="""
        return not (self < other)

# 使用比較特殊方法
p1 = Point(3, 4)
p2 = Point(3, 4)
p3 = Point(5, 6)

print(p1 == p2)  # True
print(p1 != p3)  # True
print(p1 < p3)   # True
print(p3 > p1)   # True
```

## 數值運算特殊方法
```python
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        """加法運算符 +"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """減法運算符 -"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """乘法運算符 *"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """反向乘法運算符 *"""
        return self.__mul__(scalar)
    
    def __neg__(self):
        """負號運算符 -"""
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        """絕對值運算符 abs()"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 使用數值運算特殊方法
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)   # (4, 6)
print(v1 - v2)   # (2, 2)
print(v1 * 2)    # (6, 8)
print(2 * v1)    # (6, 8)
print(-v1)       # (-3, -4)
print(abs(v1))   # 5.0
```

## 容器特殊方法
```python
class MyList:
    def __init__(self, items=None):
        self.items = items or []
    
    def __len__(self):
        """長度運算符 len()"""
        return len(self.items)
    
    def __getitem__(self, index):
        """索引運算符 []"""
        return self.items[index]
    
    def __setitem__(self, index, value):
        """索引賦值運算符 [] ="""
        self.items[index] = value
    
    def __delitem__(self, index):
        """索引刪除運算符 del []"""
        del self.items[index]
    
    def __iter__(self):
        """迭代器運算符 for in"""
        return iter(self.items)
    
    def __contains__(self, item):
        """成員運算符 in"""
        return item in self.items
    
    def __reversed__(self):
        """反向迭代器運算符 reversed()"""
        return reversed(self.items)

# 使用容器特殊方法
my_list = MyList([1, 2, 3, 4, 5])

print(len(my_list))      # 5
print(my_list[2])        # 3
my_list[1] = 10
print(my_list[1])        # 10
del my_list[0]
print(3 in my_list)      # True

# 迭代
for item in my_list:
    print(item, end=' ')  # 10 3 4 5

# 反向迭代
print()
for item in reversed(my_list):
    print(item, end=' ')  # 5 4 3 10
```

## 屬性存取特殊方法
```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    def __getattr__(self, name):
        """當訪問不存在的屬性時調用"""
        return f"屬性 '{name}' 不存在"
    
    def __setattr__(self, name, value):
        """當設置屬性時調用"""
        print(f"設置屬性 '{name}' 為 {value}")
        # 使用父類的 __setattr__ 來實際設置屬性
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        """當刪除屬性時調用"""
        print(f"刪除屬性 '{name}'")
        super().__delattr__(name)
    
    def __getattribute__(self, name):
        """當訪問任何屬性時調用（包括存在的屬性）"""
        print(f"訪問屬性 '{name}'")
        return super().__getattribute__(name)

# 使用屬性存取特殊方法
person = Person("Alice", 30)  # 設置屬性 '_name' 為 Alice
                              # 設置屬性 '_age' 為 30

print(person._name)  # 訪問屬性 '_name'
                     # Alice

print(person.xyz)    # 訪問屬性 'xyz'
                     # 訪問屬性 '__getattr__'
                     # 屬性 'xyz' 不存在

person.job = "工程師"  # 設置屬性 'job' 為 工程師

del person.job       # 刪除屬性 'job'
```

## 可調用物件
```python
class Adder:
    def __init__(self, n):
        self.n = n
    
    def __call__(self, x):
        """使物件可以像函式一樣被調用"""
        return self.n + x

# 使用可調用物件
add5 = Adder(5)
print(add5(10))  # 15
print(add5(20))  # 25

# 檢查物件是否可調用
print(callable(add5))  # True
```

## 上下文管理器
```python
class MyContext:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        """進入 with 區塊時調用"""
        print(f"進入 {self.name} 上下文")
        return self  # 返回值會被賦給 as 子句中的變數
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """離開 with 區塊時調用"""
        print(f"離開 {self.name} 上下文")
        # 如果返回 True，則會抑制任何異常
        if exc_type is not None:
            print(f"發生異常: {exc_val}")
            return True  # 抑制異常

# 使用上下文管理器
with MyContext("測試") as ctx:
    print("在上下文中")
    print(f"上下文名稱: {ctx.name}")
# 輸出:
# 進入 測試 上下文
# 在上下文中
# 上下文名稱: 測試
# 離開 測試 上下文

# 處理異常的上下文管理器
with MyContext("異常處理") as ctx:
    print("即將發生異常")
    raise ValueError("測試異常")
    print("這行不會執行")
print("繼續執行")
# 輸出:
# 進入 異常處理 上下文
# 即將發生異常
# 離開 異常處理 上下文
# 發生異常: 測試異常
# 繼續執行
```

## 描述符
```python
class Validator:
    def __init__(self, name, min_value=None, max_value=None):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
    
    def __get__(self, instance, owner):
        """獲取屬性值時調用"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        """設置屬性值時調用"""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} 必須是數字")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} 必須大於等於 {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} 必須小於等於 {self.max_value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        """刪除屬性時調用"""
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class Person:
    age = Validator("age", 0, 120)
    height = Validator("height", 0, 300)
    
    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.height = height

# 使用描述符
person = Person("Alice", 30, 165)
print(person.age)     # 30
print(person.height)  # 165

# person.age = -5     # 錯誤: age 必須大於等於 0
# person.height = 350  # 錯誤: height 必須小於等於 300
```

## 元類
```python
class Meta(type):
    def __new__(mcs, name, bases, attrs):
        """創建類時調用"""
        print(f"創建類 {name}")
        
        # 將所有方法名轉換為大寫
        uppercase_attrs = {}
        for key, value in attrs.items():
            if not key.startswith('__'):
                uppercase_attrs[key.upper()] = value
            else:
                uppercase_attrs[key] = value
        
        return super().__new__(mcs, name, bases, uppercase_attrs)
    
    def __init__(cls, name, bases, attrs):
        """初始化類時調用"""
        print(f"初始化類 {name}")
        super().__init__(name, bases, attrs)
    
    def __call__(cls, *args, **kwargs):
        """創建類的實例時調用"""
        print(f"創建 {cls.__name__} 的實例")
        instance = super().__call__(*args, **kwargs)
        return instance

# 使用元類
class MyClass(metaclass=Meta):
    def hello(self):
        return "Hello, World!"
    
    def goodbye(self):
        return "Goodbye!"

# 輸出:
# 創建類 MyClass
# 初始化類 MyClass

# 創建實例
obj = MyClass()  # 創建 MyClass 的實例

# 方法名已轉換為大寫
# print(obj.hello())  # 錯誤: 'MyClass' object has no attribute 'hello'
print(obj.HELLO())  # Hello, World!
print(obj.GOODBYE())  # Goodbye!
```

## 序列化與反序列化
```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __getstate__(self):
        """序列化時調用"""
        print("序列化 Point")
        # 返回要序列化的狀態
        return {'x': self.x, 'y': self.y}
    
    def __setstate__(self, state):
        """反序列化時調用"""
        print("反序列化 Point")
        # 從狀態恢復物件
        self.x = state['x']
        self.y = state['y']

# 使用序列化與反序列化
p = Point(3, 4)
serialized = pickle.dumps(p)  # 序列化 Point
deserialized = pickle.loads(serialized)  # 反序列化 Point
print(deserialized)  # (3, 4)
```

## 數字類型轉換
```python
class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    def __float__(self):
        """轉換為浮點數"""
        return self.numerator / self.denominator
    
    def __int__(self):
        """轉換為整數"""
        return int(float(self))
    
    def __round__(self, ndigits=0):
        """四捨五入"""
        value = float(self)
        return round(value, ndigits)
    
    def __complex__(self):
        """轉換為複數"""
        return complex(float(self))

# 使用數字類型轉換
f = Fraction(3, 4)
print(f)          # 3/4
print(float(f))   # 0.75
print(int(f))     # 0
print(round(f))   # 1
print(complex(f)) # (0.75+0j)
```
