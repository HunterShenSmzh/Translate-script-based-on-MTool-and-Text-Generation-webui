import json
import re
import os
import sys
import unicodedata

raw_data = "ManualTransFile.json"

# 检查原始数据是否存在
if not os.path.exists(raw_data):
    print(f"文件 {raw_data} 不存在，请先将MTool导出的文本放置到当前目录")
    sys.exit(1)


def clean_json(input_file_path, dictionary_file_path, output_file_path):
    # 读取字典文件
    with open(dictionary_file_path, 'r', encoding='utf-8') as file:
        removal_dict = json.load(file)

    # 读取原始 JSON 文件
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 准备用于匹配不同规则的正则表达式
    number_pattern = re.compile(r'^\d+$')  # 匹配仅包含数字
    numbers_comma_pattern = re.compile(r'^[\d,]+$')  # 匹配仅包含数字和逗号
    operators_only_pattern = re.compile(r'^[\+\-\*/=]+$')  # 匹配仅包含运算符号
    punctuation_only_pattern = re.compile(r'^[\,\.\;\_\-\*\/\+=]+$')  # 匹配仅包含标点字符的组合

    # 新的字典，用于存储清理后的数据
    new_data = {}

    for key, value in data.items():
        # 将值中的全角转成半角
        value = unicodedata.normalize('NFKC', value)

        # 检查键是否在移除字典中或符合保留条件
        if key not in removal_dict and not (number_pattern.match(key) or numbers_comma_pattern.match(key) or
                                            operators_only_pattern.match(key) or punctuation_only_pattern.match(key)):
            new_data[key] = value

    # 将清理后的数据写入到新文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)

    return new_data


# 文件路径
input_file_path = 'ManualTransFile.json'  # 原始数据文件
dictionary_file_path = '内置参数/屏蔽字典.json'  # 字典文件
output_file_path = '清理后的数据.json'  # 清理后数据的保存路径

# 使用脚本
cleaned_data = clean_json(input_file_path, dictionary_file_path, output_file_path)
print(cleaned_data)
