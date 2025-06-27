# Python 語法速查表 - 第 11 章：元組

## 元組基礎
```python
# 建立元組
t1 = ()　　　　　　　　# 空元組
t2 = (1,)　　　　　　　# 單元素元組，注意逗號是必要的
t3 = (1, 2, 3)　　　　　# 多元素元組
t4 = 1, 2, 3　　　　　　# 不使用括號也可以建立元組

# 訪問元素
t3[0]　　　　　　　　　# 1 (第一個元素)
t3[-1]　　　　　　　　# 3 (最後一個元素)

# 切片
t3[1:]　　　　　　　　# (2, 3) (從索引 1 到結尾)
```

## 元組的特性
```python
# 元組是不可變的
t = (1, 2, 3)
# t[0] = 4  # 錯誤！元組不支援項目賦值

# 元組可以包含不同類型的元素
mixed = (1, 'two', 3.0, [4, 5])

# 雙重指定運算子
(a, b) = (1, 2)  # a = 1, b = 2
```

## 元組與函式
```python
# 函式返回多個值
def min_max(t):
    return min(t), max(t)
    
smallest, largest = min_max([1, 3, 2, 5, 4])  # smallest = 1, largest = 5

# 使用 * 運算子收集剩餘的值
a, *rest = (1, 2, 3, 4)  # a = 1, rest = [2, 3, 4]
*beginning, end = (1, 2, 3, 4)  # beginning = [1, 2, 3], end = 4
```

## 元組與列表的轉換
```python
# 列表轉換為元組
list_to_tuple = tuple([1, 2, 3])  # (1, 2, 3)

# 元組轉換為列表
tuple_to_list = list((1, 2, 3))  # [1, 2, 3]
```

## 元組的應用
```python
# 作為字典的鍵
d = {}
d[(0, 0)] = 'origin'
d[(1, 0)] = 'right'
d[(0, 1)] = 'up'

# 使用 zip 函式
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f'{name} is {age} years old')
```
