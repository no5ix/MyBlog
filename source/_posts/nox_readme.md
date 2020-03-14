---
title: An alternative to Alfred/Wox/Listary/Capslock+
date: 2020-01-09 22:09:39
tags:
- GitHub
- AutoHotKey
categories:
- GitHub
top: 1
---



[<i class="fa fa-fw fa-github fa-2x"></i>nox](https://github.com/no5ix/nox) 


An alternative to **Alfred**/**Wox**/**Listary**/**Capslock+** .

Inspired by Alfred/Wox/Listary/Public-AutoHotKey-Scripts/Capslock+/utools, thank u.


**. . .**<!-- more -->


# IMPORTANT
  
- Please run as administrator.
- Please run in 32-bit mode.(Open with AutoHotKey Unicode 32-bit)


# Features

- **personalized configuration** : u can modify user_conf.ahk to override the default configuration
- **hot edges** : right/middle mouse click or `Ctrl+8` on the edge (useful for touchpad user)
- **hot corners** : just like mac hot cornes
- **web search** : just like Wox/Listary/Alfred
- **enhanced capslock** : just like Capslock+
- **double click triggers** (include `Ctrl+8`/`right mouse`/`middle mouse`/`Capslock`/`Ctrl`/`Shift`) : see default_conf.ahk
- **auto selection copy** : just like linux terminal
- **custom theme.** : two default theme(dark/light), and u can add ur own theme
- **hot key to replace string** : copy this line (`my email is @@ “”  ‘’`) to address bar, then Capslock+Shift+U, now u know, see user_conf.ahk
- **screen capture** : `Capslock + C`
- **game mode** : double Alt then input `game`


# 设置开机以管理员权限启动

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
5. 打开“运行”输入“shell:startup”然后回车，然后将“A.vbs”剪切到打开的目录中


# 设置Everything始终以运行次数排序

0. Everything设置如下:  
    [x] 保存设置和数据到%APPDATA%\Everything目录  
    [x] 随系统自启动  
    [ ] 以管理员身份运行  
    [x] Everything服务  
    显示窗口快捷键: `Ctrl+Shift+Alt+E`
1. 退出Everything
2. 找到其配置文件 Everything.ini , 并在其文件末尾添加
    ```
    sort=Run Count
    sort_ascending=0
    always_keep_sort=1
    ```
3. 运行Everything
