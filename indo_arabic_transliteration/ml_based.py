from indictrans import Transliterator
MODELS = {
    ('hi-IN', 'ur-PK'): Transliterator(source='hin', target='urd', build_lookup=True, rb=False),
    ('ur-PK', 'hi-IN'): Transliterator(source='urd', target='hin', build_lookup=True, rb=False)
}

def ml_transliterate(text: str, from_script: str, to_script: str) -> str:
    """Machine-Learning-based Transliteration for the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script
        to_script (str): Target script

    Returns:
        str: Transliterated text by models
    """
    return MODELS[(from_script, to_script)].transform(text)
