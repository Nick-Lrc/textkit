def select_length(data, min, max=-1):
    if max == -1:
        max = min + 1
    output = []
    for word in data:
        word_len = int(len(word))
        if min <= word_len < max:
            output.append(word)
    return output
