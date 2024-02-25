import json
import os


def is_empty(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return isinstance(data, dict) and not bool(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return False


script_folder = os.path.dirname(os.path.abspath(__file__))
replacements_file = os.path.join(script_folder, '特殊名词替换.json')

if is_empty(replacements_file):
    print("特殊名词替换文件内部为空，请手动配置")
    print("exiting")
else:
    with open('替换字典.json', 'r', encoding='utf-8') as file:
        replacement_dict = json.load(file)

    with open('原文.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    for old_text, new_text in replacement_dict.items():
        content = content.replace(old_text, new_text)

    with open('原文.txt', 'w', encoding='utf-8') as file:
        file.write(content)

print("特殊名词替换任务完成。")
