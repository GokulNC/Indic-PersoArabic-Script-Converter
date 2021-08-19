# Indic-PersoArabic-Script-Converter

## Indo-Pakistani Transliteration

A python library to convert from Indian scripts to Pakistani scripts and vice-versa.

### Currently supported methods

1. Rule-based conversion
  - Faster, but does not support short vowels
  - Will not be accurate, especially for Arabic-to-Indic

2. [Sangam Project's online transliteration](http://sangam.learnpunjabi.org/) API
  - Uses an online endpoint for the conversion
  - Produces much better results, but much slower

## Usage

### Installation

Pre-requisites:  
- Use Python 3.7+
- `pip install git+https://github.com/GokulNC/indic_nlp_library`

```
pip install indo-arabic-transliteration
```

### Using rule-based conversion

```py
from indo_arabic_transliteration.mapper import script_convert
script_convert(text: str, from_script: str, to_script: str)
```

### Using Sangam API

```py
from indo_arabic_transliteration.sangam_api import online_transliterate
online_transliterate(text: str, from_script: str, to_script: str)
```

## Languages

We use the standard [BCP 47 language tags](https://github.com/libyal/libfwnt/wiki/Language-Code-identifiers#0x0400---0x04ff) to refer to the language-script combinations.

### Hindi-Urdu (Hindustani)

|Language|Script|Code|
|--------|------|----|
|Hindi|Devanagari|hi-IN|
|Urdu|Perso-Arabic|ur-PK|

Example:  
```py
# Rule-based
script_convert("हैदराबाद‎", 'hi-IN', 'ur-PK') # حیدرآباد
script_convert("حيدرآباد‎", 'ur-PK', 'hi-IN') # हीदराबाद‎

# Online-API
online_transliterate("حيدرآباد‎", 'ur-PK', 'hi-IN') # हैदराबाद‎
online_transliterate("हैदराबाद‎", 'hi-IN', 'ur-PK') # حیدرآباد‎
```

Notes & Resources:  
- Both the nations share a common national language ([Hindustani](https://en.wikipedia.org/wiki/Hindustani_language)) but written in different scripts and also registered as different languages.
- Official Tools
  - [Software by Pakistani Center for Language Engineering](https://www.cle.org.pk/software/langproc/h2utransliterator.html)
  - [Online Tool by Indian Center for Development of Advanced Computing](https://gisttransserver.in/)
- [Devanagari to PersoArabic mapping](https://wikipedia.org/wiki/Hindi-Urdu_transliteration)
  - Note: This same rule-based function can be used for [Saraiki](https://en.wikipedia.org/wiki/Saraiki_alphabet#Arabic_script) and [Shina](https://en.wikipedia.org/wiki/Shina_language#Writing) languages also
    - TODO: Shina characters [here](https://omniglot.com/writing/shina.htm) seems to be bit different. So use with caution

### Panjabi

|Language|Script|Code|
|--------|------|----|
|East Punjabi|Gur'Mukhi|pa-IN|
|West Punjabi|ShahMukhi|pa-PK|

Example:  
```py
# Rule-based
script_convert("ਸਿੰਘ", 'pa-IN', 'pa-PK') # سںگھ
script_convert("سںگھ", 'pa-PK', 'pa-IN') # ਸਂਘ

# Online-API
online_transliterate("سنگھ", 'pa-PK', 'pa-IN') # ਸਿੰਘ
online_transliterate("ਸਿੰਘ", 'pa-IN', 'pa-PK') # سِنگھ
```

Notes & Resources:  
- You can also use these JavaScript libraries:
  - [Anvaad-JS by KhalisFoundation](https://khalisfoundation.github.io/anvaad-js/)
  - [Gurmukhi-Utils by ShabadOS](https://github.com/shabados/gurmukhi-utils#toshahmukhitext--string) ([Demo](https://unicode.sarabveer.me/))
- [Gurmukhi to Shahmukhi mapping](https://en.wikipedia.org/wiki/Shahmukhi_alphabet#Alphabet)

### Sindhi

|Language|Script|Code|
|--------|------|----|
|Indian Sindhi|Devanagari|sd-IN|
|Pakistani Sindhi|Perso-Arabic|sd-PK|

Example:  
```py
# Rule-based
script_convert("हैदराबाद‎", 'sd-IN', 'sd-PK') # حیدرآباد
script_convert("حيدرآباد‎", 'sd-PK', 'sd-IN') # हीदराबाद‎

# Online-API
online_transliterate("حيدرآباد‎", 'sd-PK', 'sd-IN') # हैदराबाद‎
online_transliterate("हैदराबाद‎", 'sd-IN', 'sd-PK') # حیدرآباد‎
```

Notes & Resources:  
- Before Devanagari standardization, Sindhi was written in Landa scripts like Khojki, Khudawadi, Multani, Gurmukhi, etc. depending upon the region.
  - To convert from Devanagari to the above legacy scripts, use [AksharaMukha](http://aksharamukha.appspot.com/converter)'s python library.
- You can also use this [JavaScript library](https://github.com/fahadmaqsood/sindhi-transliterator) or [online converter](http://roman.sindhila.edu.pk/).
- [Sindhi-PersoArabic to Devanagari mapping](https://en.wikipedia.org/wiki/Sindhi_transliteration)

---

## Other Methods

### MachineLearning-based Transliteration

- Uses [LibIndicTrans library](https://github.com/libindic/indic-trans) for models
  - Install it by `pip install git+https://github.com/libindic/indic-trans`
- Currently supports only Hindi-Urdu languages

API:  
```py
from indo_arabic_transliteration.ml_based import ml_transliterate
# Same interface as script_convert()
```

### Indic-to-Arabic with Diacritics

- Indic scripts are mostly phonetic. Use this to retain diacritics in PersoArabic
  - Currently only supports Hindustani (Hindi to Urdu) and Punjabi (Gurmukhi to Shahmukhi)
  - Uses [AksharaMukhi library](https://github.com/virtualvinodh/aksharamukha)

API:  
```py
from indo_arabic_transliteration.lossless_converter import convert_with_diacritics
# Same interface as script_convert()
```

---

## Support

- For help in using the library, please use the GitHub Issues section.
- For script conversion errors from the online API, please write directly to the Sangam team. We are not related to them in anyway and this is not an official library.
