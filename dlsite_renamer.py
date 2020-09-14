from tkinter import filedialog
from tkinter import messagebox
from lxml import html
import tkinter as tk
import threading
import requests
import time
import re
import os
import json

# 默認設定
template = 'workno title '  # 默認命名模板
template_RJ = 'workno title (cv) '  # 默認RJ命名模板(Voice)
template_BJ = 'workno [circle (author)] [title] '  # 默認BJ命名模板(Comic)
template_VJ = 'workno [title] '  # 默認VJ命名模板(Game)

replace_rules = []  # 替換規則

RJ_WEBPATH = 'https://www.dlsite.com/maniax/work/=/product_id/'
RJ_G_WEBPATH = 'https://www.dlsite.com/home/work/=/product_id/'
BJ_WEBPATH = 'https://www.dlsite.com/books/work/=/product_id/'
BJ_G_WEBPATH = 'https://www.dlsite.com/comic/work/=/product_id/'
VJ_WEBPATH = 'https://www.dlsite.com/pro/work/=/product_id/'
VJ_G_WEBPATH = 'https://www.dlsite.com/soft/work/=/product_id/'
R_COOKIE = {'adultchecked': '1'}

# re.compile()返回一個匹配對像
# ensure path name is exactly RJ###### or RT######
pattern = re.compile("[BRV][EJ]\d{6}")
# filter to substitute illegal filenanme characters to " "
filter = re.compile('[\\\/:"*?<>|]+')


# 避免ERROR: Max retries exceeded with url
requests.adapters.DEFAULT_RETRIES = 5  # 增加重連次數
s = requests.session()
s.keep_alive = False  # 關閉多餘連接
# s.get(url) # 你需要的網址

# 查找母串內所有子串的位置, 查找失敗返回-1


def find_all(source, dest):
    length1, length2 = len(source), len(dest)
    dest_list = []
    temp_list = []
    if length1 < length2:
        return -1
    i = 0
    while i <= length1-length2:
        if source[i] == dest[0]:
            dest_list.append(i)
        i += 1
    if dest_list == []:
        return -1
    for x in dest_list:
        #print("Now x is:%d. Slice string is :%s"% (x,repr(source[x:x+length2])),end=" ")
        if source[x:x+length2] != dest:
            #print(" dest != slice")
            temp_list.append(x)
        # else:
            #print(" dest == slice")
    for x in temp_list:
        dest_list.remove(x)
    return dest_list

# 從資料夾名稱中提取code


def get_code(originalName, matchCode):
    index_list = find_all(originalName, matchCode)
    if index_list == -1:
        return ""
    for i in range(0, len(index_list)):
        r_idx = index_list[i]
        code = originalName[r_idx:(r_idx)+8]
        pattern = re.compile("^"+matchCode+"\d{6}$")
        if pattern.match(code):
            return code.upper()
    return ""


def match_code(work_code):
    # requests函示庫是一個常用於http請求的模組
    if work_code[0] == "R" or work_code[0] == "r":
        url = RJ_WEBPATH + work_code
    if work_code[0] == "B" or work_code[0] == "b":
        url = BJ_WEBPATH + work_code
    if work_code[0] == "V" or work_code[0] == "v":
        url = VJ_WEBPATH + work_code
    try:
        # allow_redirects=False 禁止重定向
        r = s.get(url, allow_redirects=False, cookies=R_COOKIE)
        # HTTP狀態碼==200表示請求成功
        if r.status_code != 200:
            #print("    Status code:", r.status_code, "\nurl:", url)
            try:
                ## 改成一般向網址
                if work_code[0] == "R" or work_code[0] == "r":
                    url = RJ_G_WEBPATH + work_code
                if work_code[0] == "B" or work_code[0] == "b":
                    url = BJ_G_WEBPATH + work_code
                if work_code[0] == "V" or work_code[0] == "v":
                    url = VJ_G_WEBPATH + work_code
                r = s.get(url, allow_redirects=False, cookies=R_COOKIE)
                if r.status_code != 200:
                    return r.status_code, "", "", []
            except os.error as err:
                text.insert(tk.END, "**請求超時!\n")
                text.insert(tk.END, "  請檢查網絡連接\n")
                return "", "", "", []

        # fromstring()在解析xml格式時, 將字串轉換為Element對像, 解析樹的根節點
        # 在python中, 對get請求返回的r.content做fromstring()處理, 可以方便進行後續的xpath()定位等
        tree = html.fromstring(r.content)
        title = tree.xpath('//a[@itemprop="url"]/text()')[0]
        circle = tree.xpath(
            '//span[@itemprop="brand" and @class="maker_name"]/*/text()')[0]
        cvList = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "声優")]/../td/a/text()')
        authorList = tree.xpath(
            '//*[@id="work_maker"]/tr/th[contains(text(), "著者")]/../td/a/text()')

        return 200, title, circle, cvList, authorList

    except os.error as err:
        text.insert(tk.END, "**請求超時!\n")
        text.insert(tk.END, "  請檢查網絡連接\n")
        return "", "", "", []

