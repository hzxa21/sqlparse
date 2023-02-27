#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

from sqlparse import tokens as T


class _CaseFilter:
    ttype = None

    def __init__(self, case=None):
        case = case or 'upper'
        self.convert = getattr(str, case)

    def process(self, stream):
        for ttype, value in stream:
            if ttype in self.ttype:
                value = self.convert(value)
            yield ttype, value


class KeywordCaseFilter(_CaseFilter):
    ttype = T.Keyword


d = ['varying', 'numeric', 'character', 'default', 'null',
     'jsonb', 'timestamp', 'without', 'zone', 'charater', 
     'replica', 'integer', 'generate_series', 'varchar', 
     'random', 'text', 'md5', 'interval', 'sum', 'min', 
     'replace', 'string_agg', 'row_number', 'coalesce', 
     'date_part', 'cast', 'concat', 'max', 'trim', 'count']
first_ordinal = 97
last_ordinal = 122
alphabet_size = 26
s = set(d)


def shift_word(word: str, spaces: int) -> str:
    if word.lower() in d:
        return word
    res = ''
    for letter in word:
        if letter != '_':
            letter = chr((ord(letter) - last_ordinal - spaces - 1) %
                         alphabet_size + first_ordinal)
        res += letter
    return res


class IdentifierCaseFilter(_CaseFilter):
    ttype = T.Name, T.String.Symbol

    def process(self, stream):
        for ttype, value in stream:
            if ttype in self.ttype and value.strip()[0] != '"':
                value = shift_word(value, 5)
            yield ttype, value


class TruncateStringFilter:
    def __init__(self, width, char):
        self.width = width
        self.char = char

    def process(self, stream):
        for ttype, value in stream:
            if ttype != T.Literal.String.Single:
                yield ttype, value
                continue

            if value[:2] == "''":
                inner = value[2:-2]
                quote = "''"
            else:
                inner = value[1:-1]
                quote = "'"

            if len(inner) > self.width:
                value = ''.join((quote, inner[:self.width], self.char, quote))
            yield ttype, value
