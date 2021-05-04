URDU_POSTPROCESS_MAP = {
    # Normalizer to modern Urdu
    'ڃ': "ںی",
    'ݨ': 'ن',
    'ࣇ': 'ل',
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

HINDI_TO_URDU_VOWELS_ABJAD = {
    
}

INITIAL_HINDUSTANI_MAP_FILES = ['hindustani_initial_vowels.csv']
HINDUSTANI_CONSONANTS_MAP_FILES = ['hindustani_consonants.csv']
HINDUSTANI_MISC_MAP_FILES = ['hindustani_vowels.csv', 'hindustani_numerals.csv', 'hindustani_punctuations.csv']
FINAL_HINDUSTANI_MAP_FILES = ['hindustani_final_vowels.csv']

import os
import re
import pandas as pd
from .utils import StringTranslator

class HindustaniTransliterator:
    def __init__(self):
        data_dir = os.path.dirname(__file__) + '/data/'
        self.initial_urdu_to_hindi_map = {}
        self.final_urdu_to_hindi_map = {}
        self.urdu_to_hindi_map_pass1 = {}
        self.urdu_to_hindi_map_pass2 = {}

        for map_file in HINDUSTANI_MISC_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.urdu_to_hindi_map_pass1[urdu_letter] = hindi_letter

        for map_file in INITIAL_HINDUSTANI_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.initial_urdu_to_hindi_map[urdu_letter] = hindi_letter
        
        for map_file in FINAL_HINDUSTANI_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.final_urdu_to_hindi_map[urdu_letter] = hindi_letter
        
        for map_file in HINDUSTANI_CONSONANTS_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.urdu_to_hindi_map_pass2[urdu_letter] = hindi_letter

                # Non-initial forms: Consonant+ا to Consonant+ा
                self.urdu_to_hindi_map_pass2[urdu_letter+'ا'] = hindi_letter+'ा'
                if len(urdu_letter) == 1:
                    urdu_shadda, hindi_shadda = urdu_letter+" ّ".strip(), hindi_letter+'्'+hindi_letter
                    self.urdu_to_hindi_map_pass1[urdu_shadda] = hindi_shadda
                    self.urdu_to_hindi_map_pass1[urdu_shadda+'ا'] = hindi_shadda+'ा'
                    # Note on why it's not in pass-2: پکّا is converted as पक्कअ instead of पक्का (Regex sees shadda char as word boundary?)

        self.initial_urdu_to_hindi_converter = StringTranslator(self.initial_urdu_to_hindi_map, match_initial_only=True)
        self.final_urdu_to_hindi_converter = StringTranslator(self.final_urdu_to_hindi_map, match_final_only=True)
        self.urdu_to_hindi_converter_pass1 = StringTranslator(self.urdu_to_hindi_map_pass1)
        self.urdu_to_hindi_converter_pass2 = StringTranslator(self.urdu_to_hindi_map_pass2)
        # Monkey patch: Force ह to map only to ہ (not ھ)
        self.urdu_to_hindi_converter_pass2.reverse_translation_dict['ह'] = 'ہ'
        self.urdu_to_hindi_converter_pass2.reverse_translation_dict['ह'+'ा'] = 'ہ'+'ا'

        from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
        self.urdu_normalizer = IndicNormalizerFactory().get_normalizer('ur')
    
    def transliterate_from_urdu_to_hindi(self, text, nativize=False):
        text = self.urdu_normalizer.normalize(text) # Drops short-vowels/diacritics
        text = self.urdu_to_hindi_converter_pass1.translate(text)
        text = self.initial_urdu_to_hindi_converter.translate(text)
        text = self.final_urdu_to_hindi_converter.translate(text)
        text = self.urdu_to_hindi_converter_pass2.translate(text)
        return text

    def transliterate_from_hindi_to_urdu(self, text, nativize=False):
        # Assumes no short vowels
        # TODO: Pre-process to match Urdu Abjad
        text = self.urdu_to_hindi_converter_pass1.reverse_translate(text)
        text = self.initial_urdu_to_hindi_converter.reverse_translate(text)
        text = self.final_urdu_to_hindi_converter.reverse_translate(text)
        text = self.urdu_to_hindi_converter_pass2.reverse_translate(text)
        if nativize:
            text = text.translate(urdu_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'ur':
            return self.transliterate_from_hindi_to_urdu(text)
        return self.transliterate_from_urdu_to_hindi(text)
