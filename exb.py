import spacy

# SpaCyの英語モデルを読み込み
nlp = spacy.load("en_core_web_sm")

def kwic(text, search_value, search_type='token', context_size=5, highlight_style="color:red;"):
    doc = nlp(text)
    results = []

    for i, token in enumerate(doc):
        match = False

        if search_type == 'token' and token.text.lower() == search_value.lower():
            match = True
        elif search_type == 'pos' and token.pos_ == search_value:
            match = True
        elif search_type == 'entity' and token.ent_type_ == search_value:
            match = True

        if match:
            start = max(0, i - context_size)
            end = min(len(doc), i + context_size + 1)

            context_tokens = []
            for j in range(start, end):
                if j == i:
                    context_tokens.append(f"<span style='{highlight_style}'>{doc[j].text}</span>")
                else:
                    context_tokens.append(doc[j].text)
            
            results.append(" ".join(context_tokens))

    return results


# テキストファイルの読み込み
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 実行部分
if __name__ == '__main__':
    file_path = 'input.txt'
    text = read_text_file(file_path)

    # 検索の種類と条件
    search_value = "PERSON"        # 検索語（token／POS／Entityに応じて変える）
    search_type = "entity"      # 'token', 'pos', 'entity' のいずれか
    context_size = 5           # コンテキストの語数
    highlight_style = "color:blue; font-weight:bold;"  # ハイライトのスタイル

    #POStag例：NOUN, VERB, ADJ, ADV, PROPN（固有名詞）など
    #Entity例：PERSON, ORG, GPE（地名）, DATE, MONEY など

    # KWIC実行
    kwic_results = kwic(text, search_value, search_type, context_size, highlight_style)

    # HTMLとして出力
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write("<html><body>\n")
        for result in kwic_results:
            f.write(result + "<br>\n")
        f.write("</body></html>")
