# -*- coding: utf-8 -*-
# 從 chap17.ipynb 轉換而來
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

import thinkpython

# # 繼承 (Inheritance)
#
# 物件導向程式設計中最常被聯想到的語言特性是 **繼承 (inheritance)**。
# 繼承是一種能力，讓你可以定義一個新類別，作為現有類別的修改版本。
# 在本章中，我將使用代表撲克牌、牌堆和撲克牌型的類別來示範繼承。
# 如果你不玩撲克牌，別擔心 —— 我會告訴你你需要知道的。

# ## 表示紙牌 (Representing cards)
#
# 一副標準的撲克牌有 52 張 —— 每張牌都屬於四種花色 (suit) 之一和十三種點數 (rank) 之一。
# 花色是黑桃 (Spades)、紅心 (Hearts)、方塊 (Diamonds) 和梅花 (Clubs)。
# (譯註：台灣常見說法是 黑桃、紅心(愛心)、方塊(紅磚)、梅花(花))
# 點數是 A (Ace)、2、3、4、5、6、7、8、9、10、J (Jack)、Q (Queen) 和 K (King)。
# 根據你玩的遊戲不同，A 可以比 K 大，也可以比 2 小。
#
# 如果我們想定義一個新的物件來表示一張撲克牌，很明顯屬性應該是 `rank` (點數) 和 `suit` (花色)。
# 但這些屬性的型別應該是什麼，就比較不明顯了。
# 一種可能是使用像 `'Spade'` (黑桃) 這樣的字串來表示花色，用 `'Queen'` (皇后) 這樣的字串來表示點數。
# 這種實作方式的一個問題是，要比較牌的點數或花色大小會比較困難。
#
# 另一種方法是用整數來 **編碼 (encode)** 點數和花色。
# 在這裡，「編碼」的意思是我們要定義數字和花色之間，或者數字和點數之間的對應關係。
# 這種編碼並不是為了保密 (那叫做「加密 (encryption)」)。

# 例如，下表顯示了花色和對應的整數代碼：
#
#
# | 花色 (Suit) | 代碼 (Code) |
# | --- | --- |
# |  黑桃 (Spades)     |   3  |
# |  紅心 (Hearts)     |   2  |
# |  方塊 (Diamonds)   |   1  |
# |  梅花 (Clubs)      |   0  |
#
# 有了這種編碼，我們就可以透過比較它們的代碼來比較花色的大小。
# (例如，黑桃(3) > 紅心(2) > 方塊(1) > 梅花(0) 是一個常見的撲克牌花色大小順序)

# 為了編碼點數，我們會用整數 `2` 代表點數 `2`，`3` 代表 `3`，依此類推，直到 `10`。
# 下表顯示了人頭牌 (face cards) 的代碼。
#
#
# | 點數 (Rank) | 代碼 (Code) |
# | --- | --- |
# |  J (Jack)   |   11  |
# |  Q (Queen)  |   12  |
# |  K (King)   |   13  |
#
# 而我們可以用 `1` 或 `14` 來代表 A (Ace)，取決於我們想讓它被視為比其他點數小還是大。
#
# 為了表示這些編碼，我們會使用兩個字串列表，一個包含花色的名稱，另一個包含點數的名稱。
#
# 這裡是一個表示撲克牌的類別定義，它把這些字串列表當作 **類別變數 (class variables)**，
# 類別變數是定義在類別定義內部，但不在任何方法內部的變數。

class Card:
    """表示一張標準的撲克牌。"""

    # suit_names 和 rank_names 是類別變數，所有 Card 實體共享它們
    suit_names = ['梅花', '方塊', '紅心', '黑桃'] # Clubs, Diamonds, Hearts, Spades (按代碼0-3順序)
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A' # 索引1對應A(小), 索引14對應A(大)
    ]

# `rank_names` 的第一個元素是 `None`，因為沒有點數為零的牌。
# 透過加入 `None` 作為佔位符，我們得到一個列表，它具有一個很好的特性：
# 索引 `2` 對應到字串 `'2'`，依此類推。
# (索引 `1` 對應 `'A'`，索引 `11` 對應 `'J'` 等)
#
# 類別變數是與類別本身相關聯的，而不是與類別的實體相關聯，所以我們可以這樣存取它們。

print(f"Card.suit_names: {Card.suit_names}")

# 我們可以用 `suit_names` 來查詢一個花色代碼並得到對應的字串。

print(f"Card.suit_names[0]: {Card.suit_names[0]}") # 梅花

# 並用 `rank_names` 來查詢一個點數代碼。

print(f"Card.rank_names[11]: {Card.rank_names[11]}") # J

# ## 紙牌屬性 (Card attributes)
#
# 這是 `Card` 類別的 `__init__` 方法 —— 它接收 `suit` (花色代碼) 和 `rank` (點數代碼)
# 作為參數，並將它們指派給同名的屬性。

# %%add_method_to Card
# 重新定義 Card 類別以加入 __init__ 方法
class Card:
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃']
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit_code, rank_code): # 參數改名以區分屬性
        self.suit = suit_code # 花色代碼 (0-3)
        self.rank = rank_code # 點數代碼 (例如 2-10, J=11, Q=12, K=13, A=1或14)

# 現在我們可以像這樣建立一個 `Card` 物件。

queen_of_diamonds = Card(1, 12) # 方塊Q (花色代碼1是方塊，點數代碼12是Q)

# 我們可以用新的實體來存取屬性。

print(f"queen_of_diamonds 的花色代碼: {queen_of_diamonds.suit}, 點數代碼: {queen_of_diamonds.rank}")

# 用實體來存取類別變數也是合法的。

print(f"透過實體存取 suit_names: {queen_of_diamonds.suit_names}")

# 但是如果你使用類別名稱來存取，會更清楚地表明它們是類別變數，而不是實體屬性。

# ## 印出紙牌 (Printing cards)
#
# 這是 `Card` 物件的 `__str__` 方法。

# %%add_method_to Card
# 再次重新定義 Card 類別以加入 __str__ 方法
class Card:
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃']
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit_code, rank_code):
        self.suit = suit_code
        self.rank = rank_code

    def __str__(self):
        # 從類別變數中根據代碼查出名稱
        rank_name_str = Card.rank_names[self.rank]
        suit_name_str = Card.suit_names[self.suit]
        return f'{suit_name_str}{rank_name_str}' # 例如：方塊Q (Hearts Queen / 紅心Q)
                                                # 或是中文習慣：梅花A, 方塊K 等


# 當我們印出一個 `Card` 時，Python 會呼叫 `__str__` 方法來得到一個人類可讀的牌的表示法。

print(f"印出 queen_of_diamonds: {queen_of_diamonds}") # queen_of_diamonds 仍是舊版 Card 實體
# 為了測試新的 __str__，需要用新版 Card 建立實體
queen_of_diamonds_new = Card(1, 12)
print(f"印出新版 queen_of_diamonds_new: {queen_of_diamonds_new}") # 應該是 方塊Q

# 下面是 `Card` 類別物件和 Card 實體的圖表。
# `Card` 是一個類別物件，所以它的型別是 `type`。
# `queen_of_diamonds_new` 是 `Card` 的一個實體，所以它的型別是 `Card`。
# 為了節省空間，我沒有畫出 `suit_names` 和 `rank_names` 的內容。
# (圖表會顯示 Card (type) 包含 suit_names, rank_names；
#  queen_of_diamonds_new (Card) 包含 suit=1, rank=12)

from diagram import Binding, Value, Frame, Stack # diagram 模組元件

bindings_class_vars = [
    Binding(Value('suit_names'), draw_value=False), # draw_value=False 表示不畫出列表內容
    Binding(Value('rank_names'), draw_value=False)
]
frame1_card_class = Frame(bindings_class_vars, name='type', dy=-0.5, offsetx=0.77) # Card 類別本身是 type 型別
binding1_card_class_obj = Binding(Value('Card'), frame1_card_class) # Card 類別物件

bindings_instance_attrs = [
    Binding(Value('suit'), Value(queen_of_diamonds_new.suit)),
    Binding(Value('rank'), Value(queen_of_diamonds_new.rank))
]
frame2_card_instance = Frame(bindings_instance_attrs, name='Card', dy=-0.3, offsetx=0.33) # 實體的型別是 Card
binding2_card_instance_obj = Binding(Value('queen_new'), frame2_card_instance) # 書中用 'queen'

stack_card_diag = Stack([binding1_card_class_obj, binding2_card_instance_obj], dy=-1.2)


from diagram import diagram, Bbox, make_list, adjust # diagram 模組元件

width_card_diag, height_card_diag, x_card_diag, y_card_diag = [2.11, 2.14, 0.35, 1.76]
ax_card_diag = diagram(width_card_diag, height_card_diag)
bbox_stack_card = stack_card_diag.draw(ax_card_diag, x_card_diag, y_card_diag)

# 模擬列表物件的繪製 (不顯示內容)
# value_list_placeholder1 = make_list([])
# bbox_list1 = value_list_placeholder1.draw(ax_card_diag, x_card_diag + 1.66, y_card_diag)
# value_list_placeholder2 = make_list([])
# bbox_list2 = value_list_placeholder2.draw(ax_card_diag, x_card_diag + 1.66, y_card_diag - 0.5)
# bbox_card_union = Bbox.union([bbox_stack_card, bbox_list1, bbox_list2])
# adjust(x_card_diag, y_card_diag, bbox_card_union)


# 每個 `Card` 實體都有自己的 `suit` 和 `rank` 屬性，
# 但只有一個 `Card` 類別物件，也只有一份類別變數 `suit_names` 和 `rank_names` 的副本。

# ## 比較紙牌 (Comparing cards)
#
# 假設我們建立第二個 `Card` 物件，它有相同的花色和點數。

queen_of_diamonds2 = Card(1, 12) # 另一個方塊Q
print(f"queen_of_diamonds2: {queen_of_diamonds2}")

# 如果我們用 `==` 運算子比較它們，它會檢查 `queen_of_diamonds_new` 和 `queen_of_diamonds2`
# 是否參照同一個物件。

print(f"queen_of_diamonds_new == queen_of_diamonds2 (預設): {queen_of_diamonds_new == queen_of_diamonds2}") # False

# 它們不是，所以回傳 `False`。
# 我們可以透過定義特殊方法 `__eq__` 來改變這種行為。

