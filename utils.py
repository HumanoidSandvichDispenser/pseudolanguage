#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 sandvich <sandvich@manjaro>
#
# Distributed under terms of the GPLv3 license.

def merge_dict(a, b):
    """
    Merges two dictionaries together

    :return: a shallow copy of the two dictionaries merged together
    """
    return { **a, **b }
