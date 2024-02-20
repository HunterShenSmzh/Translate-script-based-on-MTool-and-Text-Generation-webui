import json
import os


def is_empty(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return isinstance(data, dict) and not bool(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def replace_in_dict(obj, replacements):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_obj[k] = replace_in_dict(v, replacements)
        return new_obj
    elif isinstance(obj, list):
        return [replace_in_dict(item, replacements) for item in obj]
    elif isinstance(obj, str):
        return replace_text(obj, replacements)
    else:
        return obj


def replace_text(text, replacements):
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


# 目录
script_folder = os.path.dirname(os.path.abspath(__file__))
replacements_folder = os.path.join(script_folder, '内置参数')
replacements_file = os.path.join(replacements_folder, '特殊名词替换.json')
manual_trans_file = os.path.join(script_folder, 'ManualTransFile.json')

if is_empty(replacements_file):
    print("特殊名词替换文件内部为空，请手动配置")
    print("exiting")
else:
    if not os.path.exists(manual_trans_file):
        print("没找到ManualTransFile.json文件，请务必先从Mtool导出")
        print("Exiting")
    else:
        # 加载特殊名词
        replacements = load_json(os.path.join(replacements_folder, '特殊名词替换.json'))

        # 清理后的数据
        data_to_replace = load_json(manual_trans_file)

        # 进行替换
        replaced_data = replace_in_dict(data_to_replace, replacements)

        # 保存
        save_json(replaced_data, manual_trans_file)

        print("特殊名词替换任务完成。")
