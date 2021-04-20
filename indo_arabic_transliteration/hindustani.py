URDU_POSTPROCESS_MAP = {
    'ڃ': "ںی",
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

HINDI_TO_URDU_VOWELS_ABJAD = {
    
}

INITIAL_HINDUSTANI_MAP_FILES = ['hindustani_initial_vowels.csv']
HINDUSTANI_MAP_FILES = ['hindustani_consonants.csv', 'hindustani_vowels.csv', 'hindustani_numerals.csv', 'hindustani_punctuations.csv']
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
        self.urdu_to_hindi_map = {}

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
        
        for map_file in HINDUSTANI_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                urdu_letter, roman_letter, hindi_letter = str(df[i][0]).strip(), str(df[i][1]).strip(), str(df[i][2]).strip()
                self.urdu_to_hindi_map[urdu_letter] = hindi_letter
                if 'consonants' in map_file:
                    # Non-initial forms: Consonant+ا to Consonant+ा
                    self.urdu_to_hindi_map[urdu_letter+'ا'] = hindi_letter+'ा'
                    if len(urdu_letter) == 1:
                        urdu_shadda, hindi_shadda = urdu_letter+" ّ".strip(), hindi_letter+'्'+hindi_letter
                        self.urdu_to_hindi_map[urdu_shadda] = hindi_shadda

        self.initial_urdu_to_hindi_converter = StringTranslator(self.initial_urdu_to_hindi_map, match_initial_only=True)
        self.final_urdu_to_hindi_converter = StringTranslator(self.final_urdu_to_hindi_map, match_final_only=True)
        self.urdu_to_hindi_converter = StringTranslator(self.urdu_to_hindi_map)

        from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
        self.urdu_normalizer = IndicNormalizerFactory().get_normalizer('ur')
    
    def transliterate_from_urdu_to_hindi(self, text):
        text = self.urdu_normalizer.normalize(text) # Drops short-vowels/diacritics
        text = self.initial_urdu_to_hindi_converter.translate(text)
        text = self.final_urdu_to_hindi_converter.translate(text)
        text = self.urdu_to_hindi_converter.translate(text)
        return text

    def transliterate_from_hindi_to_urdu(self, text):
        # Assumes no short vowels
        # TODO: Pre-process to match Urdu Abjad
        text = self.initial_urdu_to_hindi_converter.reverse_translate(text)
        text = self.final_urdu_to_hindi_converter.reverse_translate(text)
        text = self.urdu_to_hindi_converter.reverse_translate(text)
        return text
    
    def __call__(self, text, src_lang, dest_lang):
        if dest_lang == 'ur':
            return self.transliterate_from_hindi_to_urdu(text)
        return self.transliterate_from_urdu_to_hindi(text)
