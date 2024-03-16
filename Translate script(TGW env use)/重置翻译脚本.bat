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