# DLsite Renamer
自动重命名RJ/BJ/VJ编号的文件

## 更新事项

### ver3.6
- 支持了DLsite新的8位数字的编号（很好奇为什么直接变成8位了？
- 优化引用
- 调整缩进

### ver3.5
- 取消了GUI版，只保留命令行版。`dlsite.py`就是命令行版文件，使用方法参照下面的旧版说明
- 配置文件按照个人偏好配置，具体配置方案参照旧版说明文件
- 把`README.md`的图片迁移到了github
- 换了`requests`库，在网络环境不佳的情况下能更稳定一点？
- 所以现在要使用你还得加上`requests`库

---

# Information Below is **OUTDATED**!!!!!!!

---

# Recent Update
- ver3.4 Fix Getting Title Error
- ver3.3 Fork From ch010060/DLsite_Renamer

# DLsite_Renamer
![GUI](https://github.com/eroko/DLsite_Renamer/blob/master/images/GUI.png)
![DEMO](https://github.com/eroko/DLsite_Renamer/blob/master/images/demo.gif)

### Purpose
Rename the DLsite works with custom pattern and download the cover If required.

### How to use:
1. Download the binary [release pack](https://github.com/ch010060/DLsite_Renamer/releases) and run .exe or run python script by yourself.
2. There are two versions:	
	1. GUI ver. => dlsite_renamer.py(.exe)
	2. CLI ver. => dlsite_renamer-cli.py(.exe)

### Install requirements：
1. Install python3
2. Install pip
```
pip install lxml
pip install tkintertable
pip install requests
```

### Custom pattern：
We will replace the filename with this keywords.  

*Keyword List:*
1. workno: 作品番號
2. circle: サークル/會社
3. title: 標題
4. cv: 声優
5. author: 著者
6. work_age: 年齡指定
7. release_date: 販売日
8. type: 作品形式

**Default template**: "workno title"

E.g, VJ009178 英雄伝説 零の軌跡

**User defined template**: Please modify the "config.json" to custom your "type" and "to" replace rule, or use default template

The work code prefix meaning:  
RJxxxxxx => ASMR/Music   
BJxxxxxx => Doujin/Comic  
VJxxxxxx => Game 

E.g,
```
"type": "vj"        
"to": "(type)(work_age)[release_date][workno][circle] title "     
```

Before：[prefix_12345] VJ009178 零.軌跡 (postfix-56789)

After：(ゲーム)(全年齢)[150417][VJ009178][Falcom] 英雄伝説 零の軌跡  
  
*config.json example*
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
1. Please modify the config.json with **UTF-8**.
![Notepad3](https://github.com/eroko/DLsite_Renamer/blob/master/images/notepad.png)
2. You can delete the unnecessary string in【】in filename if required.
3. Skip download the cover.jpg if it does exist.
4. Special character processing: Convert the "Windows invalid character" to fullwidth form, multilple space to single space.

### (Optional) CLI version without GUI and loop：
```
usage: dlsite_renamer-cli.py [-h] [-d] [-c] [-r] -i PATH

Renamer for DLsite works v3.0

optional arguments:
  -h, --help            show this help message and exit
  -d, --DEL             delete string in 【】
  -c, --COVER           download cover
  -r, --RECUR           recursively processing
  -i PATH, --PATH PATH  path for processing
```
