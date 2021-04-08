# Indic-PersoArabic-Script-Converter

## Indo-Pakistani Transliteration

A python library to use the [SANGAM Project's online transliteration](http://sangam.learnpunjabi.org/) API, to convert from Indian scripts to Pakistani scripts and vice-versa.

## Usage

```py
from indo_arabic_transliteration.sangam_api import convert
convert(text: str, from_script: str, to_script: str)
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
convert("حيدرآباد‎", 'ur-PK', 'hi-IN') # हैदराबाद‎

convert("हैदराबाद‎", 'hi-IN', 'ur-PK') # حیدرآباد‎
```

Notes & Resources:  
- Both the nations share a common national language ([Hindustani](https://en.wikipedia.org/wiki/Hindustani_language)) but written in different scripts and also registered as different languages.
- Official Tools
  - [Software by Pakistani Center for Language Engineering](https://www.cle.org.pk/software/langproc/h2utransliterator.html)
  - [Online Tool by Indian Center for Development of Advanced Computing](https://gisttransserver.in/)
- For offline Hindi-Urdu transliteration using Python, use [LibIndic-Trans](https://github.com/libindic/indic-trans).
- [Devanagari to PersoArabic mapping](http://www.learnpunjabi.org/pdf/paper248.pdf)

### Panjabi

|Language|Script|Code|
|--------|------|----|
|East Punjabi|Gur'Mukhi|pa-IN|
|West Punjabi|ShahMukhi|pa-PK|

Example:  
```py
convert("سِنگھ", 'pa-PK', 'pa-IN') # ਸਿੰਘ

convert("ਸਿੰਘ", 'pa-IN', 'pa-PK') # سِنگھ
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
convert("حيدرآباد‎", 'sd-PK', 'sd-IN') # हैदराबाद‎

convert("हैदराबाद‎", 'sd-IN', 'sd-PK') # حیدرآباد‎
```

Notes & Resources:  
- Before Devanagari standardization, Sindhi was written in Landa scripts like Khojki, Khudawadi, Multani, Gurmukhi, etc. depending upon the region.
  - To convert from Devanagari to the above legacy scripts, use [AksharaMukha](http://aksharamukha.appspot.com/converter)'s python library.
- You can also use this [JavaScript library](https://github.com/fahadmaqsood/sindhi-transliterator) or [online converter](http://roman.sindhila.edu.pk/).
- [PersoArabic to Devanagari mapping](https://transliteration.eki.ee/pdf/Sindhi.pdf)

---

## Support

- For help in using the library, please use the GitHub Issues section.
- For script conversion errors, please write directly to the SANGAM team. We are not related to them in anyway and this is not an official library.
