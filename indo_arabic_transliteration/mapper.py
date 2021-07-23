from .hindustani import HindustaniTransliterator
hindi_urdu_converter = HindustaniTransliterator()

from .punjabi import PunjabiTransliterator
panjabi_converter = PunjabiTransliterator()

from .sindhi import SindhiTransliterator
sindhi_converter = SindhiTransliterator()

DELEGATES = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): hindi_urdu_converter.transliterate_from_hindi_to_urdu,
    ('ur-PK', 'hi-IN'): hindi_urdu_converter.transliterate_from_urdu_to_hindi,
    
    # Punjabi scripts
    ('pa-IN', 'pa-PK'): panjabi_converter.transliterate_from_gurmukhi_to_shahmukhi,
    ('pa-PK', 'pa-IN'): panjabi_converter.transliterate_from_shahmukhi_to_gurmukhi,
    
    # Sindhi scripts
    ('sd-IN', 'sd-PK'): sindhi_converter.transliterate_from_devanagari_to_sindhi,
    ('sd-PK', 'sd-IN'): sindhi_converter.transliterate_from_sindhi_to_devanagari,
}

def script_convert(text: str, from_script: str, to_script: str) -> str:
    """Raw convert the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script
        to_script (str): Target script

    Returns:
        str: Converted text
    """
    return DELEGATES[(from_script, to_script)](text)
