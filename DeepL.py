#!/usr/bin/env python
import sys
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

def is_str(v):
    return type(v) is str

def main():
    if sys.argv[1] == 'help':
        comment()
        sys.exit()
    else:    
        if len(sys.argv) < 3:
            print('Usage: %s target_language FILENAME' % (sys.argv[0]))
    args = sys.argv
    filename = sys.argv[2]
    target_lang = sys.argv[1]

    if target_lang in LANG:
        myfile = open(filename, 'r', encoding='UTF-8')
        input_text = myfile.read()

        if is_str(input_text):
            pass
        else:
            print('入力ファイルは、文字列ではありません。')
            #QMessageBox.information(None, "Notice!", filepath[0] + "\n\n is Selected", QMessageBox.Yes)

        auth_key = 'a1c00d90-9dde-652a-f8bb-0a28fe8a1943:fx'
        translator = deepl.Translator(auth_key) 
        result = translator.translate_text(input_text, target_lang=target_lang) 
        output_text = result.text
        print(output_text)
    else:
        print('\nTarget language is wrong!\n')
        comment()
        sys.exit()

if __name__ == '__main__':
    main()