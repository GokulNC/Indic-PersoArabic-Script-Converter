from aksharamukha.transliterate import process as aksharamukhi_xlit

def convert_with_diacritics(text: str, from_script: str, to_script: str) -> str:
    """Transliterate with diacritics for the given `text` from Indic script to PersoArabic.

    Args:
        text (str): Text to be converted
        from_script (str): Source Indic script
        to_script (str): Target PersoArabic script

    Returns:
        str: Transliterated text in impure-abjad
    """
    if from_script == 'hi-IN' and to_script == 'ur-PK':
        return aksharamukhi_xlit("Devanagari", "Shahmukhi", text, pre_options=["RemoveSchwaHindi", "AnuChandraEqDeva"]) #, nativize=False)
    if from_script == 'pa-IN' and to_script == 'pa-PK':
        return aksharamukhi_xlit("Gurmukhi", "Shahmukhi", text, pre_options=["SchwaFinalGurmukhi"]) #, nativize=False)
