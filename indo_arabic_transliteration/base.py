import os
import re
import pandas as pd
from .str_mapper import StringTranslator
from .common import devanagari_preprocessor, devanagari_abjadifier, devanagari_initial_vowels_abjadifier, devanagari_nuqta_consonants_simplifier

from urduhack.normalization.character import remove_diacritics, normalize_characters, normalize_combine_characters

INITIAL_MAP_FILES = ['initial_vowels.csv']
MAIN_MAP_FILES = ['vowels.csv']
MISC_MAP_FILES = ['numerals.csv', 'punctuations.csv']
FINAL_MAP_FILES = ['final_vowels.csv']
ARABIC_MAP_FILES = ['arabic.csv']

HAMZA_FILES = ['hamza.csv']
HAMZA_COMBO_FILES = ['hamza_combo.csv']

class BaseIndoArabicTransliterator:
    '''
    Common processing for all supported Indo-Pakistani languages (except Kashmiri)
    '''
    def __init__(self, consonants_map_files, data_dir=os.path.dirname(__file__) + '/data/'):
        self.data_dir = data_dir
        self.initial_arabic_to_devanagari_map = {}
        self.final_arabic_to_devanagari_map = {}
        self.arabic_to_devanagari_map_pass1 = {}
        self.arabic_to_devanagari_map_pass2 = {}
        self.arabic_to_devanagari_cleanup_pass = {} # To handle chars at erraneous/unconventional places
        self.hamza_to_devanagari_map = {}
        self.hamza_combo_to_devanagari_map = {}
        self.devanagari_postprocess_map = {}

        for map_file in MISC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.arabic_to_devanagari_map_pass1[arabic_letter] = devanagari_letter

        for map_file in INITIAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.initial_arabic_to_devanagari_map[arabic_letter] = devanagari_letter
                self.arabic_to_devanagari_cleanup_pass[arabic_letter] = devanagari_letter
        
        for map_file in FINAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.final_arabic_to_devanagari_map[arabic_letter] = devanagari_letter
                self.arabic_to_devanagari_cleanup_pass[arabic_letter] = devanagari_letter # Sometimes, Devanagari vowel-marks doesn't work without this
        
        for map_file in ARABIC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                # TODO: Some of these are initial_only matchers. Handle them
                self.arabic_to_devanagari_cleanup_pass[arabic_letter] = devanagari_letter
        
        for map_file in HAMZA_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.hamza_to_devanagari_map[arabic_letter] = devanagari_letter
        
        for map_file in HAMZA_COMBO_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.hamza_combo_to_devanagari_map[arabic_letter] = devanagari_letter

        for map_file in MAIN_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.arabic_to_devanagari_map_pass2[arabic_letter] = devanagari_letter
        
        consonants = []
        for map_file in consonants_map_files:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                arabic_letter, roman_letter, devanagari_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.arabic_to_devanagari_map_pass2[arabic_letter] = devanagari_letter

                # Non-initial forms: Consonant+ا to Consonant+ा
                self.arabic_to_devanagari_map_pass2[arabic_letter+'ا'] = devanagari_letter+'ा'
                if arabic_letter not in {'ی', 'و', 'ھ'}:
                    consonants.append((arabic_letter, roman_letter, devanagari_letter))

                arabic_shadda, devanagari_shadda = arabic_letter+" ّ".strip(), devanagari_letter+'्'+devanagari_letter
                self.arabic_to_devanagari_map_pass1[arabic_shadda] = devanagari_shadda
                self.arabic_to_devanagari_map_pass1[arabic_shadda+'ا'] = devanagari_shadda+'ा'
                # Note on why it's not in pass-2: پکّا is converted as पक्कअ instead of पक्का (Regex sees shadda char as word boundary?)

        # Assume medial ی as ी and و as ो
        for i in range(len(consonants)):
            arabic_letter_i, roman_letter_i, devanagari_letter_i = consonants[i]
            for j in range(len(consonants)):
                arabic_letter_j, roman_letter_j, devanagari_letter_j = consonants[j]
                self.devanagari_postprocess_map[devanagari_letter_i+'य'+devanagari_letter_j] = devanagari_letter_i+'ी'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'व'+devanagari_letter_j] = devanagari_letter_i+'ो'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'यं'+devanagari_letter_j] = devanagari_letter_i+'ीं'+devanagari_letter_j
                self.devanagari_postprocess_map[devanagari_letter_i+'वं'+devanagari_letter_j] = devanagari_letter_i+'ों'+devanagari_letter_j

        self.initial_arabic_to_devanagari_converter = StringTranslator(self.initial_arabic_to_devanagari_map, match_initial_only=True)
        self.final_arabic_to_devanagari_converter = StringTranslator(self.final_arabic_to_devanagari_map, match_final_only=True)
        self.arabic_to_devanagari_converter_pass1 = StringTranslator(self.arabic_to_devanagari_map_pass1)
        self.arabic_to_devanagari_converter_pass2 = StringTranslator(self.arabic_to_devanagari_map_pass2)
        self.arabic_to_devanagari_final_cleanup = StringTranslator(self.arabic_to_devanagari_cleanup_pass)
        self.hamza_to_devanagari_converter = StringTranslator(self.hamza_to_devanagari_map)
        self.hamza_combo_to_devanagari_converter = StringTranslator(self.hamza_combo_to_devanagari_map)
        self.devanagari_postprocessor = StringTranslator(self.devanagari_postprocess_map)

        from indicnlp.normalize.indic_normalize import DevanagariNormalizer
        self.devanagari_normalizer = DevanagariNormalizer()
    
    def arabic_normalize(self, text):
        text = remove_diacritics(text) # Drops short-vowels
        text = normalize_combine_characters(normalize_characters(text))
        text = text.replace(',', '،').replace('?', '؟').replace('؛', ';').replace('؍', '/').replace('٪', '%')

        # Improper hamzas
        text = text.replace("اے", "ائے")
        text = text.replace("یے", "ئے")
        return text
    
    def devanagari_normalize(self, text, abjadify_initial_vowels=False, drop_virama=False):
        text = self.devanagari_normalizer.normalize(text)
        if abjadify_initial_vowels:
            text = devanagari_initial_vowels_abjadifier.translate(text)
        if drop_virama:
            text = text.replace('्', '')

        text = self.devanagari_postprocessor.reverse_translate(text)
        text = self.devanagari_postprocessor.reverse_translate(text)
        text = devanagari_preprocessor.translate(text)
        return text
    
    def devanagari_remove_short_vowels(self, text):
        text = text.translate(devanagari_abjadifier)
        text = re.sub("े([\u0900-\u0963\u0972-\u097f])", "ी\\1", text) # bari ye can be only in final position
        return text

    def devanagari_nativize(self, text):
        return devanagari_nuqta_consonants_simplifier.translate(text)
