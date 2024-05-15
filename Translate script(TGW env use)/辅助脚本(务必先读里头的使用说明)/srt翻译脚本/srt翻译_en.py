import requests
import time
import sys
import os
import re

if len(sys.argv) != 2:
    print("必须填入api地址")
    sys.exit(1)
APIURL = sys.argv[1] + "/v1/chat/completions"

if not os.path.exists("原文.srt"):
    print(f"原文.srt不存在")
    sys.exit(1)

# 上下文历史记录列表
dialogue_history = []


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")
    # 输出换行
    if iteration == total:
        print()


def update_dialogue_history(value_update, translation_update):
    if len(dialogue_history) >= 10:  # 保持5轮对话
        dialogue_history.pop(0)  # 移除最早的user消息
        dialogue_history.pop(0)  # 移除最早的assistant消息
    dialogue_history.extend([
        {"role": "user", "content": f"这里是你需要翻译的文本：{value_update}"},
        {"role": "assistant", "content": translation_update}
    ])


def translate_text(text, temperature=0.6, frequency_penalty=0.0):
    attempts = 0
    max_attempts = 5
    last_exception = None
    while attempts < max_attempts:
        try:
            url = APIURL
            example = [
                {"role": "user",
                 "content": "将下面的英文文本翻译成中文：Hello"},
                {"role": "assistant", "content": "你好"},
                {"role": "user",
                 "content": "将下面的英文文本翻译成中文：「Is everything alright?」"},
                {"role": "assistant", "content": "「一切都还好么？」"}
            ]
            messages = [{"role": "user", "content": f"将下面的英文文本翻译成中文：{text}"}]
            # 包含上下文历史记录
            payload = {
                "messages": example + dialogue_history + messages,
                "max_tokens": 150,
                "temperature": temperature,
                "mode": "instruct",
                "instruction_template": "ChatML",
                "frequency_penalty": frequency_penalty,
                "negative_prompt": "你是一个英文翻译模型，可以流畅通顺地将英文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
                "stop": ["\n###", "\n\n", "[PAD151645]", "<|im_end|>"]
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                translated_text = response.json()['choices'][0]['message']['content'].strip()

                # 更新历史记录
                update_dialogue_history(text, translated_text)
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


def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'(\d+)\n(\d{1,2}:\d{2}:\d{2},\d{3} --> \d{1,2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)

    srt_data = []
    for match in matches:
        srt_data.append({
            'index': int(match[0]),
            'timestamp': match[1],
            'text': match[2].replace('\n', ' ')
        })

    return srt_data


def write_srt(srt_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for entry in srt_data:
            file.write(f"{entry['index']}\n")
            file.write(f"{entry['timestamp']}\n")
            file.write(f"{entry['text']}\n\n")


def translate_srt(file_path, output_path):
    srt_data = read_srt(file_path)
    total_entries = len(srt_data)
    translated_srt_data = []

    try:
        for i, entry in enumerate(srt_data, start=1):
            text = entry['text']
            print('\n')
            print(f'正在翻译 {i}/{total_entries}：\n{text}')
            translated_text = translate_text(entry['text'])

            # 检查翻译结果长度
            if len(translated_text) > len(text) + 50:
                print(f"对 {text} 的翻译未达标，正在尝试重新翻译...")
                time.sleep(0.05)
                retry_translate_text = translate_text(text, temperature=0.1, frequency_penalty=0.15)
                if len(retry_translate_text) > len(text) + 50:
                    print(f"对 {text} 的重新翻译仍未达标，保留原文")
                    translated_text = text
                else:
                    translated_text = retry_translate_text

            print(f'翻译完成：\n{translated_text}')
            entry['text'] = translated_text
            translated_srt_data.append(entry)
            print_progress_bar(i, total_entries, prefix='翻译进度:', suffix='完成')

    except Exception as e:
        print(e)
        # 保存已翻译的部分
        write_srt(translated_srt_data, '翻译完成.srt')
        # 保存未翻译的部分
        remaining_srt_data = srt_data[len(translated_srt_data):]
        write_srt(remaining_srt_data, '断点记录.srt')
        return

    # 全部翻译完成后保存
    write_srt(translated_srt_data, output_path)
    print("翻译完成")


input_srt = '原文.srt'
output_srt = '翻译完成.srt'
translate_srt(input_srt, output_srt)
