@echo off
chcp 65001

set /p num="请输入每个文件内包含的条目数："

echo 正在运行分块脚本...
cd %~dp0
python 分块脚本.py %num%

pause