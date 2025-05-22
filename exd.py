import spacy
from collections import Counter

# SpaCyの英語モデルを読み込み
nlp = spacy.load("en_core_web_sm")

def kwic(text, search_value, search_type='token', context_size=5, highlight_style="color:red;", sort_mode="sequential"):
    doc = nlp(text)
    results = []
    sort_keys = []
    raw_keys = []  # 頻度カウント用

    # メインループ
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

            result = " ".join(context_tokens)
            results.append(result)

            if i + 1 < len(doc):
                next_token = doc[i + 1]
                token_text = next_token.text.lower()
                pos = next_token.pos_
                entity = next_token.ent_type_ if next_token.ent_type_ else "NONE"

                # キーの組み立て
                if "freq:" in sort_mode:
                    criteria = sort_mode.replace("freq:", "").lower().split(">")
                    key = tuple(
                        token_text if c == "token" else
                        pos if c == "pos" else
                        entity if c == "entity" else
                        None
                        for c in criteria
                    )
                    sort_keys.append(key)
                    raw_keys.append(key)
                elif ">" in sort_mode:
                    criteria = sort_mode.lower().split(">")
                    key = tuple(
                        token_text if c == "token" else
                        pos if c == "pos" else
                        entity if c == "entity" else
                        None
                        for c in criteria
                    )
                    sort_keys.append(key)
                else:
                    if sort_mode == "token":
                        sort_keys.append(token_text)
                    elif sort_mode == "pos":
                        sort_keys.append(pos)
                    elif sort_mode == "entity":
                        sort_keys.append(entity)
                    else:
                        sort_keys.append(len(results))  # sequential
            else:
                if ">" in sort_mode or "freq:" in sort_mode:
                    key_len = len(sort_mode.replace("freq:", "").split(">"))
                    sort_keys.append(tuple([""] * key_len))
                    if "freq:" in sort_mode:
                        raw_keys.append(tuple([""] * key_len))
                else:
                    sort_keys.append("")

    # ソート
    combined = list(zip(results, sort_keys))

    if sort_mode.startswith("freq:"):
        freq = Counter(raw_keys)
        sorted_combined = sorted(
            combined,
            key=lambda x: (-freq[x[1]], x[1])  # 頻度降順、同順位は辞書順
        )
    else:
        sorted_combined = sorted(combined, key=lambda x: x[1])

    results = [item[0] for item in sorted_combined]
    return results


# テキストファイルの読み込み
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 実行部分
if __name__ == '__main__':
    file_path = 'input.txt'
    text = read_text_file(file_path)

    # 設定
    search_value = "and"             # 検索語
    search_type = "token"            # 'token', 'pos', 'entity'
    context_size = 5
    highlight_style = "color:blue; font-weight:bold;"
    sort_mode = "freq:pos"     
   
    # KWIC実行
    kwic_results = kwic(text, search_value, search_type, context_size, highlight_style, sort_mode)

    # HTMLで出力
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write("<html><body>\n")
        f.write(f"<h2>KWIC results for '{search_value}' ({search_type}), sorted by '{sort_mode}'</h2>\n")
        for result in kwic_results:
            f.write(result + "<br>\n")
        f.write("</body></html>")
