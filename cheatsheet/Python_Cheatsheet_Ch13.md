# Python 語法速查表 - 第 13 章：案例研究：資料格式

## 字串處理與格式化
```python
# 字串格式化
name = "Alice"
age = 25
print(f"{name} 今年 {age} 歲")  # Alice 今年 25 歲

# 格式規範
pi = 3.14159
print(f"圓周率約為 {pi:.2f}")  # 圓周率約為 3.14

# 對齊
print(f"{name:>10}")  # 右對齊，寬度為 10
print(f"{name:<10}")  # 左對齊，寬度為 10
print(f"{name:^10}")  # 居中對齊，寬度為 10
```

## JSON 格式
```python
import json

# 將 Python 對象轉換為 JSON 字串
data = {
    "name": "Alice",
    "age": 25,
    "is_student": True,
    "courses": ["Python", "Data Science"]
}
json_str = json.dumps(data, indent=4)
print(json_str)

# 將 JSON 字串轉換為 Python 對象
parsed_data = json.loads(json_str)
print(parsed_data["name"])  # Alice

# 從檔案讀取 JSON
with open("data.json", "r") as file:
    data = json.load(file)

# 寫入 JSON 到檔案
with open("output.json", "w") as file:
    json.dump(data, file, indent=4)
```

## CSV 格式
```python
import csv

# 讀取 CSV 檔案
with open("data.csv", "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # 每行是一個列表

# 使用 DictReader 讀取 CSV
with open("data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)  # 每行是一個字典

# 寫入 CSV 檔案
data = [
    ["Name", "Age", "City"],
    ["Alice", "25", "Taipei"],
    ["Bob", "30", "Kaohsiung"]
]
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# 使用 DictWriter 寫入 CSV
data = [
    {"Name": "Alice", "Age": "25", "City": "Taipei"},
    {"Name": "Bob", "Age": "30", "City": "Kaohsiung"}
]
with open("output.csv", "w", newline="") as file:
    fieldnames = ["Name", "Age", "City"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## XML 處理
```python
import xml.etree.ElementTree as ET

# 解析 XML 字串
xml_str = """
<students>
    <student id="1">
        <name>Alice</name>
        <age>25</age>
    </student>
    <student id="2">
        <name>Bob</name>
        <age>30</age>
    </student>
</students>
"""
root = ET.fromstring(xml_str)

# 遍歷 XML 元素
for student in root.findall("student"):
    name = student.find("name").text
    age = student.find("age").text
    print(f"{name} 是 {age} 歲")

# 從檔案解析 XML
tree = ET.parse("data.xml")
root = tree.getroot()

# 創建 XML
root = ET.Element("students")
student1 = ET.SubElement(root, "student", attrib={"id": "1"})
ET.SubElement(student1, "name").text = "Alice"
ET.SubElement(student1, "age").text = "25"

# 寫入 XML 到檔案
tree = ET.ElementTree(root)
tree.write("output.xml", encoding="utf-8", xml_declaration=True)
```

## 資料序列化與反序列化
```python
import pickle

# 序列化 Python 對象
data = {"name": "Alice", "age": 25}
serialized = pickle.dumps(data)

# 反序列化
deserialized = pickle.loads(serialized)
print(deserialized)  # {'name': 'Alice', 'age': 25}

# 序列化到檔案
with open("data.pkl", "wb") as file:
    pickle.dump(data, file)

# 從檔案反序列化
with open("data.pkl", "rb") as file:
    loaded_data = pickle.load(file)
```

## 資料格式選擇指南
```python
# 使用 JSON 的情況：
# - 需要人類可讀的格式
# - 與 Web 應用程式交換資料
# - 需要跨平台相容性

# 使用 CSV 的情況：
# - 處理表格數據
# - 與試算表程式交換資料
# - 需要簡單的文字格式

# 使用 XML 的情況：
# - 需要複雜的層次結構
# - 需要支援命名空間和模式驗證
# - 與遺留系統交換資料

# 使用 Pickle 的情況：
# - 僅在 Python 程式中使用
# - 需要序列化複雜的 Python 對象
# - 不需要人類可讀性
```
