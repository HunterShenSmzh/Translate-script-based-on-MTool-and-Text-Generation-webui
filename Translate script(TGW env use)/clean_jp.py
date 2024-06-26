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
    english_pattern = re.compile(r'^[a-zA-Z]+$')  # 匹配仅包含英文字母
    numbers_comma_pattern = re.compile(r'^[\d,]+$')  # 匹配仅包含数字和逗号
    letters_punctuation_pattern = re.compile(r'^[a-zA-Z\,\._]+$')  # 匹配包含英文字母和标点字符
    mixed_pattern = re.compile(r'^[a-zA-Z0-9\,\._; ]+$')  # 匹配包含英文字母、数字和标点字符的组合
    num_letters_operators_pattern = re.compile(r'^[\d\+\-\*/a-zA-Z ]+$')  # 匹配数字、字母和运算符号的组合
    operators_only_pattern = re.compile(r'^[\+\-\*/=]+$')  # 匹配仅包含运算符号
    letters_operators_pattern = re.compile(r'^[a-zA-Z\+\-\*/ ]+$')  # 匹配字母和运算符号的组合
    operators_letters_punctuation_pattern = re.compile(r'^[a-zA-Z\+\-\*/\,\._; ]+$')  # 匹配运算符号、字母和标点字符的组合
    punctuation_only_pattern = re.compile(r'^[\,\.\;\_\-\*\/\+=]+$')  # 匹配仅包含标点字符的组合
    slash_letters_numbers_punctuation_pattern = re.compile(r'^[a-zA-Z0-9\\,\.\;\_\-\*\/\+=]+$')  # 匹配包含反斜杠、字母、数字和标点字符的组合
    letters_space_pattern = re.compile(r'^[a-zA-Z ]+$')  # 匹配包含字母和空格的组合
    letters_space_operators_pattern = re.compile(r'^[a-zA-Z \+\-\*/]+$')  # 匹配包含字母、空格和运算符号的组合
    letters_space_punctuation_pattern = re.compile(r'^[a-zA-Z \,\.\;\_\-\*\/\+=]+$')  # 匹配包含字母、空格和标点符号的组合
    kanji_pattern = re.compile(r'^[\u4e00-\u9fff]+$')  # 匹配仅包含汉字
    japanese_pattern = re.compile(r'[\u3040-\u3096\u30A0-\u30FF\u4E00-\u9FFF\u31F0-\u31FF]+')  # 匹配包含日文字符

    # 新的字典，用于存储清理后的数据
    new_data = {}

    for key, value in data.items():
        # 将值中的全角转成半角
        value = unicodedata.normalize('NFKC', value)

        # 检查键是否在字典文件中或符合保留条件
        if key not in removal_dict and japanese_pattern.search(key) and not (
                kanji_pattern.match(key) or number_pattern.match(key) or english_pattern.match(key) or
                numbers_comma_pattern.match(key) or letters_punctuation_pattern.match(key) or
                mixed_pattern.match(key) or num_letters_operators_pattern.match(key) or
                operators_only_pattern.match(key) or letters_operators_pattern.match(key) or
                operators_letters_punctuation_pattern.match(key) or punctuation_only_pattern.match(key) or
                slash_letters_numbers_punctuation_pattern.match(key) or letters_space_pattern.match(key) or
                letters_space_operators_pattern.match(key) or letters_space_punctuation_pattern.match(key)):
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
