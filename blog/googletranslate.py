from googletrans import Translator
import sys
from . import makepdf_
import os
from config.settings import BASE_DIR


def manual_jp2eng(path):
    #print('open '+args[1])
    f = open(path)
    print(path)
    lines = f.readlines()
    f.close()
    translator = Translator()
    trans_str = ""

    for line in lines:
        ### jp -> en
        translated = translator.translate(line, dest="en");
        f.write(translated.text)
        trans_str += translated.text + '\n'
    makepdf_.make(os.path.join(BASE_DIR,'documents/manual_eng.pdf'),trans_str)