def nameChange():
    # askdirectory()檔案對話框, 選擇目錄, 返回目錄名
    path = filedialog.askdirectory()
    if path == "":
        messagebox.showinfo(title="錯誤", message="請選擇路徑!" + "\n")
    else:
        cbtn.config(state=tk.DISABLED)
        btn.config(state=tk.DISABLED)
        btn['text'] = "等待完成"
        text.insert(tk.END, "選擇路徑: " + path + "\n")
        # os.listdir()返回指定的資料夾包含的檔案或資料夾的名字的列表
        files = os.listdir(path)
        for file in files:
            # os.path.isdir()用於判斷對象是否為一個目錄。
            if os.path.isdir(os.path.join(path, file)):
                # 獲取資料夾原始名稱
                originalName = file
                # 嘗試獲取code
                code = ""
                for matchCode in ['RJ', 'rj', 'BJ', 'bj', 'VJ', 'vj']:
                    code = get_code(originalName, matchCode)
                    if code:
                        break
                # 如果沒能提取到code
                if code == "":
                    continue  # 跳過該資料夾
                else:
                    #print('Processing: ' + code)
                    text.insert(tk.END, 'Processing: ' + code + '\n')
                    r_status, title, circle, cvList, authorList = match_code(code)
                    # 如果順利爬取網頁訊息
                    if r_status == 200 and title and circle:
                        if var1.get():
                            # 刪除title中的【.*?】
                            title = re.sub(u"\\【.*?】", "", title)

                        if code[0] == "R" or code[0] == "r":
                            new_name = template_RJ.replace("workno", code)
                        if code[0] == "B" or code[0] == "b":
                            new_name = template_BJ.replace("workno", code)
                        if code[0] == "V" or code[0] == "v":
                            new_name = template_VJ.replace("workno", code)

                        new_name = new_name.replace("title", title)
                        new_name = new_name.replace("circle", circle)

                        author = ""
                        if authorList:  # 如果authorList非空
                            for name in authorList:
                                author += " " + name
                            new_name = new_name.replace("author", author[1:])
                        else:
                            new_name = new_name.replace("(author)", "")  

                        cv = ""
                        if cvList:  # 如果cvList非空
                            for name in cvList:
                                cv += "," + name
                            new_name = new_name.replace("cv", cv[1:])
                        else:
                            new_name = new_name.replace("(cv)", "")

                        # 將Windows文件名中的非法字元替換
                        # re.sub(pattern, repl, string)
                        new_name = re.sub(filter, " ", new_name)
                        # 嘗試重命名
                        try:
                            # strip() 去掉字串兩邊的空格
                            os.rename(os.path.join(path, originalName),
                                      os.path.join(path, new_name.strip()))
                        except os.error as err:
                            text.insert(tk.END, "**重命名失敗!\n")
                            text.insert(
                                tk.END, "  " + os.path.join(path, originalName) + "\n")
                            text.insert(tk.END, "  請檢查是否存在重複的名稱\n")
                    elif r_status == 404:
                        text.insert(tk.END, "**爬取DLsite過程中出現錯誤!\n")
                        text.insert(tk.END, "  請檢查本作是否已經下架或被收入合集\n")
                    elif r_status != "":
                        text.insert(tk.END, "**爬取DLsite過程中出現錯誤!\n")
                        text.insert(tk.END, "  網頁 URL: " +
                                    RJ_WEBPATH + code + "\n")
                        text.insert(tk.END, "  HTTP 狀態碼: " +
                                    str(r_status) + "\n")

                    # set delay to avoid being blocked from server
                    time.sleep(0.1)
        # print("~Finished.")
        text.insert(tk.END, "*******完成!*******\n\n\n\n")
        tk.messagebox.showinfo(title="提示", message="完成!")

        cbtn.config(state=tk.NORMAL)
        btn.config(state=tk.NORMAL)
        btn['text'] = "選擇路徑"