# %%add_method_to Card
# 再次重新定義 Card 類別以加入 __eq__ 方法
class Card:
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃']
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit_code, rank_code):
        self.suit = suit_code
        self.rank = rank_code

    def __str__(self):
        rank_name_str = Card.rank_names[self.rank]
        suit_name_str = Card.suit_names[self.suit]
        return f'{suit_name_str}{rank_name_str}'

    def __eq__(self, other_card_eq): # 參數改名
        # 首先檢查 other_card_eq 是否也是 Card 物件
        if not isinstance(other_card_eq, Card):
            return NotImplemented # 表示無法與此類型比較
        # 如果花色和點數都相同，則兩張牌等值
        return self.suit == other_card_eq.suit and self.rank == other_card_eq.rank

# `__eq__` 接收兩個 `Card` 物件作為參數，如果它們有相同的花色和點數，
# 即使它們不是同一個物件，也回傳 `True`。
# 換句話說，它檢查它們是否等值 (equivalent)，即使它們並非同一 (identical)。
#
# 當我們對 `Card` 物件使用 `==` 運算子時，Python 會呼叫 `__eq__` 方法。

# 重新建立實體，使用包含 __eq__ 的 Card 類別
queen_eq_test1 = Card(1, 12)
queen_eq_test2 = Card(1, 12)
print(f"queen_eq_test1 == queen_eq_test2 (使用 __eq__): {queen_eq_test1 == queen_eq_test2}") # True

# 作為第二個測試，我們建立一張花色相同但點數不同的牌。

six_of_diamonds = Card(1, 6) # 方塊6
print(f"six_of_diamonds: {six_of_diamonds}")

# 我們可以確認 `queen_eq_test1` 和 `six_of_diamonds` 不等值。

print(f"queen_eq_test1 == six_of_diamonds: {queen_eq_test1 == six_of_diamonds}") # False

# 如果我們使用 `!=` 運算子，Python 會調用一個叫做 `__ne__` 的特殊方法 (如果不等於)，如果它存在的話。
# 否則，它會調用 `__eq__` 並將結果反轉 —— 所以如果 `__eq__` 回傳 `True`，
# `!=` 運算子的結果就是 `False`。

print(f"queen_eq_test1 != queen_eq_test2: {queen_eq_test1 != queen_eq_test2}") # False

print(f"queen_eq_test1 != six_of_diamonds: {queen_eq_test1 != six_of_diamonds}") # True

# 現在假設我們想比較兩張牌的大小。
# 如果我們使用其中一個關係運算子 (如 <, >)，我們會得到一個 `TypeError`。
# (因為預設情況下，Python 不知道如何比較自訂物件的大小)

%%expect TypeError
# queen_eq_test1 < queen_eq_test2 # TypeError: '<' not supported between instances of 'Card' and 'Card'

# 要改變 `<` 運算子的行為，我們可以定義一個叫做 `__lt__` 的特殊方法，
# 它是 "less than" (小於) 的縮寫。
# 為了這個例子，我們假設花色比點數重要 —— 所以所有黑桃都大於所有紅心，
# 紅心大於所有方塊，依此類推。
# 如果兩張牌花色相同，則點數較高的那張較大。
#
# 為了實作這個邏輯，我們會使用下面的方法，它回傳一個包含牌的花色和點數的元組 (按此順序)。

# %%add_method_to Card
# 再次重新定義 Card 類別以加入 to_tuple 和 __lt__
class Card:
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃']
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit_code, rank_code):
        self.suit = suit_code
        self.rank = rank_code

    def __str__(self):
        return f'{Card.suit_names[self.suit]}{Card.rank_names[self.rank]}'

    def __eq__(self, other_card_eq):
        if not isinstance(other_card_eq, Card): return NotImplemented
        return self.suit == other_card_eq.suit and self.rank == other_card_eq.rank

    def to_tuple(self): # 新增的方法
        """回傳一個 (花色代碼, 點數代碼) 的元組，用於比較。"""
        return (self.suit, self.rank)

# 我們可以用這個方法來寫 `__lt__`。

# %%add_method_to Card
# 接續上面的 Card 定義，加入 __lt__
    def __lt__(self, other_card_lt): # 參數改名
        if not isinstance(other_card_lt, Card):
            return NotImplemented
        # Python 可以直接比較元組，它會逐個元素比較
        return self.to_tuple() < other_card_lt.to_tuple()

# 元組比較會先比較每個元組的第一個元素 (代表花色)。
# 如果它們相同，它會比較第二個元素 (代表點數)。
#
# 現在如果我們使用 `<` 運算子，它會調用 `__lt__` 方法。

# 重新建立實體，使用包含 __lt__ 的 Card 類別
card_six_diamonds = Card(1, 6)  # 方塊6 (suit=1, rank=6)
card_queen_diamonds = Card(1, 12) # 方塊Q (suit=1, rank=12)
card_ace_hearts = Card(2, 1)     # 紅心A (suit=2, rank=1,假設A最小)

print(f"\n--- 測試紙牌比較 (<) ---")
print(f"{card_six_diamonds} < {card_queen_diamonds}: {card_six_diamonds < card_queen_diamonds}") # True (1,6) < (1,12)
print(f"{card_queen_diamonds} < {card_ace_hearts}: {card_queen_diamonds < card_ace_hearts}") # True (1,12) < (2,1) (因為紅心 > 方塊)


# 如果我們使用 `>` 運算子，它會調用一個叫做 `__gt__` (大於) 的特殊方法，如果它存在的話。
# 否則，它會調用 `__lt__` 並交換參數的順序 (或者說，如果 a > b 等同於 b < a)。
# (實際上，如果 `__gt__` 未定義，Python 會嘗試 `not (a < b or a == b)` 或者 `other < self` 等反射操作)
# 為了明確，最好也定義 `__gt__` 或所有相關的比較方法。

# 測試相等情況下的 <
print(f"{card_queen_diamonds} < {Card(1,12)} (同張牌): {card_queen_diamonds < Card(1,12)}") # False

# 測試 >
print(f"{card_queen_diamonds} > {card_six_diamonds}: {card_queen_diamonds > card_six_diamonds}") # True (會隱式使用 __lt__)

# 最後，如果我們使用 `<=` 運算子，它會調用一個叫做 `__le__` (小於等於) 的特殊方法。
# 如果沒有 __le__，Python 會嘗試 __lt__ 和 __eq__。

# %%add_method_to Card
# 再次重新定義 Card 類別以加入 __le__
# (為了簡潔，我們把所有比較方法都加到一個完整的 Card 定義中)
class Card: # 最終的 Card 類別 (目前為止)
    """表示一張標準的撲克牌。"""
    suit_names = ['梅花', '方塊', '紅心', '黑桃']
    rank_names = [
        None, 'A', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit_code, rank_code):
        self.suit = suit_code
        self.rank = rank_code

    def __str__(self):
        return f'{Card.suit_names[self.suit]}{Card.rank_names[self.rank]}'

    def __eq__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return self.suit == other.suit and self.rank == other.rank

    def to_tuple(self):
        return (self.suit, self.rank)

    def __lt__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other): # 小於等於
        if not isinstance(other, Card): return NotImplemented
        return self.to_tuple() <= other.to_tuple()

    # 為了完整性，通常也會定義 __gt__ 和 __ge__
    # 或者使用 functools.total_ordering 裝飾器 (如果已定義 __eq__ 和一個如 __lt__ 的方法)
    def __gt__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return self.to_tuple() > other.to_tuple()

    def __ge__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return self.to_tuple() >= other.to_tuple()


# 所以我們可以檢查一張牌是否小於或等於另一張。
# 重新建立實體
card_q_le_test1 = Card(1, 12) # 方塊Q
card_q_le_test2 = Card(1, 12) # 另一個方塊Q
card_s_le_test = Card(1, 6)   # 方塊6

print(f"{card_q_le_test1} <= {card_q_le_test2}: {card_q_le_test1 <= card_q_le_test2}") # True

print(f"{card_q_le_test1} <= {card_s_le_test}: {card_q_le_test1 <= card_s_le_test}") # False (Q > 6)

# 如果我們使用 `>=` 運算子，它會使用 `__ge__` (大於等於)，如果它存在的話。
# 否則，它會調用 `__le__` 並交換參數順序 (或者說 a >= b 等同於 b <= a)。
# (同樣，Python 有其回退機制，但明確定義更好)

print(f"{card_q_le_test1} >= {card_s_le_test}: {card_q_le_test1 >= card_s_le_test}") # True

# 如同我們定義的，這些方法是完整的，因為我們可以比較任何兩個 `Card` 物件；
# 也是一致的，因為不同運算子的結果不會互相矛盾。
# 有了這兩個特性，我們可以說 `Card` 物件是 **完全有序的 (totally ordered)**。
# 這意味著，我們很快就會看到，它們可以被排序。

# ## 牌堆 (Decks)
#
# 現在我們有了代表紙牌的物件，讓我們來定義代表牌堆的物件。
# 下面是 `Deck` 的類別定義，其 `__init__` 方法接收一個 `Card` 物件列表作為參數，
# 並將其指派給一個叫做 `cards` 的屬性。

class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list): # 參數改名
        self.cards = cards_list # cards 是一個 Card 物件的列表

# 要建立一個包含標準牌堆中 52 張牌的列表，我們會使用下面的靜態方法。
# (靜態方法屬於類別本身，而不是實體)

# %%add_method_to Deck
# 重新定義 Deck 以加入 make_cards 靜態方法
class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list):
        self.cards = cards_list

    @staticmethod # 標準的靜態方法標記法
    def make_cards():
        """建立並回傳一副標準的 52 張撲克牌的列表。"""
        cards_deck = []
        # 遍歷四種花色 (0-3)
        for suit_code_deck in range(4):
            # 遍歷點數 (2 到 14，其中 A 用 14 表示較大)
            # Card.rank_names 的有效索引是 1(A_small) 到 13(K), 14(A_big)
            # 標準牌組通常 A,2,3,4,5,6,7,8,9,10,J,Q,K
            # 如果 A 當作 14，則從 2 到 14 (13 張牌)
            # Card 的 __init__ 接收的是 rank_code
            # 假設我們要的是 2,3,...,10,J,Q,K,A(大)
            # rank_codes 可以是 2,3,...,10,11,12,13,14
            for rank_code_deck in range(2, 15): # 2 到 14
                card_obj = Card(suit_code_deck, rank_code_deck) # 使用最新定義的 Card
                cards_deck.append(card_obj)
        return cards_deck

