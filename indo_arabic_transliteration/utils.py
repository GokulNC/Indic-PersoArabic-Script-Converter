import re

def sort_dict_by_descending_length(input_dict):
    output_dict = {}
    for k in sorted(input_dict, key=len, reverse=True):
        output_dict[k] = input_dict[k]
    return output_dict

def get_regex_matcher_from_array(array, match_initial_only=False, match_final_only=False, boundary_regex=r'\b'):
    regex_str = '|'.join(map(re.escape, array))
    if match_initial_only:
        regex_str = boundary_regex + regex_str.replace('|', '|'+boundary_regex)
    if match_final_only:
        regex_str = regex_str.replace('|', boundary_regex+'|') + boundary_regex
    return re.compile(regex_str)

class StringTranslator:
    '''
    A re-implementation of str.maketrans() to support multi-letter keys.
    More details: https://stackoverflow.com/q/63230213
    '''
    def __init__(self, translation_dict, sort_by_descending_key_length=True, match_initial_only=False, match_final_only=False, boundary_regex=r'\b', support_back_translation=True):

        self.translation_dict = translation_dict
        if sort_by_descending_key_length:
            self.translation_dict = sort_dict_by_descending_length(self.translation_dict)
        self.regex = get_regex_matcher_from_array(self.translation_dict, match_initial_only, match_final_only, boundary_regex)

        if support_back_translation:
            self.reverse_translation_dict = {value: key for key, value in translation_dict.items()}
            if sort_by_descending_key_length:
                self.reverse_translation_dict = sort_dict_by_descending_length(self.reverse_translation_dict)
            self.reverse_regex = get_regex_matcher_from_array(self.reverse_translation_dict, match_initial_only, match_final_only, boundary_regex)

    def translate(self, text):
        return self.regex.sub(lambda match: self.translation_dict[match.group(0)], text)

    def reverse_translate(self, text):
        return self.reverse_regex.sub(lambda match: self.reverse_translation_dict[match.group(0)], text)
