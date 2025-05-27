# ocr_module.py

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import torch
from paddleocr import PaddleOCR

# 把 ppocr 的 log 級別調低，避免 debug 訊息太多干擾主輸出。
# 這樣只會輸出錯誤，不會輸出 debug 訊息，更乾淨。
import logging
logging.getLogger('ppocr').setLevel(logging.ERROR)


def recognize_text(image_path):
    # 建立 OCR 物件，指定日文辨識
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    result = ocr.ocr(image_path, cls=True)
    
    # 把辨識結果整理成文字
    text = ''
    for line in result[0]:
        text += line[1][0] + '\n'
    
    return text