# 在 `make_cards` 中，外層迴圈遍歷花色從 `0` 到 `3`。
# 內層迴圈遍歷點數從 `2` 到 `14` —— 其中 `14` 代表比 K 大的 A。
# 每次迭代都會用目前的花色和點數建立一個新的 `Card`，並將其附加到 `cards_deck`。
#
# 這是我們如何建立一個紙牌列表和一個包含它的 `Deck` 物件。

standard_cards_list = Deck.make_cards() # 呼叫靜態方法
standard_deck = Deck(standard_cards_list)
print(f"標準牌堆中的牌數: {len(standard_deck.cards)}")

# 它如預期般包含 52 張牌。

# ## 印出牌堆 (Printing the deck)
#
# 這是 `Deck` 的 `__str__` 方法。

# %%add_method_to Deck
# 重新定義 Deck 以加入 __str__ 方法
class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list):
        self.cards = cards_list

    @staticmethod
    def make_cards():
        cards_deck = []
        for suit_code_deck in range(4):
            for rank_code_deck in range(2, 15):
                card_obj = Card(suit_code_deck, rank_code_deck)
                cards_deck.append(card_obj)
        return cards_deck

    def __str__(self):
        """回傳牌堆中所有牌的字串表示法，每張牌一行。"""
        # Card 物件本身有 __str__ 方法，所以可以直接轉換
        card_strings_list = [str(card_item) for card_item in self.cards]
        return '\n'.join(card_strings_list) # 用換行符串接所有牌的字串


# 這個方法展示了一種有效累加大字串的方式 ——
# 先建立一個字串列表，然後使用字串的 `join` 方法。
#
# 我們用一個只包含兩張牌的牌堆來測試這個方法。

# 需要用最新定義的 Card 類別建立 queen_eq_test1 和 six_of_diamonds
card_q_for_small_deck = Card(1, 12) # 方塊Q
card_s_for_small_deck = Card(1, 6)  # 方塊6
small_deck_example = Deck([card_q_for_small_deck, card_s_for_small_deck])

# 如果我們呼叫 `str()`，它會調用 `__str__`。

str_of_small_deck = str(small_deck_example)
print(f"str(small_deck_example) 的結果 (包含換行符):")
print(repr(str_of_small_deck)) # 用 repr 印出才能看到 \n

# 當 Jupyter 顯示一個字串時，它會顯示字串的「表示形式 (representational form)」，
# 其中換行符用序列 `\n` 表示。
#
# 然而，如果我們印出結果，Jupyter 會顯示字串的「可列印形式 (printable form)」，
# 其中換行符會被印成實際的換行空白。

print("\nprint(small_deck_example) 的結果 (實際換行):")
print(small_deck_example)

# 所以紙牌會分行顯示。

# ## 新增、移除、洗牌和排序 (Add, remove, shuffle and sort)
#
# 為了發牌，我們希望有一個方法可以從牌堆中移除一張牌並回傳它。
# 列表的 `pop` 方法提供了一個方便的方式來做到這點。
# (pop 預設移除並回傳列表最後一個元素)

# %%add_method_to Deck
# 重新定義 Deck 以加入 take_card, put_card, shuffle, sort
class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list):
        self.cards = cards_list # cards 是一個 Card 物件的列表

    @staticmethod
    def make_cards():
        cards_deck = []
        for suit_code_deck in range(4):
            for rank_code_deck in range(2, 15):
                card_obj = Card(suit_code_deck, rank_code_deck)
                cards_deck.append(card_obj)
        return cards_deck

    def __str__(self):
        card_strings_list = [str(card_item) for card_item in self.cards]
        return '\n'.join(card_strings_list)

    def take_card(self):
        """從牌堆頂部 (列表末端) 移除並回傳一張牌。"""
        if self.cards: # 確保牌堆不是空的
            return self.cards.pop()
        else:
            print("警告: 牌堆已空，無法抽牌。")
            return None

# 我們這樣使用它。
# 重新建立 standard_deck 以使用包含新方法的 Deck
deck_for_ops = Deck(Deck.make_cards())
print(f"\n--- 牌堆操作測試 ---")
print(f"抽牌前牌堆數量: {len(deck_for_ops.cards)}")
taken_card = deck_for_ops.take_card()
print(f"抽出的牌: {taken_card}")

# 我們可以確認牌堆裡剩下 `51` 張牌。

print(f"抽牌後牌堆數量: {len(deck_for_ops.cards)}")

# 要加回一張牌，我們可以用列表的 `append` 方法。
# (append 會加到列表末端，效果類似把牌放到牌堆底部)

# %%add_method_to Deck
# 接續上面的 Deck 定義，加入 put_card
    def put_card(self, card_to_put): # 參數改名
        """將一張牌加入到牌堆底部 (列表末端)。"""
        if isinstance(card_to_put, Card):
            self.cards.append(card_to_put)
        else:
            print(f"警告: {card_to_put} 不是有效的 Card 物件，無法加入牌堆。")


# 作為例子，我們可以把剛才抽出的牌放回去。

if taken_card: # 確保之前有成功抽出牌
    deck_for_ops.put_card(taken_card)
print(f"放回牌後牌堆數量: {len(deck_for_ops.cards)}")


# 要洗牌，我們可以用 `random` 模組中的 `shuffle` 函數：

import random

# 這個儲存格初始化隨機數產生器，這樣我們每次都能得到相同的結果。
random.seed(3)

# %%add_method_to Deck
# 接續上面的 Deck 定義，加入 shuffle
    def shuffle(self):
        """隨機打亂牌堆中的牌。"""
        random.shuffle(self.cards) # random.shuffle 會就地修改列表


# 如果我們洗牌並印出前幾張牌，可以看到它們沒有明顯的順序。

print("\n--- 洗牌測試 ---")
deck_for_ops.shuffle()
print("洗牌後牌堆的前 4 張牌:")
for card_item_shuffled in deck_for_ops.cards[:4]:
    print(card_item_shuffled)

# 要排序紙牌，我們可以用列表的 `sort` 方法，它會「就地 (in place)」排序元素
# —— 也就是說，它會修改列表本身，而不是建立一個新的列表。

# %%add_method_to Deck
# 接續上面的 Deck 定義，加入 sort
    def sort(self):
        """根據 Card 定義的比較方法排序牌堆中的牌。"""
        # list.sort() 會使用元素 (Card 物件) 的 __lt__ 方法來比較
        self.cards.sort()


# 當我們調用 `sort` 時，它會使用 `__lt__` 方法來比較紙牌。
# (Card 類別已定義了 __lt__, __le__, __gt__, __ge__, __eq__)

print("\n--- 排序測試 ---")
deck_for_ops.sort()

# 如果我們印出前幾張牌，可以確認它們是按遞增順序排列的。
# (根據 Card 的 __lt__ 定義：先比花色，梅花最小，黑桃最大；同花色再比點數，A(1或14)看如何定義)
# 目前 Card 的 rank_names 把 A(1) 放前面，A(14) 放後面，但 __init__ 通常用 2-14。
# to_tuple 用 (self.suit, self.rank)，所以會先比花色，再比點數。

print("排序後牌堆的前 4 張牌:")
for card_item_sorted in deck_for_ops.cards[:4]:
    print(card_item_sorted)


# 在這個例子中，`Deck.sort` 除了調用 `list.sort` 之外什麼也沒做。
# 像這樣把責任傳遞下去的做法稱為 **委派 (delegation)**。

# ## 父類別與子類別 (Parents and children)
#
# 繼承是定義一個新類別作為現有類別修改版本的能力。
# 作為例子，假設我們想要一個類別來代表「一手牌 (hand)」，也就是一個玩家持有的牌。
#
# * 一手牌類似於一個牌堆 —— 它們都是由一組牌組成，並且都需要像是新增和移除牌這樣的操作。
#
# * 一手牌也不同於一個牌堆 —— 有些我們想對手牌進行的操作，對牌堆來說沒有意義。
#   例如，在撲克牌中，我們可能會比較兩手牌來看哪一手贏。在橋牌中，我們可能會計算一手牌的分數來叫牌。
#
# 類別之間的這種關係 —— 其中一個是另一個的特化版本 —— 非常適合使用繼承。
#
# 要定義一個基於現有類別的新類別，我們把現有類別的名稱放在括號裡。

# 為了讓 Hand 能繼承 Deck，我們需要 Deck 的完整定義
class Deck: # Deck 的完整定義 (包含所有方法)
    """表示一副牌堆。"""
    def __init__(self, cards_list): self.cards = cards_list
    @staticmethod
    def make_cards():
        cards_deck = []
        for s in range(4):
            for r in range(2, 15): cards_deck.append(Card(s, r))
        return cards_deck
    def __str__(self): return '\n'.join([str(c) for c in self.cards])
    def take_card(self): return self.cards.pop() if self.cards else None
    def put_card(self, card):
        if isinstance(card, Card): self.cards.append(card)
    def shuffle(self): random.shuffle(self.cards)
    def sort(self): self.cards.sort()
    # move_cards 方法將在後面加入


class Hand(Deck): # Hand 繼承自 Deck
    """表示一手牌。"""
    # Hand 會自動繼承 Deck 的 __init__, __str__, take_card, put_card, shuffle, sort

# 這個定義表示 `Hand` 繼承自 `Deck`，這意味著 `Hand` 物件可以存取 `Deck` 中定義的方法，
# 像是 `take_card` 和 `put_card`。
#
# `Hand` 也會從 `Deck` 繼承 `__init__`，但是如果我們在 `Hand` 類別中定義 `__init__`，
# 它就會覆寫 (override) `Deck` 類別中的那個。

# %%add_method_to Hand
# 重新定義 Hand 以加入自己的 __init__
class Hand(Deck):
    """表示一手牌。"""

    def __init__(self, label=''): # label 是這手牌的標籤，例如玩家名稱
        self.label = label
        self.cards = [] # 一手牌一開始是空的，而不是像牌堆那樣有牌

# 這個版本的 `__init__` 接收一個選擇性的字串作為參數，並且總是從一個空的牌列表開始。
# 當我們建立一個 `Hand` 時，Python 會調用這個方法，而不是 `Deck` 中的那個
# —— 我們可以透過檢查結果是否有 `label` 屬性來確認。

