import json
import os
import sys
import glob

# 检查清理后的数据是否存在
if not os.path.exists("清理后的数据.json"):
    print(f"清理后的数据.json不存在")
    sys.exit(1)
def split_data(input_file, output_dir, items_per_file):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 清理输出目录
    if os.path.exists(output_dir):
        files = glob.glob(os.path.join(output_dir, '*.json'))
        for f in files:
            os.remove(f)

    # 读取JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 确保是字典
    if not isinstance(data, dict):
        raise ValueError("数据文件不是字典格式")

    # 拆分数据
    items = list(data.items())
    for i in range(0, len(items), items_per_file):
        # 创建分块
        chunk = dict(items[i:i + items_per_file])
        chunk_file_name = f"分块{int(i / items_per_file) + 1}.json"
        chunk_file_path = os.path.join(output_dir, chunk_file_name)

        # 保存
        with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
            json.dump(chunk, chunk_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file = '清理后的数据.json'
    output_dir = '拆分后'
    items_per_file = 500  # 默认500条目

    if len(sys.argv) > 1:
        try:
            items_per_file = int(sys.argv[1])
        except ValueError:
            print("请提供一个有效的整数")
            sys.exit(1)

    split_data(input_file, output_dir, items_per_file)

print(f"拆分完成")
