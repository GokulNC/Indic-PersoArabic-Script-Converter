# Indic-PersoArabic-Script-Converter

## Indo-Pakistani Transliteration

A python library to use the [SANGAM Project's online transliteration](http://sangam.learnpunjabi.org/) API, to convert from Indian scripts to Pakistani scripts and vice-versa.

## Usage

### Using rule-based conversion

- Use this for raw conversion.
- Will not be accurate, especially for Arabic-to-Indic
  - Because it does direct one-to-one mapping between the scripts

```py
from indo_arabic_transliteration import script_convert
script_convert(text: str, from_script: str, to_script: str)
```

### Using SANGAM API

- Uses an online API for transliteration
- Produces much better results, but much slower

```py
from indo_arabic_transliteration import online_transliterate
online_transliterate(text: str, from_script: str, to_script: str)
```

## Languages

- [Hindi-Urdu](#Hindustani)
- [Punjabi](#Panjabi)
- [Sindhi](#Sindhi)

We use the standard [BCP 47 language tags](https://github.com/libyal/libfwnt/wiki/Language-Code-identifiers#0x0400---0x04ff) to refer to the language-script combinations.

### Hindustani

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
- For offline Hindi-Urdu transliteration using Python, use [LibIndic-Trans](https://github.com/libindic/indic-trans).
- [Devanagari to PersoArabic mapping](https://wikipedia.org/wiki/Hindi-Urdu_transliteration)
  - Note: This same rule-based function can be used for [Saraiki language](https://en.wikipedia.org/wiki/Saraiki_alphabet#Arabic_script) also

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
- [PersoArabic to Devanagari mapping](https://transliteration.eki.ee/pdf/Sindhi.pdf)

---

## Support

- For help in using the library, please use the GitHub Issues section.
- For script conversion errors from the online API, please write directly to the SANGAM team. We are not related to them in anyway and this is not an official library.
