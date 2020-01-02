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

VOWELS = "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒ"

def spoonerify(sentence, return_ipa=False):
    sentence_ipa = ipa.convert(sentence)
    sentence_list = sentence_ipa.split()
    first_word = sentence_list[0]
    final_word = sentence_list[-1]
    middle_words = sentence_list[1:-1]

    first_word_list = consonant_cluster(first_word)
    final_word_list = consonant_cluster(final_word)

    first_word = final_word_list[0] + first_word_list[1]
    final_word = first_word_list[0] + final_word_list[1]

    result = ' '.join((first_word, ' '.join(middle_words), final_word))
    if return_ipa:
        result = (sentence_ipa, result)
    return result

def ssmlify(sentence):
    res = '<speak>\n'
    spoonerism = spoonerify(sentence)
    data = f'<phoneme alphabet="ipa" ph="{spoonerism}"/>\n</speak>'
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
    sentence = ' '.join(sys.argv[1:])
    result = ssmlify(sentence)
    print(result)
    # bug: for two-word spoonerisms, returns two spaces (not a big deal)