# translate_module.py

# -*- coding: utf-8 -*-
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


import sys
import torch
from paddleocr import PaddleOCR
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 不需要辨識流程的 log 訊息
import logging
logging.getLogger('ppocr').setLevel(logging.ERROR)  # ← 新增這行，讓 PaddleOCR 不輸出 log

def recognize_text(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    result = ocr.ocr(image_path, cls=True)
    text = ''
    for line in result[0]:
        text += line[1][0] + '\n'
    return text

def translate_text(text):
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    tokenizer.src_lang = "jpn_Jpan"
    tgt_lang = "zho_Hant"
    inputs = tokenizer(text, return_tensors="pt")

    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_length=128,
        num_beams=3,
        do_sample=False,
        early_stopping=False
    )
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translated_text[0]

if __name__ == '__main__':
    image_path = sys.argv[1]
    recognized_text = recognize_text(image_path)
    translated_result = translate_text(recognized_text)
    print(translated_result)
