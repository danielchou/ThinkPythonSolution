# Python 語法速查表 - 第 12 章：案例研究：資料結構選擇

## 資料結構比較
```python
# 列表：有序、可變、可用索引存取
# 元組：有序、不可變、可用索引存取
# 字典：無序、可變、使用鍵存取
# 集合：無序、可變、無重複元素
```

## 集合基礎
```python
# 建立集合
s1 = set()  # 空集合
s2 = {1, 2, 3}  # 包含元素的集合

# 新增和移除元素
s2.add(4)  # {1, 2, 3, 4}
s2.remove(1)  # 移除元素，s2 變成 {2, 3, 4}
2 in s2  # True
5 in s2  # False
```

## 集合運算
```python
a = {1, 2, 3}
b = {3, 4, 5}

# 交集
a & b  # {3}
a.intersection(b)  # {3}

# 聯集
a | b  # {1, 2, 3, 4, 5}
a.union(b)  # {1, 2, 3, 4, 5}

# 差集
a - b  # {1, 2}
a.difference(b)  # {1, 2}

# 對稱差集
a ^ b  # {1, 2, 4, 5}
a.symmetric_difference(b)  # {1, 2, 4, 5}
```

## 資料結構選擇指南
```python
# 使用列表的情況：
# - 需要保持元素的插入順序
# - 需要頻繁地修改元素
# - 需要存儲重複元素

# 使用元組的情況：
# - 需要不可變的序列
# - 作為字典的鍵
# - 函式返回多個值

# 使用字典的情況：
# - 需要快速查找、插入和刪除
# - 需要鍵值對映射

# 使用集合的情況：
# - 需要快速成員檢查
# - 需要消除重複元素
# - 需要執行數學集合運算
```

## 實際應用範例
```python
# 計算單詞出現頻率
def count_words(text):
    words = text.lower().split()
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# 找出兩個列表的共同元素
def common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return list(set1 & set2)

# 移除列表中的重複元素但保持順序
def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```
