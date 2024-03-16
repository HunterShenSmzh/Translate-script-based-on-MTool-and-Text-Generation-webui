import os
import shutil
import glob
import json
import sys


# 文件夹重命名
def rename_folder(old_name, new_name):
    if os.path.exists(new_name):
        index = 1
        while True:
            new_name_with_index = f"{new_name}_{index}"
            if not os.path.exists(new_name_with_index):
                new_name = new_name_with_index
                break
            index += 1

    os.rename(old_name, new_name)


# 文件重命名
def rename_file(old_file_name, new_file_name, directory=None):
    if directory:
        old_file_path = os.path.join(directory, old_file_name)
        new_file_path = os.path.join(directory, new_file_name)
    else:
        old_file_path = old_file_name
        new_file_path = new_file_name
    if os.path.exists(new_file_path):
        file_name, file_extension = os.path.splitext(new_file_path)
        index = 1
        while True:
            new_file_name_with_index = f"{file_name}_{index}{file_extension}"
            if not os.path.exists(new_file_name_with_index):
                new_file_path = new_file_name_with_index
                break
            index += 1

    os.rename(old_file_path, new_file_path)


# 合并TempTranslate
def merge_translate_files(temp_translate_dir, final_filename):
    if not os.path.exists(temp_translate_dir):
        print(f"{temp_translate_dir}文件夹不存在")
        sys.exit(1)

    # 合并所有临时翻译文件
    final_translations = {}
    for filename in glob.glob(os.path.join(temp_translate_dir, '*.json')):
        with open(filename, 'r', encoding='utf-8') as file:
            final_translations.update(json.load(file))

    # 保存最终的合并翻译文件
    with open(final_filename, 'w', encoding='utf-8') as file:
        json.dump(final_translations, file, ensure_ascii=False, indent=4)

    print(f"{final_filename}已经输出")


# 剔除
def exclude_translated_content(translated_file_path, original_file_path, output_file_path):
    # 读取要剔除内容
    with open(translated_file_path, 'r', encoding='utf-8') as translated_file:
        translated_content = json.load(translated_file)

    # 读取原始内容
    with open(original_file_path, 'r', encoding='utf-8') as original_file:
        original_content = json.load(original_file)

    # 比较两个文件的键，并剔除已翻译的内容
    untranslated_content = {key: value for key, value in original_content.items() if key not in translated_content}

    # 将未翻译的内容写入新文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(untranslated_content, output_file, ensure_ascii=False, indent=4)

    print(f"{output_file_path}已输出")


def main():
    # 检查TempTranslate文件夹
    if os.path.exists('TempTranslate'):
        print("TempTranslate文件夹存在")
        folder_path = os.path.join("TempTranslate")
        if os.listdir(folder_path):
            print("TempTranslate文件夹内部不为空")
        else:
            print("TempTranslate文件夹内部为空")
            print("翻译并未开始，无法继续")
            return

    else:
        print("TempTranslate文件夹不存在")
        print("翻译并未开始，无法继续")
        return

    # 检查紧急弹出备份 判断是否正常退出
    if os.path.exists('紧急弹出备份'):
        print("紧急弹出备份已经生成，无需合并TempTranslate")
        folder_path = os.path.join("紧急弹出备份")
        translate_error = os.path.join(folder_path,'断点备份-翻译错误.json')
        translate_completed = os.path.join(folder_path, '断点备份-翻译完成.json')
        translate_incomplete = os.path.join(folder_path, '断点备份-中断部分.json')
        if not os.path.exists(translate_completed):
            print("未检测到断点备份-翻译完成.json。继续失败，请手动检查紧急弹出备份文件完整性。")
            return
        if not os.path.exists(translate_incomplete):
            print("未检测到断点备份-中断部分.json。继续失败，请手动检查紧急弹出备份文件完整性。")
            return
        if not os.path.exists(translate_error):
            print("未检测到断点备份-翻译错误.json。继续失败，请手动检查紧急弹出备份文件完整性。")
            return
        # 移动断点备份-中断部分
        print("正在移动 断点备份-中断部分.json 至主目录 并进行重新命名")
        current_dir = os.getcwd()
        shutil.copy(translate_incomplete, current_dir)
        rename_file('清理后的数据.json', '清理后的数据-old.json')
        os.rename('断点备份-中断部分.json', '清理后的数据.json')
        print("移动完成 正在创建备份文件夹")
        if not os.path.exists('备份'):
            os.makedirs('备份')
        backup = os.path.join(os.path.join("备份"))
        shutil.copy(translate_error,backup)
        shutil.copy(translate_completed, backup)
        rename_file('断点备份-翻译完成.json', '翻译完成备份.json', '备份')
        rename_file('断点备份-翻译错误.json', '翻译错误备份.json', '备份')
        shutil.rmtree(folder_path)
        print("清理后的数据已经自动生成，可以正常继续")
        return

    else:
        print("紧急弹出备份未生成，需要合并TempTranslate")
        print("合并中")
        merge_translate_files('TempTranslate', '翻译完成.json')
        # 复制翻译完成至备份内部
        if not os.path.exists('备份'):
            os.makedirs('备份')
        translate_complete = os.path.join(os.getcwd(), '翻译完成.json')
        backup = os.path.join(os.path.join("备份"))
        shutil.copy(translate_complete,  backup)
        rename_file('翻译完成.json', '翻译完成备份.json', '备份')
        print("执行剔除")
        exclude_translated_content('翻译完成.json', '清理后的数据.json', '剔除完成.json')
        rename_file('清理后的数据.json', '清理后的数据-old.json')
        os.rename('剔除完成.json', '清理后的数据.json')
        print("清理后的数据已经自动生成，可以正常继续")
        return


if __name__ == "__main__":
    main()
