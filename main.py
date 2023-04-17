# Copyright (C) 2023 notoxicpeople


import glob
import json
import os
import subprocess
import sys

import openai
import requests


# 音声ファイル文字起こし（->WAVファイル検索->音声ファイル読み込み->文字起こし）
# 入力ファイル名: audio/元ファイル名.wav
# 出力ファイル名: translated/元ファイル名.txt
def audio_to_text(dir_path):
    # WAVファイル検索
    audio_files = glob.glob(os.path.join(dir_path, "*.wav"))

    # 各ファイルを読み込む
    for audio_file in sorted(audio_files):
        print(f"読み込んだファイル: {audio_file}")

        # コマンドラインでwhisperを実行
        cmd = "whisper " + audio_file + " --language English --model tiny --task translate --output_dir " + dir_path

        # whisperの実行結果を取得
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)


# ->英訳（->txtファイル検索->txtファイル読み込み->英訳->txtファイル出力）
# 入力ファイル名: txt/元ファイル名.txt
# 出力ファイル名: translated/元ファイル名.txt
def translate_text(dir_path):
    # txtファイル検索
    txt_files = glob.glob(os.path.join(dir_path, "*.txt"))

    # 各ファイルを読み込む
    for txt_file_path in sorted(txt_files):
        # ファイルを読み込む
        with open(txt_file_path, "r", encoding="utf-8") as f:
            input_text = f.read()

        # テキストを翻訳する
        translated_text = translate_text(input_text, deepl_api_key)

        if translated_text is not None:
            # 翻訳されたテキストを出力ファイルに保存する
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print("翻訳が完了しました。出力ファイル:", output_file)
        else:
            print("翻訳に失敗しました。")
    print()


# ->分割（->txtファイル検索->txtファイル読み込み->分割->txtファイル出力）
# 入力ファイル名: translated/元ファイル名.txt
# 出力ファイル名: split/元ファイル名分割アルファベット.txt
def split_txt(txt_file_path, dir_path):
    print()


# ->要約（->txtファイル検索->txtファイル読み込み->要約->txtファイル出力）
# 入力ファイル名: split/元ファイル名分割アルファベット.txt
# 出力ファイル名: summary/元ファイル名分割アルファベット.txt
def summary_txt(txt_file_path, dir_path):
    print()


def main(dir_path, mode):
    try:
        # 音声ファイルから要約を作成
        if mode == "audio":
            # WAVファイルを検索
            audio_files = glob.glob(os.path.join(dir_path, "*.wav"))

            # 各ファイルを読み込む
            for audio_file in sorted(audio_files):
                print(f"読み込んだファイル: {audio_file}")

                # コマンドラインでwhisperを実行
                cmd = "whisper " + audio_file + " --language English --model tiny --task translate --output_dir " + dir_path

                # whisperの実行結果を取得
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

                # ファイル名変数をwavからtxtへ変換
                txt_file_path = wav_to_txt_filepath(audio_file)

                # 文字起こししたファイルを要約
                summary_txt(txt_file_path, dir_path)

        # 文字起こしファイルから要約を作成
        if mode == "text":
            # txtファイルを検索
            txt_files = glob.glob(os.path.join(dir_path, "*.txt"))

            # 各ファイルを読み込む
            for txt_file_path in sorted(txt_files):
                summary_txt(txt_file_path, dir_path)

            # 分析：仮説との差異、検証として不十分な点、導かれる新たな仮説、深堀り対象の人を決定する、提供価値、機能、ペルソナの深堀り
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"Error occurred: {e}")


def translate():
    # 入力ファイル名
    input_file = "input.txt"
    # 出力ファイル名
    output_file = "out_" + os.path.splitext(input_file)[0] + ".txt"

    # 入力ファイルを開く
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    # テキストを翻訳する
    translated_text = translate_text(input_text, deepl_api_key)

    if translated_text is not None:
        # 翻訳されたテキストを出力ファイルに保存する
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated_text)
        print("翻訳が完了しました。出力ファイル:", output_file)
    else:
        print("翻訳に失敗しました。")


def translate_text(text, api_key):
    url = "https://api.deepl.com/v2/translate"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "auth_key": api_key,
        "text": text,
        "target_lang": "EN",
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        return result["translations"][0]["text"]
    else:
        print("Error: Translation request failed")
        return None


def summary_txt(txt_file_path, dir_path):
    file_name = os.path.basename(txt_file_path).split('.')[0]

    # ファイルを分割
    cmd2 = "split -b 200 " + txt_file_path + " " + dir_path + "/out_" + file_name
    result = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    # 分割ファイルの読み取り
    prefix = 'out_' + file_name
    txt_list = read_files_with_prefix(dir_path, prefix)

    for txt in txt_list:
        # プロンプト
        prompt = txt["content"] + \
                 " 以上のインタビューについて、step-by-stepで文章の意味を解釈し，足りない言葉を文脈から保管し，日本語の話者にわかりやすいように，語順を入れ替えたり，単語を具体的なものや抽象的なもの，専門用語や非専門用語で置き換え，ブレインストーミングし，段落を並び替えて，わかりやすい文章を作成してください．文章は５００字で出力してください．最終結果だけ出力してください．"

        # OpenAI APIを呼び出す
        response_data = call_openai_api(prompt)
        if response_data:
            print("Generated text:")
            print(response_data["choices"][0]["text"])

            input_string = response_data["choices"][0]["text"]
            output_file_path = dir_path + "/result_" + txt["file_name"] + ".txt"

            # OpenAIの結果をファイルに書き込む
            write_string_to_file(input_string, output_file_path)


def read_files_with_prefix(dir_path, prefix):
    file_list = []
    for file_name in sorted(os.listdir(dir_path)):
        if file_name.startswith(prefix):
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                content = f.read()
            file_list.append({'file_name': file_name, 'content': content})
    return file_list


def write_string_to_file(string, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(string)


def wav_to_txt_filepath(wav_file_path):
    # ファイル名と拡張子を分割
    file_root, file_ext = os.path.splitext(wav_file_path)

    # 新しい拡張子を追加してファイルパスを作成
    txt_file_path = f"{file_root}.txt"

    return txt_file_path


def call_openai_api(prompt):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0,
        max_tokens=500)
    return response


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    main(folder_path)
