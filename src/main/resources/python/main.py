# main.py

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


from ocr_module import recognize_text
from translate_module import translate_text

# 設定圖片路徑
image_path = 'images/test_image.png'

# 執行 OCR
recognized_text = recognize_text(image_path)
print("OCR 識別結果：")
print(recognized_text)

# 執行翻譯
final_result = translate_text(recognized_text)
print("最終翻譯結果：")
print(final_result)
