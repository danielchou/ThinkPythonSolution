# 從 chap13.ipynb 轉換而來
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

# 來源：照片從 [Lorem Picsum](https://picsum.photos/) 下載，這是一個提供佔位圖片的服務。
# 這個名字參考了 "lorem ipsum"，這是一種用於佔位文字的名稱。
# (譯註：Lorem ipsum 是一段常用於排版和設計領域的拉丁文無意義填充文字。)

# 這個儲存格會下載一個壓縮檔，裡面包含了我們在本章範例中會用到的檔案。

download('https://github.com/AllenDowney/ThinkPython/raw/v3/photos.zip');

# 警告：如果 photos/ 目錄已經存在，這個儲存格會移除它。
# photos/ 目錄中已有的任何檔案都將被刪除。

# !rm -rf photos/ # Linux/macOS 移除目錄指令，Windows 用 !rd /s /q photos

# 解壓縮 photos.zip，-o 選項表示如果檔案已存在則覆寫
# (Windows 上可能需要安裝 unzip 工具或使用其他解壓縮指令)
try:
    import subprocess
    # 檢查 unzip 是否可用
    try:
        subprocess.run(['unzip', '-h'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if exists('photos.zip'):
            !unzip -o photos.zip
            print("photos.zip 已解壓縮。")
        else:
            print("錯誤: photos.zip 未下載。")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("警告: 'unzip' 指令未找到或無法執行。請手動解壓縮 photos.zip 到目前目錄。")
        print("如果 photos 目錄已存在且包含正確內容，可以忽略此警告。")
        if not exists('photos'):
             print("錯誤: photos 目錄不存在，練習可能無法正常執行。")

except ImportError:
    print("警告: subprocess 模組無法匯入，無法自動檢查 unzip。請手動解壓縮 photos.zip。")


# # 檔案與資料庫 (Files and Databases)
#
# 到目前為止，我們看到的大部分程式都是 **短暫的 (ephemeral)**，意思是它們執行一小段時間並產生輸出，
# 但當它們結束時，它們的資料就消失了。
# 每次你執行一個短暫的程式，它都是從一個全新的狀態開始。
#
# 其他程式則是 **持久的 (persistent)**：它們會長時間 (或一直) 執行；
# 它們至少會把一部分資料保存在長期儲存空間中；而且如果它們關閉並重新啟動，它們會從上次離開的地方繼續。
#
# 程式維護資料的一個簡單方法是讀取和寫入文字檔。
# 一個更通用的替代方案是把資料儲存在資料庫中。
# 資料庫是特製的檔案，可以比文字檔更有效地讀取和寫入，並且它們提供了額外的功能。
#
# 在這一章，我們會寫一些讀寫文字檔和資料庫的程式，
# 作為練習，你將會寫一個程式來搜尋照片集中的重複照片。
# 但在你處理檔案之前，你必須先找到它，所以我們先從檔案名稱、路徑和目錄開始。

# ## 檔案名稱和路徑 (Filenames and paths)
#
# 檔案被組織在 **目錄 (directories)** 中，也稱為「資料夾 (folders)」。
# 每個正在執行的程式都有一個 **目前工作目錄 (current working directory)**，
# 它是大多數操作的預設目錄。
# 例如，當你開啟一個檔案時，Python 會在目前工作目錄中尋找它。
#
# `os` 模組提供了處理檔案和目錄的函數 ("os" 代表 "operating system"，作業系統)。
# 它提供了一個叫做 `getcwd` 的函數，可以取得目前工作目錄的名稱。

# 這個儲存格用一個回傳假路徑的函數取代了 `os.getcwd`
# (這是為了讓書中的範例在任何環境下都能得到一致的輸出)
import os

original_getcwd = os.getcwd # 先保存原始的 getcwd

def fake_getcwd():
    # 在 Windows 上，路徑可能看起來像 'C:\\Users\\Dinsdale'
    # 為了跨平台一致性，我們用 POSIX 風格的路徑，並在後面解釋差異
    if os.name == 'nt': # 如果是 Windows
        return "C:\\Users\\dinsdale" # 範例 Windows 路徑
    else: # macOS 或 Linux
        return "/home/dinsdale" # 範例 Unix 路徑

os.getcwd = fake_getcwd # 用我們偽造的函數取代

# import os # 已在上面匯入

current_dir_example = os.getcwd()
print(f"模擬的目前工作目錄: {current_dir_example}")

# 這個例子中的結果是一個叫做 `dinsdale` 的使用者的家目錄。
# 像 `'/home/dinsdale'` (或 Windows 上的 `'C:\\Users\\dinsdale'`) 這樣識別檔案或目錄的字串稱為 **路徑 (path)**。
#
# 一個簡單的檔案名稱，像是 `'memo.txt'`，也被視為一個路徑，但它是一個 **相對路徑 (relative path)**，
# 因為它指定了一個相對於目前目錄的檔案名稱。
# 在這個例子中，如果目前目錄是 `/home/dinsdale`，那麼 `'memo.txt'` 就等同於完整路徑 `'/home/dinsdale/memo.txt'`。
#
# 一個以 `/` (在 Unix/macOS 上) 或磁碟機代號 (如 `C:\` 在 Windows 上) 開頭的路徑不依賴於目前目錄 —— 它稱為 **絕對路徑 (absolute path)**。
# 要找到一個檔案的絕對路徑，你可以用 `os.path.abspath`。

# os.path.abspath 會根據「真實的」目前工作目錄來解析
# 為了讓範例一致，我們需要模擬它
# os.getcwd = original_getcwd # 暫時恢復真實的 getcwd 來測試 abspath
# print(f"os.path.abspath('memo.txt') (真實): {os.path.abspath('memo.txt')}")
# os.getcwd = fake_getcwd # 再換回偽造的

# 模擬 abspath 的行為
def fake_abspath(relative_path):
    # 簡單的模擬，只處理檔名
    current_fake_dir = os.getcwd()
    return os.path.join(current_fake_dir, relative_path)

print(f"os.path.abspath('memo.txt') (模擬): {fake_abspath('memo.txt')}")


# `os` 模組還提供了其他處理檔案名稱和路徑的函數。
# `listdir` 會回傳給定目錄內容的列表，包括檔案和其他目錄。
# 這裡有一個例子，列出一個叫做 `photos` 的目錄的內容。
# (為了執行這個，我們需要 photos 目錄真的存在於執行此 notebook 的地方)

# 確保 photos 目錄存在且有內容，以便 listdir 運作
# (在 In[5] 的 unzip 應該已經建立了它)
if exists('photos'):
    print(f"目錄 'photos' 的內容: {os.listdir('photos')}")
else:
    print("錯誤: 'photos' 目錄未找到。listdir 範例無法執行。")

# 這個目錄包含一個叫做 `notes.txt` 的文字檔和三個目錄。
# 這些目錄包含 JPEG 格式的圖片檔案。

photos_jan_path = os.path.join('photos', 'jan-2023')
if exists(photos_jan_path) and os.path.isdir(photos_jan_path):
    print(f"目錄 '{photos_jan_path}' 的內容: {os.listdir(photos_jan_path)}")
else:
    print(f"錯誤: '{photos_jan_path}' 目錄未找到或不是目錄。")

# 要檢查一個檔案或目錄是否存在，我們可以用 `os.path.exists`。

print(f"os.path.exists('photos'): {os.path.exists('photos')}")

photos_apr_path = os.path.join('photos', 'apr-2023') # apr-2023 可能不存在於 zip 中
print(f"os.path.exists('{photos_apr_path}'): {os.path.exists(photos_apr_path)}")

# 要檢查一個路徑是否指向一個目錄，我們可以用 `isdir`，如果路徑指向目錄它會回傳 `True`。

print(f"os.path.isdir('photos'): {os.path.isdir('photos')}")

# 而 `isfile` 如果路徑指向一個檔案，則回傳 `True`。

photos_notes_path = os.path.join('photos', 'notes.txt')
print(f"os.path.isfile('{photos_notes_path}'): {os.path.isfile(photos_notes_path)}")

# 處理路徑的一個挑戰是它們在不同作業系統上看起來不一樣。
# 在 macOS 和像 Linux 這樣的 UNIX 系統上，路徑中的目錄和檔案名稱是用正斜線 `/` 分隔的。
# Windows 使用反斜線 `\`。
# 所以，如果你在 Windows 上執行這些範例，你會在路徑中看到反斜線，
# 並且你需要在範例中把正斜線換掉。
#
# 或者，為了寫出能在兩種系統上運作的程式碼，你可以使用 `os.path.join`，
# 它會根據你使用的作業系統，使用正斜線或反斜線來把目錄和檔案名稱組合成路徑。

joined_path = os.path.join('photos', 'jan-2023', 'photo1.jpg')
print(f"os.path.join(...) 的結果: {joined_path}")
# 這個函數會自動使用目前作業系統正確的分隔符。

# 本章稍後我們會用這些函數來搜尋一組目錄並找出所有的圖片檔案。

# ## f-字串 (f-strings)
#
# 程式儲存資料的一種方法是把它寫到文字檔中。
# 例如，假設你是一個駱駝觀察員，你想記錄在一段觀察期間內看到的駱駝數量。
# 假設在一年半的時間裡，你看到了 `23` 隻駱駝。
# 你的駱駝觀察手冊中的資料可能看起來像這樣。

num_years = 1.5
num_camels = 23

# 要把這些資料寫到檔案裡，你可以使用我們在第八章看過的 `write` 方法。
# `write` 的參數必須是一個字串，所以如果我們想把其他值放到檔案裡，
# 我們必須把它們轉換成字串。最簡單的方法是使用內建函數 `str()`。
#
# 這是它的樣子：

try:
    writer_camel = open('camel-spotting-book.txt', 'w', encoding='utf-8')
    writer_camel.write(str(num_years))
    writer_camel.write(str(num_camels)) # 這樣會把兩個數字黏在一起
    writer_camel.close()
    print("camel-spotting-book.txt (初步寫入) 已建立。")
except IOError:
    print("錯誤: 無法寫入 camel-spotting-book.txt。")

# 那樣可行，但 `write` 不會加上空白或換行符，除非你明確地包含它們。
# 如果我們把檔案讀回來，會看到兩個數字黏在一起了。

try:
    content_camel_initial = open('camel-spotting-book.txt', 'r', encoding='utf-8').read()
    print(f"camel-spotting-book.txt (初步讀取) 的內容: '{content_camel_initial}'")
except FileNotFoundError:
    print("錯誤: camel-spotting-book.txt 未找到。")


# 至少，我們應該在數字之間加上空白。
# 順便一提，我們也來加一些說明文字吧。
#
# 要寫入字串和其他值的組合，我們可以用 **f-字串 (f-string)**，
# 它是一個在開頭引號前有字母 `f` 的字串，並且包含一個或多個用大括號包起來的 Python 表達式。
# 下面的 f-字串包含一個表達式，它是一個變數名稱。

f_string_example1 = f'我已經看到了 {num_camels} 隻駱駝'
print(f_string_example1)

# 結果是一個字串，其中表達式已經被評估並替換成結果了。
# 可以有多個表達式。

f_string_example2 = f'在 {num_years} 年裡，我已經看到了 {num_camels} 隻駱駝'
print(f_string_example2)

# 表達式也可以包含運算子和函數呼叫。

line_f_string = f'在 {round(num_years * 12)} 個月裡，我已經看到了 {num_camels} 隻駱駝'
print(line_f_string)

# 所以我們可以像這樣把資料寫到文字檔裡。

try:
    writer_camel_fstring = open('camel-spotting-book.txt', 'w', encoding='utf-8') # 'w' 會覆寫
    writer_camel_fstring.write(f'觀察年數: {num_years}\n') # \n 是換行符號
    writer_camel_fstring.write(f'看到的駱駝數: {num_camels}\n')
    writer_camel_fstring.close()
    print("camel-spotting-book.txt (使用 f-string 更新) 已寫入。")
except IOError:
    print("錯誤: 無法寫入 camel-spotting-book.txt。")

# 兩個 f-字串都以序列 `\n` 結尾，它會加入一個換行字元。
#
# 我們可以像這樣把檔案讀回來：

try:
    data_camel_fstring = open('camel-spotting-book.txt', 'r', encoding='utf-8').read()
    print("\n--- camel-spotting-book.txt (f-string 版本) ---")
    print(data_camel_fstring)
except FileNotFoundError:
    print("錯誤: camel-spotting-book.txt 未找到。")

# 在 f-字串中，大括號裡的表達式會被轉換成字串，所以你可以包含列表、字典和其他型別。

t_list_f = [1, 2, 3]
d_dict_f = {'one': 1}
f_string_with_ds = f'這裡有一個列表 {t_list_f} 和一個字典 {d_dict_f}'
print(f_string_with_ds)

# 如果 f-字串包含無效的表達式，結果會是錯誤。

%%expect TypeError
# f_string_error = f'這不是一個有效的表達式 {t_list_f + 2}' # 不能列表加整數

# ## YAML
#
# 程式讀寫檔案的原因之一是儲存 **設定資料 (configuration data)**，
# 這些資訊指定了程式應該做什麼以及如何做。
#
# 例如，在一個搜尋重複照片的程式中，我們可能有一個叫做 `config` 的字典，
# 它包含了要搜尋的目錄名稱、應該儲存結果的另一個目錄名稱，
# 以及它應該用來識別圖片檔案的副檔名列表。
#
# 它可能看起來像這樣：

config = {
    'photo_dir': 'photos', # 照片存放目錄
    'data_dir': 'photo_info', # 處理後的資料存放目錄
    'extensions': ['jpg', 'jpeg'], # 要處理的圖片副檔名
}
print(f"設定字典 config: {config}")

# 要把這些資料寫到文字檔裡，我們可以用上一節的 f-字串。
# 但使用一個專門為此設計的 `yaml` 模組會更容易。
#
# `yaml` 模組提供了處理 YAML 檔案的函數，YAML 檔案是一種文字檔格式，
# 設計成讓人類 *和* 程式都容易讀寫。
#
# 這裡有一個例子，使用 `dump` 函數把 `config` 字典寫到一個 YAML 檔案中。

# 這個儲存格會安裝 pyyaml 套件，它提供了 yaml 模組
# (通常在 Jupyter 環境中，!pip install 會在目前的 kernel 中安裝)
try:
    import yaml
except ImportError:
    print("yaml 模組未找到，嘗試安裝 pyyaml...")
    try:
        import subprocess
        subprocess.run(['pip', 'install', 'pyyaml'], check=True)
        import yaml # 再次嘗試匯入
        print("pyyaml 已成功安裝並匯入。")
    except Exception as e:
        print(f"安裝 pyyaml 失敗: {e}")
        print("請手動安裝 'pyyaml' 套件 (例如：pip install pyyaml)。")
        yaml = None # 設為 None 以便後續檢查


# import yaml # 已在上面嘗試匯入

config_filename = 'config.yaml'
if yaml: # 確保 yaml 已成功匯入
    try:
        writer_yaml = open(config_filename, 'w', encoding='utf-8')
        yaml.dump(config, writer_yaml) # 把 config 字典的內容 dump 到檔案
        writer_yaml.close()
        print(f"{config_filename} 已寫入。")
    except IOError:
        print(f"錯誤: 無法寫入 {config_filename}。")
    except Exception as e:
        print(f"寫入 YAML 時發生其他錯誤: {e}")

else:
    print("yaml 模組無法使用，無法執行 YAML 範例。")


# 如果我們把檔案的內容讀回來，就可以看到 YAML 格式長什麼樣子。

readback_yaml_content = ""
if yaml and exists(config_filename):
    try:
        readback_yaml_content = open(config_filename, 'r', encoding='utf-8').read()
        print(f"\n--- {config_filename} 的內容 ---")
        print(readback_yaml_content)
    except FileNotFoundError:
        print(f"錯誤: {config_filename} 未找到。")
else:
    if not yaml: print("yaml 模組不可用。")
    if not exists(config_filename) and yaml: print(f"{config_filename} 不存在。")


# 現在，我們可以用 `safe_load` 來把 YAML 檔案讀回來。
# (safe_load 比 load 更安全，可以防止執行任意程式碼)

config_readback = None
if yaml and exists(config_filename):
    try:
        reader_yaml = open(config_filename, 'r', encoding='utf-8')
        config_readback = yaml.safe_load(reader_yaml)
        reader_yaml.close()
        print(f"從 YAML 檔案讀回的 config_readback: {config_readback}")
    except FileNotFoundError:
        print(f"錯誤: {config_filename} 未找到。")
    except Exception as e:
        print(f"讀取 YAML 時發生錯誤: {e}")
else:
    if not yaml: print("yaml 模組不可用。")
    if not exists(config_filename) and yaml: print(f"{config_filename} 不存在。")


# 結果是一個新的字典，它包含了與原始字典相同的資訊，但它不是同一個字典物件。

if config_readback is not None:
    print(f"config is config_readback: {config is config_readback}") # False，它們是不同的物件
else:
    print("config_readback 未成功載入。")


# 把像字典這樣的物件轉換成字串的過程叫做 **序列化 (serialization)**。
# 把字串轉換回物件的過程叫做 **反序列化 (deserialization)**。
# 如果你序列化然後再反序列化一個物件，結果應該與原始物件等值 (equivalent)。

# ## Shelve
#
# 到目前為止，我們都在讀寫文字檔 —— 現在我們來考慮資料庫。
# **資料庫 (database)** 是一個為了儲存資料而組織起來的檔案。
# 有些資料庫像表格一樣組織，有列 (row) 和欄 (column) 的資訊。
# 其他的則像字典一樣組織，從鍵對應到值；它們有時被稱為 **鍵值儲存 (key-value stores)**。
#
# `shelve` 模組提供了建立和更新稱為「shelf (架子)」的鍵值儲存的函數。
# 作為例子，我們會建立一個 shelf 來存放 `photos` 目錄中圖片的說明文字。
# 我們會用 `config` 字典來取得應該放置 shelf 的目錄名稱。

if config: # 確保 config 字典存在
    print(f"config['data_dir']: {config.get('data_dir', '未設定')}") # 使用 .get 避免 KeyError
else:
    print("config 字典未定義。")


# 我們可以用 `os.makedirs` 來建立這個目錄，如果它還不存在的話。
# `exist_ok=True` 表示如果目錄已存在，不要引發錯誤。

if config and config.get('data_dir'):
    try:
        os.makedirs(config['data_dir'], exist_ok=True)
        print(f"目錄 '{config['data_dir']}' 已確認/建立。")
    except OSError as e:
        print(f"建立目錄 '{config['data_dir']}' 失敗: {e}")
else:
    print("config['data_dir'] 未設定，無法建立目錄。")


# 並用 `os.path.join` 來建立一個路徑，包含目錄名稱和 shelf 檔案名稱 `captions`。

db_file_path = ""
if config and config.get('data_dir'):
    db_file_path = os.path.join(config['data_dir'], 'captions') # shelf 檔案基礎名稱
    print(f"Shelf 檔案路徑: {db_file_path}")
else:
    print("config['data_dir'] 未設定，無法組合 shelf 檔案路徑。")


# 現在我們可以用 `shelve.open` 來開啟 shelf 檔案。
# 參數 `'c'` 表示如果檔案不存在則應建立它 (create)。

import shelve

db_shelf = None
if db_file_path:
    try:
        # 'c': 如果不存在則建立；如果存在則開啟讀寫
        db_shelf = shelve.open(db_file_path, 'c')
        print(f"Shelf 物件 db_shelf: {db_shelf}")
    except Exception as e:
        print(f"開啟或建立 shelf '{db_file_path}' 失敗: {e}")
else:
    print("db_file_path 未設定，無法開啟 shelf。")


# 回傳值正式名稱是 `DbfilenameShelf` 物件，通俗地稱為 shelf 物件。
#
# shelf 物件在很多方面都像字典一樣運作。
# 例如，我們可以用方括號運算子來加入一個項目，它是一個從鍵到值的對應。

key_shelf_example = 'photos/jan-2023/photo1.jpg' # 假設這是圖片路徑
if db_shelf is not None:
    db_shelf[key_shelf_example] = '貓咪的鼻子' # 把鍵對應到一個說明文字
    print(f"已將 '{key_shelf_example}' 加入 shelf。")
else:
    print("db_shelf 未成功開啟。")


# 在這個例子中，鍵是圖片檔案的路徑，值是描述圖片的字串。
#
# 我們也用方括號運算子來查詢一個鍵並取得對應的值。

value_from_shelf = None
if db_shelf is not None and key_shelf_example in db_shelf:
    value_from_shelf = db_shelf[key_shelf_example]
print(f"從 shelf 查詢 '{key_shelf_example}' 得到的值: {value_from_shelf}")

# 如果你對一個已存在的鍵再次賦值，`shelve` 會取代舊的值。

if db_shelf is not None:
    db_shelf[key_shelf_example] = '貓咪鼻子的特寫'
    print(f"更新後，'{key_shelf_example}' 在 shelf 中的值: {db_shelf.get(key_shelf_example)}")


# 一些字典方法，像是 `keys()`、`values()` 和 `items()`，也適用於 shelf 物件。

if db_shelf is not None:
    print(f"Shelf 中的所有鍵: {list(db_shelf.keys())}")


if db_shelf is not None:
    print(f"Shelf 中的所有值: {list(db_shelf.values())}")


# 我們可以用 `in` 運算子來檢查一個鍵是否出現在 shelf 中。

if db_shelf is not None:
    print(f"'{key_shelf_example}' in db_shelf: {key_shelf_example in db_shelf}")


# 我們也可以用 `for` 陳述式來遍歷 shelf 中的鍵。

print("\n--- Shelf 中的所有鍵值對 ---")
if db_shelf is not None:
    for key_in_loop in db_shelf:
        print(f"{key_in_loop} : {db_shelf[key_in_loop]}")
else:
    print("db_shelf 未開啟。")


# 跟其他檔案一樣，當你用完資料庫後應該關閉它。

if db_shelf is not None:
    db_shelf.close()
    print("db_shelf 已關閉。")
    db_shelf = None # 標記為已關閉


# 現在如果我們列出資料目錄的內容，會看到兩個 (或多個) 檔案。
# (shelve 可能會根據後端產生不同數量的檔案，例如 .dat, .bak, .dir)

# 當你開啟一個 shelve 檔案時，可能會建立一個後綴為 `.bak` 的備份檔。
# 如果你多次執行這個 notebook，你可能會看到那個檔案被留下來。
# 這個儲存格移除它，這樣書中顯示的輸出才會正確。
# (這主要適用於特定的 shelve 後端和操作系統行為)
backup_file_to_remove = os.path.join(config.get('data_dir', 'photo_info'), 'captions.bak')
if exists(backup_file_to_remove):
    try:
        os.remove(backup_file_to_remove)
        print(f"已移除備份檔: {backup_file_to_remove}")
    except OSError as e:
        print(f"移除備份檔 {backup_file_to_remove} 失敗: {e}")


if config and config.get('data_dir') and os.path.exists(config['data_dir']):
    print(f"目錄 '{config['data_dir']}' 的內容: {os.listdir(config['data_dir'])}")
else:
    print(f"目錄 '{config.get('data_dir', 'photo_info')}' 不存在或未設定。")


# `captions.dat` (或類似名稱，取決於系統) 包含了我們剛才儲存的資料。
# `captions.dir` (或類似名稱) 包含了關於資料庫組織的資訊，使其存取更有效率。
# 後綴 `dir` 代表 "directory"，但它與我們一直在處理的包含檔案的目錄無關。
# (譯註：不同作業系統上 shelve 產生的檔案名稱和後綴可能略有不同，例如在 Windows 上可能是 .dat, .bak, .dir；在某些 Unix 系統上可能只有一個 .db 檔案。)

# ## 儲存資料結構 (Storing data structures)
#
# 在上一個例子中，shelf 中的鍵和值都是字串。
# 但我們也可以用 shelf 來存放像是列表和字典這樣的資料結構。
#
# 作為例子，讓我們重新看看[第十一章](section_exercise_11)練習中的相同字母異序詞 (anagram) 範例。
# (譯註：section_exercise_11 指的是書中對應章節的連結)
# 回想一下，我們建立了一個字典，它把一個排序後的字母字串對應到
# 可以用那些字母拼出的單字列表。
# 例如，鍵 `'opst'` 對應到列表 `['opts', 'post', 'pots', 'spot', 'stop', 'tops']`。
#
# 我們會用下面的函數來排序一個單字中的字母。

def sort_word(word_input_sw): # 參數改名
    return ''.join(sorted(word_input_sw))

# 這裡有一個例子。

word_example_sw = 'pots'
key_example_sw = sort_word(word_example_sw)
print(f"sort_word('{word_example_sw}'): {key_example_sw}")

# 現在我們開啟一個叫做 `anagram_map` 的 shelf。
# 參數 `'n'` 表示我們應該總是建立一個新的、空的 shelf，即使已存在同名 shelf。
# ('n' 表示 new database)

db_anagram = None
anagram_map_path = 'anagram_map' # shelf 檔案基礎名稱
try:
    db_anagram = shelve.open(anagram_map_path, 'n') # 'n' 會清除現有檔案 (如果存在)
    print(f"Shelf '{anagram_map_path}' 已開啟 (模式 'n')。")
except Exception as e:
    print(f"開啟 shelf '{anagram_map_path}' (模式 'n') 失敗: {e}")


# 現在我們可以像這樣在 shelf 中加入一個項目。

if db_anagram is not None:
    db_anagram[key_example_sw] = [word_example_sw] # 值是一個包含單字的列表
    print(f"'{key_example_sw}' 在 db_anagram 中的值: {db_anagram.get(key_example_sw)}")
else:
    print("db_anagram 未成功開啟。")


# 在這個項目中，鍵是一個字串，值是一個字串列表。
#
# 現在假設我們找到另一個包含相同字母的單字，像是 `tops`

word_example_sw2 = 'tops'
key_example_sw2 = sort_word(word_example_sw2)
print(f"sort_word('{word_example_sw2}'): {key_example_sw2}")

# 這個鍵和上一個例子中的鍵相同，所以我們想把第二個單字附加到同一個字串列表中。
# 如果 `db_anagram` 是一個普通的字典，我們會這樣做：

# db_anagram[key_example_sw2].append(word_example_sw2) # 錯誤的！直接修改取出的列表不會更新 shelf

# 但如果我們這樣做然後再查詢 shelf 中的鍵，它看起來並沒有被更新。

# 為了正確示範，我們先執行錯誤的做法 (如果 db_anagram 是字典，這樣是對的)
# 但因為它是 shelf，這樣不會永久保存。
if db_anagram is not None and key_example_sw2 in db_anagram:
    # temp_list = db_anagram[key_example_sw2] # 取出列表
    # temp_list.append(word_example_sw2)     # 修改列表 (這個修改只在記憶體中)
    # print(f"嘗試直接 append 後，shelf 中的值 (錯誤方式): {db_anagram[key_example_sw2]}")
    # 這裡應該還是只有 ['pots']
    pass # 跳過執行錯誤的程式碼，直接解釋


# 問題在這裡：當我們查詢鍵時，我們得到一個字串列表，
# 但如果我們修改這個字串列表，它不會影響 shelf 本身。
# (因為我們得到的是列表的一個副本，或者是一個無法直接回寫 shelf 的參照)
# 如果我們想更新 shelf，我們必須讀取舊的值，更新它，然後再把新的值寫回 shelf。

if db_anagram is not None and key_example_sw2 in db_anagram:
    anagram_list_from_shelf = db_anagram[key_example_sw2] # 1. 讀取舊值
    anagram_list_from_shelf.append(word_example_sw2)      # 2. 更新取出的列表
    db_anagram[key_example_sw2] = anagram_list_from_shelf # 3. 把更新後的列表寫回 shelf
    print(f"正確更新後，'{key_example_sw2}' 在 db_anagram 中的值: {db_anagram.get(key_example_sw2)}")


# 現在 shelf 中的值被更新了。

# (上面已經印出更新後的值了)

# 作為練習，你可以完成這個範例，讀取單字列表 (words.txt) 並將所有相同字母異序詞儲存在一個 shelf 中。

if db_anagram is not None:
    db_anagram.close()
    print(f"Shelf '{anagram_map_path}' 已關閉。")
    db_anagram = None


# ## 檢查等效檔案 (Checking for equivalent files)
#
# 現在讓我們回到本章的目標：搜尋包含相同資料的不同檔案。
# 一種檢查方法是讀取兩個檔案的內容並進行比較。
#
# 如果檔案包含圖片，我們必須以 `'rb'` 模式開啟它們，其中 `'r'` 表示我們要讀取內容，
# `'b'` 表示 **二進位模式 (binary mode)**。
# 在二進位模式下，內容不會被解讀為文字 —— 它們被視為一個位元組 (byte) 序列。
#
# 這裡有一個開啟和讀取圖片檔案的例子。
# (需要 'photos/jan-2023/photo1.jpg' 存在)

path1_img = os.path.join('photos', 'jan-2023', 'photo1.jpg')
data1_bytes = None
if exists(path1_img):
    try:
        with open(path1_img, 'rb') as f_img1: # 'rb' = read binary
            data1_bytes = f_img1.read()
        print(f"從 '{path1_img}' 讀取的資料型別: {type(data1_bytes)}")
        print(f"資料開頭 (前 20 bytes): {data1_bytes[:20] if data1_bytes else 'N/A'}")
    except IOError as e:
        print(f"讀取檔案 '{path1_img}' 失敗: {e}")
else:
    print(f"錯誤: 檔案 '{path1_img}' 未找到。")

# `read` 的結果是一個 `bytes` 物件 —— 如其名，它包含一個位元組序列。
#
# 一般來說，圖片檔案的內容不是人類可讀的。
# 但如果我們從第二個檔案讀取內容，我們可以用 `==` 運算子來比較。

path2_img = os.path.join('photos', 'jan-2023', 'photo2.jpg') # 假設這是不同的圖片
data2_bytes = None
are_files_same = False
if exists(path2_img) and data1_bytes is not None:
    try:
        with open(path2_img, 'rb') as f_img2:
            data2_bytes = f_img2.read()
        are_files_same = (data1_bytes == data2_bytes)
        print(f"'{path1_img}' 和 '{path2_img}' 的內容是否相同: {are_files_same}")
    except IOError as e:
        print(f"讀取檔案 '{path2_img}' 失敗: {e}")
else:
    if not exists(path2_img): print(f"錯誤: 檔案 '{path2_img}' 未找到。")
    if data1_bytes is None: print("data1_bytes 未成功讀取。")


# 這兩個檔案不相等 (除非它們真的是同一個檔案的副本)。
#
# 讓我們把目前為止的內容封裝到一個函數裡。

def same_contents(path1_func, path2_func):
    try:
        with open(path1_func, 'rb') as f1:
            data1_func = f1.read()
        with open(path2_func, 'rb') as f2:
            data2_func = f2.read()
        return data1_func == data2_func
    except FileNotFoundError:
        print(f"錯誤: 檔案 {path1_func} 或 {path2_func} 未找到。")
        return False
    except IOError as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return False

# 如果我們只有兩個檔案，這個函數是一個不錯的選擇。
# 但假設我們有大量的檔案，並且想知道是否有任何兩個檔案包含相同的資料。
# 比較每一對檔案效率會很低。
#
# 一個替代方案是使用 **雜湊函數 (hash function)**，它接收檔案內容並計算出一個
# **摘要 (digest)**，通常是一個很大的整數。
# 如果兩個檔案包含相同的資料，它們會有相同的摘要。
# 如果兩個檔案不同，它們幾乎總是會有不同的摘要。
# (雖然理論上可能發生碰撞，即不同內容產生相同摘要，但對於好的雜湊函數來說機率極低)
#
# `hashlib` 模組提供了幾種雜湊函數 —— 我們要用的是叫做 `md5` 的。
# 我們先用 `hashlib.md5()` 來建立一個 `HASH` 物件。

import hashlib

md5_hash_obj = hashlib.md5()
print(f"hashlib.md5() 建立的物件型別: {type(md5_hash_obj)}")

# `HASH` 物件提供了一個 `update` 方法，它接收檔案內容作為參數。

if data1_bytes is not None: # 確保 data1_bytes 已讀取
    md5_hash_obj.update(data1_bytes) # 用第一個圖片檔案的內容來更新雜湊物件
    print("md5_hash_obj 已用 data1_bytes 更新。")
else:
    print("data1_bytes 為空，無法更新 md5_hash_obj。")


# 現在我們可以用 `hexdigest()` 來取得摘要，它是一個表示十六進位整數的十六進位數字字串。

digest_hex = ""
if data1_bytes is not None: # 確保已更新
    digest_hex = md5_hash_obj.hexdigest()
print(f"data1_bytes 的 MD5 摘要 (十六進位): {digest_hex}")

# 下面的函數封裝了這些步驟。

def md5_digest(file_path_md5): # 參數改名
    try:
        with open(file_path_md5, 'rb') as f_md5:
            data_md5 = f_md5.read()
        md5_hash_func_obj = hashlib.md5()
        md5_hash_func_obj.update(data_md5)
        digest_hex_func = md5_hash_func_obj.hexdigest()
        return digest_hex_func
    except FileNotFoundError:
        print(f"錯誤: 檔案 {file_path_md5} 未找到，無法計算 MD5。")
        return None
    except IOError as e:
        print(f"讀取檔案 {file_path_md5} 時發生錯誤: {e}")
        return None

# 如果我們對不同檔案的內容進行雜湊，可以確認我們會得到不同的摘要。

filename2_md5_test = os.path.join('photos', 'feb-2023', 'photo2.jpg') # 假設這個檔案存在且不同
if exists(filename2_md5_test):
    digest_file2 = md5_digest(filename2_md5_test)
    print(f"'{filename2_md5_test}' 的 MD5 摘要: {digest_file2}")
    if digest_hex and digest_file2:
        print(f"兩個摘要是否相同: {digest_hex == digest_file2}")
else:
    print(f"錯誤: 檔案 '{filename2_md5_test}' 未找到，無法比較 MD5。")


# 現在我們幾乎擁有了找出等效檔案所需的一切。
# 最後一步是搜尋一個目錄並找出所有的圖片檔案。

# ## 遍歷目錄 (Walking directories)
#
# 下面的函數接收我們要搜尋的目錄作為參數。
# 它使用 `listdir` 來遍歷目錄的內容。
# 當它找到一個檔案時，它會印出其完整路徑。
# 當它找到一個目錄時，它會遞迴地呼叫自己來搜尋子目錄。

def walk(dirname_to_walk): # 參數改名
    if not os.path.exists(dirname_to_walk) or not os.path.isdir(dirname_to_walk):
        print(f"錯誤: '{dirname_to_walk}' 不是一個有效的目錄。")
        return

    for name_in_dir in os.listdir(dirname_to_walk):
        path_item = os.path.join(dirname_to_walk, name_in_dir)

        if os.path.isfile(path_item):
            print(path_item) # 如果是檔案，印出路徑
        elif os.path.isdir(path_item):
            walk(path_item) # 如果是目錄，遞迴呼叫 walk

# 我們可以這樣使用它：

print("\n--- 遍歷 'photos' 目錄 ---")
walk('photos') # 假設 photos 目錄存在

# 結果的順序取決於作業系統的細節。

# ## 除錯 (Debugging)
#
# 當你讀寫檔案時，可能會遇到空白字元 (whitespace) 的問題。
# 這些錯誤很難除錯，因為空白字元通常是看不見的。
# 例如，這裡有一個字串，它包含空格、用序列 `\t` 表示的定位字元 (tab)，
# 和用序列 `\n` 表示的換行符。當我們印出它時，我們看不到這些空白字元。

s_whitespace = '1 2\t 3\n 4'
print("--- s_whitespace 直接 print ---")
print(s_whitespace)

# 內建函數 `repr()` 可以幫上忙。它接收任何物件作為參數，並回傳該物件的字串表示法。
# 對於字串，它會用反斜線序列來表示空白字元。

print("\n--- s_whitespace 使用 repr() ---")
print(repr(s_whitespace))

# 這對於除錯很有幫助。
#
# 你可能遇到的另一個問題是，不同的系統使用不同的字元來表示一行的結束。
# 有些系統使用換行符，表示為 `\n`。其他系統使用歸位字元 (return character)，表示為 `\r`。
# 有些則兩者都用。如果你在不同系統之間移動檔案，這些不一致性可能會導致問題。
# (譯註：Python 的通用換行模式通常能處理大部分情況，但了解這個差異仍有幫助。)
#
# 檔案名稱的大小寫是另一個如果你在不同作業系統上工作可能會遇到的問題。
# 在 macOS 和 UNIX 中，檔案名稱可以包含小寫和大寫字母、數字和大多數符號。
# 但許多 Windows 應用程式會忽略小寫和大寫字母之間的差異，
# 並且 macOS 和 UNIX 中允許的一些符號在 Windows 中是不允許的。

# ## 詞彙表 (Glossary)
#
# **短暫的 (ephemeral):**
#  一個短暫的程式通常執行時間很短，當它結束時，它的資料就會遺失。
#
# **持久的 (persistent):**
#  一個持久的程式會無限期地執行，並且至少會將其部分資料保存在永久儲存空間中。
#
# **目錄 (directory):**
#  檔案和其他目錄的集合。
#
# **目前工作目錄 (current working directory):**
#  除非指定了其他目錄，否則程式使用的預設目錄。
#
# **路徑 (path):**
#  一個字串，指定了一系列的目錄，通常指向一個檔案。
#
# **相對路徑 (relative path):**
#  一個從目前工作目錄或其他指定目錄開始的路徑。
#
# **絕對路徑 (absolute path):**
#  一個不依賴於目前目錄的路徑。
#
# **f-字串 (f-string):**
#  一個在開頭引號前有字母 `f` 的字串，並且包含一個或多個用大括號包起來的表達式。
#
# **設定資料 (configuration data):**
#  通常儲存在檔案中的資料，用來指定程式應該做什麼以及如何做。
#
# **序列化 (serialization):**
#  將一個物件轉換成字串。
#
# **反序列化 (deserialization):**
#  將一個字串轉換成物件。
#
# **資料庫 (database):**
#  一個其內容被組織起來以便有效執行某些操作的檔案。
#
# **鍵值儲存 (key-value stores):**
#  一種資料庫，其內容像字典一樣組織，鍵對應到值。
#
# **二進位模式 (binary mode):**
#  一種開啟檔案的方式，使其內容被解讀為位元組序列而不是字元序列。
#
# **雜湊函數 (hash function):**
#  一個接收物件並計算出一個整數的函數，這個整數有時被稱為摘要 (digest)。
#
# **摘要 (digest):**
#  雜湊函數的結果，特別是用來檢查兩個物件是否相同時。

# ## 練習 (Exercises)

# 這個儲存格告訴 Jupyter 在發生執行期錯誤時提供詳細的除錯資訊。
# 在開始做練習之前先執行它。

%xmode Verbose

# ### 問問虛擬助理 (Ask a virtual assistant)
#
# 本章中提到的一些主題我沒有詳細解釋。
# 以下是一些你可以問虛擬助理以獲取更多資訊的問題。
#
# * 「短暫程式和持久程式之間有什麼區別？」
#
# * 「有哪些持久程式的例子？」
#
# * 「相對路徑和絕對路徑有什麼區別？」
#
# * 「為什麼 `yaml` 模組有叫做 `load` 和 `safe_load` 的函數？」
#
# * 「當我寫入一個 Python shelf 時，那些後綴為 `dat` 和 `dir` (或 `.db` 等) 的檔案是什麼？」
#
# * 「除了鍵值儲存之外，還有哪些其他種類的資料庫？」
#
# * 「當我讀取檔案時，二進位模式和文字模式有什麼區別？」
#
# * 「bytes 物件和 string 物件之間有什麼區別？」
#
# * 「什麼是雜湊函數？」
#
# * 「什麼是 MD5 摘要？」
#
# 一如往常，如果你在下面的任何練習中卡住了，可以考慮請虛擬助理幫忙。
# 除了你的問題之外，你可能還想把本章的相關函數貼給它。

# ### 練習
#
# 寫一個叫做 `replace_all` 的函數，它接收一個樣板字串、一個替換字串和兩個檔案名稱作為參數。
# 它應該讀取第一個檔案，並將內容寫入第二個檔案 (如果不存在則建立它)。
# 如果樣板字串出現在內容中的任何地方，它應該被替換成替換字串。

# 這裡有一個函數大綱讓你開始。

def replace_all_starter(old_pattern, new_replacement, source_path_ra, dest_path_ra): # 參數改名
    # 讀取來源檔案的內容
    try:
        reader_ra = open(source_path_ra, 'r', encoding='utf-8')
        # 你的程式碼會在這裡處理讀取
        reader_ra.close() # 記得關閉
    except FileNotFoundError:
        print(f"錯誤: 來源檔案 '{source_path_ra}' 未找到。")
        return
    except IOError as e:
        print(f"讀取來源檔案 '{source_path_ra}' 時發生錯誤: {e}")
        return


    # 把舊字串換成新的

    # 把結果寫入目標檔案
    try:
        writer_ra = open(dest_path_ra, 'w', encoding='utf-8')
        # 你的程式碼會在這裡處理寫入
        writer_ra.close() # 記得關閉
    except IOError as e:
        print(f"寫入目標檔案 '{dest_path_ra}' 時發生錯誤: {e}")
        return

# 解答

def replace_all(old_pattern, new_replacement, source_path_ra, dest_path_ra):
    try:
        with open(source_path_ra, 'r', encoding='utf-8') as reader_ra: # 使用 with 自動關閉檔案
            contents_ra = reader_ra.read()
    except FileNotFoundError:
        print(f"錯誤: 來源檔案 '{source_path_ra}' 未找到。")
        return
    except IOError as e:
        print(f"讀取來源檔案 '{source_path_ra}' 時發生錯誤: {e}")
        return

    # replace() 方法會回傳一個新的字串，其中所有出現的 old_pattern 都被 new_replacement 取代
    replaced_contents = contents_ra.replace(old_pattern, new_replacement)

    try:
        with open(dest_path_ra, 'w', encoding='utf-8') as writer_ra:
            writer_ra.write(replaced_contents)
        print(f"已成功將替換後的內容寫入 '{dest_path_ra}'。")
    except IOError as e:
        print(f"寫入目標檔案 '{dest_path_ra}' 時發生錯誤: {e}")


# 為了測試你的函數，讀取檔案 `photos/notes.txt`，
# 把 `'photos'` 換成 `'images'`，然後把結果寫到檔案 `photos/new_notes.txt`。

source_path_test_ra = os.path.join('photos', 'notes.txt')
original_notes_content = ""
if exists(source_path_test_ra):
    try:
        with open(source_path_test_ra, 'r', encoding='utf-8') as f_notes:
            original_notes_content = f_notes.read()
        print(f"\n--- '{source_path_test_ra}' 的原始內容 ---")
        print(original_notes_content)
    except IOError:
        print(f"無法讀取 '{source_path_test_ra}'。")
else:
    print(f"錯誤: '{source_path_test_ra}' 未找到。")


dest_path_test_ra = os.path.join('photos', 'new_notes.txt')
old_string_ra = 'photos'
new_string_ra = 'images'
if original_notes_content: # 確保有讀到內容才執行替換
    replace_all(old_string_ra, new_string_ra, source_path_test_ra, dest_path_test_ra)


if exists(dest_path_test_ra):
    try:
        with open(dest_path_test_ra, 'r', encoding='utf-8') as f_new_notes:
            replaced_notes_content = f_new_notes.read()
        print(f"\n--- '{dest_path_test_ra}' 的內容 (替換後) ---")
        print(replaced_notes_content)
    except IOError:
        print(f"無法讀取 '{dest_path_test_ra}'。")
else:
    if original_notes_content: # 只有在執行過 replace_all 且它應該產生檔案時才報錯
        print(f"錯誤: '{dest_path_test_ra}' 未找到 (預期由 replace_all 建立)。")


# ### 練習
#
# 在[前面的一個小節](section_storing_data_structure)中，我們使用 `shelve` 模組
# 建立了一個鍵值儲存，它把一個排序後的字母字串對應到一個相同字母異序詞的列表。
# (譯註：section_storing_data_structure 指的是書中對應章節的連結)
# 要完成這個範例，寫一個叫做 `add_word_to_shelf` (原書 `add_word`) 的函數，
# 它接收一個字串和一個 shelf 物件作為參數。
#
# 它應該排序單字的字母來建立一個鍵，然後檢查該鍵是否已在 shelf 中。
# 如果不在，它應該建立一個包含新單字的列表，並將其加入 shelf。
# 如果在，它應該將新單字附加到現有的值 (列表) 中。
# (注意：如前所述，直接附加到從 shelf 取出的列表不會自動更新 shelf，需要重新賦值。)

# 解答
# sort_word 函數已在 In[86] 定義

def add_word_to_shelf(word_to_add, shelf_db): # 參數改名
    key_sorted_word = sort_word(word_to_add)

    if key_sorted_word not in shelf_db:
        shelf_db[key_sorted_word] = [word_to_add] # 第一次遇到這個鍵，建立新列表
    else:
        # 鍵已存在，需要取出列表，附加新單字，然後再存回去
        current_anagram_list = shelf_db[key_sorted_word]
        if word_to_add not in current_anagram_list: # 避免重複加入同一個字
             current_anagram_list.append(word_to_add)
        shelf_db[key_sorted_word] = current_anagram_list # 把修改後的列表存回 shelf

# 你可以用這個迴圈來測試你的函數。

download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

word_list_for_shelf_anagram = []
if exists('words.txt'):
    word_list_for_shelf_anagram = open('words.txt', encoding='utf-8').read().split()
else:
    print("錯誤: words.txt 未找到，無法建立 anagram shelf。")

db_anagram_shelf_ex = None
anagram_shelf_path_ex = 'anagram_map_exercise.db' # 用新檔名避免與前面衝突
print(f"\n--- 將 words.txt 中的單字加入 anagram shelf '{anagram_shelf_path_ex}' ---")
if word_list_for_shelf_anagram:
    try:
        db_anagram_shelf_ex = shelve.open(anagram_shelf_path_ex, 'n') # 'n' 模式會清除舊檔
        for word_item_sa in word_list_for_shelf_anagram:
            add_word_to_shelf(word_item_sa, db_anagram_shelf_ex)
        print(f"已將 {len(word_list_for_shelf_anagram)} 個單字 (或其相同字母異序詞) 加入 shelf。")
        print(f"Shelf 中共有 {len(db_anagram_shelf_ex)} 個鍵 (不同的字母組合)。")
    except Exception as e:
        print(f"處理 anagram shelf 時發生錯誤: {e}")
    finally:
        if db_anagram_shelf_ex is not None:
            db_anagram_shelf_ex.close() # 確保關閉
            db_anagram_shelf_ex = None # 重設
else:
    print("單字列表是空的。")


# 如果一切運作正常，你應該能夠查詢像 `'opst'` 這樣的鍵，
# 並得到一個可以用這些字母拼出的單字列表。

# 重新開啟 shelf 來驗證
retrieved_opst_list = None
try:
    # 'r' 唯讀模式開啟
    with shelve.open(anagram_shelf_path_ex, 'r') as db_check_opst:
        retrieved_opst_list = db_check_opst.get('opst', []) # 使用 get 避免 KeyError
    print(f"從 shelf 查詢 'opst' 得到的列表: {sorted(retrieved_opst_list)}") # 排序以方便比較
except Exception as e:
    print(f"重新開啟或查詢 anagram shelf '{anagram_shelf_path_ex}' 失敗: {e}")


# 印出一些包含超過8個相同字母異序詞的組
print("\n--- 包含超過 8 個相同字母異序詞的組 (來自 shelf) ---")
try:
    with shelve.open(anagram_shelf_path_ex, 'r') as db_check_long_anagrams:
        found_long = False
        for key_la, value_la_list in db_check_long_anagrams.items():
            if len(value_la_list) > 8:
                print(sorted(value_la_list)) # 排序以方便查看
                found_long = True
        if not found_long:
            print("未找到包含超過 8 個相同字母異序詞的組。")
except Exception as e:
    print(f"查詢 anagram shelf 時發生錯誤: {e}")

# db_anagram_shelf_ex.close() # 已在 In[148] 的 finally 中處理

# ### 練習
#
# 在一個大型檔案集合中，同一個檔案可能有多個副本，儲存在不同的目錄或使用不同的檔案名稱。
# 這個練習的目標是搜尋重複檔案。
# 作為例子，我們將處理 `photos` 目錄中的圖片檔案。
#
# 它的運作方式如下：
#
# * 我們會使用[前面小節](section_walking_directories)的 `walk` 函數 (或其變體)
#   來搜尋這個目錄，找出副檔名在 `config['extensions']` 中的檔案。
#   (譯註：section_walking_directories 指的是書中對應章節的連結)
#
# * 對於每個檔案，我們會使用[前面小節](section_md5_digest)的 `md5_digest`
#   來計算內容的摘要。
#   (譯註：section_md5_digest 指的是書中對應章節的連結)
#
# * 使用 shelf，我們會建立一個從每個摘要對應到具有該摘要的路徑列表的映射。
#
# * 最後，我們會搜尋 shelf 中是否有任何摘要對應到多個檔案。
#
# * 如果我們找到任何，我們會用 `same_contents` 來確認這些檔案是否包含相同的資料。

# 我會先建議一些要寫的函數，然後我們再把它們整合起來。
#
# 1. 要識別圖片檔案，寫一個叫做 `is_image` 的函數，它接收一個路徑和一個副檔名列表，
#    如果路徑以列表中的任一副檔名結尾，則回傳 `True`。
#    提示：使用 `os.path.splitext` —— 或者請虛擬助理幫你寫這個函數。

# 解答
# os 模組已在前面匯入

def is_image(path_input_ii, extensions_list_ii): # 參數改名
    """檢查路徑是否以指定的任一副檔名結尾。

    path_input_ii: 字串檔案路徑
    extensions_list_ii: 副檔名列表 (例如 ['jpg', 'jpeg'])

    >>> is_image('photo.jpg', ['jpg', 'jpeg'])
    True
    >>> is_image('PHOTO.JPG', ['jpg', 'jpeg']) # 應忽略大小寫
    True
    >>> is_image('notes.txt', ['jpg', 'jpeg'])
    False
    >>> is_image('image.JPEG', ['jpg', 'jpeg'])
    True
    """
    # os.path.splitext 會把 'path/to/file.ext' 分割成 ('path/to/file', '.ext')
    filename_part, extension_part = os.path.splitext(path_input_ii)
    # 移除開頭的 '.' 並轉成小寫以進行不區分大小寫的比較
    actual_extension = extension_part.strip('.').lower()
    # 把傳入的 extensions_list_ii 也轉成小寫以防萬一
    normalized_extensions = [ext.lower() for ext in extensions_list_ii]
    return actual_extension in normalized_extensions

# 你可以用 `doctest` 來測試你的函數。

# from doctest import run_docstring_examples # 已在前面匯入
# def run_doctests(func): # 已在前面定義

print("\n--- 測試 is_image ---")
run_doctests(is_image)

# 2. 寫一個叫做 `add_path_to_digest_shelf` (原書 `add_path`) 的函數，它接收一個路徑和一個 shelf 作為參數。
#    它應該使用 `md5_digest` 來計算檔案內容的摘要。
#    然後它應該更新 shelf，要嘛建立一個從摘要對應到包含該路徑的列表的新項目，
#    要嘛將該路徑附加到已存在的列表中。

# 解答
# md5_digest 函數已在 In[118] 定義

def add_path_to_digest_shelf(path_to_add, shelf_db_ap): # 參數改名
    digest_val = md5_digest(path_to_add) # 計算檔案的 MD5 摘要

    if digest_val is None: # 如果計算摘要失敗 (例如檔案不存在)
        print(f"警告: 無法計算 '{path_to_add}' 的摘要，跳過。")
        return

    if digest_val not in shelf_db_ap:
        shelf_db_ap[digest_val] = [path_to_add] # 摘要是新的，建立新列表
    else:
        # 摘要已存在，取出列表，附加新路徑，然後存回去
        paths_list = shelf_db_ap[digest_val]
        if path_to_add not in paths_list: # 避免重複加入相同的路徑
            paths_list.append(path_to_add)
        shelf_db_ap[digest_val] = paths_list # 把修改後的列表存回


# 3. 寫一個 `walk` 的版本，叫做 `walk_images`，它接收一個目錄並遍歷該目錄及其子目錄中的檔案。
#    對於每個檔案，它應該使用 `is_image` 來檢查它是否為圖片檔案，
#    並使用 `add_path_to_digest_shelf` (原書 `add_path`) 把它加入到 shelf 中。
#    (注意: `walk_images` 需要能存取 shelf 物件，可以把它當作參數傳入，或設為全域變數)

# 解答
# walk 已在 In[123] 定義
# is_image 已在 In[155] 定義
# add_path_to_digest_shelf 已在 In[159] 定義
# config 字典已在 In[47] 定義 (包含 extensions)

# 我們需要一個 shelf 物件讓 walk_images 使用
# 這裡假設 shelf_for_images 會在呼叫 walk_images 之前建立
# 並作為參數傳遞給 walk_images

def walk_images(dirname_wi, shelf_for_images): # 加入 shelf_for_images 參數
    if not os.path.exists(dirname_wi) or not os.path.isdir(dirname_wi):
        print(f"錯誤: '{dirname_wi}' 不是一個有效的目錄 (在 walk_images 中)。")
        return
    if not config or 'extensions' not in config:
        print("錯誤: config 或 config['extensions'] 未定義。")
        return

    for name_wi in os.listdir(dirname_wi):
        path_wi = os.path.join(dirname_wi, name_wi)

        if os.path.isfile(path_wi):
            if is_image(path_wi, config['extensions']): # 檢查是否為圖片
                add_path_to_digest_shelf(path_wi, shelf_for_images) # 加入 shelf
        elif os.path.isdir(path_wi):
            walk_images(path_wi, shelf_for_images) # 遞迴搜尋子目錄


# 當一切運作正常時，你可以使用下面的程式來建立 shelf，
# 搜尋 `photos` 目錄並將路徑加入 shelf，
# 然後檢查是否有摘要對應到多個檔案。

digest_shelf_path = os.path.join('photos', 'digests.db') # shelf 檔案名稱
db_image_digests = None

print(f"\n--- 搜尋重複圖片 (使用 MD5 摘要) ---")
try:
    # 'n' 模式確保每次都從新的 shelf 開始
    db_image_digests = shelve.open(digest_shelf_path, 'n')
    print(f"開始遍歷 'photos' 目錄中的圖片...")
    walk_images('photos', db_image_digests) # 傳入 db_image_digests
    print("圖片遍歷完成。")

    found_duplicates_md5 = False
    print("\n具有相同 MD5 摘要的檔案路徑列表 (可能是重複檔案):")
    for digest_key, paths_val_list in db_image_digests.items():
        if len(paths_val_list) > 1: # 如果一個摘要對應到多個路徑
            print(paths_val_list)
            found_duplicates_md5 = True
    
    if not found_duplicates_md5:
        print("未找到任何具有相同 MD5 摘要的檔案組。")

except Exception as e:
    print(f"處理圖片摘要 shelf 時發生錯誤: {e}")
finally:
    if db_image_digests is not None:
        db_image_digests.close()
        db_image_digests = None


# 你應該會找到一對具有相同摘要的檔案。
# 使用 `same_contents` 來檢查它們是否真的包含相同的資料。
# (書中暗示 'photos/mar-2023/photo2.jpg' 和 'photos/jan-2023/photo1.jpg' 是重複的)

# 解答
print("\n--- 驗證找到的重複檔案內容是否相同 ---")
# 根據書中提示的可能重複檔案路徑 (實際路徑可能因 photos.zip 內容而異)
# 如果上面的程式碼正確找出了重複組，這裡應該用那些找出的路徑
# 假設我們手動指定一組來測試 same_contents
path_dup1 = os.path.join('photos', 'mar-2023', 'photo2.jpg')
path_dup2 = os.path.join('photos', 'jan-2023', 'photo1.jpg')

# 檢查這些檔案是否存在
if exists(path_dup1) and exists(path_dup2):
    # same_contents 函數已在 In[110] 定義
    are_they_same = same_contents(path_dup1, path_dup2)
    print(f"檔案 '{path_dup1}' 和 '{path_dup2}' 的內容是否相同: {are_they_same}")
else:
    print(f"警告: 檔案 '{path_dup1}' 或 '{path_dup2}' 未找到，無法比較內容。")
    print("請檢查 photos.zip 的內容和你的 walk_images 是否正確找到了重複檔案組。")


# (這個儲存格是空的)

# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
#
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
#
# 程式碼授權: [MIT License](https://mit-license.org/)
#
# 文字內容授權: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)