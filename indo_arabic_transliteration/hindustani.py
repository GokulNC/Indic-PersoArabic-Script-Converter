from .base import BaseIndoArabicTransliterator
import re

URDU_POSTPROCESS_MAP = {
    # Normalizer to modern Urdu
    'ݨ': "ن",
    'ࣇ': "ل",
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

CONSONANT_MAP_FILES = ['hindustani_consonants.csv']

class HindustaniTransliterator(BaseIndoArabicTransliterator):
    def __init__(self):
        super().__init__(CONSONANT_MAP_FILES)
        
        # Monkey patch: Force ह to map only to Urdu ہ (not ھ)
        self.arabic_to_devanagari_converter_pass2.reverse_translation_dict['ह'] = 'ہ'
        self.arabic_to_devanagari_converter_pass2.reverse_translation_dict['ह'+'ा'] = 'ہ'+'ا'
        self.arabic_to_devanagari_converter_pass1.reverse_translation_dict['ह्ह'] = 'ہّ'
        self.arabic_to_devanagari_converter_pass1.reverse_translation_dict['ह्ह'+'ा'] = 'ہّ'+'ا'
    
    def transliterate_ambiguous_urdu_words_to_hindi(self, text):
        # TODO: Handle these using mapper
        text = re.sub(r"(\b)و(\b)", "\\1व\\2", text)
        text = re.sub(r"(\b)میں(\b)", "\\1में\\2", text)
        text = re.sub(r"(\b)ہیں(\b)", "\\1हें\\2", text)
        return text
    
    def transliterate_from_urdu_to_hindi(self, text, nativize=False):
        text = self.arabic_normalize(text)
        text = self.transliterate_ambiguous_urdu_words_to_hindi(text)
        text = self.initial_arabic_to_devanagari_converter.translate(text)
        text = self.arabic_to_devanagari_converter_pass1.translate(text)
        text = self.final_arabic_to_devanagari_converter.translate(text)
        text = self.arabic_to_devanagari_converter_pass2.translate(text)
        text = self.arabic_to_devanagari_final_cleanup.translate(text)
        text = self.devanagari_postprocessor.translate(text) #  (جمہوریہ) जमहवरयह -> जमहोरयह
        text = self.devanagari_postprocessor.translate(text) # जमहोरयह -> जमहोरीह
        return text

    def transliterate_from_hindi_to_urdu(self, text, nativize=False):
        text = self.devanagari_normalize(text)
        text = self.arabic_to_devanagari_converter_pass1.reverse_translate(text)
        text = self.devanagari_remove_short_vowels(text) # Running it now since previous pass could have handled some short vowels (hamza_combos)
        text = text.replace('ा', 'ا') # Regex finds 'ा' as a \b unfortunately. So a quick hack to avoid those confusions
        text = self.initial_arabic_to_devanagari_converter.reverse_translate(text)
        text = self.final_arabic_to_devanagari_converter.reverse_translate(text)
        text = self.arabic_to_devanagari_converter_pass2.reverse_translate(text)
        text = self.arabic_to_devanagari_final_cleanup.reverse_translate(text)
        text = text.replace('ी', 'ی').replace('ो', 'و').replace('े', 'ے') # In-case anything remains, should never happen tho
        if nativize:
            text = text.translate(urdu_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'ur':
            return self.transliterate_from_hindi_to_urdu(text, nativize)
        return self.transliterate_from_urdu_to_hindi(text, nativize)