hand_player1 = Hand('玩家1')
print(f"手牌標籤: {hand_player1.label}")
print(f"手牌中的牌 (初始): {hand_player1.cards}") # 應該是空列表 []

# 要發一張牌，我們可以用 `take_card` 從 `Deck` 中移除一張牌，
# 並用 `put_card` 把牌加到 `Hand` 中。
# (這些方法是從 Deck 繼承來的)

# 建立一個新的標準牌堆
deck_for_dealing = Deck(Deck.make_cards())
print(f"\n--- 發牌測試 ---")
print(f"發牌前牌堆數量: {len(deck_for_dealing.cards)}")
print(f"發牌前玩家手牌: {hand_player1}") # 應該是空的

card_dealt = deck_for_dealing.take_card() # 從牌堆抽一張
if card_dealt:
    hand_player1.put_card(card_dealt) # 把抽到的牌加入手牌
print(f"發一張牌後，玩家手牌 ({hand_player1.label}):")
print(hand_player1)
print(f"發牌後牌堆數量: {len(deck_for_dealing.cards)}")


# 讓我們把這段程式碼封裝到 `Deck` 的一個叫做 `move_cards` 的方法中。
# (這個方法會從 self (一個 Deck 或 Hand) 移動牌到 other (另一個 Deck 或 Hand))

# %%add_method_to Deck
# 再次重新定義 Deck 以加入 move_cards
class Deck:
    """表示一副牌堆。"""
    def __init__(self, cards_list): self.cards = cards_list
    @staticmethod
    def make_cards():
        cards_deck = [];
        for s in range(4):
            for r in range(2, 15): cards_deck.append(Card(s, r))
        return cards_deck
    def __str__(self): return '\n'.join([str(c) for c in self.cards])
    def take_card(self): return self.cards.pop() if self.cards else None
    def put_card(self, card):
        if isinstance(card, Card): self.cards.append(card)
    def shuffle(self): random.shuffle(self.cards)
    def sort(self): self.cards.sort()

    def move_cards(self, other_hand_or_deck, num_cards): # 參數改名
        """從目前的牌堆/手牌移動 num_cards 張牌到 other_hand_or_deck。"""
        for _ in range(num_cards):
            if not self.cards: break # 如果沒牌了就停止
            card_to_move = self.take_card() # 從自己這裡抽牌
            if card_to_move: # 確保成功抽到牌
                other_hand_or_deck.put_card(card_to_move) # 把牌加入對方

# 由於 Deck 被重新定義，Hand 也需要重新定義以繼承新的 Deck
class Hand(Deck):
    """表示一手牌。"""
    def __init__(self, label=''):
        self.label = label
        self.cards = []


# 這個方法是多型的 —— 也就是說，它適用於多種類型：
# `self` 和 `other_hand_or_deck` 可以是 `Hand` 或 `Deck`。
# 所以我們可以用這個方法從 `Deck` 發牌到 `Hand`，從一手牌到另一手牌，
# 或者從 `Hand` 把牌放回 `Deck`。

# 當一個新類別繼承自一個現有類別時，現有類別稱為 **父類別 (parent class)**，
# 新類別稱為 **子類別 (child class)**。一般來說：
#
# * 子類別的實體應該擁有父類別的所有屬性，但它們可以有額外的屬性。
#
# * 子類別應該擁有父類別的所有方法，但它可以有額外的方法。
#
# * 如果子類別覆寫了父類別的方法，新方法應該接收相同的參數並回傳相容的結果。
#
# 這套規則稱為「里氏替換原則 (Liskov substitution principle)」，
# 以計算機科學家芭芭拉·利斯科夫 (Barbara Liskov) 的名字命名。
#
# 如果你遵守這些規則，任何設計來處理父類別實體 (像是 `Deck`) 的函數或方法，
# 也將適用於子類別的實體 (像是 `Hand`)。
# 如果你違反這些規則，你的程式碼可能會像紙牌屋一樣崩塌 (抱歉，用了雙關語)。
# (譯註：house of cards 指紙牌屋，也指不穩固的計畫或結構。)

# ## 特化 (Specialization)
#
# 讓我們建立一個叫做 `BridgeHand` 的類別，用來表示橋牌中的一手牌 ——
# 橋牌是一種廣泛流行的紙牌遊戲。
# 我們會從 `Hand` 繼承，並新增一個叫做 `high_card_point_count` 的新方法，
# 它會使用「大牌點計算法 (high card point)」來評估一手牌，
# 也就是把手中大牌的點數加總起來。
#
# 這裡有一個類別定義，它包含一個類別變數，是一個把牌名對應到其點數值的字典。
# (橋牌計點：A=4, K=3, Q=2, J=1)

class BridgeHand(Hand): # BridgeHand 繼承自 Hand (而 Hand 繼承自 Deck)
    """表示橋牌中的一手牌。"""

    hcp_dict = { # High Card Points (大牌點) 字典
        'A': 4, # Ace
        'K': 3, # King
        'Q': 2, # Queen
        'J': 1, # Jack
        # 其他牌 (2-10) 不計大牌點
    }

# 給定一張牌的點數代碼，像是 `12` (Q)，我們可以用 `Card.rank_names` 來取得點數的字串表示法，
# 然後用 `hcp_dict` 來取得它的分數。

example_rank_code_hcp = 12 # Q 的代碼
example_rank_name_hcp = Card.rank_names[example_rank_code_hcp] # 'Q'
example_score_hcp = BridgeHand.hcp_dict.get(example_rank_name_hcp, 0) # 從字典中取得分數，若無則為0
print(f"點數名稱: {example_rank_name_hcp}, 大牌點分數: {example_score_hcp}")

# 下面的方法會遍歷 `BridgeHand` 中的牌並加總它們的分數。

# %%add_method_to BridgeHand
# 重新定義 BridgeHand 以加入 high_card_point_count
class BridgeHand(Hand):
    """表示橋牌中的一手牌。"""
    hcp_dict = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}

    # __init__ 是從 Hand 繼承來的 (如果 Hand 有自己的 __init__)
    # 如果 Hand 沒有自己的 __init__，就會用 Deck 的 __init__，
    # 但我們之前為 Hand 定義了 __init__(self, label='')，所以 BridgeHand 會用那個。
    # 如果 BridgeHand 需要自己的 __init__，可以這樣定義：
    # def __init__(self, label=''):
    #     super().__init__(label) # 呼叫父類別 Hand 的 __init__
    #     # 這裡可以加 BridgeHand 特有的初始化

    def high_card_point_count(self):
        """計算並回傳這手橋牌的大牌點總數。"""
        count_hcp = 0
        for card_in_bridge_hand in self.cards:
            rank_name_bh = Card.rank_names[card_in_bridge_hand.rank]
            count_hcp += BridgeHand.hcp_dict.get(rank_name_bh, 0) # 取得點數，若不在字典中則為0
        return count_hcp

# 這個儲存格建立一個新的牌堆並初始化隨機數產生器
standard_cards_list_bh_test = Deck.make_cards()
deck_bh_test = Deck(standard_cards_list_bh_test)
random.seed(3) # 確保每次洗牌結果一樣，方便測試

# 為了測試它，我們會發一手包含五張牌的牌
# —— 橋牌一手通常有十三張，但用小例子測試程式碼比較容易。

hand_bridge_test = BridgeHand('玩家2 (橋牌)') # 建立 BridgeHand 實體
print(f"\n--- 橋牌大牌點計算測試 ---")
deck_bh_test.shuffle() # 洗牌
# 從 deck_bh_test 發 5 張牌到 hand_bridge_test
# 需要 Deck 類別有 move_cards 方法
# (我們在 In[112] 定義的 Deck 版本有 move_cards)
deck_bh_test.move_cards(hand_bridge_test, 5)
print(f"玩家2的橋牌手牌 ({len(hand_bridge_test.cards)} 張):")
print(hand_bridge_test) # 會用 Deck 的 __str__，因為 Hand/BridgeHand 沒有覆寫它

# 這是 K 和 Q 的總分。
# (根據 seed(3) 和抽5張，實際手牌內容會固定，我們可以手動驗證)
# 洗牌後的牌堆 (seed=3)，抽前5張 (pop 從尾巴抽):
# 假設 Deck.make_cards 產生的順序是 梅花2...梅花A, 方塊2...方塊A, ..., 黑桃2...黑桃A
# 洗牌後尾巴的5張牌可能是 (需要實際執行 deck_bh_test.cards[-5:] 在洗牌後看看)
# 為了範例，我們假設手牌是：黑桃K, 紅心Q, 梅花A, 方塊J, 黑桃10
# HCP: K=3, Q=2, A=4, J=1, 10=0 => 3+2+4+1+0 = 10
# 實際執行的結果 (seed=3, pop 5): 黑桃K, 梅花2, 方塊A, 方塊6, 紅心Q
# HCP: K=3, 2=0, A=4, 6=0, Q=2 => 3+0+4+0+2 = 9

hcp_score = hand_bridge_test.high_card_point_count()
print(f"這手牌的大牌點總數: {hcp_score}") # 應該是 9

# `BridgeHand` 繼承了 `Hand` 的變數和方法，並新增了一個類別變數和一個特定於橋牌的方法。
# 這種使用繼承的方式稱為 **特化 (specialization)**，因為它定義了一個新類別，
# 該類別是為特定用途 (例如玩橋牌) 而特化的。

# ## 除錯 (Debugging)
#
# 繼承是一個有用的特性。
# 有些沒有繼承就會很重複的程式，用了繼承可以寫得更簡潔。
# 此外，繼承可以促進程式碼重用，因為你可以自訂父類別的行為而無需修改它。
# 在某些情況下，繼承結構反映了問題的自然結構，這使得設計更容易理解。
#
# 另一方面，繼承可能會使程式難以閱讀。
# 當一個方法被調用時，有時不清楚它的定義在哪裡 —— 相關的程式碼可能分散在好幾個模組中。
#
# 每當你不確定程式的執行流程時，最簡單的解決方法是在相關方法的開頭加入印出陳述式。
# 如果 `Deck.shuffle` 印出一條類似 `執行 Deck.shuffle 中` 的訊息，
# 那麼當程式執行時，它就會追蹤執行流程。
#
# 作為替代方案，你可以使用下面的函數，它接收一個物件和一個方法名稱 (字串形式)，
# 並回傳提供該方法定義的類別。

