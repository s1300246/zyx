import spacy
from collections import Counter

# SpaCyの英語モデルを読み込み
nlp = spacy.load("en_core_web_sm")

def kwic(text, search_value, search_type='token', context_size=5, highlight_style="color:red;", sort_mode="sequential"):
    doc = nlp(text)
    results = []
    sortable_keys = []
    next_tokens = []
    next_pos_tags = []

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
                next_tokens.append(next_token.text.lower())
                next_pos_tags.append(next_token.pos_)
                if sort_mode == "token" or sort_mode == "freq":
                    sortable_keys.append(next_token.text.lower())
                elif sort_mode == "pos" or sort_mode == "posfreq":
                    sortable_keys.append(next_token.pos_)
                else:
                    sortable_keys.append(len(results))  # sequential
            else:
                next_tokens.append("")
                next_pos_tags.append("")
                sortable_keys.append("")

    # 並び替え
    if sort_mode == "freq":
        # トークンの頻度順で並べ替え
        freq = Counter(next_tokens)
        combined = list(zip(results, sortable_keys))
        sorted_combined = sorted(combined, key=lambda x: (-freq[x[1]], x[1]))  # 頻度降順、次にトークン順
        results = [item[0] for item in sorted_combined]

    elif sort_mode == "posfreq":
        # POSタグの頻度順で並べ替え
        freq = Counter(next_pos_tags)
        combined = list(zip(results, sortable_keys))
        sorted_combined = sorted(combined, key=lambda x: (-freq[x[1]], x[1]))  # 頻度降順、次にPOSタグ順
        results = [item[0] for item in sorted_combined]


    return results


# テキストファイルの読み込み
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 実行部分
if __name__ == '__main__':
    file_path = 'input.txt'  # 解析したいテキストファイルのパス
    text = read_text_file(file_path)  # ファイル内容を読み込む

    # 検索の設定
    search_value = "the"        # 検索する単語を指定
    search_type = "token"       # 'token', 'pos', 'entity' から選択
    context_size = 5            # キーワード前後の語数
    highlight_style = "color:blue; font-weight:bold;"  # 強調表示のスタイル
    sort_mode = "posfreq"       # 'sequential', 'freq', 'posfreq' から選択

    # KWIC 実行
    kwic_results = kwic(text, search_value, search_type, context_size, highlight_style, sort_mode)

    # HTMLとして出力
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write("<html><body>\n")
        f.write(f"<h2>KWIC results for '{search_value}' ({search_type}), sorted by '{sort_mode}'</h2>\n")
        for result in kwic_results:
            f.write(result + "<br>\n")
        f.write("</body></html>")
