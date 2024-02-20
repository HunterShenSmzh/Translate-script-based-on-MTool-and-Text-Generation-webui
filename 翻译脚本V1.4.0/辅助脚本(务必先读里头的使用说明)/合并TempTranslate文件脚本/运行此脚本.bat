@echo off
chcp 65001

echo 正在运行合并脚本...
cd %~dp0
python 合并TempTranslate文件.py

pause