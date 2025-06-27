# Python 語法速查表 - 第 18 章：繼承

## 基本繼承
```python
# 父類（基類）
class Parent:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"您好，我是 {self.name}"
    
    def work(self):
        return "我正在工作"

# 子類（派生類）
class Child(Parent):
    def __init__(self, name, school):
        # 調用父類的 __init__ 方法
        super().__init__(name)
        self.school = school
    
    # 覆寫父類方法
    def greet(self):
        return f"嗨！我是 {self.name}，我在 {self.school} 上學"
    
    # 新增子類特有方法
    def study(self):
        return "我正在學習"

# 使用繼承
parent = Parent("張爸爸")
child = Child("小明", "台北國小")

print(parent.greet())  # 您好，我是 張爸爸
print(parent.work())   # 我正在工作

print(child.greet())   # 嗨！我是 小明，我在 台北國小 上學
print(child.work())    # 我正在工作 (繼承自父類)
print(child.study())   # 我正在學習 (子類特有)
```

## 多重繼承
```python
class A:
    def method_a(self):
        return "這是 A 的方法"
    
    def common(self):
        return "這是 A 的共同方法"

class B:
    def method_b(self):
        return "這是 B 的方法"
    
    def common(self):
        return "這是 B 的共同方法"

# 多重繼承
class C(A, B):
    def method_c(self):
        return "這是 C 的方法"
    
    def common(self):
        # 調用父類的方法
        result = super().common()  # 根據 MRO 順序調用 A 的 common 方法
        return f"C 覆寫: {result}"

# 使用多重繼承
c = C()
print(c.method_a())  # 這是 A 的方法
print(c.method_b())  # 這是 B 的方法
print(c.method_c())  # 這是 C 的方法
print(c.common())    # C 覆寫: 這是 A 的共同方法

# 查看方法解析順序 (MRO)
print(C.__mro__)  # (<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
```

## 抽象基類
```python
from abc import ABC, abstractmethod

# 抽象基類
class Shape(ABC):
    @abstractmethod
    def area(self):
        """計算面積"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """計算周長"""
        pass
    
    def describe(self):
        """形狀描述（非抽象方法）"""
        return "這是一個形狀"

# 具體子類
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def describe(self):
        return f"這是一個 {self.width}x{self.height} 的矩形"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 使用抽象基類
# shape = Shape()  # 錯誤：無法實例化抽象類
rectangle = Rectangle(5, 10)
circle = Circle(7)

print(rectangle.area())       # 50
print(rectangle.perimeter())  # 30
print(rectangle.describe())   # 這是一個 5x10 的矩形

print(circle.area())          # 153.93791
print(circle.perimeter())     # 43.98226
print(circle.describe())      # 這是一個形狀 (繼承自抽象基類)
```

## 繼承與組合的選擇
```python
# 使用繼承（是一種關係）
class Vehicle:
    def __init__(self, speed):
        self.speed = speed
    
    def move(self):
        return f"以 {self.speed} km/h 的速度移動"

class Car(Vehicle):
    def __init__(self, speed, brand):
        super().__init__(speed)
        self.brand = brand
    
    def honk(self):
        return "嗶嗶！"

# 使用組合（有一個關係）
class Engine:
    def start(self):
        return "引擎啟動"
    
    def stop(self):
        return "引擎停止"

class Car:
    def __init__(self, speed, brand):
        self.speed = speed
        self.brand = brand
        self.engine = Engine()  # 組合
    
    def start(self):
        return f"{self.brand} 車輛啟動：{self.engine.start()}"
    
    def move(self):
        return f"以 {self.speed} km/h 的速度移動"
```

## 方法覆寫與擴展
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "某種聲音"
    
    def sleep(self):
        return f"{self.name} 正在睡覺"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    # 完全覆寫父類方法
    def make_sound(self):
        return "汪汪！"
    
    # 擴展父類方法
    def sleep(self):
        original = super().sleep()
        return f"{original}，並且在做夢"

# 使用覆寫與擴展
dog = Dog("小黑", "拉布拉多")
print(dog.make_sound())  # 汪汪！
print(dog.sleep())       # 小黑 正在睡覺，並且在做夢
```

## 繼承與特殊方法
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name}, {self.age}歲"
    
    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id
    
    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, 員工ID: {self.employee_id}"
    
    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return super().__eq__(other) and self.employee_id == other.employee_id

# 使用特殊方法
person = Person("張三", 30)
emp1 = Employee("李四", 25, "E001")
emp2 = Employee("李四", 25, "E001")
emp3 = Employee("李四", 25, "E002")

print(person)  # 張三, 30歲
print(emp1)    # 李四, 25歲, 員工ID: E001
print(emp1 == emp2)  # True
print(emp1 == emp3)  # False
```

## 混入類 (Mixins)
```python
# 混入類提供可重用的功能
class LoggerMixin:
    def log(self, message):
        print(f"[LOG] {message}")

class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

# 使用混入類
class User(LoggerMixin, JSONSerializableMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save(self):
        self.log(f"保存用戶 {self.name}")
        return f"用戶 {self.name} 已保存"

# 使用混入功能
user = User("小明", "ming@example.com")
user.log("創建了新用戶")  # [LOG] 創建了新用戶
print(user.to_json())    # {"name": "小明", "email": "ming@example.com"}
print(user.save())       # [LOG] 保存用戶 小明
                         # 用戶 小明 已保存
```

## 繼承與私有屬性
```python
class Base:
    def __init__(self):
        self.public = "公開屬性"
        self._protected = "受保護屬性"  # 約定俗成，單下劃線
        self.__private = "私有屬性"     # 名稱修飾，雙下劃線
    
    def get_private(self):
        return self.__private

class Derived(Base):
    def __init__(self):
        super().__init__()
        self.derived_public = "派生公開屬性"
        # 可以訪問父類的公開和受保護屬性
        print(f"公開: {self.public}")
        print(f"受保護: {self._protected}")
        # 無法直接訪問父類的私有屬性
        # print(self.__private)  # 錯誤
        
        # 但可以通過父類的方法訪問
        print(f"私有 (通過方法): {self.get_private()}")
        
        # 或者通過名稱修飾後的屬性名訪問
        print(f"私有 (通過修飾名): {self._Base__private}")

# 使用私有屬性
derived = Derived()
# 輸出:
# 公開: 公開屬性
# 受保護: 受保護屬性
# 私有 (通過方法): 私有屬性
# 私有 (通過修飾名): 私有屬性
```

## super() 函數的使用
```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()  # 調用父類的方法

class C(A):
    def method(self):
        print("C.method")
        super().method()  # 調用父類的方法

class D(B, C):
    def method(self):
        print("D.method")
        super().method()  # 根據 MRO 調用下一個類的方法

# 使用 super()
d = D()
d.method()
# 輸出:
# D.method
# B.method
# C.method
# A.method

# 在 __init__ 中使用 super()
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)  # 調用父類的 __init__
```
