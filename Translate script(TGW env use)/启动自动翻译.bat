@echo off
chcp 65001
cd /D "%~dp0"
set PATH=%PATH%;%SystemRoot%\system32
echo "%CD%"| findstr /C:" " >nul && echo 路径中不能有空格 && goto end
set TMP=..\text-generation-webui\installer_files
set TEMP=..\text-generation-webui\installer_files
(call conda deactivate && call conda deactivate && call conda deactivate) 2>nul
set CONDA_ROOT_PREFIX=..\text-generation-webui\installer_files\conda
set INSTALL_ENV_DIR=..\text-generation-webui\installer_files\env
set PYTHONNOUSERSITE=1
set PYTHONPATH=
set PYTHONHOME=
set "CUDA_PATH=%INSTALL_ENV_DIR%"
set "CUDA_HOME=%CUDA_PATH%"
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo Miniconda hook not found. && goto end )

:start
echo 是否是继续翻译？
set /p continue="是否是继续翻译？(是输入1，否输入2)"
if /i "%continue%"=="1" goto continue_True
if /i "%continue%"=="2" goto continue_False
goto invalid

:continue_True
echo 正在运行 auto_continue 脚本...
python auto_continue.py
goto continue_False

:continue_False
echo 正在运行 自动翻译 脚本...
echo 使用kaggle平台在线翻译选1，本地翻译选2
set /p platform="请输入使用的翻译平台(kaggle输入1，本地输入2)："
if /i "%platform%" NEQ "1" if /i "%platform%" NEQ "2" goto invalid

echo 翻译日语请使用Sakura模型，翻译英语请使用Qwen模型
set /p language="请输入需要被翻译的主要语言 (日语输入1，英语输入2)："
if /i "%language%" NEQ "1" if /i "%language%" NEQ "2" goto invalid

if /i "%platform%"=="1" set "platform_type=online"
if /i "%platform%"=="2" set "platform_type=local"

if /i "%language%"=="1" set "language_model=jp"
if /i "%language%"=="2" set "language_model=en"

if /i "%platform_type%"=="online" set /p URL="请输入URL地址:"

if /i "%platform_type%"=="local" (
    goto ask_model_type
)

call :translate_%language_model%_%platform_type%
goto end

:ask_model_type
echo 是否使用1b8模型翻译
set /p model="是或否(是输入1，否输入2)："
if /i "%model%"=="1" (
    set "model_type=1b8"
) else if /i "%model%"=="2" (
    set "model_type=standard"
) else (
    echo 无效的输入，请输入1或2.
    goto ask_model_type
)
goto translate_local

:translate_jp_online
echo 正在运行translate_kaggle_jp脚本...
goto translate_script

:translate_en_online
echo 正在运行translate_kaggle_en脚本...
goto translate_script

:translate_local
if "%language_model%"=="jp" if "%model_type%"=="1b8" (
    echo 正在运行translate_jp_1b8脚本...
    python translate_jp_1b8.py http://127.0.0.1:5000
) else if "%language_model%"=="jp" (
    echo 正在运行translate_jp脚本...
    python translate_jp.py http://127.0.0.1:5000
)

if "%language_model%"=="en" if "%model_type%"=="1b8" (
    echo 正在运行translate_en_1b8脚本...
    python translate_en_1b8.py http://127.0.0.1:5000
) else if "%language_model%"=="en" (
    echo 正在运行translate_en脚本...
    python translate_en.py http://127.0.0.1:5000
)
goto end

:translate_script
cd %~dp0
if /i "%language_model%"=="jp" if /i "%platform_type%"=="local" python translate_jp.py http://127.0.0.1:5000
if /i "%language_model%"=="en" if /i "%platform_type%"=="local" python translate_en.py http://127.0.0.1:5000
if /i "%language_model%"=="jp" if /i "%platform_type%"=="online" python translate_kaggle_jp.py %URL%
if /i "%language_model%"=="en" if /i "%platform_type%"=="online" python translate_kaggle_en.py %URL%
if errorlevel 1 goto end
echo 请务必检查翻译完成.json内的内容
goto end

:invalid
echo 无效的输入，请重新输入有效的内容。
pause
goto start

:end
echo 执行完成。
pause

