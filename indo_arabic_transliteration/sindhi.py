import os
import re
import pandas as pd
from .utils import StringTranslator

from urduhack.normalization.character import remove_diacritics, normalize_characters, normalize_combine_characters

URDU_TO_SINDHI = {
    'ی': 'ي',
    'ے': 'ی',
}
sindhi_postprocessor = str.maketrans(URDU_TO_SINDHI)

SINDHI_PREPROCESS = {
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
sindhi_preprocessor = StringTranslator(SINDHI_PREPROCESS)

INITIAL_MAP_FILES = ['initial_vowels.csv']
MAIN_MAP_FILES = ['sindhi_consonants.csv', 'vowels.csv']
MISC_MAP_FILES = ['numerals.csv', 'punctuations.csv', 'hamza.csv', 'hamza_combo.csv']
FINAL_MAP_FILES = ['final_vowels.csv','sindhi_final_consonants.csv']
ARABIC_MAP_FILES = ['arabic.csv']
ISOLATED_MAP_FILES = ['sindhi_isolated.csv']

class SindhiTransliterator:
    def __init__(self):
        data_dir = os.path.dirname(__file__) + '/data/'
        self.initial_sindhi_to_devanagari_map = {}
        self.final_sindhi_to_devanagari_map = {}
        self.sindhi_to_devanagari_map_pass1 = {}
        self.sindhi_to_devanagari_map_pass2 = {}
        self.sindhi_to_devanagari_cleanup_pass = {} # To handle chars at erraneous/unconventional places
        self.devanagari_postprocess_map = {}

        self.isolated_sindhi_to_devanagari_map = {}

        for map_file in MISC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.sindhi_to_devanagari_map_pass1[sindhi_letter] = devanagari_letter

        for map_file in INITIAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.initial_sindhi_to_devanagari_map[sindhi_letter] = devanagari_letter
                self.sindhi_to_devanagari_cleanup_pass[sindhi_letter] = devanagari_letter
        
        for map_file in FINAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.final_sindhi_to_devanagari_map[sindhi_letter] = devanagari_letter
                self.sindhi_to_devanagari_cleanup_pass[sindhi_letter] = devanagari_letter # Devanagari vowel-marks doesn't work without this
        
        for map_file in ISOLATED_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.isolated_sindhi_to_devanagari_map[' '+sindhi_letter+' '] = ' '+devanagari_letter+' '
                self.sindhi_to_devanagari_cleanup_pass[sindhi_letter] = devanagari_letter
        
        for map_file in ARABIC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                # TODO: Some of these are initial_only matchers. Handle them
                self.sindhi_to_devanagari_cleanup_pass[sindhi_letter] = devanagari_letter
        
        consonants = []
        for map_file in MAIN_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                sindhi_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.sindhi_to_devanagari_map_pass2[sindhi_letter] = devanagari_letter
                if 'consonants' not in map_file:
                    continue

                # Non-initial forms: Consonant+ا to Consonant+ा
                self.sindhi_to_devanagari_map_pass2[sindhi_letter+'ا'] = devanagari_letter+'ा'
                if sindhi_letter not in {'ی', 'و', 'ھ'}:
                    consonants.append((sindhi_letter, roman_letter, devanagari_letter))

                if len(sindhi_letter) == 1:
                    sindhi_shadda, devanagari_shadda = sindhi_letter+" ّ".strip(), devanagari_letter+'्'+devanagari_letter
                    self.sindhi_to_devanagari_map_pass1[sindhi_shadda] = devanagari_shadda
                    self.sindhi_to_devanagari_map_pass1[sindhi_shadda+'ا'] = devanagari_shadda+'ा'
                    # Note on why it's not in pass-2: پکّا is converted as पक्कअ instead of पक्का (Regex sees shadda char as word boundary?)

        # Assume medial ی as ी and و as ो
        for i in range(len(consonants)):
            sindhi_letter_i, roman_letter_i, devanagari_letter_i = consonants[i]
            for j in range(len(consonants)):
                sindhi_letter_j, roman_letter_j, devanagari_letter_j = consonants[j]
                self.devanagari_postprocess_map[devanagari_letter_i+'य'+devanagari_letter_j] = devanagari_letter_i+'ी'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'व'+devanagari_letter_j] = devanagari_letter_i+'ो'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'यं'+devanagari_letter_j] = devanagari_letter_i+'ीं'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'वं'+devanagari_letter_j] = devanagari_letter_i+'ों'+devanagari_letter_j

        self.initial_sindhi_to_devanagari_converter = StringTranslator(self.initial_sindhi_to_devanagari_map, match_initial_only=True)
        self.final_sindhi_to_devanagari_converter = StringTranslator(self.final_sindhi_to_devanagari_map, match_final_only=True)
        self.sindhi_to_devanagari_converter_pass1 = StringTranslator(self.sindhi_to_devanagari_map_pass1)
        self.sindhi_to_devanagari_converter_pass2 = StringTranslator(self.sindhi_to_devanagari_map_pass2)
        self.sindhi_to_devanagari_final_cleanup = StringTranslator(self.sindhi_to_devanagari_cleanup_pass)
        self.devanagari_postprocessor = StringTranslator(self.devanagari_postprocess_map)

        self.isolated_sindhi_to_devanagari_converter = StringTranslator(self.isolated_sindhi_to_devanagari_map)

        from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
        self.devanagari_normalizer = IndicNormalizerFactory().get_normalizer('hi')
    
    def sindhi_normalize(self, text):
        text = remove_diacritics(text) # Drops short-vowels
        text = normalize_combine_characters(normalize_characters(text))
        text = text.replace(',', '،').replace('?', '؟').replace('؛', ';').replace('؍', '/').replace('٪', '%')
        text = sindhi_preprocessor.translate(text)
        text = re.sub(r"ھ\B", "ه", text)

        # Ensure the isolated characters have space around them
        text = re.sub(r"\s۾\s", " ۾ ", text)
        text = re.sub(r"\s۽\s", " ۽ ", text)
        text = re.sub(r"\s۾([^\w ])", r" ۾ \1", text)
        text = re.sub(r"\s۽([^\w ])", r" ۽ \1", text)
        return text
    
    def transliterate_from_sindhi_to_devanagari(self, text, nativize=False):
        text = self.sindhi_normalize(text)
        text = self.isolated_sindhi_to_devanagari_converter.translate(text)
        text = self.initial_sindhi_to_devanagari_converter.translate(text)
        text = self.sindhi_to_devanagari_converter_pass1.translate(text)
        text = self.final_sindhi_to_devanagari_converter.translate(text)
        text = text.replace('ھ', 'ه') # Now convert Urdu do-chashmi he into Arabic he
        text = self.sindhi_to_devanagari_converter_pass2.translate(text)
        text = self.sindhi_to_devanagari_final_cleanup.translate(text)
        text = self.devanagari_postprocessor.translate(text) #  (جمهوریه) जमहवरयह -> जमहोरयह
        text = self.devanagari_postprocessor.translate(text) # जमहोरयह -> जमहोरीह
        return text
    
    def devanagari_normalize(self, text):
        # Assumes no short vowels
        # TODO: Pre-process to match Urdu Abjad
        text = self.devanagari_postprocessor.reverse_translate(text)
        text = self.devanagari_postprocessor.reverse_translate(text)
        text = re.sub(r"\sमें\s", " में ", text)
        text = re.sub(r"\sऐं\s", " ऐं ", text)
        return text

    def transliterate_from_devanagari_to_sindhi(self, text, nativize=False):
        text = self.devanagari_normalize(text)
        text = self.isolated_sindhi_to_devanagari_converter.reverse_translate(text)
        text = self.initial_sindhi_to_devanagari_converter.reverse_translate(text)
        text = self.sindhi_to_devanagari_converter_pass1.reverse_translate(text)
        text = self.final_sindhi_to_devanagari_converter.reverse_translate(text)
        text = self.sindhi_to_devanagari_converter_pass2.reverse_translate(text)
        text = self.sindhi_to_devanagari_final_cleanup.reverse_translate(text)
        text = text.replace('ा', 'ا').replace('ी', 'ی').replace('ो', 'و')
        if nativize:
            text = text.translate(sindhi_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'sd':
            return self.transliterate_from_devanagari_to_sindhi(text, nativize)
        return self.transliterate_from_sindhi_to_devanagari(text, nativize)
