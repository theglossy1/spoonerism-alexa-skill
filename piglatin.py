"""
Split the words into a list (ipa module can do for us)
Take the first list item and get all characters up to the first vowel
Take the final list item and get all characters up to the first vowel
Swap the first set and the last set
"""

import sys
import eng_to_ipa as ipa

def consonant_cluster(word):
    res = ['']
    for (i, char) in enumerate(word):
        if char not in VOWELS:
            res[0] += char
        else:
            res.append(word[i:])
            break
    return res

TRANSFORMS = {'a':'an'}
CUSTOM_CONVERSIONS = {'to': 'uteɪ', 'too': 'uteɪ', 'two': 'uteɪ'}
SKIPS = ['the','in','an','is','of']
VOWELS = "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒ"
VOWELS += VOWELS.upper()

def pigify(word):
    if word in TRANSFORMS:
        return ipa.convert(TRANSFORMS[word])
    if word in SKIPS:
        return ipa.convert(word)
    elif word in CUSTOM_CONVERSIONS:
        return CUSTOM_CONVERSIONS[word]
    else:
        #if word[-2:] == "'s":
        #    word = word[:-2]
        #    suffix = "eɪz"
        #else:
        suffix = "eɪ"
        word_parts = consonant_cluster(ipa.convert(word))        
        return word_parts[1] + word_parts[0] + suffix

def ssmlify(sentence):
    res = '<speak>\n'
    data = '<phoneme alphabet="ipa" ph="{piglatined}"/>\n'
    word_list = sentence.split()
    for (i,words) in enumerate(word_list):
        piglatined = pigify(words)
        res += data.format(piglatined=piglatined)
    res += '</speak>'
    return res

if __name__ == '__main__':
    # word_list = ' '.join(sys.argv[1:]).split()
    #     print(pigify(words))
    print(ssmlify(' '.join(sys.argv[1:])))