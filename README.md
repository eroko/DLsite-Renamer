# DLsite_Renamer
![範例圖片](https://i.imgur.com/BSOwho9.png)

### Purpose
Rename the DLsite works and download the cover If required.

### How to use:
1. Download the binary [release pack](https://github.com/ch010060/DLsite_Renamer/releases) and run .exe or run python script by yourself.
2. There are two versions:	
	1. GUI ver. => dlsite_renamer.py(.exe)
	2. CLI ver. => dlsite_renamer-cli.py(.exe)

**Install requirements：**
1. Install python3
2. Install pip
```
pip install lxml
pip install tkintertable
pip install requests
```

**Keyword**："workno", "circle", "title", "cv", "author", "work_age", "release_date", "type", 模板中的這8個關鍵字將會被程式替換  

*關鍵字分別代表:*
1. workno: 作品編號
2. circle: 社團/公司名
3. title: 標題
4. cv: 聲優
5. author: 作者
6. work_age: 年齡指定
7. release_date: 發售日
8. type: 作品形式

**Default template**: "workno title "

例如： VJ009178 英雄伝説 零の軌跡

**User defined template**: 請修改 "config.json" 中對應的 "type" 來替換自訂規則 "to", 若無定義則使用默認模板

作品編號意義如下(僅供大略參考)     

RJ開頭 => 音聲/音樂 作品    
BJ開頭 => 書 作品  
VJ開頭 => 遊戲 作品     

例如：
```
"type": "vj"        
"to": "(type)(work_age)[release_date][workno][circle] title "     
```

重命名前：[不必要的前綴] VJ009178 零.軌跡 (要刪掉的後綴)

重命名後：(ゲーム)(全年齢)[150417][VJ009178][Falcom] 英雄伝説 零の軌跡

*config.json範例*
```json
{
	 "replace_rules":
	 [
		{
            		"type": "rj",
			"from": "",
			"to": "workno title (CV. cv) "
		},
		{
            		"type": "bj",
			"from": "",
			"to": "[workno][circle (author)] title "
		},
		{
            		"type": "vj",
			"from": "",
			"to": "[workno][circle] title "
		}
	]
}
```

### Notice：
1. config.json 文件使用 **UTF-8** 編碼, 請不要用 Windows 系統自帶的記事本進行編輯，推薦使用專業的**文件編輯器**，例如: [Notepad3](https://www.appinn.com/notepad3/), [Notepad++](https://notepad-plus-plus.org/), [vscode](https://code.visualstudio.com/)
![Notepad3](https://i.imgur.com/L73BXEZ.png)
2. 去除標題中【】之間的內容主要用於去掉不必要的標註，可多加利用~
3. 若封面(cover.jpg)已存在資料夾中，則會自動跳過下載
4. 標題字串特殊處理: 轉換標題中的"Windows非法字元"為"全形"，"多空格"變為"單空格"

### (Optional) CLI version without GUI and loop：
```
usage: dlsite_renamer-cli.py [-h] [-d] [-c] -i PATH

Renamer for DLsite works v3.0

optional arguments:
  -h, --help            show this help message and exit
  -d, --DEL             delete string in 【】
  -c, --COVER           download cover
  -i PATH, --PATH PATH  path for processing
```
