import os
import shutil


def delete_folder(folder_name):
    try:
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
            print(f"文件夹 '{folder_name}' 已成功删除。")
        else:
            print(f"文件夹 '{folder_name}' 不存在。")
    except OSError as e:
        print(f"删除文件夹 '{folder_name}' 时出现错误：{e}")


def delete_file(file_name):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"文件 '{file_name}' 已成功删除。")
        else:
            print(f"文件 '{file_name}' 不存在。")
    except OSError as e:
        print(f"删除文件 '{file_name}' 时出现错误：{e}")


def delete_files_with_prefix(prefix):
    try:
        files = os.listdir()
        for file in files:
            if file.startswith(prefix) and file.endswith('.json'):
                file_path = os.path.join(os.getcwd(), file)
                os.remove(file_path)
                print(f"文件 '{file}' 已成功删除。")
    except OSError as e:
        print(f"删除文件时出现错误：{e}")


delete_folder('TempTranslate')
delete_folder('备份')
delete_file('ManualTransFile.json')
delete_file('翻译错误.json')
delete_file('翻译完成.json')
delete_files_with_prefix('清理后的数据')
