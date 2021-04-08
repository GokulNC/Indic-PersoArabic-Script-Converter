ARABIC_NORMALIZE_MAP = {
    'أ': 'ا',
    'ۃ': "ت",
}
arabic_normalizer = str.maketrans(ARABIC_NORMALIZE_MAP)

URDU_POSTPROCESS_MAP = {
    'ڃ': "ںی",
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

HINDUSTANI_MAP_FILES = ['hindustani_consonants.csv', 'hindustani_initial_vowels.csv', 'hindustani_vowels.csv', 'hindustani_numerals.csv', 'hindustani_punctuations.csv']

import os
import re
import pandas as pd
from .utils import StringTranslator

class HindustaniTransliterator:
    def __init__(self):
        data_dir = os.path.dirname(__file__) + '/data/'
        self.urdu_to_hindi_map = {}
        
        for map_file in HINDUSTANI_MAP_FILES:
            df = pd.read_csv(data_dir+map_file, header=None)
            for i in df.columns:
                self.urdu_to_hindi_map[str(df[i][0]).strip()] = str(df[i][2]).strip()
                if 'consonants' in map_file:
                    # Non-initial forms: Consonant+ا to Consonant+ा
                    self.urdu_to_hindi_map[str(df[i][0]).strip()+'ا'] = str(df[i][2]).strip()+'ा'
                    # Final forms: Consonant+ی to Consonant+ी
                    self.urdu_to_hindi_map[str(df[i][0]).strip()+'ی'+' '] = str(df[i][2]).strip()+'ी '
                    # Final forms: Consonant+و to Consonant+ो (Approximation for readability)
                    self.urdu_to_hindi_map[str(df[i][0]).strip()+'و'+' '] = str(df[i][2]).strip()+'ो '

        self.urdu_to_hindi_converter = StringTranslator(self.urdu_to_hindi_map)

        from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
        self.urdu_normalizer = IndicNormalizerFactory().get_normalizer('ur')

    def normalize_urdu(self, text):
        text = self.urdu_normalizer.normalize(text) # Drops short-vowels/diacritics
        text = text.translate(arabic_normalizer) # Normalize Arabics not handled in UrduHack
        return text
    
    def transliterate_from_urdu_to_hindi(self, text):
        text = self.normalize_urdu(text)
        text = self.urdu_to_hindi_converter.translate(text)

        return text
