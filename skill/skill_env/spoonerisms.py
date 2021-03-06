"""
Split the words into a list (ipa module can do for us)
Take the first list item and get all characters up to the first vowel
Take the final list item and get all characters up to the first vowel
Swap the first set and the last set
"""

import sys
import requests, io
import eng_to_ipa as ipa
from zipfile import ZipFile

def consonant_cluster(word):
    res = ['']
    for (i, char) in enumerate(word):
        if char not in VOWELS:
            res[0] += char
        else:
            res.append(word[i:])
            break
    else: res.append('')
    return tuple(res)

VOWELS = "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒ"
VOWELS += VOWELS.upper()
SWEARS = []
def init():
    SWEARS[:] = ZipFile('swear_list.zip').open('swear_list.txt', pwd=b'openZipUp').read().decode().split('\r\n')

def spoonerify(sentence):
    sentence_list = sentence.split()
    if len(sentence_list) == 0:
        # pseudocode: if the "sentence" is only 1 word, break it up according to the following rules:
        #  if it's only 1 syllable, pass
        #  else if it hits a [ˌ'] character (unless [ˌ'] is the first or second position), split the word on that, with ˌ or ' going on end of 1st word
        #     if there's a vowel right after ' then copy the previous consonant (e.g., "ˌsɪndərˈɛlə" becomes "ˌsɪndərˈ rɛlə" spoonerizes to "ˌrɪndərˈ sɛlə")
        #  else if it hits a consonant (after the first one or after the beginning of line), take that consonant as part of the second word
        #  re-combine words for prounciation
        pass
    else:
        first_word = sentence_list[0]
        final_word = sentence_list[-1]
        middle_words = sentence_list[1:-1]

    first_word_list = list(consonant_cluster(first_word))
    final_word_list = list(consonant_cluster(final_word))

    first_word = final_word_list[0] + first_word_list[1]
    final_word = first_word_list[0] + final_word_list[1]

    result = ' '.join((first_word, ' '.join(middle_words), final_word))
    return result

def ssmlify(sentence):
    res = '<speak><prosody rate="slow">\n'
    swear_data = """<phoneme alphabet="ipa" ph="%s"/>
<say-as interpret-as="expletive">%s</say-as>
<phoneme alphabet="ipa" ph="%s"/>\n"""
    data = '<phoneme alphabet="ipa" ph="%s">%s</phoneme>'
    data_original = '<phoneme alphabet="ipa" ph="%s"/>%s'
    spoonerism = spoonerify(sentence)
    spoonerism_ipa = spoonerify(ipa.convert(sentence))
    splitted = spoonerism.split()
    splitted_ipa = spoonerism_ipa.split()
    broken = False
    for (i, word) in enumerate(splitted_ipa):
        original = splitted[i]
        if original.lower() in SWEARS:
            res += swear_data % (consonant_cluster(word)[0], original[:-2], word[-1])
            continue
        if not (i < len(splitted) - 1 and i > 0):
            if word[-1] != '*':
                res += data % (word, original)
            else:
                word = word[:-1]
                res += data_original % consonant_cluster(word)
        else:
            res += original
        if i < len(splitted) - 1:
            res += '<break strength="x-weak"/>'
        res += '\n'
    res += '</prosody></speak>\n'
    return res

    # The following works very well for "bleeping out" the middle of a censored word (e.g., the shi-word)
    # we should make a dictionary of IPA words (just two for now)
    # <speak>
    #  <phoneme alphabet="ipa" ph="ʃ"/>
    #  <say-as interpret-as="expletive">shoot</say-as>
    #  <phoneme alphabet="ipa" ph="t"/>
    # </speak>
    # See: https://developer.amazon.com/it-IT/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html

    # This is Matt's previous stuff:
    # data = '<phoneme alphabet="ipa" ph="{spoonerism}"/>\n</speak>'
    # return res + data

if __name__ == '__main__':
    init()
    sentence = ' '.join(sys.argv[1:])
    result = ssmlify(sentence)
    print(result)
    # bug: for two-word spoonerisms, returns two spaces (not a big deal)