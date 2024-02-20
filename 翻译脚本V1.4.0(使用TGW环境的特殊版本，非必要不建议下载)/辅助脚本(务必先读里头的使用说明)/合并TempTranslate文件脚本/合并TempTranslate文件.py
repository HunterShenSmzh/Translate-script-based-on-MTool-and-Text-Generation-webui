import os
import glob
import json
import sys

temp_translate_dir = 'TempTranslate'

if not os.path.exists(temp_translate_dir):
    print(f"TempTranslate文件夹不存在")
    sys.exit(1)

# 合并所有临时翻译文件
final_translations = {}
for filename in glob.glob(os.path.join(temp_translate_dir, '*.json')):
    with open(filename, 'r', encoding='utf-8') as file:
        final_translations.update(json.load(file))

# 保存最终的合并翻译文件
final_filename = '合并后.json'
with open(final_filename, 'w', encoding='utf-8') as file:
    json.dump(final_translations, file, ensure_ascii=False, indent=4)

print(f"合并后.json已经输出")