def find_defining_class(obj_to_check, method_name_str): # 參數改名
    """找出給定方法是在哪個類別中定義的。"""
    # type(obj_to_check).mro() 回傳一個類別列表，代表方法解析順序 (Method Resolution Order)
    for class_in_mro in type(obj_to_check).mro():
        # vars(class_in_mro) 回傳類別的 __dict__，其中包含直接在該類別中定義的方法和屬性
        if method_name_str in vars(class_in_mro):
            return class_in_mro # 找到了定義該方法的類別
    return f"方法 '{method_name_str}' 未在物件的類別層級結構中找到。"


# `find_defining_class` 使用 `mro()` 方法來取得將被搜尋方法的類別物件 (型別) 列表。
# "MRO" 代表「方法解析順序 (method resolution order)」，
# 它是 Python 搜尋以「解析」方法名稱 (也就是找到該名稱所參照的函數物件) 的類別序列。
#
# 作為例子，讓我們實體化一個 `BridgeHand`，然後找出 `shuffle` 方法的定義類別。

hand_find_def_class = BridgeHand('玩家3') # 使用最新定義的 BridgeHand
defining_class_shuffle = find_defining_class(hand_find_def_class, 'shuffle')
print(f"\n--- 尋找方法定義類別 ---")
print(f"'shuffle' 方法是在 {defining_class_shuffle.__name__} 類別中定義的。") # Deck

# `BridgeHand` 物件的 `shuffle` 方法是 `Deck` 中的那個。
# (因為 BridgeHand -> Hand -> Deck，而 shuffle 在 Deck 中定義，Hand 和 BridgeHand 沒有覆寫它)

# ## 詞彙表 (Glossary)
#
# **繼承 (inheritance):**
#  定義一個新類別作為先前定義類別的修改版本的能力。
#
# **編碼 (encode):**
#  透過在兩組值之間建立對應關係，用一組值來表示另一組值。
#
# **類別變數 (class variable):**
#  定義在類別定義內部，但不在任何方法內部的變數。
#
# **完全有序的 (totally ordered):**
#  如果我們可以比較任何兩個元素並且結果是一致的，那麼一組物件就是完全有序的。
#
# **委派 (delegation):**
#  當一個方法把大部分或全部工作責任傳遞給另一個方法時。
#
# **父類別 (parent class):**
#  被繼承的類別。也稱為超類 (superclass) 或基類 (base class)。
#
# **子類別 (child class):**
#  繼承自另一個類別的類別。也稱為衍生類 (derived class) 或子類 (subclass)。
#
# **特化 (specialization):**
#  一種使用繼承來建立新類別的方式，該新類別是現有類別的特化版本。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a Virtual Assistant)
#
# 如果進展順利，物件導向程式設計可以使程式更具可讀性、可測試性和可重用性。
# 但它也可能使程式變得複雜且難以維護。
# 因此，OOP 是一個有爭議的話題 —— 有些人喜歡它，有些人不喜歡。
#
# 要了解更多關於這個主題的資訊，可以問問虛擬助理：
#
# * 物件導向程式設計有哪些優點和缺點？
#
# * 當人們說「優先使用組合而非繼承 (favor composition over inheritance)」時是什麼意思？
#
# * 什麼是里氏替換原則 (Liskov substitution principle)？
#
# * Python 是一種物件導向語言嗎？
#
# * 一個集合要成為完全有序的，需要滿足哪些條件？
#
# 一如往常，可以考慮請虛擬助理協助完成以下練習。

# ### 練習
#
# 在合約橋牌 (contract bridge) 中，「一墩 (trick)」是指一輪出牌，其中四位玩家各出一張牌。
# 為了表示這些牌，我們將定義一個繼承自 `Deck` 的類別。
# (注意：Trick 通常只包含4張牌，且可能有特定的出牌順序和規則，
#  繼承自 Deck 可能只是為了重用 Deck 的某些功能，例如儲存 cards 列表)

class Trick(Deck): # Trick 繼承自 Deck
    """表示合約橋牌中的一墩牌。"""
    # Trick 會繼承 Deck 的 __init__(self, cards_list)
    # 和其他 Deck 的方法，例如 __str__ (如果 Trick 不覆寫它)

# 作為例子，考慮這一墩牌，第一位玩家出了方塊3，這表示方塊是「引牌花色 (led suit)」。
# 第二和第三位玩家「跟花 (follow suit)」，意思是他們出了引牌花色的牌。
# 第四位玩家出了一張不同花色的牌，這表示他們無法贏得這一墩。
# 所以這一墩的贏家是第三位玩家，因為他們出了引牌花色中最大的牌。

# 使用最新定義的 Card 類別
cards_for_trick_example = [
    Card(1, 3),  # 方塊3 (引牌)
    Card(1, 10), # 方塊10
    Card(1, 12), # 方塊Q (應為贏家)
    Card(2, 13)  # 紅心K (非引牌花色)
]
trick_example = Trick(cards_for_trick_example) # 建立 Trick 物件
print(f"\n--- 橋牌一墩 (Trick) 練習 ---")
print("這一墩牌:")
print(trick_example) # 會使用 Deck 的 __str__

# 為 `Trick` 類別編寫一個叫做 `find_winner` 的方法，
# 它遍歷 `Trick` 中的牌，並回傳贏得這一墩的牌在列表中的索引。
# 在上一個例子中，贏牌的索引是 `2` (方塊Q)。

# 你可以用下面的大綱開始。

# %%add_method_to Trick
#     def find_winner(self):
#         return 0 # 預留位置

# 直接在 Trick 中定義 find_winner
class Trick(Deck):
    """表示合約橋牌中的一墩牌。"""
    # __init__ 從 Deck 繼承

    def find_winner(self):
        """找出並回傳這一墩牌中贏牌的索引。
        規則：
        1. 第一張出的牌決定引牌花色。
        2. 贏家是出了引牌花色中最大的牌的玩家。
        3. 如果玩家沒有引牌花色，他們出的任何其他花色的牌都不能贏 (除非是王牌，但這裡先不考慮王牌)。
        """
        if not self.cards: # 如果沒有牌
            return -1 # 或引發錯誤，表示無效的墩

        lead_card = self.cards[0] # 第一張牌是引牌
        lead_suit = lead_card.suit

        winner_index = 0 # 假設第一張牌暫時是贏家
        # winner_card = lead_card # 用來比較點數，但其實只需要 winner_index 和 winner_rank_in_lead_suit

        # 我們需要追蹤引牌花色中目前最大的點數
        # Card 的 rank 14 代表 A (大)，所以直接比較 rank 即可
        # Card 的 suit 0-3 代表 梅花-黑桃，可以直接比較 suit
        
        # Card 的 __lt__ 已經定義了比較邏輯 (先花色後點數)
        # 但橋牌比墩的規則是：
        # 1. 王牌 (trump suit) > 其他花色 (本練習先不考慮王牌)
        # 2. 在引牌花色 (led suit) 中，點數大者勝
        # 3. 非引牌花色者不能贏 (除非是王牌)
        
        # 簡化版：只考慮引牌花色，不考慮王牌
        current_winning_card_in_led_suit = lead_card # 目前引牌花色中最大的牌

        for i in range(1, len(self.cards)): #從第二張牌開始比較
            current_card = self.cards[i]
            # 只有與引牌花色相同的牌才能參與比較大小 (以贏得此墩)
            if current_card.suit == lead_suit:
                # 如果目前的牌比目前引牌花色中最大的牌還要大
                # (Card 的比較已定義，會先比花色再比點數，但這裡 suit 相同，所以只比 rank)
                # 或者更直接：current_card.rank > current_winning_card_in_led_suit.rank
                if current_card > current_winning_card_in_led_suit : # 使用 Card 的 __gt__
                    current_winning_card_in_led_suit = current_card
                    winner_index = i
            # 如果花色不同，則不能贏 (在此簡化規則下)

        return winner_index

# 如果你用上一個例子測試你的方法，贏牌的索引應該是 `2`。

# 重新建立 trick_example 以使用包含 find_winner 的 Trick 類別
trick_example_fw = Trick(cards_for_trick_example)
winner_idx = trick_example_fw.find_winner()
print(f"這一墩的贏牌索引: {winner_idx}") # 應該是 2
if winner_idx != -1:
    print(f"贏的牌是: {trick_example_fw.cards[winner_idx]}")


# ### 練習
#
# 接下來的幾個練習要求你編寫函數來分類撲克牌型。
# 如果你不熟悉撲克牌，我會解釋你需要知道的。
# 我們會用下面的類別來表示撲克牌型。

class PokerHand(Hand): # PokerHand 繼承自 Hand
    """表示一手撲克牌。"""

    def get_suit_counts(self):
        """計算每種花色出現的次數。回傳一個 (花色代碼 -> 次數) 的字典。"""
        suit_counter = {}
        for card_ph_sc in self.cards:
            key_suit = card_ph_sc.suit # 花色代碼是鍵
            suit_counter[key_suit] = suit_counter.get(key_suit, 0) + 1
        return suit_counter

    def get_rank_counts(self):
        """計算每種點數出現的次數。回傳一個 (點數代碼 -> 次數) 的字典。"""
        rank_counter = {}
        for card_ph_rc in self.cards:
            key_rank = card_ph_rc.rank # 點數代碼是鍵
            rank_counter[key_rank] = rank_counter.get(key_rank, 0) + 1
        return rank_counter

# `PokerHand` 提供了兩個有助於練習的方法。
#
# * `get_suit_counts` 遍歷 `PokerHand` 中的牌，計算每種花色牌的數量，
#   並回傳一個把花色代碼對應到其出現次數的字典。
#
# * `get_rank_counts` 對牌的點數做同樣的事情，
#   回傳一個把點數代碼對應到其出現次數的字典。
#
# 以下所有練習都只使用我們目前學過的 Python 功能就可以完成，
# 但其中一些比之前大部分練習要困難一些。
# 我鼓勵你向虛擬助理尋求幫助。
#
# 對於這類問題，向虛擬助理詢問關於策略和演算法的一般建議通常效果很好。
# 然後你可以自己編寫程式碼，或者請求程式碼。
# 如果你請求程式碼，你可能需要在提示中提供相關的類別定義。

