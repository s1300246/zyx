def kwic(text, target_ngram, context_size=5):
    words = text.split()
    target_words = target_ngram.split()
    target_length = len(target_words)

    # 小文字に変換して検索の精度を上げる
    words_lower = [word.lower() for word in words]
    target_words_lower = [word.lower() for word in target_words]

    results = []

    for i in range(len(words_lower) - target_length + 1):
        # ターゲット語句と一致する部分を探す
        if words_lower[i:i + target_length] == target_words_lower:
            start = max(0, i - context_size)
            end = min(len(words), i + target_length + context_size)
            context = words[start:end]

            highlighted_context = []
            for j in range(len(context)):
                # 現在の位置がハイライトすべき位置かどうかを判定
                if start + j == i:
                    # ハイライト部分を追加（赤色）
                    highlighted_context.append(
                        f"<span style='color:red;'>{' '.join(words[i:i + target_length])}</span>"
                    )
                    # スキップする語数分進める
                    for _ in range(1, target_length):
                        j += 1  # この j はループ外で使われないため影響なし
                    continue
                if not (i <= start + j < i + target_length):
                    highlighted_context.append(context[j])

            results.append(' '.join(highlighted_context))

    return results


# テキストファイルからテキストを読み込む
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 実行部分
if __name__ == '__main__':
    file_path = 'input.txt'  # 入力ファイルのパスを指定
    text = read_text_file(file_path)
    target_ngram = "in the"  # 検索したい語句（n-gram）

    # KWIC実行
    kwic_results = kwic(text, target_ngram, context_size=5)

    # HTMLとして出力
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write("<html><body>\n")
        for result in kwic_results:
            f.write(result + '<br>\n')
        f.write("</body></html>")
