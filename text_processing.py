def preprocess(text: str) -> str:
    translation_table = str.maketrans({"'":r"\'",'"':r'\"'})
    return text.translate(translation_table)