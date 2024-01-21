def chunk_string(s, length):
    return [s[i : i + length] for i in range(0, len(s), length)]