# 作為第一個練習，我們要寫一個叫做 `has_flush` 的方法，
# 它檢查一手牌是否有「同花 (flush)」—— 也就是說，是否包含至少五張相同花色的牌。
#
# 在大多數種類的撲克牌遊戲中，一手牌包含五張或七張牌，
# 但有些奇特的變體中，一手牌可能包含其他數量的牌。
# 但無論一手牌中有多少張牌，只有組成最佳牌型的五張牌才算數。
# (這個練習的 has_flush 假設只要有5張同花就算，不一定剛好5張牌)

# 你可以用下面的大綱開始。

# %%add_method_to PokerHand
#     def has_flush(self):
#         """檢查這手牌是否有同花。"""
#         return False # 預留位置

# 直接在 PokerHand 中定義 has_flush
class PokerHand(Hand):
    """表示一手撲克牌。"""
    def get_suit_counts(self):
        suit_counter = {};
        for card in self.cards: suit_counter[card.suit] = suit_counter.get(card.suit, 0) + 1
        return suit_counter
    def get_rank_counts(self):
        rank_counter = {};
        for card in self.cards: rank_counter[card.rank] = rank_counter.get(card.rank, 0) + 1
        return rank_counter

    def has_flush(self):
        """檢查這手牌是否有同花 (至少五張同花色)。"""
        suit_counts_dict = self.get_suit_counts()
        for count_val_flush in suit_counts_dict.values(): # 遍歷每種花色的數量
            if count_val_flush >= 5:
                return True # 只要有一種花色達到5張或以上，就是同花
        return False # 如果沒有花色達到5張，就不是同花

# 為了測試這個方法，我們構造一手包含五張梅花牌的牌，所以它是一個同花。
# (梅花代碼是 0)
print(f"\n--- 撲克牌型練習：同花 (Flush) ---")
good_hand_flush_test = PokerHand('同花測試牌')

suit_for_flush = 0 # 梅花
# 點數 10, J, Q, K, A (大)
for rank_for_flush in range(10, 15): # 10, 11, 12, 13, 14
    card_flush = Card(suit_for_flush, rank_for_flush) # 用最新的 Card 定義
    good_hand_flush_test.put_card(card_flush)

print("同花測試牌 (good_hand_flush_test):")
print(good_hand_flush_test)


# 如果我們調用 `get_suit_counts`，可以確認花色代碼 `0` (梅花) 出現了 `5` 次。

print(f"good_hand_flush_test 的花色計數: {good_hand_flush_test.get_suit_counts()}")

# 所以 `has_flush` 應該回傳 `True`。

print(f"good_hand_flush_test.has_flush(): {good_hand_flush_test.has_flush()}")

# 作為第二個測試，我們構造一手包含三張梅花和另外兩種不同花色的牌。

cards_for_bad_flush = [
    Card(0, 2),  # 梅花2
    Card(0, 3),  # 梅花3
    Card(2, 4),  # 紅心4
    Card(3, 5),  # 黑桃5
    Card(0, 7),  # 梅花7
]
bad_hand_flush_test = PokerHand('非同花測試牌')
for card_bf in cards_for_bad_flush:
    bad_hand_flush_test.put_card(card_bf)

print("\n非同花測試牌 (bad_hand_flush_test):")
print(bad_hand_flush_test)
print(f"bad_hand_flush_test 的花色計數: {bad_hand_flush_test.get_suit_counts()}")


# 所以 `has_flush` 應該回傳 `False`。

print(f"bad_hand_flush_test.has_flush(): {bad_hand_flush_test.has_flush()}")

# ### 練習
#
# 編寫一個叫做 `has_straight` 的方法，它檢查一手牌是否包含順子 (straight)，
# 也就是一組五張點數連續的牌。
# 例如，如果一手牌包含點數 `5`、`6`、`7`、`8` 和 `9`，它就包含一個順子。
#
# A 可以放在 2 的前面，也可以放在 K 的後面，所以 `A、2、3、4、5` 是一個順子，
# `10、J、Q、K、A` 也是一個順子。
# 但是順子不能「繞圈」，所以 `K、A、2、3、4` 不是一個順子。
# (Card.rank_names 中 A(1) 和 A(14) 可以幫助處理這個)

# 你可以用下面的大綱開始。
# 它包含幾行程式碼，用來計算 A 的數量 (用代碼 `1` 或 `14` 表示)，
# 並將總數儲存在計數器的兩個位置 (索引1和14)。
# 這樣方便檢查以 A 開頭的順子 (A-2-3-4-5) 和以 A 結尾的順子 (10-J-Q-K-A)。

# %%add_method_to PokerHand
#     def has_straight(self, n=5): # n 是形成順子所需的最少連續牌數
#         """檢查這手牌是否有至少 n 張牌的順子。"""
#         counter = self.get_rank_counts()
#         # 處理 A 的兩種表示法 (1 和 14)
#         aces_count = counter.get(1, 0) + counter.get(14, 0)
#         # 如果手牌中有 A，則在計數器中把 rank 1 和 rank 14 的計數都設為 A 的總數
#         # (或者至少設為 1，如果我們只關心是否存在而不是數量)
#         # 這裡的邏輯是如果 original A(1) 或 original A(14) 存在，則兩者都視為存在。
#         if aces_count > 0:
#             counter[1] = max(counter.get(1,0), aces_count) # 更新，確保不會減少已有的計數
#             counter[14] = max(counter.get(14,0), aces_count)

#         return False # 預留位置

# 直接在 PokerHand 中定義 has_straight
class PokerHand(Hand): # 重新定義以加入新方法
    """表示一手撲克牌。"""
    def get_suit_counts(self):
        sc = {};
        for c in self.cards: sc[c.suit] = sc.get(c.suit, 0) + 1
        return sc
    def get_rank_counts(self):
        rc = {};
        for c in self.cards: rc[c.rank] = rc.get(c.rank, 0) + 1
        return rc
    def has_flush(self):
        sc = self.get_suit_counts();
        for v in sc.values():
            if v >= 5: return True
        return False

    def has_straight(self, n=5):
        """檢查這手牌是否有至少 n 張牌的順子。"""
        rank_counts = self.get_rank_counts() # 取得點數的計數

        # 處理 A：如果手牌中有 A (rank 1 或 14)，
        # 為了方便檢查兩種順子 (A-2-3-4-5 和 10-J-Q-K-A)，
        # 我們假設如果有點數 14 (大A)，也同時存在點數 1 (小A)。
        # Card.rank_names[1] 是 'A', Card.rank_names[14] 也是 'A'
        # 我們的 Card 物件的 rank 通常是 2-14。
        # 所以 get_rank_counts() 的鍵會是 2-14。
        # 如果手牌中有 A (rank=14)，我們也把它視為 rank=1 (用於 A2345 順子)
        # Card 類別的 rank_names[1] = 'A'
        if 14 in rank_counts and rank_counts[14] > 0: # 如果手牌有大 A
            rank_counts[1] = rank_counts.get(1, 0) + rank_counts[14] # 把大A也算作小A
            # 或者，如果只在乎是否存在，可以 rank_counts[1] = rank_counts.get(1,0) or rank_counts[14]
            # 書中原文的邏輯是:
            # aces = counter.get(1, 0) + counter.get(14, 0)
            # counter[1] = aces
            # counter[14] = aces
            # 這意味著如果手牌中有一張A，它在計數器中同時被視為rank 1和rank 14。
            # 我們這裡假設 Card 的 rank 統一用 2-14 (A 為 14)。
            # 如果需要檢查 A2345，則需要把 rank 14 視為 rank 1。

        # 檢查是否有連續 n 張牌
        # 點數範圍：A(1), 2, ..., 10, J(11), Q(12), K(13), A(14)
        # 檢查從 A(1) 到 10 的五張連續牌 (A2345, 23456, ..., TJQKA 中的 10JQKA)
        # rank_names 的索引是 1 到 14。
        # 我們需要檢查從 rank i 到 i+n-1 是否都存在於手牌中。
        # 最高的順子是 10-J-Q-K-A(14)。 起始點是 10。 i+n-1 = 10+5-1 = 14。
        # 最低的順子是 A(1)-2-3-4-5。 起始點是 1。 i+n-1 = 1+5-1 = 5。
        # 所以 i 的範圍可以是 1 到 10。 (共10種可能的順子起點)
        for i in range(1, 15 - n + 1 + 1): # 這樣寫法不對
                                        # 應該是 range(1, 11) for 5-card straight (A to T starts)
                                        # 如果是 A(14), 則 i 最大是 14-n+1
            
            # 書中原文的迴圈是 range(1, 15)，然後內部判斷連續性
            # 這樣比較通用，即使 n 不是 5
            consecutive_count = 0
            for rank_to_check in range(i, i + n): # 檢查從 i 開始的 n 個連續點數
                # 特殊處理：如果 rank_to_check 是 1 (A)，但手牌中只有 rank 14 (大A)
                # 我們在前面已經把 rank 14 的計數加到 rank 1 了 (如果 rank_counts 這樣處理的話)
                # 或者，更簡單的方式是，如果檢查到 rank_to_check = 1, 並且 rank_counts 中沒有 1 但有 14，
                # 則視為有 rank 1。
                # 我們的 Card rank 是 2-14。get_rank_counts() 的鍵也是 2-14。
                # 所以我們需要一個映射，或者在檢查 A2345 時特殊處理。

                # 簡化邏輯：建立一個包含所有手牌點數的集合 (去重)
                # 並加入 A(1) 如果手牌中有 A(14)
                unique_ranks_in_hand = set(rank_counts.keys())
                if 14 in unique_ranks_in_hand: # 如果有大A
                    unique_ranks_in_hand.add(1) # 也加入小A

                # 現在檢查從 i 開始的 n 個連續點數是否存在於 unique_ranks_in_hand
                is_current_straight = True
                for j in range(n): # 檢查 rank i, i+1, ..., i+n-1
                    if (i+j) not in unique_ranks_in_hand:
                        is_current_straight = False
                        break
                if is_current_straight:
                    return True # 找到了 n 張連續的順子

            # 這裡的 i 是順子的最低點數。
            # A2345 -> i=1
            # ...
            # TJQKA -> i=10
            # 所以 i 的範圍是 1 到 10 (包含10)
            # 結束條件是 i+n-1 <= 14 (A最大為14) => i <= 14-n+1
            if i > (14 - n + 1): # 如果最低點數太高，不可能形成n張順子了
                 break
        return False # 遍歷完所有可能的起點都沒找到順子


