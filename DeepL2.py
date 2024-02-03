#!/usr/bin/env python
import sys
import os

import deepl

# https://www.deepl.com/ja/docs-api/translating-text/
# as of 2021.11.14
LANG = ["BG",\
        "CS",\
        "DA",\
        "DE",\
        "EL",\
        "EN-GB",\
        "EN-US",\
        "EN",\
        "ES",\
        "ET",\
        "FI",\
        "FR",\
        "HU",\
        "IT",\
        "JA",\
        "LT",\
        "LV",\
        "NL",\
        "PL",\
        "PT-PT",\
        "PT-BR",\
        "PT",\
        "RO",\
        "RU",\
        "SK",\
        "SL",\
        "SV",\
        "ZH"]

def comment():
    print('Usage: %s target_lang FILENAME' % (sys.argv[0]))
    text = """
target_lang:    
    "DE" - German
    "EN-GB" - English (British)
    "EN-US" - English (American)
    "JA" - Japanese
    
!!!!!!!!!!!!!!!!!!! NOTE !!!!!!!!!!!!!!!!!!!
Input file must be UTF8-encoded plain text.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    print(text)

def translate(input_text, target_lang):
    if is_str(input_text):
        pass
    else:
        print('入力ファイルは、文字列ではありません。')

    auth_key = 'a1c00d90-9dde-652a-f8bb-0a28fe8a1943:fx'
    translator = deepl.Translator(auth_key) 
    result = translator.translate_text(input_text, target_lang=target_lang) 
    return result.text

def is_str(v):
    return type(v) is str

def get_file(filename):
    with open(filename, mode='r') as contents:
        try:
            input_text = contents.read()
        except OSError as e:
            print(e)
        else:
            return input_text


def main():
    std_input = []
    target_lang = sys.argv[1]

    # tty入力のチェック
    if sys.stdin.isatty():
        # パイプあるいはリダイレクトからの入力ではない場合、ファイルからの入力処理を実行
        # まずは、helpが引数として指定された場合の処理       
        if sys.argv[1] == 'help':
            comment()
            sys.exit()
        # 次に、target_langのチェック
        if target_lang not in LANG:
            print('\nTarget language is wrong!\n')
            sys.exit()
        # 次は、引数の数が多い場合
        elif len(sys.argv) > 3:
            print('Usage: %s target_language FILENAME' % (sys.argv[0]))
            sys.exit()
        elif len(sys.argv) == 3 :
            filename = sys.argv[2]
            input_text = get_file(filename)
        else:
            comment()
            sys.exit()
        print(translate(input_text, target_lang))
    # パイプあるいはリダイレクトからの入力の場合、標準入力からの処理を実行
    else:
        for std_input_row in sys.stdin:
            std_input.append(str(std_input_row))
        std_input_to_str = ''.join(std_input)
        print(translate(std_input_to_str, target_lang))



if __name__ == '__main__':
    main()