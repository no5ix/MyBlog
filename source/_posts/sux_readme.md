---
title: 一个只有800k大小的强大效率工具sux
date: 2020-01-09 22:09:39
tags:
- GitHub
- AutoHotKey
categories:
- GitHub
top: 1
---



<!-- [<i class="fa fa-fw fa-github fa-2x"></i>nox](https://github.com/no5ix/sux) 

An alternative to **Alfred**/**Wox**/**Listary**/**Capslock+** .

Inspired by Alfred/Wox/Listary/Capslock+/utools, thank u.

<video width="100%" controls="controls">
<source src="/img/sux/sux_intro.mp4" type="video/mp4" />
</video> -->


![sux](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/sux.svg)

`sux` 是一个只有800k大小的强大效率工具同时拥有
- [翻译](#翻译)
- [历史剪切板](#历史剪切板clipboard-plus)
- [截图 & 贴图](#截图和贴图)
- [类似listary/alfred/wox的快捷搜索](#快捷搜索search-plus): `shift+空格`
- [类似macos的触发角](#类似macos的触发角hot-corner)
- [屏幕边缘触发器](#屏幕边缘触发器hot-edge)
- [全局自定义快捷键实现各种操作](#快捷键完全自定义)
- [文本替换器](#文字替换器replace-text)
- [文本变换器](#文本变换器)
- 自定义主题
- [托盘菜单](#托盘菜单)
- [快捷指令](#cmds指令)
- [可自定义的json配置](#自定义配置)
- blabla...

An alternative to **Alfred**/**Wox**/**Listary**/**Capslock+**/**OneQuick** .

Inspired by Alfred/Wox/Listary/Capslock+/utools/OneQuick, thank u.

<!-- [![](https://github.com/no5ix/no5ix.github.io/blob/source/source//sux/sux/web_search.gif)](https://hulinhong.com/2020/01/09/sux_readme/)
点击图片来看完整视频.click img to see full video. -->


**. . .**<!-- more -->


# 重要

- 请以管理员身份运行sux
- 防止杀毒软件误杀处理 :
    - 打开win10托盘的`Windows安全中心`-`病毒和威胁防护`-`病毒和威胁防护设置的管理设置`-`排除项的添加或删除排除项`-`添加排除项`-`文件夹`, 然后选中sux所在文件夹即可
    - 如果被其他杀毒软件报杀则将sux列入白名单
    - 如果是windows安全中心杀了的话则在它的`病毒和威胁保护`-`保护历史记录`-找到删除sux的历史记录-`还原`
- Please run sux as administrator.

Just download [<i class="fa fa-download fa-2x fa-fw"></i>sux.zip](https://github.com/no5ix/sux/releases) and unzip it then run sux.exe as admin !


# 快捷搜索search-plus

大多数时候其实都是 `shift+空格` 然后空格搜东西, 如果要取消菜单则按`alt`或者`esc`, 所有的菜单都是可以选中某段文字然后直接查询的, 右边这一排`q/w/e/r`啥的都是快捷键
![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/search_plus.gif)

也可以先选中某段文字然后`shift+空格`然后直接查询的.

所有的默认快捷键都是可以改的, 在`conf.user.json`里找到`ShowSuxMenu`改, 改成`capslock_q`或者`alt_space`或者`doublehit_ctrl`或者`triplehit_shift`或者其他的任何你喜欢的快捷键都行, 不过不建议`doublehit_alt`, 因为`alt`会丢失焦点.

*为什么`shift+空格` 出来的不是搜索框?*

原来是那样的, 后来我给一些用户(比如运营岗用户)用, 发现他们记不住key.
比如百度是`bd`, 谷歌是`gg`这种对吧?
后来我就做了个这种快捷菜单, 用过几次熟悉快捷键之后也十分迅捷方便, 省去了每次都要输入什么`gg`/`bd`的烦恼


# 托盘菜单

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/tray_menu.gif)

直接鼠标点击sux托盘图标可以快速禁用sux


## 禁用win10系统的自动更新

win10的自动更新经常会搞得电脑蓝屏或者各种崩溃或者长时间占用电脑, 十分恼人. win10的自动更新用win10本身自带的机制是无法禁止的, 即使关闭了win10的 `Windows Update`服务, 他隔一段时间后也会自动开启.  
sux的这个功能就彻底解决了这个问题, 不再烦恼.


## 窗口移动器-永远保持新窗口在鼠标所在的显示器打开

对于多显示器的用户来说, 在2显示器上双击了某程序准备打开它, 很可能它这个程序窗口却会在1显示器上打开, sux的窗口移动器就是解决这个问题的

注: 当检测到用户只有一个显示器的时候, 此选项会自动禁用(灰掉)


# 类似macos的触发角hot-corner

若要用的话, 需要去sux托盘菜单里开启触发角功能

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/hot_corner.gif)

当开启之后, 鼠标移动到屏幕左上/左下/右上右下都会触发不同的动作:
- 左上: 跳到浏览器前一个标签页
- 右上: 跳到浏览器后一个标签页
- 左下: 模拟按下`win`键
- 右下: 模拟按下`alt+tab`

这些是默认动作, 你都可以改动自定义配置`conf.user.json`来更改
``` json
  "hot-corner": {
    "action": {
      "LeftTopCorner": {
        "hover": "JumpToPrevTab"
      },
      "RightTopCorner": {
        "hover": "JumpToNextTab"
      },
      "LeftBottomCorner": {
        "hover": "win"
      },
      "RightBottomCorner": {
        "hover": "GotoPreApp"
      }
    }
  },
```


# 翻译

翻译集成在快捷菜单中了

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/translate_text.gif)


# 历史剪切板clipboard-plus

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/clipboard_plus.gif)

这个历史粘贴板目前是不支持图片和其他的二进制文件, 支持一键粘贴所有历史剪切板记录和清空所有,   
有时候需要去各种地方去一次性复制很多东西, 然后一次性粘贴, 那这时就可以先清空历史然后一键粘贴所有了


# 截图和贴图

`shift+空格` 弹出菜单之后: 
- 按`tab`是截图
- 按`s`是贴图

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/snip_plus.gif)


# 屏幕边缘触发器hot-edge

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/hot_edge.gif)

- 你把鼠标放到左边缘, 然后滚轮, 你会发现可以调节音量
- 你把鼠标放到右边缘, 然后滚轮, 你会发现可以 向上翻页 / 向下翻页
- 放到显示器上边缘, 滚轮你会发现可以
    - 上边缘偏左: 可以 回到页面顶部 / 去页面底部
    - 上边缘偏右: 可以 向上翻页 / 向下翻页
- 放到屏幕下边缘, 滚轮则可以切换桌面
- 放到屏幕左边缘, 然后按鼠标中键则可以把当前窗口移到屏幕左边
- 放到屏幕右边缘, 然后按鼠标中键则可以把当前窗口移到屏幕右边


# 快捷键完全自定义

这个工具其实很重磅的功能是 `hotkey`
- 实现文本输入增强, 你可以通过 Capslock 键配合以下辅助按键实现大部分文本操作需求，不再需要在鼠标和键盘间来回切换
- 也可以自定义各种快捷键来触发各种动作, 比如为笔记本的触摸板的`三指点击`设定为快捷键`ctrl_8`, 然后就可以模拟鼠标按下不放的操作了, 达到类似mac的`三指拖动`的效果

可以类似vim一样的, 各种光标移动都十分方便, 比如
- `caps+e`是上
- `caps+h/j/k/l` 也可以来上下左右的
- `caps+d`是下
- `caps+s`是左, 比如`caps+alt+s`就是往左选中哈
- `caps+f`是右
- `caps+w`是选择当前单词
- `caps+c`是模拟`ctrl+c`
- `caps+r`是模拟`ctrl+y`
- `caps+v`是模拟`shift+insert`(终端爱好者的福音)
- `caps+逗号`是光标移动到最左边
- `caps+句号`是光标移动到最右边
- `caps+i`就是往左跳一个单词
- `caps+o`就是往右跳一个单词
- `caps+tab`就是整行缩进, 不管光标在当前行的任何地方
- `caps+alt+i`就是往左选中一个单词
- `caps+alt+o`就是往右选中一个单词
- `caps+backspace` : 删除光标所在行所有文字
- `capslock+enter` : 无论光标是否在行末都能新起一个换行而不截断原句子
- `capslock+alt+enter` : 无论光标是否在行末都能在上面新起一行而不截断原句子
- 加`alt`就是选中, 不加就是移动
- ...

默认配置概览: 

``` json
  "hotkey": {
    "enable": 1,
    "buildin": {
      "shift_space": "ShowSuxMenu",
      "capslock_c": "ctrl_c",
      "capslock_e": "up",
      "capslock_alt_e": "shift_up",
      "capslock_s": "left",
      "capslock_alt_s": "shift_left",
      "capslock_f": "right",
      "capslock_alt_f": "shift_right",
      "capslock_d": "down",
      "capslock_alt_d": "shift_down",
      "ctrl_8": "SimulateClickDown",
      "ctrl_shift_alt_m": "MaxMinWindow",
      "capslock_w": ["ctrl_left", "ctrl_shift_right"],
      "capslock_shift_w": ["home", "shift_end"],
      "capslock_`": "SwitchCapsState",
      "capslock_tab": ["home", "tab"],
      "capslock_v": "shift_ins",
      "capslock_shift_v": "shift_6",
      "capslock_r": "ctrl_y",
      "capslock_enter": "InsertLineBelow",
      "capslock_shift_enter": "InsertLineAbove",
      "capslock_backspace": ["home", "shift_end", "backspace"],
      "capslock_y": "shift_8",
      "capslock_alt_y": "shift_5",
      "capslock_u": "shift_1",
      "capslock_alt_u": "shift_2",
      "capslock_h": "left",
      "capslock_alt_h": "shift_left",
      "capslock_j": "down",
      "capslock_alt_j": "shift_down",
      "capslock_k": "up",
      "capslock_alt_k": "shift_up",
      "capslock_l": "right",
      "capslock_alt_l": "shift_right",
      "capslock_p": "shift_7",
      "capslock_alt_p": "shift_3",
      "capslock_i": "ctrl_left",
      "capslock_alt_i": "shift_ctrl_left",
      "capslock_o": "ctrl_right",
      "capslock_alt_o": "shift_ctrl_right",
      "capslock_9": "[",
      "capslock_alt_9": "{",
      "capslock_0": "]",
      "capslock_alt_0": "}",
      "capslock_n": "ctrl_bs",
      "capslock_alt_n": "shift_home_del",
      "capslock_m": "ctrl_del",
      "capslock_alt_m": "shift_end_del",
      "capslock_,": "home",
      "capslock_alt_,": "shift_home",
      "capslock_.": "end",
      "capslock_alt_.": "shift_end",
      "capslock_;": "_",
      "capslock_alt_;": "-",
      "capslock_'": "=",
      "capslock_alt_'": "shift_=",
      "capslock_/": "\\",
      "capslock_alt_/": "shift_\\"
    },
    "custom": {}
  }
```


# 文字替换器replace-text

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/replace_text.gif)

比如把`h/`替换为`http://`之类的, 配置可以自由定义, 已经选中文字则是只替换选中文字, 否则替换整行, 
默认配置如下: 

``` json
  "replace-text": {
    "enable": 1,
    "buildin": {
      "h/": "http://",
      "hs/": "https://",
      "qc@": "@qq.com",
      "gc@": "@gmail.com",
      "16@": "@163.com"
    },
    "custom": {}
  },
```  


# 文本变换器

经常写代码的朋友应该经常会有把驼峰命名的文本 转换为 蛇形命名文本之类的需求, 或者把小写的文本转为大写的需求

![](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/transform_text.gif)


# CMDs指令

* `cmd` : open a command prompt window on the current explorer path, 打开命令行窗口, 如果当前在文件管理器则打开后会立即进入当前文件管理器路径
* `git` : open a git bash window on the current explorer path, 打开git窗口, 如果当前在文件管理器则打开后会立即进入当前文件管理器路径
* `Everything` : 打开Everything, 如果已经选中了文字, 则直接用everything搜索此文字
* `sux` : sux official site


# 自定义配置

可以在托盘菜单里找到"编辑配置文件"的菜单的, 改了配置记得重启sux哈

配置编写规则: 
- action类型: 直接从下方的所有action里选即可
    - ShowSuxMenu
    - StartSuxAhkWithWin
    - MoveWindowToLeftSide
    - MoveWindowToRightSide
    - OpenFileExplorer
    - OpenActionCenter
    - CloseCurrentWindow
    - GoTop
    - GoBottom
    - GoBack
    - GoForward
    - LockPc
    - OpenTaskView
    - VolumeMute
    - VolumeUp
    - VolumeDown
    - GotoNextDesktop
    - GotoPreDesktop
    - RefreshTab
    - ReopenLastTab
    - GotoPreApp
    - JumpToPrevTab
    - JumpToNextTab
    - SwitchCapsState
    - SwitchInputMethodAndDeleteLeft
    - MaxMinWindow
    - MaxWindow
    - MinWindow
    - ReloadSux
    - SelectCurrentWord
    - SelectCurrentLine
    - InsertLineBelow
    - InsertLineAbove
    - DeleteCurrentLine
    - IndentCurrentLine
    - SimulateClickDown
- 发送的单个键盘操作: 比如要发送`shift+下` 就是`shift_down`
- 发送一段键盘操作序列, 比如要实现`caps
+w`选中当前单词, 首先得移动到词的左边, 然后往右选中单词, 则配置为: `"capslock_w": ["ctrl_left", "ctrl_shift_right"]`
- 一些特殊的热键定义对照表:
    - `lbutton:  左键单击 `
    - `rbutton:  右键单击 `
    - `mbutton: 中键单击`
    - `wheelup: 滚轮上滑`
    - `wheeldown: 滚轮下滑`
    - `hover: 悬停 `, 只能用在触发角的配置里
    - `doublehit_: 双击 `, 比如`doublehit_alt`表示双击`alt`
    - `triplehit_: 三击 `


<!-- # Features

* **personalized configuration** : u can modify `conf.user.json` to override all default configuration
* **hot edges** : `Ctrl+8` on the edge (useful for touchpad user, set 3 fingers click to `Ctrl+8`), see `conf.user.json`-`hot-edge`
* **hot corners** : just like mac hot cornes, see `conf.user.json`-`hot-corner`
* **web search** : just like Wox/Listary/Alfred, see `conf.user.json`-`search-plus`
* **enhanced capslock** : just like Capslock+, see `conf.user.json`-`capslock_plus`
* **work with Everything**
* **custom theme** : two default theme(dark/light), and u can add ur own theme, see `conf.user.json`-`theme`
* **screen capture**
* **disable win10 auto update**
* **start sux with windows**
* **custom command line**:  see `conf.user.json`-`command`
* **custom hotkey**:  see `conf.user.json`-`hotkey`
* **clipboard-plus**:  clipboard history -->
<!-- * **auto selection copy** : just like linux terminal -->
<!-- * **hot key to replace string** : copy this line (`my email is @@ “”  ‘’`) to address bar, then Capslock+Shift+F, now u know, see user_conf.ahk -->
<!-- * **game mode** : double Alt then input `game` -->
<!-- * **auto update when launch sux** : see `default_conf.ahk` : `auto_update_when_launch_sux` -->


# 设置Everything始终以运行次数排序

0. Everything设置如下:  
    * [ ] 保存设置和数据到%APPDATA%\Everything目录  
    * [x] 随系统自启动  
    * [x] 以管理员身份运行  
    * [x] Everything服务  
1. 退出Everything
2. 找到其配置文件 Everything.ini , 并在其文件末尾添加
    ```
    sort=Run Count
    sort_ascending=0
    always_keep_sort=1
    ```
3. 运行Everything



# 捐赠

捐赠! 让作者更有动力给sux加新功能! ^_^

- 微信
  - ![微信](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/donate_wechat.png)
- 支付宝
  - ![支付宝](https://github.com/no5ix/no5ix.github.io/blob/source/source/img/sux/donate_alipay.png)



# TODO List

<!-- - refractor HandleMouseOnEdges -->
<!-- - ini -->
<!-- - clipboard history -->
<!-- - 处理不要caps plus的逻辑 -->
<!-- - 托盘暂停 -->
<!-- - auto install ahk -->
<!-- - custom tray menu -->
<!-- - rshift issue -->
<!-- - git cmd not goto desktop -->
<!-- - check update -->
<!-- - add about sux version -->
<!-- - add donate page -->
<!-- - add icon -->
<!-- - hover tray icon display sux -->
<!-- - 短语替换 -->
<!-- - 同时搜两个 -->
<!-- - bug: 双屏tophalfleft -->
<!-- - caps + alt -->
<!-- - add ver to code -->
<!-- - limit mode notify in full screen app -->
<!-- - hot corner bug -->
<!-- - rshift bug -->
<!-- - theme dark/light tray menu -->
<!-- - search/replace conf key modify -->
<!-- - 最小化 -->
<!-- - TEST double rshift/single rshift exist together -->
<!-- - 点击了菜单之后双击alt没反应, 还得点击一下其他地方才有反应 -->
<!-- - 暗模式的其他gui的阴影不正常 -->
<!-- - add donate gui pic -->
<!-- - caps+f一键搜索并弹出菜单可选yd/gg等 -->
<!-- - 删除记录, 把多条复制记录一次性粘贴到目标窗口 -->
- smart selection 双引号, 括号内, 单引号内
<!-- - 清空clipboard有bug -->
<!-- - 单显示器 window mover 的menu没有disable -->
<!-- - conf 排列组合, 如 `["https://wyagd001.github.io/zh-cn/docs/AutoHotkey.htm", "Win"]` 或者 `["ctrl_9", "sleep", "ctrl_8"]` , 或者自动加上sleep -->
<!-- - 把conf里的`!`和`+`等的做一个转为`{alt}`的解析器, 方便新手配置 -->
<!-- - bug: 下划线出不来 -->
<!-- - 有空格的时候变换文本有bug, 还有比如 INI_SetCheckUpdatesOnStartup 变成AA_BB, 也有问题 -->
<!-- - select sth tips on menu top -->
<!-- - add google translate to search plus -->
<!-- - msgbox 标题改成sux -->
<!-- - add newbie tutorial -->
<!-- - hot corner/edge/capslock switcher to tray menu -->
- update chinese readme, add some gif/mp4
- add more action
<!-- - 出现在和鼠标同一个屏幕做成选项 -->
<!-- - 报一个bug，caps+q，q，用百度查询时，弹窗出现在另一个屏幕，因为我有2个显示器，建议设置一下默认的弹窗。
- 上述bug包括everything -->
<!-- - 独立贴图菜单 -->
<!-- - casplock + tab 2 tab -->
<!-- - 替换/历史剪切板也集成到菜单里 -->
<!-- - 看还有哪些编辑器里常用的操作如转为大写这类的可以做, 做成菜单 -->
<!-- - bug: 历史剪切板有些历史的开头莫名多出一个下划线 ; 经查是因为前面有空格或者tab -->
<!-- - bug: 历史剪切板粘贴之后, 顺序乱了 -->
<!-- - 默认配置的中键触发有问题, 各种win+left -->
<!-- - 菜单顺序应该和yaml一致 -->
<!-- - 重新整理conf -->
<!-- - donate width
- Capslock + Backspace（删除光标所在行所有文字）
- Capslock + Enter（无论光标是否在行末都能新起一个换行而不截断原句子） -->
<!-- - 截图后弹出贴图菜单 -->
<!-- - bug:截图后保存则再也无法贴图 -->
- trans gui change color to gray/ dpi / voice audio / soundmark encoding
- clip_plus support img
<!-- - 翻译如果没选, 则弹出提示没选 -->
<!-- - 弄个build看看拿得到ver么 -->
<!-- - 中文翻译 -->
<!-- - 弄个clip guard对象, 来处理 Send, {Blind}{Text}慢的问题 -->
<!-- - 即时光标在单词中间也能复制此单词的快捷键 -->
<!-- - unify all menu -->
<!-- - after copy from clip_plus mess up the order -->
<!-- - 支持command菜单 -->
<!-- - 支持url直接书写 -->
<!-- - 支持不输入任何东西则为官网 -->
<!-- - 截图贴图menu -->
<!-- - check update失败, 点击"取消"打开浏览器的时候有乱切换软件的bug -->
<!-- - 限制menu宽度 -->
<!-- - 看看caps+的词语替换如何做的 -->
<!-- - 改default的上下左右快捷键 -->
<!-- - 看怎么调用js -->
<!-- - suspend img -->
<!-- - 弄个有道翻译面板 -->
<!-- - fix check update -->
<!-- - click down 之后记得释放 -->
<!-- - 浏览器中, click down之后双击就没选中了 -->
<!-- - rshift双击和单击可以分开conf -->
- auto update
<!-- - fix bug: cant open conf.user.json with notepad -->
<!-- - refactor tray menu code -->
<!-- - fix lang logic: "Autorun" -> "Start with Windows" -->
<!-- - modify default conf: disable win auto update -->
<!-- - hot corner: check on same monitor  -->
<!-- - occasional: fix web search gui window lost caret - make caret center -->
- 失焦则销毁
<!-- - 第二个屏幕就显示sux在第二个屏幕上 -->
<!-- - fix default lang -->

<!-- - 增加可供用户扩展的脚本, 方便用户配置各种自定义action -->
<!-- - gitignore user conf -->
<!-- - start with win -->
- ext ahk
<!-- - auto compile -->
<!-- - fix 启动之后马上打开自动消失web-search窗口的bug: 已经找到, 是因为UpdateSuxImpl的锅 -->
<!-- - internal Everything -->


<!-- # 设置开机以管理员权限启动

1. 对“A.exe”创建快捷方式, 然后将这个快捷方式改名为“A” (不用改名为A.lnk, 因为windows的快捷方式默认扩展名就是lnk)
2. 右键这个快捷方式-> 高级，勾选用管理员身份运行； 
3. 新建“A.bat”文件，将这个快捷方式的路径信息写入并保存，如：
```
@echo off
start C:\Users\b\Desktop\A.lnk
```
4. 因为直接运行 A.bat 会有个窗口一闪而过, 所以新建个 A.vbs 来运行这个bat来避免这个窗口
```
createobject("wscript.shell").run "D:\A.bat",0
```
5. 打开“运行”输入“shell:startup”然后回车，然后将“A.vbs”剪切到打开的目录中 -->
