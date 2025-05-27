# translate_module

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch # 確認 torch 有被 import 到，雖然您的程式碼中有，但習慣上會在用到的檔案 import

# 載入 NLLB 模型
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("模型和 Tokenizer 載入成功!")

def translate_text(text):
    # 設定來源語言和目標語言代碼
    # NLLB 使用這種格式的語言代碼作為特殊 token
    src_lang_code = "jpn_Jpan"  # 日文
    tgt_lang_code = "zho_Hant"  # 繁體中文

    # === 關鍵修改：在輸入文字前加上來源語言的特殊標籤 ===
    # 這告訴模型輸入文字是日文
    text_with_src_token = f"__{src_lang_code}__ {text}"
    # ====================================================

    # token 化
    # 使用加入特殊標籤的文字進行 tokenization
    inputs = tokenizer(text_with_src_token, return_tensors="pt")

    # 翻譯
    generated_tokens = model.generate(
        **inputs,
        # 強制第一個生成的 token 是目標語言的特殊標籤，引導模型生成繁體中文
        # 注意這裡也使用了特殊標籤的格式
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(f"__{tgt_lang_code}__"),
        max_length=512,
        num_beams=5,          # 使用 beam search
        do_sample=False,      # 關閉隨機性，選擇最有可能的翻譯
        early_stopping=True   # 提前停止
    )

    # 解碼
    # skip_special_tokens=True 會移除我們加入的語言標籤
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translated_text[0]

# 測試範例 (您原本的 main.py 會呼叫這個函式，這裡只是方便在單一檔案內測試)
# 如果您只修改 translate_module.py，並執行原本的 main.py 即可看到效果
if __name__ == '__main__':
    # 模擬 OCR 識別結果
    test_text1 = "おはよう。"
    test_text2 = "メリークリスマス諸君" # 更正為標準的聖誕快樂寫法

    print(f"原始日文: {test_text1}")
    translated1 = translate_text(test_text1)
    print(f"翻譯結果: {translated1}\n")

    print(f"原始日文: {test_text2}")
    translated2 = translate_text(test_text2)
    print(f"翻譯結果: {translated2}\n")