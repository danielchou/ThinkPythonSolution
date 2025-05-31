# -*- coding: utf-8 -*-
# 從 chap16.ipynb 轉換而來
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
# jupyturtle 是在 Jupyter 環境中使用的海龜繪圖庫
download('https://github.com/ramalho/jupyturtle/releases/download/2024-03/jupyturtle.py');

import thinkpython

# # 類別與物件 (Classes and Objects)
#
# 到目前為止，我們已經定義了類別並建立了代表一天中時間和一年中日期的物件。
# 我們也定義了建立、修改這些物件以及用這些物件進行計算的方法。
#
# 在這一章，我們將繼續我們的物件導向程式設計 (OOP) 之旅，定義代表幾何物件的類別，
# 包括點、線、矩形和圓形。
# 我們會編寫建立和修改這些物件的方法，並且會使用 `jupyturtle` 模組來繪製它們。
#
# 我會用這些類別來示範 OOP 的主題，包括物件的同一性 (identity) 和等值性 (equivalence)、
# 淺複製 (shallow copy) 和深複製 (deep copy)，以及多型 (polymorphism)。

# ## 建立一個點 (Creating a Point)
#
# 在電腦圖學中，螢幕上的一個位置通常使用 `x`-`y` 平面中的一對座標來表示。
# 依照慣例，點 `(0, 0)` 通常代表螢幕的左上角，
# 而 `(x, y)` 代表從原點向右 `x` 單位、向下 `y` 單位的點。
# 與你在數學課上可能見過的笛卡兒座標系統相比，`y` 軸是上下顛倒的。
#
# 我們有好幾種方法可以在 Python 中表示一個點：
#
# -   我們可以把座標分別儲存在兩個變數 `x` 和 `y` 中。
#
# -   我們可以把座標當作元素儲存在列表或元組中。
#
# -   我們可以建立一個新的型別來把點表示為物件。
#
# 在物件導向程式設計中，最「道地」的做法是建立一個新的型別。
# 為此，我們從 `Point` 的類別定義開始。

class Point:
    """表示一個二維空間中的點。"""

    def __init__(self, x_coord, y_coord): # 參數改名以區分屬性
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        return f'Point({self.x}, {self.y})' # 使用 f-string 格式化輸出

# `__init__` 方法接收座標作為參數，並將它們指派給屬性 `x` 和 `y`。
# `__str__` 方法回傳 `Point` 的字串表示法。
#
# 現在我們可以像這樣實體化並顯示一個 `Point` 物件。

start_point = Point(0, 0) # 建立一個 Point 物件，座標 (0,0)
print(start_point)      # 會呼叫 Point 的 __str__ 方法

# 下面的圖表顯示了這個新物件的狀態。
# (圖表會顯示 start_point 指向一個 Point 物件，該物件有 x=0 和 y=0 兩個屬性)

from diagram import make_frame, make_binding # diagram 模組用於繪圖

d1_point_attrs = vars(start_point) # vars(obj) 回傳物件的 __dict__ 屬性 (一個包含其屬性的字典)
frame_point = make_frame(d1_point_attrs, name='Point', dy=-0.25, offsetx=0.18)
binding_point = make_binding('start_point', frame_point) # 書中用 'start'

from diagram import diagram, adjust # diagram 模組元件

width_point, height_point, x_diag_point, y_diag_point = [1.41, 0.89, 0.26, 0.5]
ax_point = diagram(width_point, height_point)
bbox_point = binding_point.draw(ax_point, x_diag_point, y_diag_point)
#adjust(x_diag_point, y_diag_point, bbox_point)

# 如同往常，程式設計師自訂的型別用一個方框表示，方框外面是型別的名稱，裡面是屬性。
#
# 一般來說，程式設計師自訂的型別是可變的 (mutable)，所以我們可以寫一個像 `translate` 這樣的方法，
# 它接收兩個數字 `dx` 和 `dy`，並把它們加到屬性 `x` 和 `y` 上。

# %%add_method_to Point
# 重新定義 Point 類別以加入 translate 方法
class Point:
    """表示一個二維空間中的點。"""

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def translate(self, dx, dy): # dx, dy 代表 x 和 y 方向的位移量
        self.x += dx # 直接修改物件的 x 屬性
        self.y += dy # 直接修改物件的 y 屬性

# 這個函數會把 `Point` 從平面上的一個位置平移到另一個位置。
# 如果我們不想修改現有的 `Point`，我們可以用 `copy` 來複製原始物件，然後修改副本。

from copy import copy # 匯入 copy 函數 (淺複製)

start_point_translate = Point(0, 0) # 使用更新後的 Point 類別
end1_point = copy(start_point_translate) # 複製 start_point_translate
end1_point.translate(300, 0) # 平移副本
print(f"原始點 (start_point_translate): {start_point_translate}") # 應為 Point(0, 0)
print(f"平移後的副本 (end1_point): {end1_point}") # 應為 Point(300, 0)

# 我們可以把這些步驟封裝到另一個叫做 `translated` 的方法中。
# (translated 通常表示回傳一個新的、已平移的物件，而不修改原始物件)

# %%add_method_to Point
# 再次重新定義 Point 類別以加入 translated 方法
class Point:
    """表示一個二維空間中的點。"""

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def translated(self, dx=0, dy=0): # dx, dy 設有預設值 0
        point_copy = copy(self) # 複製目前的點物件
        point_copy.translate(dx, dy) # 在副本上執行平移
        return point_copy # 回傳平移後的副本

# 就像內建函數 `sort` 會修改列表，而 `sorted` 函數會建立一個新的列表一樣，
# 現在我們有一個會修改 `Point` 的 `translate` 方法，
# 和一個會建立新 `Point` 的 `translated` 方法。
#
# 這裡有一個例子：

start_point_translated_test = Point(0, 0)
end2_point = start_point_translated_test.translated(0, 150) # 呼叫 translated
print(f"原始點 (start_point_translated_test): {start_point_translated_test}") # 應為 Point(0, 0)
print(f"translated 方法回傳的新點 (end2_point): {end2_point}") # 應為 Point(0, 150)

# 在下一節，我們會用這些點來定義和繪製一條線。

# ## 建立一條線 (Creating a Line)
#
# 現在讓我們定義一個類別來表示兩點之間的線段。
# 如同往常，我們先從 `__init__` 方法和 `__str__` 方法開始。

class Line:
    """表示一條由兩點定義的線段。"""
    def __init__(self, point1, point2): # 參數改名
        # 這裡應該儲存 Point 物件的副本，以避免外部修改影響 Line 的端點
        # 但書中目前還沒強調這一點，我們先照書中邏輯
        self.p1 = point1
        self.p2 = point2

    def __str__(self):
        # __str__ 會自動呼叫 self.p1 和 self.p2 的 __str__ 方法 (如果它們是 Point 物件)
        return f'Line({self.p1}, {self.p2})'

# 有了這兩個方法，我們可以實體化並顯示一個 `Line` 物件，
# 我們將用它來表示 `x` 軸 (的一部分)。
# (這裡 start_point_translate 和 end1_point 來自 In[13] 的 Point 物件)
# 為了讓 Line 使用最新定義的 Point，我們重新建立這些點

