# Python 語法速查表 - 第 15 章：類別與物件

## 定義類別
```python
# 基本類別定義
class Point:
    """表示二維空間中的點"""
    
    # 類別變數（所有實例共享）
    default_color = "black"
    
    # 初始化方法
    def __init__(self, x=0, y=0):
        # 實例變數（每個實例獨有）
        self.x = x
        self.y = y
    
    # 實例方法
    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
        
    # 字串表示方法
    def __str__(self):
        return f"Point({self.x}, {self.y})"
```

## 創建和使用物件
```python
# 創建物件實例
p1 = Point(3, 4)
p2 = Point()  # 使用默認參數值

# 訪問屬性
print(p1.x)  # 3
print(p1.y)  # 4

# 修改屬性
p1.x = 5
p1.color = "red"  # 動態添加新屬性

# 調用方法
distance = p1.distance_from_origin()  # 6.4031...

# 訪問類別變數
print(Point.default_color)  # black
print(p1.default_color)     # black

# 修改類別變數
Point.default_color = "blue"  # 影響所有實例
```

## 私有屬性和方法
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance      # 約定俗成的保護屬性（單下劃線）
        self.__account_number = "12345"  # 私有屬性（雙下劃線）
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def __generate_statement(self):  # 私有方法
        return f"Balance: {self._balance}"
    
    def get_statement(self):
        return self.__generate_statement()
```

## 屬性裝飾器
```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    # 使用 property 裝飾器定義 getter
    @property
    def celsius(self):
        return self._celsius
    
    # 定義 setter
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    # 定義另一個屬性
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# 使用屬性
temp = Temperature(25)
print(temp.celsius)      # 25
temp.celsius = 30        # 使用 setter
print(temp.fahrenheit)   # 86.0
temp.fahrenheit = 68     # 使用 fahrenheit 的 setter
print(temp.celsius)      # 20.0
```

## 靜態方法和類別方法
```python
class MathUtils:
    # 類別變數
    pi = 3.14159
    
    # 靜態方法（不訪問類別或實例）
    @staticmethod
    def add(a, b):
        return a + b
    
    # 類別方法（訪問類別，不訪問實例）
    @classmethod
    def circle_area(cls, radius):
        return cls.pi * radius ** 2
    
    # 實例方法（訪問實例）
    def multiply(self, a, b):
        return a * b

# 使用靜態方法和類別方法
print(MathUtils.add(5, 3))           # 8，不需要創建實例
print(MathUtils.circle_area(5))      # 78.53975，使用類別變數

# 實例方法需要創建實例
math = MathUtils()
print(math.multiply(5, 3))           # 15
```

## 特殊方法（魔術方法）
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 字串表示
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    # 運算符重載
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # 比較運算符
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # 長度
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    # 迭代器
    def __iter__(self):
        yield self.x
        yield self.y

# 使用特殊方法
v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)           # Vector(4, 6)
print(v1 * 2)            # Vector(6, 8)
print(v1 == v2)          # False
print(len(v1))           # 5
x, y = v1                # 解包迭代器
```

## 封裝、繼承和多型
```python
# 封裝：使用私有屬性和方法隱藏實現細節
class Car:
    def __init__(self, make, model):
        self.__make = make    # 私有屬性
        self.__model = model
        self.__speed = 0
    
    def accelerate(self, amount):
        self.__speed += amount
        self.__update_dashboard()
    
    def __update_dashboard(self):  # 私有方法
        pass  # 實際實現會更新儀表板

# 繼承：子類繼承父類的屬性和方法
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass  # 由子類實現

class Dog(Animal):  # Dog 繼承 Animal
    def speak(self):
        return "Woof!"

class Cat(Animal):  # Cat 繼承 Animal
    def speak(self):
        return "Meow!"

# 多型：不同類型的對象對同一操作有不同的響應
def animal_sound(animal):
    return animal.speak()

dog = Dog("Rex")
cat = Cat("Whiskers")
print(animal_sound(dog))  # Woof!
print(animal_sound(cat))  # Meow!
```

## 組合與聚合
```python
# 組合：強關聯，部分不能脫離整體而存在
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.engine = Engine()  # 組合關係
    
    def start(self):
        return self.engine.start()

# 聚合：弱關聯，部分可以脫離整體而存在
class Student:
    def __init__(self, name):
        self.name = name

class Course:
    def __init__(self, name):
        self.name = name
        self.students = []  # 聚合關係
    
    def add_student(self, student):
        self.students.append(student)
    
    def remove_student(self, student):
        self.students.remove(student)
```
