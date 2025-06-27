# Python 語法速查表（第 1-10 章）

## 目錄
- [第 1 章：程式設計作為一種思考方式](#第-1-章程式設計作為一種思考方式)
- [第 2 章：變數與陳述句](#第-2-章變數與陳述句)
- [第 3 章：函式](#第-3-章函式)
- [第 4 章：條件與遞迴](#第-4-章條件與遞迴)
- [第 5 章：分支與迴圈](#第-5-章分支與迴圈)
- [第 6 章：漸進式開發](#第-6-章漸進式開發)
- [第 7 章：字串](#第-7-章字串)
- [第 8 章：字串處理](#第-8-章字串處理)
- [第 9 章：列表](#第-9-章列表)
- [第 10 章：字典](#第-10-章字典)

[點此查看第 11-19 章](./Python_Cheatsheet_Part2.md)

---

## 第 1 章：程式設計作為一種思考方式

### 算術運算子
```python
# 基本運算
2 + 3    # 加法，結果為 5
43 - 1   # 減法，結果為 42
6 * 7    # 乘法，結果為 42
84 / 2   # 除法，結果為 42.0 (浮點數)
84 // 2  # 整數除法，結果為 42 (整數)
5 ** 2   # 次方，結果為 25
7 % 3    # 取餘數，結果為 1
```

### 運算子優先順序
```python
# 括號 > 次方 > 乘除 > 加減
2 + 3 * 4      # 結果為 14，因為乘法優先
(2 + 3) * 4    # 結果為 20，括號內先計算
```

### 內建函數
```python
round(42.7)    # 四捨五入，結果為 43
round(42.3)    # 四捨五入，結果為 42
abs(-42)       # 絕對值，結果為 42
```

### 值的類型
```python
type(42)       # <class 'int'> 整數
type(42.0)     # <class 'float'> 浮點數
type('42')     # <class 'str'> 字串
```

---

## 第 2 章：變數與陳述句

### 變數與賦值
```python
n = 17         # 將 17 賦值給變數 n
pi = 3.14159   # 將 3.14159 賦值給變數 pi
message = 'Hello'  # 將字串 'Hello' 賦值給變數 message
```

### 變數命名規則
- 可以包含字母、數字和底線
- 不能以數字開頭
- 不能使用保留關鍵字 (如 class, if, for 等)
- 習慣上使用小寫字母和底線

### 模組導入
```python
import math             # 導入整個 math 模組
math.pi                 # 使用 math 模組中的 pi 常數
math.sqrt(25)           # 使用 math 模組中的 sqrt 函數，結果為 5.0

from math import pi     # 只導入 pi 常數
pi                      # 直接使用 pi，不需要 math. 前綴
```

### 輸出
```python
print('Hello')          # 顯示 Hello
print('n =', n)         # 顯示 n = 17
print(f'pi = {pi:.2f}') # 格式化輸出：pi = 3.14
```

---

## 第 3 章：函式

### 定義函式
```python
def print_lyrics():
    print("我是一個伐木工，我過得很好。")
    print("我整夜睡覺，整天工作。")
```

### 帶參數的函式
```python
def print_twice(string):
    print(string)
    print(string)

print_twice('Hello')  # 顯示 Hello 兩次
```

### 函式呼叫
```python
def repeat_lyrics():
    print_lyrics()
    print_lyrics()

repeat_lyrics()  # 呼叫 repeat_lyrics 函式，會執行 print_lyrics 兩次
```

### 迴圈
```python
# 使用 for 迴圈
for i in range(5):  # i 會依序為 0, 1, 2, 3, 4
    print(i)

# 使用 range 的其他形式
for i in range(2, 5):  # i 會依序為 2, 3, 4
    print(i)

for i in range(0, 10, 2):  # i 會依序為 0, 2, 4, 6, 8
    print(i)

for i in range(5, 0, -1):  # i 會依序為 5, 4, 3, 2, 1
    print(i)
```

---

## 第 4 章：條件與遞迴

### 條件陳述句
```python
if x > 0:
    print('x 是正數')
elif x == 0:
    print('x 是零')
else:
    print('x 是負數')
```

### 比較運算子
```python
x == y  # x 等於 y
x != y  # x 不等於 y
x > y   # x 大於 y
x < y   # x 小於 y
x >= y  # x 大於等於 y
x <= y  # x 小於等於 y
```

### 邏輯運算子
```python
x > 0 and x < 10  # x 大於 0 且小於 10
x < 0 or x > 10   # x 小於 0 或大於 10
not (x > 0)       # x 不大於 0 (即 x <= 0)
```

### 遞迴函式
```python
def countdown(n):
    if n <= 0:
        print('發射！')
    else:
        print(n)
        countdown(n-1)

countdown(3)  # 顯示 3, 2, 1, 發射！
```

---

## 第 5 章：分支與迴圈

### while 迴圈
```python
n = 5
while n > 0:
    print(n)
    n = n - 1
print('發射！')
```

### break 與 continue
```python
# break 跳出迴圈
while True:
    line = input('> ')
    if line == 'done':
        break
    print(line)

# continue 跳過本次迴圈剩餘部分
for i in range(10):
    if i % 2 == 0:
        continue  # 跳過偶數
    print(i)  # 只印出奇數
```

---

## 第 6 章：漸進式開發

### 漸進式開發步驟
1. 從一個能工作的小程式開始
2. 一次增加一小部分功能並測試
3. 使用臨時變數和中間值來除錯
4. 尋找常見的程式碼模式並重構

### 函式設計原則
```python
def distance(x1, y1, x2, y2):
    """計算兩點之間的距離
    
    x1, y1: 第一個點的座標
    x2, y2: 第二個點的座標
    
    返回: 兩點之間的歐幾里得距離
    """
    dx = x2 - x1
    dy = y2 - y1
    return (dx**2 + dy**2)**0.5
```

---

## 第 7 章：字串

### 字串操作
```python
# 字串建立
s1 = 'Hello'
s2 = "World"
s3 = '''多行
字串'''

# 字串連接
s = s1 + ' ' + s2  # 'Hello World'

# 字串重複
s = 'Ha' * 3  # 'HaHaHa'

# 字串長度
len(s1)  # 5

# 字串索引 (從 0 開始)
s1[0]  # 'H'
s1[-1]  # 'o' (倒數第一個字元)

# 字串切片
s1[1:3]  # 'el' (從索引 1 到索引 2)
s1[:3]   # 'Hel' (從開頭到索引 2)
s1[2:]   # 'llo' (從索引 2 到結尾)
```

### 字串方法
```python
s = 'hello, world'
s.upper()       # 'HELLO, WORLD'
s.capitalize()  # 'Hello, world'
s.find('o')     # 4 (第一個 'o' 的索引)
s.find('o', 5)  # 8 (從索引 5 開始找 'o')
s.count('l')    # 3 (字母 'l' 出現的次數)
s.replace('o', 'x')  # 'hellx, wxrld'
```

### 字串判斷
```python
'a' in 'apple'  # True
'b' in 'apple'  # False

s.startswith('he')  # True
s.endswith('ld')    # True
s.isalpha()         # False (因為有逗號和空格)
s.isdigit()         # False
```

---

## 第 8 章：字串處理

### 字串格式化
```python
# 使用 format 方法
'{} {}'.format('Hello', 'World')  # 'Hello World'
'{1} {0}'.format('World', 'Hello')  # 'Hello World'
'{:.2f}'.format(3.14159)  # '3.14'

# 使用 f-string (Python 3.6+)
name = 'World'
f'Hello, {name}!'  # 'Hello, World!'
pi = 3.14159
f'π 約等於 {pi:.2f}'  # 'π 約等於 3.14'
```

### 正則表達式
```python
import re

# 搜尋模式
text = 'My phone number is 123-456-7890.'
pattern = r'\d{3}-\d{3}-\d{4}'
match = re.search(pattern, text)
if match:
    print(match.group())  # '123-456-7890'

# 替換
new_text = re.sub(r'\d{3}-\d{3}-\d{4}', 'XXX-XXX-XXXX', text)
# 'My phone number is XXX-XXX-XXXX.'

# 查找所有匹配
text = 'Phone: 123-456-7890, Office: 098-765-4321'
matches = re.findall(r'\d{3}-\d{3}-\d{4}', text)
# ['123-456-7890', '098-765-4321']
```

---

## 第 9 章：列表

### 列表基礎
```python
# 建立列表
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, 'two', 3.0, [4, 5]]

# 訪問元素
numbers[0]    # 1 (第一個元素)
numbers[-1]   # 5 (最後一個元素)
mixed[3][0]   # 4 (巢狀列表)

# 切片
numbers[1:3]  # [2, 3] (索引 1 到索引 2)
numbers[:3]   # [1, 2, 3] (開頭到索引 2)
numbers[2:]   # [3, 4, 5] (索引 2 到結尾)

# 列表長度
len(numbers)  # 5
```

### 列表操作
```python
# 修改元素
numbers[0] = 10  # numbers 變成 [10, 2, 3, 4, 5]

# 添加元素
numbers.append(6)  # numbers 變成 [10, 2, 3, 4, 5, 6]
numbers.insert(1, 15)  # numbers 變成 [10, 15, 2, 3, 4, 5, 6]
numbers.extend([7, 8])  # numbers 變成 [10, 15, 2, 3, 4, 5, 6, 7, 8]

# 刪除元素
numbers.remove(15)  # 刪除值為 15 的元素
popped = numbers.pop()  # 刪除並返回最後一個元素
del numbers[0]  # 刪除索引為 0 的元素
```

### 列表方法
```python
numbers = [3, 1, 4, 1, 5, 9, 2]
numbers.sort()  # 排序，numbers 變成 [1, 1, 2, 3, 4, 5, 9]
numbers.reverse()  # 反轉，numbers 變成 [9, 5, 4, 3, 2, 1, 1]
numbers.count(1)  # 2 (值為 1 的元素個數)
numbers.index(5)  # 1 (值為 5 的元素的索引)
```

### 列表推導式
```python
# 建立 1 到 10 的平方列表
squares = [x**2 for x in range(1, 11)]  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 帶條件的列表推導式
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]  # [4, 16, 36, 64, 100]
```

---

## 第 10 章：字典

### 字典基礎
```python
# 建立字典
empty_dict = {}
person = {'name': 'Alice', 'age': 25, 'city': 'Taipei'}

# 訪問值
person['name']  # 'Alice'

# 修改值
person['age'] = 26  # person 變成 {'name': 'Alice', 'age': 26, 'city': 'Taipei'}

# 添加新鍵值對
person['email'] = 'alice@example.com'

# 檢查鍵是否存在
'name' in person  # True
'phone' in person  # False

# 安全獲取值
person.get('phone')  # None
person.get('phone', 'Not found')  # 'Not found'
```

### 字典方法
```python
# 獲取所有鍵
person.keys()  # dict_keys(['name', 'age', 'city', 'email'])

# 獲取所有值
person.values()  # dict_values(['Alice', 26, 'Taipei', 'alice@example.com'])

# 獲取所有鍵值對
person.items()  # dict_items([('name', 'Alice'), ('age', 26), ('city', 'Taipei'), ('email', 'alice@example.com')])

# 刪除鍵值對
del person['email']
popped = person.pop('city')  # 刪除並返回 'city' 對應的值

# 合併字典
person.update({'phone': '123-456-7890', 'gender': 'female'})
```

### 字典推導式
```python
# 建立平方字典
squares = {x: x**2 for x in range(1, 6)}  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 反轉字典
inverted = {v: k for k, v in person.items()}
```




### 集合基礎
```python
# 建立集合
s1 = set()  # 空集合
s2 = {1, 2, 3}  # 包含元素的集合
s3 = set([1, 2, 2, 3, 3, 3])  # 從列表建立集合，會自動移除重複元素，結果為 {1, 2, 3}

# 集合操作
s2.add(4)  # 添加元素，s2 變成 {1, 2, 3, 4}
s2.remove(1)  # 移除元素，s2 變成 {2, 3, 4}
2 in s2  # True
5 in s2  # False
```

### 資料結構選擇指南
```python
# 使用列表的情況：
# - 需要保持元素的插入順序
# - 需要频繁地修改元素
# - 需要存儲重複元素

# 使用元組的情況：
# - 需要保持元素的插入順序
# - 不需要修改元素
# - 需要作為字典的鍵

# 使用字典的情況：
# - 需要快速查找元素
# - 需要將值關聯到鍵

# 使用集合的情況：
# - 需要檢查元素是否存在
# - 需要移除重複元素
# - 需要進行集合運算（交、聯、差）
```

---

## 第 13 章：案例研究：資料格式

### JSON 處理
```python
import json

# Python 物件轉換為 JSON 字串
python_dict = {'name': 'Alice', 'age': 25, 'scores': [95, 88, 92]}
json_str = json.dumps(python_dict)  # '{"name": "Alice", "age": 25, "scores": [95, 88, 92]}'

# 格式化輸出
json_formatted = json.dumps(python_dict, indent=2, sort_keys=True)

# JSON 字串轉換為 Python 物件
json_str = '{"name": "Bob", "age": 30, "scores": [85, 90, 88]}'
python_obj = json.loads(json_str)  # {'name': 'Bob', 'age': 30, 'scores': [85, 90, 88]}

# 讀取 JSON 檔案
with open('data.json', 'r') as f:
    data = json.load(f)

# 寫入 JSON 檔案
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### CSV 處理
```python
import csv

# 讀取 CSV 檔案
with open('data.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # row 是一個列表，包含每一行的各個欄位

# 使用 DictReader 讀取 CSV
with open('data.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)  # 假設第一行是標題
    for row in reader:
        print(row)  # row 是一個字典，鍵是標題，值是欄位值

# 寫入 CSV 檔案
data = [['Name', 'Age', 'Country'], ['Alice', '25', 'USA'], ['Bob', '30', 'Canada']]
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

# 使用 DictWriter 寫入 CSV
data = [
    {'Name': 'Alice', 'Age': '25', 'Country': 'USA'},
    {'Name': 'Bob', 'Age': '30', 'Country': 'Canada'}
]
with open('output.csv', 'w', newline='') as f:
    fieldnames = ['Name', 'Age', 'Country']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # 寫入標題行
    for row in data:
        writer.writerow(row)
```

### 網路 API 與 HTTP 請求
```python
import requests

# 發送 GET 請求
response = requests.get('https://api.example.com/data')
if response.status_code == 200:
    data = response.json()  # 假設回應是 JSON 格式
    print(data)
else:
    print(f'Error: {response.status_code}')

# 發送帶參數的 GET 請求
params = {'q': 'python', 'page': 1}
response = requests.get('https://api.example.com/search', params=params)

# 發送 POST 請求
data = {'username': 'user', 'password': 'pass'}
response = requests.post('https://api.example.com/login', json=data)

# 設置標頭
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/profile', headers=headers)
```

---

## 第 14 章：檔案

### 檔案讀寫基礎
```python
# 讀取檔案
with open('filename.txt', 'r') as f:
    content = f.read()  # 讀取整個檔案
    
with open('filename.txt', 'r') as f:
    lines = f.readlines()  # 讀取所有行為列表
    
with open('filename.txt', 'r') as f:
    for line in f:  # 逐行讀取
        print(line.strip())  # strip() 移除行尾的換行符

# 寫入檔案
with open('output.txt', 'w') as f:  # 'w' 模式會覆蓋現有檔案
    f.write('Hello, World!\n')
    f.write('Another line.\n')
    
with open('output.txt', 'a') as f:  # 'a' 模式會附加到檔案尾端
    f.write('Appended line.\n')
```

### 檔案路徑處理
```python
import os

# 獲取目前工作目錄
current_dir = os.getcwd()

# 創建目錄
os.mkdir('new_directory')  # 創建單一層目錄
os.makedirs('path/to/nested/directory', exist_ok=True)  # 創建嵌套目錄

# 列出目錄內容
files = os.listdir('directory_path')

# 檢查檔案或目錄是否存在
os.path.exists('path/to/file')  # 返回 True 或 False

# 判斷是檔案還是目錄
os.path.isfile('path/to/file')  # 如果是檔案則返回 True
os.path.isdir('path/to/directory')  # 如果是目錄則返回 True

# 路徑操作
file_name = os.path.basename('/path/to/file.txt')  # 返回 'file.txt'
directory = os.path.dirname('/path/to/file.txt')  # 返回 '/path/to'
full_path = os.path.join('directory', 'file.txt')  # 返回 'directory/file.txt'
```

### 使用 pathlib 模組
```python
from pathlib import Path

# 創建 Path 物件
p = Path('path/to/file.txt')

# 路徑屬性
p.name  # 'file.txt'
p.stem  # 'file'
p.suffix  # '.txt'
p.parent  # Path('path/to')

# 路徑操作
new_path = p.with_name('newfile.txt')  # 更改檔案名
new_path = p.with_suffix('.md')  # 更改副檔名

# 目錄操作
Path('new_directory').mkdir(exist_ok=True)  # 創建目錄

# 列出目錄內容
for file in Path('directory').iterdir():
    print(file)
    
# 搜尋檔案
for file in Path('directory').glob('*.txt'):  # 搜尋所有 .txt 檔案
    print(file)
    
for file in Path('directory').rglob('*.txt'):  # 遍歷子目錄並搜尋所有 .txt 檔案
    print(file)
```

### 二進位檔案讀寫
```python
# 讀取二進位檔案
with open('binary_file.bin', 'rb') as f:  # 'rb' 模式表示二進位讀取
    binary_data = f.read()
    
# 寫入二進位檔案
with open('output.bin', 'wb') as f:  # 'wb' 模式表示二進位寫入
    f.write(b'\x00\x01\x02\x03')
```

---

## 第 15 章：類別與物件

### 定義類別
```python
class Point:
    """2D 座標點的類別"""
    
    def __init__(self, x=0, y=0):
        """Point 類別的建構子"""
        self.x = x
        self.y = y
```

### 創建物件
```python
# 創建 Point 類別的物件
p1 = Point()  # 使用預設值 x=0, y=0
p2 = Point(3, 4)  # 指定 x=3, y=4

# 存取屬性
print(p2.x)  # 3
print(p2.y)  # 4

# 修改屬性
p2.x = 5
p2.y = 6
```

### 類別方法
```python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def distance_from_origin(self):
        """Calculate distance from the origin (0, 0)"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def distance_from_point(self, other_point):
        """Calculate distance from another point"""
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        return (dx ** 2 + dy ** 2) ** 0.5

p = Point(3, 4)
print(p.distance_from_origin())  # 5.0

p2 = Point(0, 0)
print(p.distance_from_point(p2))  # 5.0
```

### 類別變數與實例變數
```python
class Circle:
    pi = 3.14159  # 類別變數，所有實例共享
    
    def __init__(self, radius=1):
        self.radius = radius  # 實例變數，每個實例獨立
    
    def area(self):
        return Circle.pi * self.radius ** 2  # 使用類別變數
    
    def circumference(self):
        return 2 * Circle.pi * self.radius

c1 = Circle(5)
print(c1.area())  # 78.53975
print(c1.circumference())  # 31.4159

# 修改類別變數
Circle.pi = 3.14
print(c1.area())  # 78.5
```

### 物件屬性與方法
```python
# 加入新屬性
p = Point(1, 2)
p.color = 'red'  # 加入新屬性

# 檢查屬性
hasattr(p, 'x')  # True
hasattr(p, 'color')  # True
hasattr(p, 'z')  # False

# 取得屬性
getattr(p, 'x')  # 1
getattr(p, 'z', 0)  # 0 (預設值)

# 設定屬性
setattr(p, 'z', 3)
p.z  # 3

# 刪除屬性
delattr(p, 'color')
```
