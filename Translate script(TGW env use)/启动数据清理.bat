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

set /p replace_name="是否需要替换特殊名词？ 需要手动配置：内置参数/特殊名词替换.json(是输入1，否输入2)"
if /i "%replace_name%"=="1" goto replace
if /i "%replace_name%"=="2" goto language
goto invalid

:replace
echo 注意！！！替换特殊名词后会对ManualTransFile.json文件造成不可逆修改 
echo 如果想反悔，请务必重新导出ManualTransFile.json 
echo --------------------------------------------------------------------- 
echo 正在运行name_replace脚本...
cd %~dp0
python name_replace.py
goto language

:language
set /p language="请输入需要被翻译的主要语言 (日语输入1，英语输入2)："
if /i "%language%"=="1" goto jp
if /i "%language%"=="2" goto en
goto invalid

:jp
echo --------------------------------------------------------------------- 
echo 正在运行clean_jp脚本...
cd %~dp0
python clean_jp.py

if errorlevel 1 (
    goto :end
)

echo 日语清理完成
echo 注意 自动数据清理可能存在疏漏 请务必手动翻阅纠错
goto end

:en
echo --------------------------------------------------------------------- 
echo 正在运行clean_en脚本...
cd %~dp0
python clean_en.py

if errorlevel 1 (
    goto :end
)

echo 英语清理完成
echo 注意 自动数据清理可能存在疏漏 请务必手动翻阅纠错
goto end

:invalid
echo 无效的语言输入
echo 请重新输入有效的语言
pause>nul
goto start

:end
pause