# `good_hand_flush_test` (梅花10,J,Q,K,A) 之前建立的，它也包含一個順子。
# 如果我們用 `get_rank_counts`，可以確認它在五個連續的點數上至少各有一張牌。
print(f"\n--- 撲克牌型練習：順子 (Straight) ---")
print(f"good_hand_flush_test 的點數計數: {good_hand_flush_test.get_rank_counts()}")

# 所以 `has_straight` 應該回傳 `True`。

print(f"good_hand_flush_test.has_straight(): {good_hand_flush_test.has_straight()}")

# `bad_hand_flush_test` (梅花2,3,7, 紅心4, 黑桃5) 不包含順子，
# 所以 `has_straight` 應該回傳 `False`。
print(f"bad_hand_flush_test 的點數計數: {bad_hand_flush_test.get_rank_counts()}")
print(f"bad_hand_flush_test.has_straight(): {bad_hand_flush_test.has_straight()}")

# ### 練習
#
# 如果一手牌同時是順子也是同花 —— 也就是五張相同花色且點數連續的牌 ——
# 那麼這手牌就有同花順 (straight flush)。
# 編寫一個 `PokerHand` 的方法來檢查一手牌是否有同花順。

# 你可以用下面的大綱開始。

# %%add_method_to PokerHand
#     def has_straightflush(self):
#         """檢查這手牌是否有同花順。"""
#         return False # 預留位置

# %%add_method_to PokerHand
# 書中提供了一個 partition 方法來輔助
# 我們先把它加到 PokerHand
class PokerHand(Hand): # 重新定義以加入新方法
    """表示一手撲克牌。"""
    def get_suit_counts(self):
        sc = {};
        for c in self.cards: sc[c.suit] = sc.get(c.suit, 0) + 1
        return sc
    def get_rank_counts(self):
        rc = {};
        for c in self.cards: rc[c.rank] = rc.get(c.rank, 0) + 1
        return rc
    def has_flush(self):
        sc = self.get_suit_counts();
        for v in sc.values():
            if v >= 5: return True
        return False
    def has_straight(self, n=5):
        rank_counts = self.get_rank_counts()
        unique_ranks = set(rank_counts.keys())
        if 14 in unique_ranks: unique_ranks.add(1)
        for i in range(1, 14 - n + 2): # A to 10 start
            is_straight = True
            for j in range(n):
                if (i+j) not in unique_ranks:
                    is_straight = False; break
            if is_straight: return True
        return False

    def partition(self):
        """將手牌按花色分成四手牌 (PokerHand 物件) 的列表。"""
        hands_by_suit = []
        for i_suit_part in range(4): # 0 到 3 代表四種花色
            # 為每種花色建立一個空的 PokerHand
            # 需要給 PokerHand 的 __init__ 一個 label (如果它需要的話)
            # Hand 的 __init__ 有 label='' 預設值
            hands_by_suit.append(PokerHand(label=f'Suit {Card.suit_names[i_suit_part]}'))

        for card_part in self.cards:
            hands_by_suit[card_part.suit].put_card(card_part) # 把牌加到對應花色的手牌中

        return hands_by_suit

# %%add_method_to PokerHand
# 現在加入 has_straightflush
    def has_straightflush(self):
        """檢查這手牌是否有同花順。"""
        # 策略：先把手牌按花色分開。
        # 對於每種花色的子手牌，如果該子手牌張數 >= 5，
        # 就檢查該子手牌是否構成順子。
        hands_partitioned_by_suit = self.partition()
        for single_suit_hand in hands_partitioned_by_suit:
            # PokerHand 的 has_flush 檢查的是否 >= 5 張同花
            # PokerHand 的 has_straight 檢查的是否有點數連續的5張牌
            # 如果一個 single_suit_hand (它本身所有牌都同花)
            # 同時張數 >= 5 並且它又構成一個順子，那麼它就是同花順。
            if len(single_suit_hand.cards) >= 5 and single_suit_hand.has_straight(n=5):
                return True
        return False


# 使用下面的例子來測試你的方法。
print(f"\n--- 撲克牌型練習：同花順 (Straight Flush) ---")
# good_hand_flush_test (梅花10,J,Q,K,A) 是同花順
print(f"good_hand_flush_test (梅花10-A) is straight flush: {good_hand_flush_test.has_straightflush()}") # True

# bad_hand_flush_test 不是同花順
print(f"bad_hand_flush_test is straight flush: {bad_hand_flush_test.has_straightflush()}") # False

# 注意，僅僅檢查一手牌是否有順子 *且* 有同花是不夠的。
# 要了解原因，考慮下面這手牌。
from copy import deepcopy # 用於複製物件

straight_and_flush_not_sf = deepcopy(bad_hand_flush_test) # 從非同花牌開始
# bad_hand_flush_test: 梅花2,3,7, 紅心4, 黑桃5
# 加入 梅花6, 梅花9
straight_and_flush_not_sf.put_card(Card(0, 6)) # 梅花6
straight_and_flush_not_sf.put_card(Card(0, 9)) # 梅花9
# 現在手牌是: 梅花2,3,6,7,9, 紅心4, 黑桃5 (共7張)
# 同花部分：梅花2,3,6,7,9 (5張梅花，是同花)
# 順子部分：2,3,4,5,6 (梅花2, 梅花3, 紅心4, 黑桃5, 梅花6，是順子)
# 但這兩組牌不完全相同，所以不是同花順
print("\n一手牌，有同花也有順子，但不是同花順:")
print(straight_and_flush_not_sf)


# 這手牌包含一個順子和一個同花，但它們不是同一組五張牌。
print(f"  它有順子嗎? {straight_and_flush_not_sf.has_straight()}")   # True (2-3-4-5-6)
print(f"  它有同花嗎? {straight_and_flush_not_sf.has_flush()}")     # True (5張梅花)


# 所以它不包含同花順。
print(f"  它有同花順嗎? {straight_and_flush_not_sf.has_straightflush()}") # False

# ### 練習
#
# 如果一手撲克牌包含兩張或更多相同點數的牌，則稱為有一對 (pair)。
# 編寫一個 `PokerHand` 的方法來檢查一手牌是否包含一對。
# (書中接下來介紹的 check_sets 是更通用的方法，可以檢查對子、三條、四條、葫蘆等)

# 你可以用下面的大綱開始。
# (check_sets 方法是書中為了這個和下個練習引入的輔助方法)

# %%add_method_to PokerHand
#     def check_sets(self, *need_list_args): # *need_list_args 會收集參數成元組
#         # need_list_args 是一個期望的點數出現次數列表，按降序排列
#         # 例如，葫蘆 (3帶2) 是 (3, 2)
#         # 四條是 (4, 1) 或 (4)
#         # 對子是 (2, 1, 1, 1) 或 (2)
#         return True # 預留位置

# %%add_method_to PokerHand
# 再次重新定義 PokerHand 以加入 check_sets 和 has_pair
class PokerHand(Hand):
    """表示一手撲克牌。"""
    def get_suit_counts(self):
        sc={}; For c in self.cards: sc[c.suit]=sc.get(c.suit,0)+1; return sc
    def get_rank_counts(self):
        rc={}; For c in self.cards: rc[c.rank]=rc.get(c.rank,0)+1; return rc
    def has_flush(self):
        sc=self.get_suit_counts(); For v in sc.values(): if v>=5: return True; return False
    def has_straight(self, n=5):
        rc=self.get_rank_counts(); ur=set(rc.keys()); If 14 in ur: ur.add(1)
        For i in range(1,14-n+2):
            iss=True; For j in range(n): if(i+j)not in ur: iss=False;break
            If iss:return True
        return False
    def partition(self):
        h=[PokerHand(f'S{Card.suit_names[i]}')for i in range(4)]; For c in self.cards:h[c.suit].put_card(c)
        return h
    def has_straightflush(self):
        For h in self.partition(): if len(h.cards)>=5 and h.has_straight(5):return True
        return False

    def check_sets(self, *needed_counts_tuple): # e.g., (3,2) for full house, (2,) for a pair
        """檢查手牌中點數的組合是否符合 needed_counts_tuple 的要求。
        needed_counts_tuple: 一個元組，包含期望的相同點數牌的數量，按降序。
                             例如，葫蘆是 (3, 2)，一對是 (2,)。
        """
        rank_counts_dict = self.get_rank_counts() # {'rank_code': count, ...}
        # 取得所有點數的出現次數，並按降序排序
        # 例如，如果手牌是 AA KK Q -> ranks_counts.values() = [2, 2, 1] (順序不定)
        # sorted_actual_counts = [2, 2, 1]
        sorted_actual_counts = sorted(rank_counts_dict.values(), reverse=True)

        # 比較期望的組合和實際的組合
        # 例如，檢查葫蘆 (3,2)：
        #   如果 needed_counts_tuple 是 (3,2)
        #   如果 sorted_actual_counts 是 [3,2,...] 或 [3,2] -> True
        #   如果 sorted_actual_counts 是 [3,1,1] -> False (因為 2 > 1)
        #   如果 sorted_actual_counts 是 [2,2,1] -> False (因為 3 > 2)

        # zip 會在最短的序列結束時停止
        # 如果 needed_counts_tuple 比 sorted_actual_counts 長，表示牌不夠形成期望組合
        if len(needed_counts_tuple) > len(sorted_actual_counts):
            # 例如，期望 (2,2) (兩對)，但手上只有 AA K Q J (counts [2,1,1,1])
            # zip 只會比較第一對 (2,2)。但這其實不對。
            # 我們應該確保 sorted_actual_counts 至少能滿足 needed_counts_tuple 的所有要求。
            # 例如，要 (3,2)，那麼 sorted_actual_counts 的第一個元素必須 >=3，第二個必須 >=2。

            # 更好的邏輯：
            for i_check_sets in range(len(needed_counts_tuple)):
                needed = needed_counts_tuple[i_check_sets]
                # 檢查實際計數列表是否足夠長
                if i_check_sets >= len(sorted_actual_counts):
                    return False # 實際的組合不夠形成期望的組合 (例如期望兩對，但只有一對)
                have = sorted_actual_counts[i_check_sets]
                if needed > have: # 如果期望的數量大於實際擁有的最大數量
                    return False # 就不滿足條件
            return True # 所有期望的組合都滿足了

        # 書中原文的 zip 邏輯，假設 needed_counts_tuple 的長度 <= sorted_actual_counts 的長度
        # for needed, have_actual in zip(needed_counts_tuple, sorted_actual_counts):
        #     if needed > have_actual: # 如果需要的比擁有的多
        #         return False
        # return True # 如果迴圈跑完都沒返回 False，表示滿足條件

