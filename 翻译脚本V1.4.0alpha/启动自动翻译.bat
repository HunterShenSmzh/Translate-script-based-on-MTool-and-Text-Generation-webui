@echo off
chcp 65001
echo 正在运行 自动翻译 脚本...
echo 使用kaggle平台在线翻译选1，本地翻译选2 
set /p platform="请输入使用的翻译平台(kaggle输入1，本地输入2)："
if /i "%platform%"=="1" goto online
if /i "%platform%"=="2" goto local
goto invalid

:online
set /p URL="请输入URL地址:"
echo 翻译日语请使用Sakura模型，翻译英语请使用Qwen模型 
set /p language="请输入需要被翻译的主要语言 (日语输入1，英语输入2)："
if /i "%language%"=="1" goto jp_online
if /i "%language%"=="2" goto en_online
goto invalid

:local
echo 翻译日语请使用Sakura模型，翻译英语请使用Qwen模型 
set /p language="请输入需要被翻译的主要语言 (日语输入1，英语输入2)："
if /i "%language%"=="1" goto jp_local
if /i "%language%"=="2" goto en_local
goto invalid

:jp_local
echo 正在运行translate_jp脚本...
cd %~dp0
python translate_jp.py http://127.0.0.1:5000
if errorlevel 1 (
    goto :end
)
echo 请务必检查翻译完成.json内的内容 
goto :end

:en_local
echo 正在运行translate_en脚本...
cd %~dp0
python translate_en.py http://127.0.0.1:5000
if errorlevel 1 (
    goto :end
)
echo 请务必检查翻译完成.json内的内容 
goto :end

:jp_online
echo 正在运行translate_kaggle_jp脚本...
cd %~dp0
python translate_kaggle_jp.py %URL%
if errorlevel 1 (
    goto :end
)
echo 请务必检查翻译完成.json内的内容 
goto :end

:en_online
echo 正在运行translate_kaggle_en脚本...
cd %~dp0
python translate_kaggle_en.py %URL%
if errorlevel 1 (
    goto :end
)
echo 请务必检查翻译完成.json内的内容 
goto :end

:invalid
echo 无效的输入
echo 请重新输入有效的内容
pause>nul
goto start

:end
pause

