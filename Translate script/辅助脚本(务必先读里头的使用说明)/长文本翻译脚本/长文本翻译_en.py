import requests
import time
import sys
import os

if len(sys.argv) != 2:
    print("必须填入api地址")
    sys.exit(1)
APIURL = sys.argv[1] + "/v1/chat/completions"

if not os.path.exists("原文.txt"):
    print(f"原文.txt不存在")
    sys.exit(1)


def translate_text(text, temperature=0.2, frequency_penalty=0.0):
    attempts = 0
    max_attempts = 5
    last_exception = None
    while attempts < max_attempts:
        try:
            url = APIURL
            prompt_with_text = f"将下面的英文文本翻译成中文：{text}"
            messages = [{"role": "user", "content": prompt_with_text}]
            payload = {
                "messages": messages,
                "max_tokens": 1024,
                "temperature": temperature,
                "mode": "instruct",
                "instruction_template": "ChatML",
                "frequency_penalty": frequency_penalty,
                "negative_prompt": "你是一个英文轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将英文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
                "stop": ["\n###", "\n\n", "[PAD151645]", "<|im_end|>"]
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                translated_text = response.json()['choices'][0]['message']['content'].strip()
                return translated_text
            else:
                attempts += 1
                time.sleep(1)
        except Exception as e:
            print(f"尝试 {attempts + 1}/{max_attempts} 次失败: {e}")
            attempts += 1
            time.sleep(1)
            last_exception = e
    print(f"API调用出错: {last_exception}")
    raise Exception(f"API调用连续失败{max_attempts}次，停止脚本。")


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")
    # 输出换行
    if iteration == total:
        print()


def read_novel(filename_txt):
    encodings = ['utf-8', 'shift_jis', 'gbk', 'big5']
    for encoding in encodings:
        try:
            with open(filename_txt, 'r', encoding=encoding) as file:
                content = file.read()
            return content
        except UnicodeDecodeError:
            continue
    raise ValueError(f'解码失败 {filename_txt} ')


def split_paragraphs(text):
    paragraphs = text.split('\n')
    combined_paragraphs = []
    current_paragraph = ""

    for paragraph in paragraphs:
        if not paragraph.strip():
            if current_paragraph:
                combined_paragraphs.append(current_paragraph)
                current_paragraph = ""  # 重置累积段落
            combined_paragraphs.append("")  # 分隔
        else:
            # 合并逻辑
            if len(current_paragraph + '\n' + paragraph) < 600:
                current_paragraph += ('\n' + paragraph if current_paragraph else paragraph)
            else:
                if not current_paragraph:
                    current_paragraph = paragraph
                else:
                    combined_paragraphs.append(current_paragraph)
                    current_paragraph = paragraph

    # 添加最后累积的段落
    if current_paragraph:
        combined_paragraphs.append(current_paragraph)

    return combined_paragraphs


def main(filename_main):
    novel_content = read_novel(filename_main)
    paragraphs = split_paragraphs(novel_content)

    translated_paragraphs = []
    total_paragraphs = len(paragraphs)
    try:
        for i, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                translated_paragraphs.append(paragraph)
            else:
                print('\n')
                print(f'正在翻译：\n{paragraph}')
                translated_text = translate_text(paragraph)
                print('\n')
                print(f'翻译完成：\n{translated_text}')
                if translated_text:
                    translated_paragraphs.append(translated_text)
                else:
                    print("翻译失败，跳过该段落。")
                    translated_paragraphs.append(paragraph)  # 保留原文以防万一
            print_progress_bar(i + 1, total_paragraphs, prefix='进度:', suffix='完成', length=50)
    except Exception as e:
        print(e)
        with open('翻译完成.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(translated_paragraphs))
        with open('断点记录.txt', 'w', encoding='utf-8') as file:
            remaining_paragraphs = paragraphs[len(translated_paragraphs):]
            file.write('\n'.join(remaining_paragraphs))
        return

    with open('翻译完成.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(translated_paragraphs))
        print("翻译完成")


if __name__ == "__main__":
    filename = "原文.txt"  # 替换为你的小说文件名
    main(filename)
