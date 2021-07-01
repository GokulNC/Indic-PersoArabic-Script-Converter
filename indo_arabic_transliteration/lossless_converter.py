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
    return aksharamukhi_xlit("Devanagari", "Urdu", text, pre_options=["RemoveSchwaHindi", "AnuChandraEqDeva"]) #, nativize=False)