point_for_line_start = Point(0,0)
point_for_line_end_x = Point(300,0)
point_for_line_end_y = Point(0,150)


line1_xaxis = Line(point_for_line_start, point_for_line_end_x) # 線段從 (0,0) 到 (300,0)
print(line1_xaxis)

# 當我們呼叫 `print` 並傳遞 `line1_xaxis` 作為參數時，`print` 會調用 `line1_xaxis` 的 `__str__` 方法。
# `__str__` 方法使用 f-字串來建立 `line1_xaxis` 的字串表示法。
#
# f-字串包含兩個在大括號中的表達式：`self.p1` 和 `self.p2`。
# 當這些表達式被評估時，結果是 `Point` 物件。
# 然後，當它們被轉換成字串時，會調用 `Point` 類別中的 `__str__` 方法。
#
# 這就是為什麼當我們顯示一個 `Line` 時，結果會包含 `Point` 物件的字串表示法。
#
# 下面的物件圖顯示了這個 `Line` 物件的狀態。
# (圖表會顯示 line1_xaxis 指向一個 Line 物件，該物件有 p1 和 p2 兩個屬性，
#  p1 和 p2 分別指向不同的 Point 物件)

from diagram import Binding, Value, Frame # diagram 模組元件

# 假設 line1_xaxis 和其端點已定義
d1_line_p1_attrs = vars(line1_xaxis.p1)
frame1_line_p1 = make_frame(d1_line_p1_attrs, name='Point', dy=-0.25, offsetx=0.17)

d2_line_p2_attrs = vars(line1_xaxis.p2)
frame2_line_p2 = make_frame(d2_line_p2_attrs, name='Point', dy=-0.25, offsetx=0.17)

# Line 物件的屬性是指向 Point 物件的參照
binding1_line_attr = Binding(Value('p1'), frame1_line_p1, dx=0.4, draw_value=False) # draw_value=False 表示畫箭頭指向物件
binding2_line_attr = Binding(Value('p2'), frame2_line_p2, dx=0.4, draw_value=False)
frame3_line_obj = Frame([binding1_line_attr, binding2_line_attr], name='Line', dy=-0.9, offsetx=0.4, offsety=-0.25)

binding_line_diag = make_binding('line1_xaxis', frame3_line_obj)


width_line, height_line, x_diag_line, y_diag_line = [2.45, 2.12, 0.27, 1.76]
ax_line = diagram(width_line, height_line)
# 需要分別繪製 Line 物件和它參照的 Point 物件
bbox_binding_line = binding_line_diag.draw(ax_line, x_diag_line, y_diag_line)
# Point 物件的 frame 需要獨立繪製，因為它們是獨立的物件
# 這裡的 diagram 繪製方式可能需要調整才能正確顯示共享或獨立的 Point 物件
# adjust(x_diag_line, y_diag_line, bbox_binding_line)


# 字串表示法和物件圖對於除錯很有用，
# 但這個例子的重點是產生圖形，而不是文字！
# 所以我們會使用 `jupyturtle` 模組在螢幕上繪製線條。
#
# 如同我們在[第四章](section_turtle_module)做的那樣，我們會用 `make_turtle` 來建立一個 `Turtle` 物件
# 和一個它可以在上面繪圖的小畫布。
# (譯註：section_turtle_module 指的是書中對應章節的連結)
# 要繪製線條，我們會使用 `jupyturtle` 模組中的兩個新函數：
#
# * `jumpto`：接收兩個座標，並將 `Turtle` 移動到給定位置而不繪製線條，以及
#
# * `moveto`：將 `Turtle` 從目前位置移動到給定位置，並在它們之間繪製一條線段。
#
# 我們這樣匯入它們。

try:
    from jupyturtle import make_turtle, jumpto, moveto # 從 jupyturtle 匯入繪圖函數
except ImportError:
    print("警告: jupyturtle 模組未找到。繪圖功能將無法使用。")
    print("你可以嘗試執行: pip install jupyturtle")
    # 定義假的繪圖函數以避免後續錯誤
    def make_turtle(width=200, height=200, delay=0.1): print("make_turtle (模擬): 建立畫布")
    def jumpto(x, y): print(f"jumpto (模擬): 跳到 ({x}, {y})")
    def moveto(x, y): print(f"moveto (模擬): 移動到 ({x}, {y}) 並畫線")


# 這是繪製 `Line` 的方法。

