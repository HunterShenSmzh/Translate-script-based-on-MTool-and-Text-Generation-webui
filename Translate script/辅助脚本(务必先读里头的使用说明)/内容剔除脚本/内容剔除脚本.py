import json
import os
import sys

# 检查清理后的数据是否存在
if not os.path.exists("剔除.json"):
    print(f"文件 剔除.json不存在")
    sys.exit(1)

# 检查清理后的数据是否存在
if not os.path.exists("原文.json"):
    print(f"文件 原文.json不存在")
    sys.exit(1)

# 读取要剔除内容
with open('剔除.json', 'r', encoding='utf-8') as translated_file:
    translated_content = json.load(translated_file)

# 读取倍剔除内容
with open('原文.json', 'r', encoding='utf-8') as original_file:
    original_content = json.load(original_file)

# 比较两个文件的键，并剔除已翻译的内容
untranslated_content = {key: value for key, value in original_content.items() if key not in translated_content}

# 将未翻译的内容写入新文件
with open('剔除完成.json', 'w', encoding='utf-8') as output_file:
    json.dump(untranslated_content, output_file, ensure_ascii=False, indent=4)

print("已保存至'剔除完成.json'")
