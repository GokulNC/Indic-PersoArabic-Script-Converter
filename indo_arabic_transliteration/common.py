from .str_mapper import StringTranslator

DEVANAGARI_PREPROCESS_MAP = {

    # Desanskritize
    'ँ': 'ं',
    'ऋ': 'र',
    'ॠ': 'र',
    'ऌ': 'ल',
    'ॡ': 'ल',
    'ृ': '्र',
    'ॄ': '्र',
    'ॢ': '्ल',
    'ॣ': '्ल',

    # Dekashmirize
    'ऄ': 'अ',
    'ऎ': 'ए',
    'ऒ': 'ओ',
    'ॆ': 'े',
    'ॊ': 'ो',

    # Delatinize
    'ॲ': 'अ',
    'ऑ': 'आ',
    'ऍ': 'ए',
    'ॅ': '',
    'ॉ': 'ा',

    # Dedravidize
    'ऩ': 'न',
    'ऱ': 'र',
    'ल़': 'ल',
    'ऴ': 'ळ',

    # De-bangalize
    'य़': 'य',
    'व़': 'व', # W->V

    # Misc
    'थ़': 'थ', # https://wiktionary.org/wiki/थ़
    'म़': 'म',
    '॰': '.',
}
devanagari_preprocessor = StringTranslator(DEVANAGARI_PREPROCESS_MAP)

DEVANAGARI_ABJAD_MAP = {
    # Abjadi-purifier
    'ि': '',
    'ु': '',
    'ै': 'े',
    'ौ': 'ो',

    # Handle non-initial vowels missing in sheet
    'ई': 'इ',
    'उ': 'ओ',
    'ऊ': 'ओ',
    'ऐ': 'ए',
    'औ': 'ओ',
}
devanagari_abjadifier = str.maketrans(DEVANAGARI_ABJAD_MAP)

DEVANAGARI_INITIAL_VOWELS_ABJADIFY = {
    'इ': 'अ',
    'ई': 'ए',
    'उ': 'अ',
    'ऊ': 'ओ',
    'ऐ': 'ए',
    'औ': 'ओ',
}
devanagari_initial_vowels_abjadifier = StringTranslator(DEVANAGARI_INITIAL_VOWELS_ABJADIFY, match_initial_only=True, support_back_translation=False)

DEVANAGARI_NUQTA_CONSONANTS_SIMPLIFY_MAP = {
    # Unicode chars
    'क़': 'क',
    'ख़': 'ख',
    'ग़': 'ग',
    # 'ज़': 'ज',
    'ड़': 'ड',
    'ढ़': 'ढ',
    'फ़': 'फ',

    # Constructed chars
    'ज़़': 'ज़',
    'ॹ': 'ज़',
    'ॹ़': 'ज़',
    'त़': 'त',
    'स़': 'स',
    'स़़': 'स',
    'ह़': 'ह',
    'ह॒': 'ह',

    # Implosive to germination (approx)
    'ॻ': 'ग्ग',
    'ॼ': 'ज्ज',
    'ॾ': 'ड्ड',
    'ॿ': 'ब्ब',
}
devanagari_nuqta_consonants_simplifier = StringTranslator(DEVANAGARI_NUQTA_CONSONANTS_SIMPLIFY_MAP, support_back_translation=False)