# %%add_method_to PokerHand
# 現在加入 has_pair
    def has_pair(self):
        """檢查手牌是否至少有一對。"""
        # 一對意味著點數計數中至少有一個值 >= 2。
        # 用 check_sets: 期望至少有一個計數是 2。
        return self.check_sets(2) # 傳遞 (2,) 表示我們需要至少一個2張同點的組合

# 為了測試你的方法，這裡有一手有一對的牌。
print(f"\n--- 撲克牌型練習：一對 (Pair) ---")
pair_test_hand = deepcopy(bad_hand_flush_test) # 從非同花牌開始 (梅花2,3,7, 紅心4, 黑桃5)
pair_test_hand.put_card(Card(1, 2)) # 加入一張方塊2，現在有兩張2 (梅花2, 方塊2)
print("有一對的牌 (pair_test_hand):")
print(pair_test_hand)
print(f"  點數計數: {pair_test_hand.get_rank_counts()}")


print(f"pair_test_hand.has_pair(): {pair_test_hand.has_pair()}")    # True

print(f"bad_hand_flush_test.has_pair(): {bad_hand_flush_test.has_pair()}")    # False

print(f"good_hand_flush_test.has_pair(): {good_hand_flush_test.has_pair()}")   # False (它是同花順，沒有對子)

# ### 練習
#
# 如果一手牌包含三張同點數的牌和另外兩張同點數的牌，則稱為葫蘆 (full house)。
# (例如 AAA KK)
# 編寫一個 `PokerHand` 的方法來檢查一手牌是否有葫蘆。

# 你可以用下面的大綱開始。

# %%add_method_to PokerHand
#     def has_full_house(self):
#         return False # 預留位置

# 直接在 PokerHand 中定義 has_full_house
class PokerHand(Hand): # 包含所有前面定義的方法
    """表示一手撲克牌。"""
    def get_suit_counts(self): sc={}; For c in self.cards: sc[c.suit]=sc.get(c.suit,0)+1; return sc
    def get_rank_counts(self): rc={}; For c in self.cards: rc[c.rank]=rc.get(c.rank,0)+1; return rc
    def has_flush(self): sc=self.get_suit_counts(); For v in sc.values(): if v>=5: return True; return False
    def has_straight(self, n=5):
        rc=self.get_rank_counts(); ur=set(rc.keys()); If 14 in ur: ur.add(1)
        For i in range(1,15-n+1): # A to (14-n+1)
            iss=True; For j in range(n): if(i+j)not in ur: iss=False;break
            If iss:return True
        return False
    def partition(self):
        h=[PokerHand(f'S{Card.suit_names[i]}')for i in range(4)]; For c in self.cards:h[c.suit].put_card(c)
        return h
    def has_straightflush(self):
        For h_sf in self.partition(): if len(h_sf.cards)>=5 and h_sf.has_straight(5):return True
        return False
    def check_sets(self, *needed_counts_tuple):
        rc_dict = self.get_rank_counts(); sorted_actual_counts = sorted(rc_dict.values(), reverse=True)
        For i_cs in range(len(needed_counts_tuple)):
            needed = needed_counts_tuple[i_cs]
            If i_cs >= len(sorted_actual_counts): return False
            have = sorted_actual_counts[i_cs]
            If needed > have: return False
        return True
    def has_pair(self): return self.check_sets(2)

    def has_full_house(self):
        """檢查手牌是否有葫蘆 (三條帶一對)。"""
        # 葫蘆需要一個三條和一個對子。
        # 所以點數計數的值中，最大的應該是3，第二大的應該是2。
        return self.check_sets(3, 2) # 期望的計數組合是 (3, 2)


# 你可以用這手牌來測試你的方法。
print(f"\n--- 撲克牌型練習：葫蘆 (Full House) ---")
# pair_test_hand 有一對2 (梅花2, 方塊2) 和單張 梅花3, 紅心4, 黑桃5, 梅花7
boat_test_hand = deepcopy(pair_test_hand) # 從有一對2的牌開始
# 加入 第三張2 (例如紅心2) -> 形成三條2
boat_test_hand.put_card(Card(2, 2)) # 紅心2
# 加入 第二張3 (例如方塊3) -> 形成一對3
boat_test_hand.put_card(Card(1, 3)) # 方塊3
# 現在手牌應該是：(梅花2, 方塊2, 紅心2), (梅花3, 方塊3), 紅心4, 黑桃5, 梅花7 (共8張)
# 葫蘆是 22233
print("葫蘆測試牌 (boat_test_hand):")
print(boat_test_hand)
print(f"  點數計數: {boat_test_hand.get_rank_counts()}")


print(f"boat_test_hand.has_full_house(): {boat_test_hand.has_full_house()}")     # True

print(f"pair_test_hand.has_full_house(): {pair_test_hand.has_full_house()}")     # False (只有一對)

print(f"good_hand_flush_test.has_full_house(): {good_hand_flush_test.has_full_house()}") # False (是同花順)

# ### 練習
#
# 這個練習是一個關於一個常見且難以除錯的錯誤的警示故事。
# 考慮下面的類別定義。

class Kangaroo: # 袋鼠
    """袋鼠是一種有袋動物。"""

    def __init__(self, name_k, contents_k=[]): # 參數改名，contents_k 的預設值是個列表
        """初始化育兒袋的內容。

        name_k: 字串，袋鼠的名字
        contents_k: 初始的育兒袋內容列表。
        """
        # 警告：使用可變物件 (如列表) 作為預設參數值通常是個壞主意！
        # 因為預設值只在函數定義時建立一次。
        # 所有不提供 contents_k 參數的 Kangaroo 實體都會共享同一個預設列表。
        self.name = name_k
        self.contents = contents_k # contents 指向傳入的列表，或預設的那個共享列表

    def __str__(self):
        """回傳此袋鼠的字串表示法。"""
        lines_k_str = [ self.name + ' 的育兒袋內容有:' ]
        for obj_in_pouch in self.contents:
            # object.__str__(obj) 可以取得任何物件的預設字串表示法 (通常是 <類別名 object at 記憶體位址>)
            # 如果 obj_in_pouch 本身有 __str__，那樣會更好。
            # 為了與書中一致，我們先用 object.__str__
            # s_item_str = '    ' + object.__str__(obj_in_pouch)
            # 或者，如果我們想看到物件本身的字串 (如果它有__str__)：
            s_item_str = '    ' + str(obj_in_pouch)
            lines_k_str.append(s_item_str)
        return '\n'.join(lines_k_str)

    def put_in_pouch(self, item_to_put):
        """將一個新物品加入到育兒袋內容中。

        item_to_put: 要加入的物件
        """
        self.contents.append(item_to_put) # 直接修改 self.contents 列表

# `__init__` 接收兩個參數：`name_k` 是必要的，但 `contents_k` 是選擇性的
# —— 如果沒有提供，預設值是一個空列表。
#
# `__str__` 回傳一個物件的字串表示法，包含名字和育兒袋的內容。
#
# `put_in_pouch` 接收任何物件並將其附加到 `contents_k`。
#
# 現在讓我們看看這個類別如何運作。
# 我們建立兩個 `Kangaroo` 物件，名字分別是 `'Kanga'` 和 `'Roo'`。
# (Kanga 和 Roo 是小熊維尼故事中的袋鼠母子)

print(f"\n--- 袋鼠育兒袋問題 ---")
kanga = Kangaroo('Kanga') # 沒有提供 contents，所以 kanga.contents 會是預設的那個列表
roo = Kangaroo('Roo')   # roo.contents 也會是同一個預設列表！

# 我們在 Kanga 的育兒袋裡放兩個字串和 Roo。

kanga.put_in_pouch('錢包')
kanga.put_in_pouch('車鑰匙')
kanga.put_in_pouch(roo) # 把 roo 物件本身放進 kanga 的袋子

# 如果我們印出 `kanga`，看起來一切都運作正常。

print("Kanga 的狀態:")
print(kanga)

# 但是如果我們印出 `roo` 會發生什麼事呢？

print("\nRoo 的狀態 (問題所在！):")
print(roo)

# Roo 的育兒袋包含了和 Kanga 相同的內容，包括一個對 `roo` 自身的參照！
#
# 看看你是否能找出問題所在。
# (提示：問題出在 `__init__` 方法中 `contents_k=[]` 這個預設參數。)
# 然後問問虛擬助理：「下面這個程式有什麼問題？」並貼上 `Kangaroo` 的定義。
#
# 解釋：
# 當 `__init__` 方法的 `contents_k` 參數使用預設值 `[]` 時，
# 這個空列表 `[]` 只在函數 *定義* 時被建立一次。
# 所有後續呼叫 `Kangaroo()` (不傳遞 `contents_k` 參數) 時，
# `self.contents` 都會指向 *同一個* 在函數定義時建立的列表物件。
# 因此，當 `kanga.put_in_pouch(...)` 修改 `kanga.contents` 時，
# 它實際上修改了那個共享的列表。
# 因為 `roo` 在建立時也使用了這個共享的預設列表作為 `roo.contents`，
# 所以 `roo.contents` 也會反映出這些改變。
#
# 正確的做法是在 `__init__` 內部，如果 `contents_k` 是預設值 (或 None)，
# 則將 `self.contents` 初始化為一個 *新的* 空列表。例如：
#
# class Kangaroo_Fixed:
#     def __init__(self, name_k, contents_k=None): # 預設值改為 None
#         self.name = name_k
#         if contents_k is None:
#             self.contents = [] # 如果是預設，建立一個新的空列表
#         else:
#             self.contents = list(contents_k) # 或者建立傳入列表的一個副本，以防外部修改
#     ... (其他方法不變) ...

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

(這個 cell 在原始 .py 中是空的)
(這個 cell 在原始 .py 中是參考連結)