from .hindustani import HindustaniTransliterator

class PunjabiTransliterator(HindustaniTransliterator):
    def __init__(self):
        super().__init__()

        from indicnlp.normalize.indic_normalize import GurmukhiNormalizer
        self.gurmukhi_normalizer = GurmukhiNormalizer()

        from aksharamukha.transliterate import process
        self.aksharamukha_xlit = process
    
    def transliterate_from_gurmukhi_to_shahmukhi(self, text):
        text = self.gurmukhi_normalizer.normalize(text)
        text = self.aksharamukha_xlit("Gurmukhi", "Devanagari", text)
        return self.transliterate_from_hindi_to_urdu(text)

    def transliterate_from_shahmukhi_to_gurmukhi(self, text):
        text = self.transliterate_from_urdu_to_hindi(text)
        return self.aksharamukha_xlit("Devanagari", "Gurmukhi", text)

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if src_lang == 'pa' and dest_lang == 'pnb':
            return self.transliterate_from_gurmukhi_to_shahmukhi(text)
        else:
            return self.transliterate_from_shahmukhi_to_gurmukhi(text)
