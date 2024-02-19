@echo off
chcp 65001

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python不存在，请先运行安装。
) else (
    echo Python已安装，版本信息如下：
    python --version
    echo 安装pip中，请稍等……
    python -m ensurepip --upgrade
    echo 安装requests中，请稍等……
    pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo 安装完成，请检查安装过程是否有报错，如有报错请务必加群发送报错，qq群719518427
)

pause