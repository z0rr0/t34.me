#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import settings

# t34dict = settings.ALPHABET
t34dict = settings.SIMPLE_ALPHABET
basLen = len(t34dict)

# This file contains base methods
def t34_decode(x, basis=basLen):
    """Convert any number basis-based to decimal, result - decimal number"""
    global t34dict
    i, result = 0, 0
    syms = str(x)
    while syms:
        result += t34dict.index(syms[-1]) * (basis**i)
        syms = syms[:-1]
        i += 1
    return result

def t34_encode(x, basis=basLen):
    """Convert any number from decimal to basis-based, result - str"""
    global t34dict
    result = ""
    while x > 0:
        i = x % basis
        result = t34dict[i] + result
        x = x // basis
    return result

def std_decode(x, basis):
    """starndart python converter any number basis-based to decimal"""
    if basis <= 36:
        result = int(str(x), basis)
        return result
    return None