# %%add_method_to Line
# 重新定義 Line 類別以加入 draw 方法
class Line:
    """表示一條由兩點定義的線段。"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def __str__(self):
        return f'Line({self.p1}, {self.p2})'

    def draw(self): # 新增的 draw 方法
        # Turtle 會從 p1 跳到 p2，並畫線
        print(f"準備繪製 Line: 從 {self.p1} 到 {self.p2}")
        jumpto(self.p1.x, self.p1.y) # 海龜跳到線的起點
        moveto(self.p2.x, self.p2.y) # 海龜移動到線的終點，並畫線


# 為了展示如何使用它，我會建立第二條線來表示 `y` 軸。

line2_yaxis = Line(point_for_line_start, point_for_line_end_y) # 線段從 (0,0) 到 (0,150)
print(line2_yaxis)

# 然後繪製座標軸。

print("\n--- 繪製線條 (座標軸) ---")
make_turtle(width=400, height=200) # 建立一個海龜畫布
if hasattr(line1_xaxis, 'draw'): # 確保方法存在
    line1_xaxis.draw() # 繪製 x 軸
    line2_yaxis.draw() # 繪製 y 軸
else:
    print("Line 類別沒有 draw 方法。")


# 當我們定義和繪製更多物件時，我們會再次使用這些線條。
# 但首先讓我們談談物件的等值性和同一性。

# ## 等值性與同一性 (Equivalence and identity)
#
# 假設我們建立兩個具有相同座標的點。

p1_eq_test = Point(200, 100)
p2_eq_test = Point(200, 100)
print(f"\n--- 等值性與同一性測試 ---")
print(f"p1_eq_test: {p1_eq_test}")
print(f"p2_eq_test: {p2_eq_test}")


# 如果我們用 `==` 運算子比較它們，我們會得到程式設計師自訂型別的預設行為
# —— 結果只有在它們是同一個物件時才會是 `True`，但它們不是。

print(f"p1_eq_test == p2_eq_test (預設行為): {p1_eq_test == p2_eq_test}") # False

# 如果我們想改變這種行為，我們可以提供一個叫做 `__eq__` 的特殊方法，
# 它定義了兩個 `Point` 物件相等的意義。

# %%add_method_to Point
# 再次重新定義 Point 類別以加入 __eq__ 方法
class Point:
    """表示一個二維空間中的點。"""
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def translated(self, dx=0, dy=0):
        point_copy = copy(self)
        point_copy.translate(dx, dy)
        return point_copy

    def __eq__(self, other_point_eq): # 參數改名
        # 檢查 other_point_eq 是否也是 Point 物件
        if not isinstance(other_point_eq, Point):
            return NotImplemented # 表示無法比較此類型
        # 如果 x 和 y 座標都相等，則兩點等值
        return (self.x == other_point_eq.x) and (self.y == other_point_eq.y)

# 這個定義認為如果兩個 `Point` 的屬性相等，則它們相等。
# 現在當我們使用 `==` 運算子時，它會調用 `__eq__` 方法，
# 這表示 `p1_eq_test` 和 `p2_eq_test` 被認為是相等的。

# 重新建立 p1_eq_test 和 p2_eq_test，使用包含 __eq__ 的 Point 類別
p1_eq_test_redef = Point(200, 100)
p2_eq_test_redef = Point(200, 100)
print(f"p1_eq_test_redef == p2_eq_test_redef (使用 __eq__): {p1_eq_test_redef == p2_eq_test_redef}") # True

# 但是 `is` 運算子仍然表示它們是不同的物件。

print(f"p1_eq_test_redef is p2_eq_test_redef: {p1_eq_test_redef is p2_eq_test_redef}") # False

# 無法覆寫 `is` 運算子 —— 它總是檢查物件是否相同 (同一性)。
# 但是對於程式設計師自訂的型別，你可以覆寫 `==` 運算子，使其檢查物件是否等值。
# 你可以自己定義什麼是等值。

# ## 建立一個矩形 (Creating a Rectangle)
#
# 現在讓我們定義一個類別來表示和繪製矩形。
# 為了簡單起見，我們假設矩形是垂直或水平的，而不是傾斜的。
# 你認為我們應該用哪些屬性來指定矩形的位置和大小？
#
# 至少有兩種可能性：
#
# -   你可以指定矩形的寬度和高度，以及一個角的位置。
#
# -   你可以指定兩個相對的角。
#
# 此時很難說哪一個比另一個好，所以我們先實作第一種。
# 這是類別定義。

class Rectangle:
    """表示一個矩形。

    屬性: width (寬), height (高), corner (左上角 Point 物件)。
    """
    def __init__(self, width_rect, height_rect, corner_point_rect): # 參數改名
        self.width = width_rect
        self.height = height_rect
        # 這裡也應該考慮儲存 corner_point_rect 的副本，以避免外部修改
        self.corner = corner_point_rect # corner 是一個 Point 物件

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

# 如同往常，`__init__` 方法將參數指派給屬性，`__str__` 回傳物件的字串表示法。
# 現在我們可以實體化一個 `Rectangle` 物件，使用一個 `Point` 作為左上角的位置。

corner_rect_example = Point(30, 20) # 使用最新定義的 Point 類別
box1_rect = Rectangle(100, 50, corner_rect_example) # 寬100, 高50, 左上角 (30,20)
print(f"\n--- 建立矩形 ---")
print(box1_rect)

# 下面的圖表顯示了這個物件的狀態。
# (圖表會顯示 box1_rect 指向 Rectangle 物件，它有 width, height 和 corner 屬性，
#  corner 屬性指向一個 Point 物件)

from diagram import Binding, Value # diagram 模組元件

def make_rectangle_binding_custom(name, box_obj, **options): # 參數改名
    # 取得 corner Point 物件的屬性字典
    d1_rect_corner_attrs = vars(box_obj.corner)
    frame_rect_corner = make_frame(d1_rect_corner_attrs, name='Point', dy=-0.25, offsetx=0.07)

    # Rectangle 物件本身的屬性 (width, height)
    d2_rect_attrs = dict(width=box_obj.width, height=box_obj.height)
    frame_rect_obj = make_frame(d2_rect_attrs, name='Rectangle', dy=-0.25, offsetx=0.45)

    # Rectangle 的 corner 屬性指向 Point 物件
    binding_rect_corner_attr = Binding(Value('corner'), frame_rect_corner, dx=0.92, draw_value=False, **options)
    frame_rect_obj.bindings.append(binding_rect_corner_attr) # 把 corner 的 binding 加到 Rectangle 的 frame

    # 最外層的 binding，變數名指向 Rectangle 物件
    binding_outer_rect = Binding(Value(name), frame_rect_obj)
    return binding_outer_rect, frame_rect_corner # 回傳外層 binding 和 corner 的 frame (用於繪製)

binding_box1_diag, frame_corner1_diag = make_rectangle_binding_custom('box1_rect', box1_rect)


from diagram import Bbox # diagram 模組元件

width_rect_diag, height_rect_diag, x_rect_diag, y_rect_diag = [2.83, 1.49, 0.27, 1.1]
ax_rect_diag = diagram(width_rect_diag, height_rect_diag)
bbox_binding_rect = binding_box1_diag.draw(ax_rect_diag, x_rect_diag, y_rect_diag)
# frame_corner1_diag 需要被繪製，它代表 Rectangle 參照的 Point 物件
bbox_frame_corner = frame_corner1_diag.draw(ax_rect_diag, x_rect_diag + 1.85, y_rect_diag - 0.6) # 調整位置
# bbox_rect_union = Bbox.union([bbox_binding_rect, bbox_frame_corner])
# adjust(x_rect_diag, y_rect_diag, bbox_rect_union)


# 要繪製一個矩形，我們會用下面的方法來建立代表四個角的 `Point` 物件。

# %%add_method_to Rectangle
# 再次重新定義 Rectangle 類別以加入方法
class Rectangle:
    """表示一個矩形。"""
    def __init__(self, width_rect, height_rect, corner_point_rect):
        self.width = width_rect
        self.height = height_rect
        self.corner = corner_point_rect # 左上角

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

    def make_points(self):
        """計算並回傳矩形的四個角點 (Point 物件)。"""
        # 假設 self.corner 是左上角 (x_min, y_min)
        # 由於螢幕座標 y 向下增加，所以 height 應該是向下加
        p1_top_left = self.corner
        # p2 右上角: x 增加 width, y 不變
        p2_top_right = p1_top_left.translated(self.width, 0)
        # p3 右下角: 從 p2 開始，x 不變, y 增加 height
        p3_bottom_right = p2_top_right.translated(0, self.height)
        # p4 左下角: 從 p3 開始，x 減少 width, y 不變 (或者從 p1 開始 y 增加 height)
        p4_bottom_left = p3_bottom_right.translated(-self.width, 0)
        # 或者 p4_bottom_left = p1_top_left.translated(0, self.height)
        return p1_top_left, p2_top_right, p3_bottom_right, p4_bottom_left

# 然後我們會建立四個 `Line` 物件來表示矩形的四條邊。

# %%add_method_to Rectangle
# 繼續加入方法到 Rectangle
class Rectangle:
    """表示一個矩形。"""
    def __init__(self, width_rect, height_rect, corner_point_rect):
        self.width = width_rect
        self.height = height_rect
        self.corner = corner_point_rect

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

    def make_points(self):
        p1 = self.corner
        p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height)
        p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4

    def make_lines(self):
        """使用 make_points 的結果建立並回傳代表四條邊的 Line 物件元組。"""
        p1, p2, p3, p4 = self.make_points()
        # 建立四條線：上、右、下、左
        line_top = Line(p1, p2)
        line_right = Line(p2, p3)
        line_bottom = Line(p3, p4)
        line_left = Line(p4, p1)
        return line_top, line_right, line_bottom, line_left

# 然後我們會繪製這些邊。

# %%add_method_to Rectangle
# 最終的 Rectangle 類別定義 (包含 draw)
class Rectangle:
    """表示一個矩形。"""
    def __init__(self, width_rect, height_rect, corner_point_rect):
        self.width = width_rect
        self.height = height_rect
        self.corner = corner_point_rect

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

    def make_points(self):
        p1 = self.corner
        p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height)
        p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4

    def make_lines(self):
        p1, p2, p3, p4 = self.make_points()
        return Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)

    def draw(self): # 新增的 draw 方法
        """繪製矩形的四條邊。"""
        lines_of_rect = self.make_lines()
        print(f"準備繪製 Rectangle: {self}")
        for line_side in lines_of_rect:
            if hasattr(line_side, 'draw'): # 確保 Line 物件有 draw 方法
                line_side.draw() # 呼叫 Line 物件的 draw 方法
            else:
                print(f"警告: Line 物件 {line_side} 沒有 draw 方法。")


# 這裡有一個例子。
# 重新建立 box1_rect，使用包含所有方法的 Rectangle 類別
corner_rect_draw_test = Point(30, 20)
box1_rect_draw_test = Rectangle(100, 50, corner_rect_draw_test)

print("\n--- 繪製矩形和座標軸 ---")
make_turtle(width=400, height=200) # 建立畫布
# 假設 line1_xaxis 和 line2_yaxis (座標軸線) 已定義並有 draw 方法
if hasattr(line1_xaxis, 'draw'): line1_xaxis.draw()
if hasattr(line2_yaxis, 'draw'): line2_yaxis.draw()
# 繪製矩形
if hasattr(box1_rect_draw_test, 'draw'):
    box1_rect_draw_test.draw()
else:
    print("Rectangle 物件沒有 draw 方法。")

# 圖中包含了兩條線來表示座標軸。

# ## 修改矩形 (Changing rectangles)
#
# 現在讓我們考慮兩個修改矩形的方法：`grow` (放大/縮小) 和 `translate` (平移)。
# 我們會看到 `grow` 如預期般運作，但 `translate` 有一個隱微的 bug。
# 在我解釋之前，看看你是否能找出問題所在。
#
# `grow` 接收兩個數字 `dwidth` (寬度變化量) 和 `dheight` (高度變化量)，
# 並把它們加到矩形的 `width` 和 `height` 屬性上。

# %%add_method_to Rectangle
# 重新定義 Rectangle 以加入 grow
class Rectangle:
    """表示一個矩形。"""
    def __init__(self, width_rect, height_rect, corner_point_rect):
        self.width = width_rect
        self.height = height_rect
        self.corner = corner_point_rect

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

    def make_points(self):
        p1 = self.corner
        p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height)
        p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4

    def make_lines(self):
        p1, p2, p3, p4 = self.make_points()
        return Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)

    def draw(self):
        lines_of_rect = self.make_lines()
        for line_side in lines_of_rect:
            if hasattr(line_side, 'draw'): line_side.draw()

    def grow(self, dwidth, dheight): # 新增的 grow 方法
        self.width += dwidth
        self.height += dheight
        # 注意：grow 只改變大小，不改變左上角 corner 的位置

# 這裡有一個例子，透過建立 `box1_rect_draw_test` 的副本並在副本上調用 `grow` 來展示效果。
# 重新建立 box1_rect_grow_test
corner_rect_grow_test = Point(30, 20)
box1_rect_grow_test = Rectangle(100, 50, corner_rect_grow_test) # 使用包含 grow 的 Rectangle


box2_grown_rect = copy(box1_rect_grow_test) # 淺複製
box2_grown_rect.grow(60, 40) # 寬度變 100+60=160, 高度變 50+40=90
print(f"\n--- 測試 Rectangle 的 grow 方法 ---")
print(f"原始 box1_rect_grow_test: {box1_rect_grow_test}")
print(f"放大後的 box2_grown_rect: {box2_grown_rect}")


# 如果我們繪製 `box1_rect_grow_test` 和 `box2_grown_rect`，可以確認 `grow` 如預期般運作。

print("\n--- 繪製原始矩形和放大後的矩形 ---")
make_turtle(width=400, height=250)
if hasattr(line1_xaxis, 'draw'): line1_xaxis.draw() # 座標軸
if hasattr(line2_yaxis, 'draw'): line2_yaxis.draw()

if hasattr(box1_rect_grow_test, 'draw'): box1_rect_grow_test.draw() # 原始
if hasattr(box2_grown_rect, 'draw'): box2_grown_rect.draw()       # 放大後


# 現在我們來看看 `translate`。
# 它接收兩個數字 `dx` 和 `dy`，並將矩形在 `x` 和 `y` 方向上移動給定的距離。

# %%add_method_to Rectangle
# 再次重新定義 Rectangle 以加入 translate
class Rectangle:
    """表示一個矩形。"""
    def __init__(self, width_rect, height_rect, corner_point_rect):
        self.width = width_rect
        self.height = height_rect
        self.corner = corner_point_rect # corner 是一個 Point 物件

    def __str__(self):
        return f'Rectangle({self.width}, {self.height}, {self.corner})'

    def make_points(self):
        p1 = self.corner; p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height); p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4

    def make_lines(self):
        p1, p2, p3, p4 = self.make_points()
        return Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)

    def draw(self):
        for line_side in self.make_lines():
            if hasattr(line_side, 'draw'): line_side.draw()

    def grow(self, dwidth, dheight):
        self.width += dwidth; self.height += dheight

    def translate(self, dx, dy): # 新增的 translate 方法
        # 問題點：這裡直接修改了 self.corner Point 物件
        # 如果有多個 Rectangle 共享同一個 corner Point 物件 (例如透過淺複製)
        # 那麼平移一個 Rectangle 會導致所有共享該 corner 的 Rectangle 都被平移
        if hasattr(self.corner, 'translate'): # 確保 corner 有 translate 方法
            self.corner.translate(dx, dy)
        else:
            print("警告: self.corner 沒有 translate 方法。")


# 為了展示效果，我們把 `box2_grown_rect` (之前 grow 過的) 向右和向下平移。
# 重新建立 box2_grown_rect 以確保使用的是最新的 Rectangle 定義
# 並且與 box1_rect_translate_test 共享 corner (模擬淺複製後的狀況)
corner_shared = Point(30, 20)
box1_rect_translate_test = Rectangle(100, 50, corner_shared)
box2_rect_translate_target = copy(box1_rect_translate_test) # box2 和 box1 共享 corner_shared
box2_rect_translate_target.grow(60, 40) # 先 grow box2

print(f"\n--- 測試 Rectangle 的 translate 方法 (有 bug 的情況) ---")
print(f"平移前 box1_rect_translate_test: {box1_rect_translate_test}")
print(f"平移前 box2_rect_translate_target (已 grow): {box2_rect_translate_target}")


box2_rect_translate_target.translate(30, 20) # 平移 box2
print(f"平移後 box2_rect_translate_target: {box2_rect_translate_target}")
# 因為 box1 和 box2 共享 corner，所以 box1 的 corner 也會被修改！
print(f"平移 box2 後，box1_rect_translate_test 的狀態 (corner 應已改變): {box1_rect_translate_test}")


# 現在讓我們看看如果再次繪製 `box1_rect_translate_test` 和 `box2_rect_translate_target` 會發生什麼。

print("\n--- 繪製因共享 corner 而一起移動的矩形 ---")
make_turtle(width=500, height=300)
if hasattr(line1_xaxis, 'draw'): line1_xaxis.draw()
if hasattr(line2_yaxis, 'draw'): line2_yaxis.draw()

if hasattr(box1_rect_translate_test, 'draw'): box1_rect_translate_test.draw() # box1 也移動了！
if hasattr(box2_rect_translate_target, 'draw'): box2_rect_translate_target.draw()


# 看起來兩個矩形都移動了，這不是我們想要的！
# 下一節解釋了哪裡出了問題。

# ## 深複製 (Deep copy)
#
# 當我們使用 `copy` (淺複製) 來複製 `box1_rect_translate_test` 時，它複製了 `Rectangle` 物件，
# 但沒有複製它所包含的 `Point` 物件 (即 `corner` 屬性)。
# 所以 `box1_rect_translate_test` 和 `box2_rect_translate_target` 是不同的 `Rectangle` 物件，正如預期的那樣。

print(f"box1_rect_translate_test is box2_rect_translate_target: {box1_rect_translate_test is box2_rect_translate_target}") # False

# 但是它們的 `corner` 屬性指向同一個 `Point` 物件。

print(f"box1_rect_translate_test.corner is box2_rect_translate_target.corner: {box1_rect_translate_test.corner is box2_rect_translate_target.corner}") # True

# 下面的圖表顯示了這些物件的狀態。
# (圖表會顯示兩個 Rectangle 物件，但它們的 corner 屬性都指向記憶體中同一個 Point 物件)

from diagram import Stack # diagram 模組元件
# from copy import deepcopy # deepcopy 稍後會用到

# 使用之前定義的 make_rectangle_binding_custom
# binding_box1_shared_diag, frame_corner_shared1_diag = make_rectangle_binding_custom('box1_shared', box1_rect_translate_test)
# binding_box2_shared_diag, _ = make_rectangle_binding_custom('box2_shared', box2_rect_translate_target, dy=0.4)
# binding_box2_shared_diag.value.bindings.reverse() # 調整繪圖順序

# stack_shared_corner = Stack([binding_box1_shared_diag, binding_box2_shared_diag], dy=-1.3)

# from diagram import Bbox # diagram 模組元件

# width_shared_diag, height_shared_diag, x_shared_diag, y_shared_diag = [2.76, 2.54, 0.27, 2.16]
# ax_shared_diag = diagram(width_shared_diag, height_shared_diag)
# bbox_stack_shared = stack_shared_corner.draw(ax_shared_diag, x_shared_diag, y_shared_diag)
# # 由於 corner 是共享的，只需要畫一次 Point 物件的 frame
# bbox_frame_shared_corner = frame_corner_shared1_diag.draw(ax_shared_diag, x_shared_diag + 1.85, y_shared_diag - 0.6)
# bbox_shared_union = Bbox.union([bbox_stack_shared, bbox_frame_shared_corner])
# adjust(x_shared_diag, y_shared_diag, bbox_shared_union)


# `copy` 所做的是所謂的 **淺複製 (shallow copy)**，因為它複製了物件本身，但沒有複製它所包含的物件。
# 結果是，改變一個 `Rectangle` 的 `width` 或 `height` 不會影響另一個，
# 但改變共享的 `Point` 的屬性會同時影響兩個 `Rectangle`！
# 這種行為令人困惑且容易出錯。
#
# 幸運的是，`copy` 模組提供了另一個函數，叫做 `deepcopy`，
# 它不僅複製物件本身，還複製它所參照的物件，以及 *那些* 物件所參照的物件，依此類推。
# 這個操作稱為 **深複製 (deep copy)**。
#
# 為了示範，我們先建立一個包含新 `Point` 的新 `Rectangle`。

corner_for_deepcopy = Point(20, 20)
box3_orig_deep = Rectangle(100, 50, corner_for_deepcopy) # 使用最新的 Rectangle 定義
print(f"\n--- 深複製測試 ---")
print(f"box3_orig_deep: {box3_orig_deep}")

# 我們來做一個深複製。

from copy import deepcopy # 匯入 deepcopy

box4_deepcopied = deepcopy(box3_orig_deep) # box4 是 box3 的一個深複製

# 我們可以確認這兩個 `Rectangle` 物件參照的是不同的 `Point` 物件。

print(f"box3_orig_deep.corner is box4_deepcopied.corner: {box3_orig_deep.corner is box4_deepcopied.corner}") # False

# 因為 `box3_orig_deep` 和 `box4_deepcopied` 是完全獨立的物件，所以我們可以修改一個而不影響另一個。
# 為了示範，我們移動 `box3_orig_deep` 並放大 `box4_deepcopied`。

box3_orig_deep.translate(50, 30) # 移動 box3
box4_deepcopied.grow(100, 60)     # 放大 box4
print(f"移動後的 box3_orig_deep: {box3_orig_deep}")
print(f"放大後的 box4_deepcopied: {box4_deepcopied}")


# 我們可以確認效果如預期。

print("\n--- 繪製經過深複製後獨立修改的矩形 ---")
make_turtle(width=500, height=300)
if hasattr(line1_xaxis, 'draw'): line1_xaxis.draw()
if hasattr(line2_yaxis, 'draw'): line2_yaxis.draw()

if hasattr(box3_orig_deep, 'draw'): box3_orig_deep.draw()
if hasattr(box4_deepcopied, 'draw'): box4_deepcopied.draw()


# ## 多型 (Polymorphism)
#
# 在上一個例子中，我們在兩個 `Line` 物件和兩個 `Rectangle` 物件上調用了 `draw` 方法。
# 我們可以透過建立一個物件列表來更簡潔地做同樣的事情。

# 為了有多個形狀，我們重新建立一些物件
# 確保使用最新定義的類別
shape_start_point = Point(0,0)
shape_end_x_axis = Point(300,0)
shape_end_y_axis = Point(0,150)
shape_line1 = Line(shape_start_point, shape_end_x_axis)
shape_line2 = Line(shape_start_point, shape_end_y_axis)

shape_corner_rect3 = Point(20, 20) # box3_orig_deep 的原始 corner
shape_rect3 = Rectangle(100, 50, shape_corner_rect3) # 這是未移動的 box3
shape_rect3.translate(50,30) # 手動應用之前的移動

shape_corner_rect4 = Point(20, 20) # box4_deepcopied 的原始 corner
shape_rect4 = Rectangle(100, 50, shape_corner_rect4) # 這是未放大的 box4
shape_rect4.grow(100,60) # 手動應用之前的放大

shapes_list_poly = [shape_line1, shape_line2, shape_rect3, shape_rect4]
print(f"\n--- 多型範例：shapes_list_poly ---")
for sh in shapes_list_poly: print(sh)


# 這個列表的元素型別不同，但它們都提供了 `draw` 方法，
# 所以我們可以遍歷這個列表並在每個元素上調用 `draw`。

print("\n--- 使用多型繪製不同形狀 ---")
make_turtle(width=500, height=300)

for shape_item in shapes_list_poly:
    if hasattr(shape_item, 'draw'):
        shape_item.draw()
    else:
        print(f"警告: 物件 {shape_item} 沒有 draw 方法。")


# 迴圈第一次和第二次執行時，`shape_item` 指向一個 `Line` 物件，
# 所以當 `draw` 被調用時，執行的是 `Line` 類別中定義的那個方法。
#
# 迴圈第三次和第四次執行時，`shape_item` 指向一個 `Rectangle` 物件，
# 所以當 `draw` 被調用時，執行的是 `Rectangle` 類別中定義的那個方法。
#
# 從某種意義上說，每個物件都知道如何繪製自己。
# 這個特性稱為 **多型 (polymorphism)**。
# 這個詞來自希臘詞根，意思是「多種形狀的 (many shaped)」。
# 在物件導向程式設計中，多型是指不同型別提供相同方法的能力，
# 這使得可以透過在不同型別的物件上調用相同的方法來執行許多計算 —— 例如繪製形狀。
#
# 在本章末尾的一個練習中，你將定義一個代表圓形的新類別，並提供一個 `draw` 方法。
# 然後你就可以使用多型來繪製線條、矩形和圓形。

# ## 除錯 (Debugging)
#
# 在本章中，我們遇到了一個隱微的 bug，它發生在我們建立了一個被兩個 `Rectangle` 物件共享的 `Point`，
# 然後我們修改了那個 `Point`。
# 一般來說，有兩種方法可以避免這類問題：你可以避免共享物件，或者你可以避免修改它們。
#
# 要避免共享物件，你可以使用深複製 (deep copy)，就像我們在本章做的那樣。
#
# 要避免修改物件，可以考慮用純函數 (pure function)（像是 `translated`）取代非純函數 (impure function)（像是 `translate`）。
# 例如，這裡有一個 `translated` 的版本，它會建立一個新的 `Point` 並且永遠不會修改其屬性。
# (這應該是 Point 類別的方法，而不是獨立函數)

# 這應該是 Point 類別的一個方法，而且我們之前已經定義過一個類似的 translated 方法了。
# 這裡可能是想強調 Point 的 translated 方法本身就是純的。
# class Point:
#     ... (其他方法) ...
#     def translated(self, dx=0, dy=0):
#         new_x = self.x + dx
#         new_y = self.y + dy
#         return Point(new_x, new_y) # 建立並回傳一個新的 Point 物件，不修改 self

# Python 提供了一些功能，可以更容易地避免修改物件。
# 它們超出了本書的範圍，但如果你好奇，可以問問虛擬助理：「如何讓 Python 物件不可變？」
#
# 建立一個新物件比修改一個現有物件花費更多時間，但在實務中這種差異通常不重要。
# 避免共享物件和非純函數的程式通常更容易開發、測試和除錯 ——
# 而最好的除錯就是你不需要做的那種。

# ## 詞彙表 (Glossary)
#
# **淺複製 (shallow copy):**
#  一種不複製巢狀物件的複製操作。
#
# **深複製 (deep copy):**
#  一種同時也複製巢狀物件的複製操作。
#
# **多型 (polymorphism):**
#  方法或運算子能夠與多種類型的物件一起運作的能力。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 對於下面所有的練習，都可以考慮請虛擬助理幫忙。
# 如果你這樣做，你會想在提示中包含 `Point`、`Line` 和 `Rectangle` 的類別定義
# —— 否則虛擬助理會猜測它們的屬性和函數，而它產生的程式碼將無法運作。

# ### 練習
#
# 為 `Line` 類別編寫一個 `__eq__` 方法，如果 `Line` 物件參照的 `Point` 物件等值
# (順序不拘)，則回傳 `True`。

# 你可以用下面的大綱開始。
# (為了能執行，我們需要 Line 和 Point 的完整定義)
# 我們使用本章節中最新定義的 Point (包含 __eq__) 和 Line (不含 __eq__)

class Point_For_Line_Eq: # 避免與前面的 Point 衝突，用於此練習
    def __init__(self, x, y): self.x = x; self.y = y
    def __str__(self): return f'Point({self.x}, {self.y})'
    def __eq__(self, other):
        if not isinstance(other, Point_For_Line_Eq): return NotImplemented
        return self.x == other.x and self.y == other.y
    # translated (為了讓 Line 的方法能用，如果需要的話)
    def translated(self, dx=0, dy=0):
        return Point_For_Line_Eq(self.x + dx, self.y + dy)


class Line_For_Eq: # 避免與前面的 Line 衝突
    def __init__(self, p1, p2): self.p1 = p1; self.p2 = p2
    def __str__(self): return f'Line({self.p1}, {self.p2})'
    # draw (為了讓後面的練習能用)
    def draw(self): jumpto(self.p1.x, self.p1.y); moveto(self.p2.x, self.p2.y)

    # midpoint (為後面練習準備)
    def midpoint(self):
        mid_x = (self.p1.x + self.p2.x) / 2
        mid_y = (self.p1.y + self.p2.y) / 2
        return Point_For_Line_Eq(mid_x, mid_y) # 假設 Point 有 __init__

    # __eq__ 方法將在這裡定義
    # def __eq__(self, other):
    #     return None


# %%add_method_to Line_For_Eq
# 直接在 Line_For_Eq 中定義 __eq__
class Line_For_Eq:
    def __init__(self, p1, p2): self.p1 = p1; self.p2 = p2
    def __str__(self): return f'Line({self.p1}, {self.p2})'
    def draw(self): jumpto(self.p1.x, self.p1.y); moveto(self.p2.x, self.p2.y)
    def midpoint(self):
        mid_x = (self.p1.x + self.p2.x) / 2
        mid_y = (self.p1.y + self.p2.y) / 2
        return Point_For_Line_Eq(mid_x, mid_y)

    def __eq__(self, other_line_eq): # 參數改名
        if not isinstance(other_line_eq, Line_For_Eq):
            return NotImplemented # 無法與不同類型比較

        # 檢查情況1: p1==other.p1 且 p2==other.p2
        # Point 物件的比較會使用 Point 的 __eq__ 方法
        if (self.p1 == other_line_eq.p1) and (self.p2 == other_line_eq.p2):
            return True
        # 檢查情況2: p1==other.p2 且 p2==other.p1 (順序相反)
        if (self.p1 == other_line_eq.p2) and (self.p2 == other_line_eq.p1):
            return True
        return False

# (上面是書中解答的直接翻譯，但實際上 __eq__ 應該在類別定義內)

# 你可以用這些例子來測試你的程式碼。
print(f"\n--- Line 的 __eq__ 方法測試 ---")
start1_leq = Point_For_Line_Eq(0, 0)
start2_leq = Point_For_Line_Eq(0, 0) # 與 start1_leq 等值但不同一
end_leq = Point_For_Line_Eq(200, 100)

# 這個例子應該是 `True`，因為 `Line` 物件參照的 `Point` 物件等值，且順序相同。

line_a_leq = Line_For_Eq(start1_leq, end_leq)
line_b_leq = Line_For_Eq(start2_leq, end_leq)
print(f"line_a_leq == line_b_leq (預期 True): {line_a_leq == line_b_leq}")

# 這個例子應該是 `True`，因為 `Line` 物件參照的 `Point` 物件等值，但順序相反。

line_c_leq = Line_For_Eq(end_leq, start1_leq)
print(f"line_a_leq == line_c_leq (預期 True): {line_a_leq == line_c_leq}")

# 等值性應該總是具有傳遞性 —— 也就是說，如果 `line_a` 和 `line_b` 等值，
# 且 `line_a` 和 `line_c` 等值，那麼 `line_b` 和 `line_c` 也應該等值。

print(f"line_b_leq == line_c_leq (預期 True，傳遞性): {line_b_leq == line_c_leq}")

# 這個例子應該是 `False`，因為 `Line` 物件參照的 `Point` 物件不等值。

line_d_leq = Line_For_Eq(start1_leq, start2_leq) # 這是一條長度為0的線，從 (0,0) 到 (0,0)
print(f"line_a_leq == line_d_leq (預期 False): {line_a_leq == line_d_leq}")


# ### 練習
#
# 為 `Line_For_Eq` (原書 `Line`) 類別編寫一個叫做 `midpoint` 的方法，
# 它計算線段的中點並以 `Point_For_Line_Eq` (原書 `Point`) 物件的形式回傳結果。
# (midpoint 方法已在 In[105]/In[106] 的 Line_For_Eq 中定義了)

# 你可以用下面的大綱開始。
# (midpoint 已在上面定義)

# %%add_method_to Line_For_Eq
#     def midpoint(self):
#         return Point_For_Line_Eq(0, 0) # 預留位置

# (midpoint 已在上面定義)

# 你可以用下面的例子來測試你的程式碼並繪製結果。
print(f"\n--- Line 的 midpoint 方法測試 ---")
start_mid_test = Point_For_Line_Eq(0, 0)
end1_mid_test = Point_For_Line_Eq(300, 0)
end2_mid_test = Point_For_Line_Eq(0, 150)
line1_mid_test = Line_For_Eq(start_mid_test, end1_mid_test)
line2_mid_test = Line_For_Eq(start_mid_test, end2_mid_test)

mid1_result = line1_mid_test.midpoint()
print(f"line1_mid_test 的中點: {mid1_result}") # (150, 0)

mid2_result = line2_mid_test.midpoint()
print(f"line2_mid_test 的中點: {mid2_result}") # (0, 75)

line3_connecting_midpoints = Line_For_Eq(mid1_result, mid2_result)

print("\n--- 繪製線條及其連接中點的線 ---")
make_turtle(width=400, height=200)
shapes_to_draw_mid = [line1_mid_test, line2_mid_test, line3_connecting_midpoints]
for shape_mid in shapes_to_draw_mid:
    if hasattr(shape_mid, 'draw'): shape_mid.draw()


# ### 練習
#
# 為 `Rectangle` 類別編寫一個叫做 `midpoint` 的方法，
# 它找出矩形中心點並以 `Point` 物件的形式回傳結果。
# (我們需要 Rectangle 類別的完整定義)

class Rectangle_For_Midpoint: # 避免與前面的 Rectangle 衝突
    def __init__(self, width, height, corner): # corner 是 Point_For_Line_Eq 物件
        self.width = width; self.height = height; self.corner = corner
    def __str__(self): return f'Rectangle({self.width}, {self.height}, {self.corner})'
    def make_points(self):
        p1 = self.corner; p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height); p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4
    def make_lines(self):
        p1, p2, p3, p4 = self.make_points()
        return Line_For_Eq(p1, p2), Line_For_Eq(p2, p3), Line_For_Eq(p3, p4), Line_For_Eq(p4, p1)
    def draw(self):
        for line_side in self.make_lines():
            if hasattr(line_side, 'draw'): line_side.draw()
    # midpoint 方法將在這裡定義


# 你可以用下面的大綱開始。

# %%add_method_to Rectangle_For_Midpoint
#     def midpoint(self):
#         return Point_For_Line_Eq(0, 0) # 預留位置

# 直接在 Rectangle_For_Midpoint 中定義 midpoint
class Rectangle_For_Midpoint:
    def __init__(self, width, height, corner):
        self.width = width; self.height = height; self.corner = corner
    def __str__(self): return f'Rectangle({self.width}, {self.height}, {self.corner})'
    def make_points(self):
        p1 = self.corner; p2 = p1.translated(self.width, 0)
        p3 = p2.translated(0, self.height); p4 = p3.translated(-self.width, 0)
        return p1, p2, p3, p4
    def make_lines(self):
        p1, p2, p3, p4 = self.make_points()
        return Line_For_Eq(p1, p2), Line_For_Eq(p2, p3), Line_For_Eq(p3, p4), Line_For_Eq(p4, p1)
    def draw(self):
        for line_side in self.make_lines():
            if hasattr(line_side, 'draw'): line_side.draw()

    def midpoint(self):
        # 矩形中心點的 x 座標 = 左上角 x + 寬度的一半
        # 矩形中心點的 y 座標 = 左上角 y + 高度的一半
        mid_x_rect = self.corner.x + self.width / 2
        mid_y_rect = self.corner.y + self.height / 2
        return Point_For_Line_Eq(mid_x_rect, mid_y_rect)


# 你可以用下面的例子來測試你的程式碼。
print(f"\n--- Rectangle 的 midpoint 方法測試 ---")
corner_rect_mid_test = Point_For_Line_Eq(30, 20)
rectangle_mid_test = Rectangle_For_Midpoint(100, 80, corner_rect_mid_test)
print(f"矩形: {rectangle_mid_test}")

midpoint_of_rect = rectangle_mid_test.midpoint()
print(f"矩形的中點: {midpoint_of_rect}") # x = 30 + 100/2 = 80, y = 20 + 80/2 = 60 => Point(80,60)

diagonal_line_to_mid = Line_For_Eq(corner_rect_mid_test, midpoint_of_rect) # 從左上角到中心的線

print("\n--- 繪製矩形及其到中心點的對角線 ---")
make_turtle(width=400, height=200)
# 假設 line1_xaxis, line2_yaxis 已定義 (座標軸)
if 'line1_xaxis' in globals() and hasattr(line1_xaxis, 'draw'): line1_xaxis.draw()
if 'line2_yaxis' in globals() and hasattr(line2_yaxis, 'draw'): line2_yaxis.draw()

if hasattr(rectangle_mid_test, 'draw'): rectangle_mid_test.draw()
if hasattr(diagonal_line_to_mid, 'draw'): diagonal_line_to_mid.draw()


# ### 練習
#
# 為 `Rectangle_For_Midpoint` (原書 `Rectangle`) 類別編寫一個叫做 `make_cross` 的方法，它：
#
# 1. 使用 `make_lines` 取得代表矩形四條邊的 `Line_For_Eq` 物件列表。
#
# 2. 計算這四條線的中點。
#
# 3. 建立並回傳一個包含兩個 `Line_For_Eq` 物件的列表 (或元組)，
#    這兩個物件代表連接相對中點的線，形成穿過矩形中心的十字。

# 你可以用這個大綱開始。
# (make_cross 應該是 Rectangle_For_Midpoint 的方法)

# %%add_method_to Rectangle_For_Midpoint
#     def make_cross(self): # 書中用 make_diagonals，但題目要求 make_cross
#         return [] # 預留位置

# 直接在 Rectangle_For_Midpoint 中定義 make_cross
class Rectangle_For_Cross(Rectangle_For_Midpoint): # 繼承自 Rectangle_For_Midpoint 以包含其方法
    def make_cross(self):
        # 1. 取得四條邊的 Line 物件
        # make_lines() 回傳 (top, right, bottom, left)
        line_top, line_right, line_bottom, line_left = self.make_lines()

        # 2. 計算四條線的中點
        # Line_For_Eq 類別需要有 midpoint 方法 (已在 In[106] 中加入)
        mid_top = line_top.midpoint()
        mid_right = line_right.midpoint()
        mid_bottom = line_bottom.midpoint()
        mid_left = line_left.midpoint()

        # 3. 建立連接相對中點的線
        # 十字線是連接 上中點和下中點，以及 左中點和右中點
        cross_line_vertical = Line_For_Eq(mid_top, mid_bottom)
        cross_line_horizontal = Line_For_Eq(mid_left, mid_right)

        return cross_line_vertical, cross_line_horizontal # 回傳一個元組包含兩條線

# 你可以用下面的例子來測試你的程式碼。
print(f"\n--- Rectangle 的 make_cross 方法測試 ---")
corner_rect_cross_test = Point_For_Line_Eq(30, 20)
rectangle_cross_test = Rectangle_For_Cross(100, 80, corner_rect_cross_test)
print(f"矩形: {rectangle_cross_test}")

cross_lines_list = rectangle_cross_test.make_cross()
print(f"形成的十字線: {cross_lines_list[0]} 和 {cross_lines_list[1]}")


print("\n--- 繪製矩形及其中心的十字線 ---")
make_turtle(width=400, height=200)
if hasattr(rectangle_cross_test, 'draw'): rectangle_cross_test.draw()
for cross_l in cross_lines_list:
    if hasattr(cross_l, 'draw'): cross_l.draw()


# ### 練習
#
# 編寫一個名為 `Circle` 的類別定義，具有屬性 `center` (中心點) 和 `radius` (半徑)，
# 其中 `center` 是一個 Point 物件，`radius` 是一個數字。
# 包括特殊方法 `__init__` 和 `__str__`，以及一個叫做 `draw` 的方法，
# 使用 `jupyturtle` 函數來繪製圓形。

# 你可以使用下面的函數，它是我們在第四章寫的 `circle` 函數的一個版本。
# (這個 draw_circle 是全域函數，Circle 的 draw 方法會呼叫它)

# from jupyturtle import make_turtle, forward, left, right # 已在前面匯入過
import math

def draw_circle_global(radius_dcg): # 參數改名，避免與 Circle 的 radius 混淆
    # 這個函數假設海龜已經在圓周上，並且方向正確 (與圓周相切)
    # 通常是先移動到圓心，再移動到圓周上某點，然後調整方向開始畫
    circumference_dcg = 2 * math.pi * radius_dcg
    n_sides_dcg = 60 # 用更多邊來畫圓，使其更平滑 (書中用30)
    length_side_dcg = circumference_dcg / n_sides_dcg
    angle_turn_dcg = 360.0 / n_sides_dcg # 確保是浮點數除法

    # 為了讓多邊形的「起始點」看起來像是在圓的底部或側面，而不是一個角
    # 我們可以先稍微轉動一下，或者調整 jumpto 的位置
    # 書中 Circle.draw 的邏輯是先跳到 (center.x + radius, center.y)，然後左轉90度
    # 這裡我們假設呼叫 draw_circle_global 之前，海龜已就位並朝向正確
    # left(angle_turn_dcg / 2) # 這一行是為了讓多邊形的邊「平躺」在底部

    for _ in range(n_sides_dcg):
        forward(length_side_dcg)
        left(angle_turn_dcg)
    # right(angle_turn_dcg / 2) # 轉回來 (如果前面有轉的話)

# 解答

class Circle:
    """表示一個圓形，具有中心點和半徑。"""
    def __init__(self, center_point_circle, radius_circle): # 參數改名
        # 應該檢查 center_point_circle 是否為 Point 物件，radius_circle 是否為數字
        self.center = center_point_circle # Point 物件
        self.radius = radius_circle       # 數字

    def __str__(self):
        return f'Circle(中心點={self.center}, 半徑={self.radius})' # 中文化輸出

    def draw(self):
        """使用 jupyturtle 繪製圓形。"""
        # 1. 把海龜抬起，移動到圓周上的一個起始點
        #    例如，圓的最右邊的點 (center.x + radius, center.y)
        start_draw_x = self.center.x + self.radius
        start_draw_y = self.center.y

        print(f"準備繪製 Circle: {self}")
        print(f"  海龜跳到圓周起始點: ({start_draw_x}, {start_draw_y})")
        jumpto(start_draw_x, start_draw_y) # 海龜不可見地移動

        # 2. 讓海龜放下筆，並調整方向使其與圓周相切
        #    如果起始點在最右邊，海龜應該向上 (或向下) 開始畫
        #    預設海龜朝右 (0度)，所以需要左轉 90 度使其朝上
        print(f"  海龜左轉 90 度")
        left(90)

        # 3. 呼叫全域的 draw_circle_global 函數來繪製多邊形近似圓
        print(f"  開始繪製半徑為 {self.radius} 的圓...")
        draw_circle_global(self.radius)

        # 4. (選擇性) 繪製完畢後可以把海龜方向恢復，或抬筆
        #    例如，再右轉 90 度，使其方向恢復水平朝右
        # right(90)
        print(f"圓形繪製完成。")


# 你可以用下面的例子來測試你的程式碼。
# 我們先從一個寬高為 `100` 的正方形 `Rectangle_For_Cross` (或類似的 Rectangle 類別) 開始。
# (需要使用定義了 midpoint 的 Rectangle 類別，例如 Rectangle_For_Cross)
print(f"\n--- Circle 類別測試 ---")
corner_for_circle_test = Point_For_Line_Eq(20, 20) # 使用與 Rectangle 相容的 Point
square_for_circle = Rectangle_For_Cross(100, 100, corner_for_circle_test)
print(f"用於容納圓的正方形: {square_for_circle}")

# 下面的程式碼應該建立一個剛好能放進正方形內的 `Circle`。

center_of_square = square_for_circle.midpoint() # Rectangle 需要有 midpoint 方法
radius_of_incircle = square_for_circle.height / 2 # 對於正方形，用寬或高的一半都行

circle_in_square = Circle(center_of_square, radius_of_incircle)
print(f"建立的圓形: {circle_in_square}")

# 如果一切運作正確，下面的程式碼應該會在正方形內部繪製圓形 (四邊相切)。

print("\n--- 繪製正方形及其內切圓 ---")
make_turtle(width=200, height=200, delay=0.01) # delay=0.01 讓繪圖快一點

if hasattr(square_for_circle, 'draw'): square_for_circle.draw()
if hasattr(circle_in_square, 'draw'): circle_in_square.draw()


# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)