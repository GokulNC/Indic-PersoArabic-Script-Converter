import requests

BASE_URL = "http://sangam.learnpunjabi.org/SindhiTransliteration.asmx/"

ENDPOINTS = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): BASE_URL+'Hindi2Urdu',
    ('ur-PK', 'hi-IN'): BASE_URL+'Urdu2Hindi',
    
    # Punjabi scripts
    ('pa-IN', 'pa-PK'): BASE_URL+'Gurmukhi2Shahmukhi',
    ('pa-PK', 'pa-IN'): BASE_URL+'Shahmukhi2Gurmukhi',
    
    # Sindhi scripts
    ('sd-IN', 'sd-PK'): BASE_URL+'SindhiDEV2SindhiUR',
    ('sd-PK', 'sd-IN'): BASE_URL+'SindhiUR2SindhiDEV',
}

def online_transliterate(text: str, from_script: str, to_script: str, retry_attempts=5) -> str:
    """Transliterate the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script
        to_script (str): Target script

    Returns:
        str: Transliterated text from SANGAM server
    """
    api_url = ENDPOINTS[(from_script, to_script)]
    for i in range(retry_attempts):
        try:
            response = requests.post(api_url, json={'input': text}, timeout=5)
            return response.json()['d']
        except requests.exceptions.Timeout:
            pass
    
    raise requests.exceptions.Timeout

if __name__ == '__main__':
    # Test
    print(convert(convert('हिन्दुस्तानी', 'hi-IN', 'ur-PK'), 'ur-PK', 'hi-IN'))
    print(convert(convert('ਪੰਜਾਬੀ', 'pa-IN', 'pa-PK'), 'pa-PK', 'pa-IN'))
    print(convert(convert('सिन्धी', 'sd-IN', 'sd-PK'), 'sd-PK', 'sd-IN'))
