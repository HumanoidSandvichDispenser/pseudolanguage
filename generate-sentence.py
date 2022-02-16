#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 sandvich <sandvich@manjaro>
#
# Distributed under terms of the GPLv3 license.

import random
import click
from dotmap import DotMap
import toml


language = DotMap()

@click.command()
def main():
    global language
    language = DotMap(toml.load("./languages/pseudolatin.toml"))
    parts = [ ]
    for _ in range(random.randint(1, 3)):
        parts.append(subject())
        parts.append(predicate())
    print(" ".join(parts) + ".")

def subject():
    global language
    words = [ ]
    include_adjective = random.choice([ True, False, False ])
    declension = random.choice(language.misc.declensions)

    article = random.choice(language.words.articles)
    words.append(article + declension)

    if include_adjective:
        adjective = random.choice(language.words.adjectives)
        words.append(adjective + declension)

    noun = random.choice(language.words.nouns)
    words.append(noun + declension)

    return " ".join(words)

def predicate():
    global language
    conjugation = random.choice(language.misc.conjugations)
    return random.choice(language.words.verbs) + conjugation

if __name__ == "__main__":
    main()