def thread_it(func, *args):
    '''將函數打包進線程'''
    # 建立
    t = threading.Thread(target=func, args=args)
    # 守護 !!!
    t.setDaemon(True)
    # 啟動
    t.start()
    # 阻塞--卡死界面！
    # t.join()


root = tk.Tk()  # 實例化object，建立視窗root
root.title('DLsite重命名工具 v2.0')  # 給視窗的標題取名字
root.eval('tk::PlaceWindow . center')
root.geometry('300x375')  # 設定視窗的大小(橫向 * 縱向)

text = tk.Text(root)
text.pack()

# 讀取配置文件
# os.path.dirname(__file__) 當前腳本所在路徑
basedir = os.path.abspath(os.path.dirname(__file__))
try:
    fname = os.path.join(basedir, 'config.json')
    with open(fname, 'r', encoding='utf-8') as f:
        config = json.load(f)
        for tag in config['replace_rules']:  # 模板非空
            if ("workno" in tag['to']):
                if tag['type'] == "rj":
                    text.insert(tk.END, "**使用自定義RJ命名模板:\n")
                    template_RJ = tag['to']
                    text.insert(tk.END, "  " + template_RJ.strip() + "\n\n")
                if tag['type'] == "bj":
                    text.insert(tk.END, "**使用自定義BJ命名模板:\n")
                    template_BJ = tag['to']
                    text.insert(tk.END, "  " + template_BJ.strip() + "\n\n")
                if tag['type'] == "vj":
                    text.insert(tk.END, "**使用自定義VJ命名模板:\n")
                    template_VJ = tag['to']
                    text.insert(tk.END, "  " + template_VJ.strip() + "\n\n")
            else:
                text.insert(tk.END, "**模板格式錯誤: 模板中必須包含\"workno\"!\n")
                text.insert(tk.END, "  使用默認命名模板:\n")
                text.insert(tk.END, "  workno title \n\n")
        else:
            text.insert(tk.END, "**使用默認命名模板:\n")
            text.insert(tk.END, "  workno title \n\n")

        if config["replace_rules"] and type(config["replace_rules"]) == list and len(config["replace_rules"]):
            replace_rules = config["replace_rules"]

except os.error as err:
    # 生成配置文件
    with open(fname, "w", encoding='utf-8') as f:
        json.dump({'template': '', "replace_rules": []}, f, ensure_ascii=False, sort_keys=True,
                  indent=4, separators=(',', ': '))
    text.insert(tk.END, "**使用默認命名模板:\n")
    text.insert(tk.END, "  workno [circle] \n")

var1 = tk.IntVar()  # 定義var1整型變數用來存放選擇行為返回值
cbtn = tk.Checkbutton(root, text='去除title中【】之間的內容', variable=var1,
                      onvalue=1, offvalue=0)  # 傳值原理類似於radiobutton物件

btn = tk.Button(root, text='選擇路徑', command=lambda: thread_it(nameChange))

btn.pack()
cbtn.pack()

root.mainloop()
