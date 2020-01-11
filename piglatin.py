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

# sentence = "i am funny"

TRANSFORMS = {'a':'an'}
SKIPS = ['the','in','an','is','of']
VOWELS = "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒ"
VOWELS += VOWELS.upper()

def pigify(word):
    if word in TRANSFORMS:
        return ipa.convert(TRANSFORMS[word])
    if word in SKIPS:
        return ipa.convert(word)
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
    piglatined = pigify(sentence)
    data = f'<phoneme alphabet="ipa" ph="{piglatined}"/>\n</speak>'
    return res + data

    # The following works very well for "bleeping out" the middle of a censored word (e.g., the shi-word)
    # we should make a dictionary of IPA words (just two for now)
    # <speak>
    #  <phoneme alphabet="ipa" ph="ʃ"/>
    #  <say-as interpret-as="expletive">shoot</say-as>
    #  <phoneme alphabet="ipa" ph="t"/>
    # </speak>
    # See: https://developer.amazon.com/it-IT/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html

    # This is Josiah's previous stuff:
    # splitted = spoonerism.split()
    # for word in splitted:
    #     if word[-1] != '*':
    #         res += data % word
    #     else:
    #         res += word[:-1]
    #     res += '\n'
    # res += '</speak>\n'
    # return res

if __name__ == '__main__':
    word_list = ' '.join(sys.argv[1:]).split()
    for (i,words) in enumerate(word_list):
        print(pigify(words))