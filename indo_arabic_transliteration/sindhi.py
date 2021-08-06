import re
import pandas as pd
from .base import BaseIndoArabicTransliterator
from .str_mapper import StringTranslator

URDU_TO_SINDHI = {
    'ی': 'ي',
    'ے': 'ي',
}
sindhi_postprocessor = str.maketrans(URDU_TO_SINDHI)

SINDHI_PREPROCESS_MAP = {
    # Lazy people write like these
    ' ء ': ' ۽ ',
    ' م ': ' ۾ ',

    # Since most Sindh people are forced to study Urdu before Sindhi,
    # it's usual to mix-up Urdu and Sindhi chars. Clean 'em up
    'ہ': 'ه', # Urdu to Arabic gol he
    'ٹ': 'ٽ',
    'ٹھ': 'ٺ',
    'ڈ': 'ڊ',
    'ڈھ': 'ڍ',
    'ڑ': 'ڙ',
    # Below are ambiguous, uncomment for extreme cases
    # 'ڑھ': 'ڙه',
    # 'تھ': 'ٿ',
    # 'دھ': 'ڌ',
    # 'پھ': 'ڦ',
    # 'بھ': 'ڀ',
}
sindhi_preprocessor = StringTranslator(SINDHI_PREPROCESS_MAP)

CONSONANT_MAP_FILES = ['sindhi_consonants.csv']
ADDITIONAL_FINAL_MAP_FILES = ['sindhi_final.csv']
ISOLATED_MAP_FILES = ['sindhi_isolated.csv']

class SindhiTransliterator(BaseIndoArabicTransliterator):
    def __init__(self):
        super().__init__(CONSONANT_MAP_FILES)
        self.isolated_sindhi_to_devanagari_map = {}
        
        for map_file in ISOLATED_MAP_FILES:
            df = pd.read_csv(self.data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.isolated_sindhi_to_devanagari_map[' '+sindhi_letter+' '] = ' '+devanagari_letter+' '
                self.arabic_to_devanagari_cleanup_pass[sindhi_letter] = devanagari_letter
        
        for map_file in ADDITIONAL_FINAL_MAP_FILES:
            df = pd.read_csv(self.data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.final_arabic_to_devanagari_map[arabic_letter] = devanagari_letter
        
        self.isolated_sindhi_to_devanagari_converter = StringTranslator(self.isolated_sindhi_to_devanagari_map)
        self.final_arabic_to_devanagari_converter = StringTranslator(self.final_arabic_to_devanagari_map, match_final_only=True)
        self.arabic_to_devanagari_final_cleanup = StringTranslator(self.arabic_to_devanagari_cleanup_pass)
    
    def arabic_normalize(self, text):
        text = super().arabic_normalize(text)
        text = text.replace('ے', 'ی')
        text = sindhi_preprocessor.translate(text)
        text = re.sub(r"ھ\B", "ه", text)
        text = re.sub('([^ڙجگ])ھ', r'\1ه', text) # Except final {گھ, جھ, ڙھ}, all other do-chasmi endings can be converted to Arabic he

        # Ensure the isolated characters have space around them
        # text = re.sub(" م ", " ۾ ", text)
        # text = re.sub(" ء ",  " ۽ ", text)
        text = re.sub(r"\s۾([^\w ])", r" ۾ \1", text)
        text = re.sub(r"\s۽([^\w ])", r" ۽ \1", text)
        return text
    
    def transliterate_from_sindhi_to_devanagari(self, text, nativize=False):
        text = self.arabic_normalize(text)
        text = self.isolated_sindhi_to_devanagari_converter.translate(text)
        text = self.initial_arabic_to_devanagari_converter.translate(text)

        # Convert Hamza-combos first, then remaining hamza
        text = self.hamza_combo_to_devanagari_converter.translate(text)
        text = self.hamza_to_devanagari_converter.translate(text)

        text = self.arabic_to_devanagari_converter_pass1.translate(text)
        text = self.final_arabic_to_devanagari_converter.translate(text)
        text = text.replace('ھ', 'ه') # Now convert Urdu do-chashmi he into Arabic he
        text = self.arabic_to_devanagari_converter_pass2.translate(text)
        text = self.arabic_to_devanagari_final_cleanup.translate(text)
        text = self.devanagari_postprocessor.translate(text) #  (جمهوریه) जमहवरयह -> जमहोरयह
        text = self.devanagari_postprocessor.translate(text) # जमहोरयह -> जमहोरीह
        if nativize:
            text = self.devanagari_nativize(text)
        return text
    
    def devanagari_normalize(self, text, abjadify_initial_vowels=False, drop_virama=False):
        text = super().devanagari_normalize(text, abjadify_initial_vowels, drop_virama)
        text = re.sub(r"\sमें\s", " में ", text)
        text = re.sub(r"\sऐं\s", " ऐं ", text)
        return text
    
    def devanagari_remove_short_vowels(self, text):
        text = super().devanagari_remove_short_vowels(text)
        text = text.replace('े', 'ी') # Arabic-Sindhi (unfortunately) doesnot have bari ye
        return text

    def transliterate_from_devanagari_to_sindhi(self, text, nativize=False):
        text = self.devanagari_normalize(text)
        text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))ए', '\\1ای', text) # Patch: ए is present in both hamza and initial vowels, so handle first
        text = self.isolated_sindhi_to_devanagari_converter.reverse_translate(text)

        # Convert Devanagari-Hamza first, then hamza-combos
        text = self.hamza_to_devanagari_converter.reverse_translate(text)
        text = self.hamza_combo_to_devanagari_converter.reverse_translate(text)

        text = self.arabic_to_devanagari_converter_pass1.reverse_translate(text)
        text = self.devanagari_remove_short_vowels(text) # Running it now since previous pass could have handled some short vowels (hamza_combos)
        text = text.replace('ा', 'ا') # Regex finds 'ा' as a \b unfortunately. So a quick hack to avoid those confusions
        text = self.final_arabic_to_devanagari_converter.reverse_translate(text)
        text = text.replace('ी', 'ی').replace('ो', 'و').replace('े', 'ی') # In-case anything remains, should never happen tho
        text = self.initial_arabic_to_devanagari_converter.reverse_translate(text)
        text = text.replace("ओ", "ؤ")
        text = self.arabic_to_devanagari_converter_pass2.reverse_translate(text)
        text = self.arabic_to_devanagari_final_cleanup.reverse_translate(text)
        if nativize:
            text = text.translate(sindhi_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'sd':
            return self.transliterate_from_devanagari_to_sindhi(text, nativize)
        return self.transliterate_from_sindhi_to_devanagari(text, nativize)
