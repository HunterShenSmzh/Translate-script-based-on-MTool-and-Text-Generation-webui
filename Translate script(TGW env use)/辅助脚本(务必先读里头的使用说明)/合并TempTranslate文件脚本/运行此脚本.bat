@echo off
chcp 65001
cd /D "%~dp0"
set PATH=%PATH%;%SystemRoot%\system32
echo "%CD%"| findstr /C:" " >nul && echo 路径中不能有空格 && goto end
set TMP=..\..\..\text-generation-webui\installer_files
set TEMP=..\..\..\text-generation-webui\installer_files
(call conda deactivate && call conda deactivate && call conda deactivate) 2>nul
set CONDA_ROOT_PREFIX=..\..\..\text-generation-webui\installer_files\conda
set INSTALL_ENV_DIR=..\..\..\text-generation-webui\installer_files\env
set PYTHONNOUSERSITE=1
set PYTHONPATH=
set PYTHONHOME=
set "CUDA_PATH=%INSTALL_ENV_DIR%"
set "CUDA_HOME=%CUDA_PATH%"
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo Miniconda hook not found. && goto end )

echo 正在运行合并脚本...
cd %~dp0
python 合并TempTranslate文件.py

pause

:end
pause