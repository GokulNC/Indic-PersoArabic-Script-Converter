URDU_POSTPROCESS_MAP = {
    # Normalizer to modern Urdu
    'ڃ': "ںی",
    'ݨ': "ن",
    'ࣇ': "ل",
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

HINDI_TO_URDU_VOWELS_ABJAD = {
    
}

INITIAL_MAP_FILES = ['initial_vowels.csv']
MAIN_MAP_FILES = ['hindustani_consonants.csv', 'vowels.csv']
MISC_MAP_FILES = ['numerals.csv', 'punctuations.csv', 'hamza.csv', 'hamza_combo.csv']
FINAL_MAP_FILES = ['final_vowels.csv']

import os
import re
import pandas as pd
from .utils import StringTranslator

from urduhack.normalization.character import remove_diacritics, normalize_characters, normalize_combine_characters

class HindustaniTransliterator:
    def __init__(self):
        data_dir = os.path.dirname(__file__) + '/data/'
        self.initial_urdu_to_hindi_map = {}
        self.final_urdu_to_hindi_map = {}
        self.urdu_to_hindi_map_pass1 = {}
        self.urdu_to_hindi_map_pass2 = {}
        self.urdu_to_hindi_cleanup_pass = {} # To handle chars at erraneous/unconventional places
        self.hindi_postprocess_map = {}

        for map_file in MISC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.urdu_to_hindi_map_pass1[urdu_letter] = hindi_letter

        for map_file in INITIAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.initial_urdu_to_hindi_map[urdu_letter] = hindi_letter
                self.urdu_to_hindi_cleanup_pass[urdu_letter] = hindi_letter
        
        for map_file in FINAL_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.final_urdu_to_hindi_map[urdu_letter] = hindi_letter
        
        consonants = []
        for map_file in MAIN_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.urdu_to_hindi_map_pass2[urdu_letter] = hindi_letter
                if 'consonants' not in map_file:
                    continue

                # Non-initial forms: Consonant+ا to Consonant+ा
                self.urdu_to_hindi_map_pass2[urdu_letter+'ا'] = hindi_letter+'ा'
                if urdu_letter not in {'ی', 'و', 'ھ'}:
                    consonants.append((urdu_letter, roman_letter, hindi_letter))

                if len(urdu_letter) == 1:
                    urdu_shadda, hindi_shadda = urdu_letter+" ّ".strip(), hindi_letter+'्'+hindi_letter
                    self.urdu_to_hindi_map_pass1[urdu_shadda] = hindi_shadda
                    self.urdu_to_hindi_map_pass1[urdu_shadda+'ا'] = hindi_shadda+'ा'
                    # Note on why it's not in pass-2: پکّا is converted as पक्कअ instead of पक्का (Regex sees shadda char as word boundary?)

        # Assume medial ی as ी and و as ो
        for i in range(len(consonants)):
            urdu_letter_i, roman_letter_i, hindi_letter_i = consonants[i]
            for j in range(len(consonants)):
                urdu_letter_j, roman_letter_j, hindi_letter_j = consonants[j]
                self.hindi_postprocess_map[hindi_letter_i+'य'+hindi_letter_j] = hindi_letter_i+'ी'+hindi_letter_j
                self.hindi_postprocess_map[hindi_letter_i+'व'+hindi_letter_j] = hindi_letter_i+'ो'+hindi_letter_j
                self.hindi_postprocess_map[hindi_letter_i+'यं'+hindi_letter_j] = hindi_letter_i+'ीं'+hindi_letter_j
                self.hindi_postprocess_map[hindi_letter_i+'वं'+hindi_letter_j] = hindi_letter_i+'ों'+hindi_letter_j

        self.initial_urdu_to_hindi_converter = StringTranslator(self.initial_urdu_to_hindi_map, match_initial_only=True)
        self.final_urdu_to_hindi_converter = StringTranslator(self.final_urdu_to_hindi_map, match_final_only=True)
        self.urdu_to_hindi_converter_pass1 = StringTranslator(self.urdu_to_hindi_map_pass1)
        self.urdu_to_hindi_converter_pass2 = StringTranslator(self.urdu_to_hindi_map_pass2)
        self.urdu_to_hindi_final_cleanup = StringTranslator(self.urdu_to_hindi_cleanup_pass)
        self.hindi_postprocessor = StringTranslator(self.hindi_postprocess_map)
        
        # Monkey patch: Force ह to map only to Urdu ہ (not ھ)
        self.urdu_to_hindi_converter_pass2.reverse_translation_dict['ह'] = 'ہ'
        self.urdu_to_hindi_converter_pass2.reverse_translation_dict['ह'+'ा'] = 'ہ'+'ا'
        self.urdu_to_hindi_converter_pass1.reverse_translation_dict['ह्ह'] = 'ہّ'
        self.urdu_to_hindi_converter_pass1.reverse_translation_dict['ह्ह'+'ा'] = 'ہّ'+'ا'

        from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
        self.hindi_normalizer = IndicNormalizerFactory().get_normalizer('hi')
    
    def urdu_normalize(self, text):
        text = remove_diacritics(text) # Drops short-vowels
        text = normalize_combine_characters(normalize_characters(text))
        return text
    
    def transliterate_from_urdu_to_hindi(self, text, nativize=False):
        text = self.urdu_normalize(text)
        text = self.urdu_to_hindi_converter_pass1.translate(text)
        text = self.initial_urdu_to_hindi_converter.translate(text)
        text = self.final_urdu_to_hindi_converter.translate(text)
        text = self.urdu_to_hindi_converter_pass2.translate(text)
        text = self.urdu_to_hindi_final_cleanup.translate(text)
        text = self.hindi_postprocessor.translate(text) #  (جمہوریہ) जमहवरयह -> जमहोरयह
        text = self.hindi_postprocessor.translate(text) # जमहोरयह -> जमहोरीह
        return text

    def transliterate_from_hindi_to_urdu(self, text, nativize=False):
        # Assumes no short vowels
        # TODO: Pre-process to match Urdu Abjad
        text = self.hindi_postprocessor.reverse_translate(text)
        text = self.hindi_postprocessor.reverse_translate(text)
        text = self.urdu_to_hindi_converter_pass1.reverse_translate(text)
        text = self.initial_urdu_to_hindi_converter.reverse_translate(text)
        text = self.final_urdu_to_hindi_converter.reverse_translate(text)
        text = self.urdu_to_hindi_converter_pass2.reverse_translate(text)
        text = self.urdu_to_hindi_final_cleanup.reverse_translate(text)
        if nativize:
            text = text.translate(urdu_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'ur':
            return self.transliterate_from_hindi_to_urdu(text)
        return self.transliterate_from_urdu_to_hindi(text)
