@echo off
chcp 65001


echo ！！！！警告！！！！
echo ---------------------------------------------------------------------
echo 你正在试图完全重置脚本，运行当前程序将会自动删除所有脚本生成的，已经翻译或者未翻译的内容。
echo ---------------------------------------------------------------------
set /p reset="你确定要这么做么？（确定请输入1）"
if /i "%reset%"=="1" goto reset2
goto invalid

:reset2
echo ---------------------------------------------------------------------
echo 你正在试图完全重置脚本，运行当前程序将会自动删除所有脚本生成的，已经翻译或者未翻译的内容。这是二次确认，确认请输入2
echo ---------------------------------------------------------------------
echo 这是二次确认，你真的要这么做么？
set /p reset2="你确定要这么做么？（确定请输入2）"
if /i "%reset2%"=="2" goto reset3

:reset3
echo ---------------------------------------------------------------------
echo 正在运行reset脚本...
echo ---------------------------------------------------------------------
cd %~dp0
python reset.py
echo ---------------------------------------------------------------------
echo 重置完成！
goto end

:invalid
echo 无效的输入，退出中

:end
pause