import re

class StringTranslator:
    '''
    A re-implementation of str.maketrans() to support multi-letter keys.
    More details: https://stackoverflow.com/q/63230213
    '''
    def __init__(self, translation_dict, sort_by_descending_key_length=True):

        if sort_by_descending_key_length:
            self.translation_dict = {}
            for k in sorted(translation_dict, key=len, reverse=True):
                self.translation_dict[k] = translation_dict[k]
        else:
            self.translation_dict = translation_dict
        
        self.regex = re.compile('|'.join(map(re.escape, self.translation_dict)))

    def translate(self, text):
        return self.regex.sub(lambda match: self.translation_dict[match.group(0)], text)
