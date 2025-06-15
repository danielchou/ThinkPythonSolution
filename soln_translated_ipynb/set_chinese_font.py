import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
import sys

def set_chinese_font():
    """
    設定 matplotlib 使用支援中文的字體
    """
    system = platform.system()
    
    if system == 'Windows':
        # Windows 系統常見的中文字體
        font_list = ['Microsoft JhengHei', 'Microsoft YaHei', 'SimHei', 'SimSun', 'DengXian', 'KaiTi']
    elif system == 'Darwin':  # macOS
        # macOS 系統常見的中文字體，按優先順序排列
        font_list = [
            'PingFang TC', 'PingFang SC',  # 蘋方
            'Heiti TC', 'Heiti SC',         # 黑體
            'Hiragino Sans GB',             # 冬青黑體
            'Apple LiGothic',               # 蘋果儷黑
            'STHeiti', 'STSong',            # 華文黑體、宋體
            'Source Han Sans TC', 'Source Han Sans SC',  # 思源黑體
            'Noto Sans CJK TC', 'Noto Sans CJK SC'       # Noto Sans 中文
        ]
    else:  # Linux 或其他系統
        font_list = ['Noto Sans CJK TC', 'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback']
    
    # 列出所有可用字體（僅用於調試）
    # print("系統中的所有字體：")
    # for font in sorted([f.name for f in fm.fontManager.ttflist]):
    #     print(font)
    
    # 嘗試找到可用的中文字體
    chinese_font = None
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in font_list:
        if font in available_fonts:
            chinese_font = font
            break
    
    # 如果找到支援中文的字體，設定為 matplotlib 的默認字體
    if chinese_font:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [chinese_font] + plt.rcParams['font.sans-serif']
        print(f"已設定使用 {chinese_font} 字體")
    else:
        print("警告：找不到支援中文的字體，圖表中的中文可能無法正確顯示")
        # 嘗試使用可能支援中文的字體作為備選
        plt.rcParams['font.sans-serif'] = ['Noto Sans', 'Arial Unicode MS', 'DejaVu Sans'] + plt.rcParams['font.sans-serif']
    
    # 解決負號顯示問題
    plt.rcParams['axes.unicode_minus'] = False
    
    # 嘗試使用 matplotlib-chinese-fonts 套件（如果已安裝）
    try:
        import matplotlib_chinese_fonts
        matplotlib_chinese_fonts.set_font_family()
        print("已載入 matplotlib-chinese-fonts 套件")
    except ImportError:
        pass


def list_available_chinese_fonts():
    """
    列出系統中可能支援中文的字體
    """
    # 常見的中文字體關鍵字
    chinese_keywords = ['chinese', 'cjk', 'ming', 'song', 'hei', 'kai', 'gothic', 
                       '黑體', '宋體', '明體', '楷體', 'pingfang', 'heiti', 
                       'source han', '思源', 'noto', 'microsoft', '微軟', 'wenquanyi', '文泉']
    
    # 獲取所有可用字體
    all_fonts = sorted([f.name for f in fm.fontManager.ttflist])
    
    # 篩選可能支援中文的字體
    chinese_fonts = []
    for font in all_fonts:
        font_lower = font.lower()
        if any(keyword in font_lower for keyword in chinese_keywords):
            chinese_fonts.append(font)
    
    return chinese_fonts
