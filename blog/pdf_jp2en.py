#coding:utf-8
from googletrans import Translator
import sys
from . import makepdf_
import os
from config.settings import BASE_DIR
import argparse
import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re


def manual_jp2eng(path):
    #print('open '+args[1])
    f = open(path)
    print(path)
    lines = f.readlines()
    f.close()
    translator = Translator()
    trans_str = ''

    for line in lines:
        ### jp -> en
        translated = translator.translate(line, dest="en")
        #f.write(translated.text)
        trans_str += translated.text + '<br/>'
    makepdf_.make(os.path.join(BASE_DIR,'documents/manual_eng.pdf'),trans_str)



def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True


def get_text_from_pdf(pdfname, limit=1000):
    if (pdfname == ''):
        return ''
    else:
        # 処理するPDFファイルを開く/開けなければ
        try:
            fp = open(pdfname, 'rb')
        except:
            return ''

    # PDFからテキストの抽出
    rsrcmgr = PDFResourceManager()
    out_fp = StringIO()
    la_params = LAParams()
    la_params.detect_vertical = True
    device = TextConverter(rsrcmgr, out_fp, codec='utf-8', laparams=la_params)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None, caching=True, check_extractable=True):
        interpreter.process_page(page)
    text = out_fp.getvalue()
    fp.close()
    device.close()
    out_fp.close()

    # 改行で分割する
    #lines = text.splitlines()
    lines = []
    lines.append(text)

    outputs = []
    output = ""

    # 除去するutf8文字
    replace_strs = [b'\x00']

    is_blank_line = False

    # 分割した行でループ
    for line in lines:

        # byte文字列に変換
        line_utf8 = line.encode('utf-8')

        # 余分な文字を除去する
        for replace_str in replace_strs:
            line_utf8 = line_utf8.replace(replace_str, b'')

        # strに戻す
        line = line_utf8.decode()

        # 連続する空白を一つにする
        line = re.sub("[ ]+", " ", line)

        # 前後の空白を除く
        line = line.strip()
        #print("aft:[" + line + "]")

        # 空行は無視
        if len(line) == 0:
            is_blank_line = True
            continue

        # 数字だけの行は無視
        if is_float(line):
            continue

        # 1単語しかなく、末尾がピリオドで終わらないものは無視
        if line.split(" ").count == 1 and not line.endswith("."):
            continue

        # 文章の切れ目の場合
        if is_blank_line or output.endswith("."):
            # 文字数がlimitを超えていたらここで一旦区切る
            if(len(output) > limit):
                outputs.append(output)
                output = ""
            else:
                output += "\r\n"
        #前の行からの続きの場合
        elif not is_blank_line and output.endswith("-"):
            output = output[:-1]
        #それ以外の場合は、単語の切れ目として半角空白を入れる
        else:
            output += " "

        #print("[" + str(line) + "]")
        output += str(line)
        is_blank_line = False

    outputs.append(output)
    outputs.append('\n')
    return outputs


def main_():

    # pdfをテキストに変換
    #inputs = get_text_from_pdf(args.input, limit=args.limit)
    inputs = get_text_from_pdf(os.path.join(BASE_DIR,'documents/manual.pdf'))
    #print(path + os.sep)

    #pathをjsonファイルに登録
    with open(os.path.join(BASE_DIR,'documents/text.txt'), "w", encoding="utf-8") as f_text:
        with open(os.path.join(BASE_DIR,'documents/translate.txt'), "w", encoding="utf-8") as f_trans:
            # 一定文字列で分割した文章毎にAPIを叩く
            for i, input in enumerate(inputs):
                print("{0}/{1} is proccessing".format((i+1), len(inputs)))
                # 結果をファイルに出力
                f_text.write(input)
                translator = Translator()
                translated = translator.translate(input, dest="en")
                f_trans.write(translated.text)

    manual_jp2eng(os.path.join(BASE_DIR,'documents/translate.txt'))


if __name__ == "__main__":
    main()
