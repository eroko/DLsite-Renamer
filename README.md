# DLsite_Renamer

### 使用說明:

**Install requirements：**
```
pip install tkintertable
pip install requests
```

**關鍵字**："workno", "circle", "title", "cv", "author", 模板中的這五個關鍵字將會被程式替換  

*分別代表:*
1. workno: 作品編號
2. circle: 社團/公司名
3. title: 標題
4. cv: 聲優
5. author: 作者

**默認模板**: "to": "workno title "

**自定義模板**: 請修改 "config.json" 中的 "template"

例如："to": "[workno][circle] title "

重命名前：[不必要的前綴] VJ009178 零.軌跡 (要刪掉的後綴)

重命名後：[VJ009178][Falcom] 英雄伝説 零の軌跡

**自定義替換規則**: 請修改 "config.json" 中的 "replace_rules", 作品編號意義如下     

RJ開頭 => 音聲/音樂 作品    
BJ開頭 => 書 作品  
VJ開頭 => 遊戲 作品     

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
		},
		{
            "type": "default",
			"from": "",
			"to": "workno title "
		}
	]
}
```

### 注意：
1. config.json 文件使用 **UTF-8** 編碼, 請不要用 Windows 系統自帶的記事本進行編輯，推薦使用專業的**文本編輯器**，例如: [Notepad3](https://www.appinn.com/notepad3/), [Notepad++](https://notepad-plus-plus.org/), [vscode](https://code.visualstudio.com/)
![Notepad3](https://i.imgur.com/5ouMclD.png)
2. 去除標題中【】之間的內容主要用於去掉不必要的標註，可多加利用~

![範例圖片](https://i.imgur.com/g9L14QI.png)
