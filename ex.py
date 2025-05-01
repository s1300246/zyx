def kwic(text, target_ngram, context_size=5):
    words = text.split()
    target_words = target_ngram.split()
    target_length = len(target_words)

    # 小文字に変換
    words_lower = [word.lower() for word in words]
    target_words_lower = [word.lower() for word in target_words]

    results = []

    for i in range(len(words_lower)):
        if words_lower[i:i + target_length] == target_words_lower:
            start = max(0, i - context_size)
            end = min(len(words), i + target_length + context_size)
            context = words[start:end]

            highlighted_context = []
            for j in range(len(context)):
                if j < len(context) - target_length + 1 and context[j:j + target_length] == target_words:
                    highlighted_context.append(f"<{' '.join(target_words)}>")
                    j += target_length - 1  # Skip the target words
                    continue  # 次のループへ進む
                else:
                    highlighted_context.append(context[j])

            results.append(' '.join(highlighted_context))

    return results

# テキストファイルからテキストを読み込む
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# 使用例
file_path = 'input.txt'  # 読み込むテキストファイルのパス
text = read_text_file(file_path)
target_ngram = "in the"
kwic_results = kwic(text, target_ngram)

# 出力結果をresult.txtに書き込む
with open('result.txt', 'w', encoding='utf-8') as f:
    for result in kwic_results:
        f.write(result + '\n')