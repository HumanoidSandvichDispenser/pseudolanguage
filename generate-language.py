#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 sandvich <sandvich@manjaro>
#
# Distributed under terms of the GPLv3 license.

from typing import Dict, List
import toml
import click
import utils
import random


phonemes = { }
syllables = { }

@click.command()
#@click.option("-n", "--nouns", default = 50)
#@click.option("-v", "--verbs", default = 50)
#@click.option("-a", "--adjectives", default = 20)
#@click.option("--conjugations", default = 8)
#@click.option("--declensions", default = 8)
def main():
    global phonemes
    phonemes = toml.load("./phonemes/latin.toml")

    nouns: List[str] = [ ]
    articles: List[str] = [ ]
    verbs: List[str] = [ ]
    adjectives: List[str] = [ ]

    print("Generating nouns...")
    for _ in range(200):
        nouns.append(generate_word(2, 3))

    print("Generating articles...")
    for _ in range(5):
        articles.append(generate_word(1, 1))

    print("Generating verbs...")
    for _ in range(150):
        verbs.append(generate_word(2, 3))

    print("Generating adjectives...")
    for _ in range(50):
        adjectives.append(generate_word(2, 3))

    language = {
        "words": {
            "articles": articles,
            "nouns": nouns,
            "verbs": verbs,
            "adjectives": adjectives,
        },
        "misc": {
            "declensions": phonemes["misc"]["declensions"],
            "conjugations": phonemes["misc"]["conjugations"],
        }
    }

    with open("./languages/pseudolatin.toml", "w") as file:
        toml.dump(language, file)

def generate_word(min_syllables = 1, max_syllables = 3):
    word = ""
    must_start_with_consonant = False
    for _ in range(random.randint(min_syllables, max_syllables)):
        syllable, must_start_with_consonant = generate_syllable(
            must_start_with_consonant)
        word += syllable
    return word


def generate_syllable(must_start_with_consonant = False):
    """
    Generates a syllable

    :param must_start_with_consonant: set this to True if the previous
    consonant was a vowel
    """
    global phonemes

    # a syllable must have at most 2 consonant phonemes and 1 vowel phoneme
    syllable = ""
    number_of_phonemes = random.choice([ 1, 1, 2, 2, 2, 3 ])

    current_phoneme_type = "consonants"

    if must_start_with_consonant:
        current_phoneme_type = "consonants"
        if number_of_phonemes == 1:
            number_of_phonemes = 2
    elif number_of_phonemes == 1:
        current_phoneme_type = "vowels"
    else:
        current_phoneme_type = random.choice([ "consonants", "vowels" ])

    for i in range(number_of_phonemes):
        possible_phonemes: List[str] = phonemes["any"][current_phoneme_type].copy()
        
        if i == 0:
            possible_phonemes.extend(phonemes["start"][current_phoneme_type])
        elif i == number_of_phonemes - 1:
            possible_phonemes.extend(phonemes["end"][current_phoneme_type])
            for excluded_phoneme in phonemes["end"]["exclude"]:
                #possible_phonemes = filter(lambda x: x != excluded_phoneme, possible_phonemes)
                possible_phonemes = [
                        x for x in possible_phonemes if x != excluded_phoneme
                ]

        #possible_phonemes: List[str] = possible_phoneme_lists[1]
        if current_phoneme_type == "consonants":
            current_phoneme_type = "vowels"
        else:
            current_phoneme_type = "consonants"

        phoneme = random.choice(possible_phonemes)
        syllable += phoneme
    return syllable, current_phoneme_type == "consonants"

if __name__ == "__main__":
    main()
