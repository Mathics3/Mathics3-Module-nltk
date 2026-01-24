# -*- coding: utf-8 -*-
"""
Language Translation

"""

# This is under Text Normalization in WR. But also in Natural Language Processing,
# and Linguistic Data. I put here because is the only module that uses langid and pycountry
# modules.
#
# TODO: WordTranslation, TextTranslation

from typing import Union

import langid  # see https://github.com/saffsd/langid.py
import pycountry
from mathics.core.atoms import String
from mathics.core.builtin import Builtin
from mathics.core.evaluation import Evaluation
from mathics.core.list import ListExpression
from mathics.core.symbols import Symbol
from mathics.core.systemsymbols import SymbolFailed
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError

sort_order = "Language Translation"


class LanguageIdentify(Builtin):
    """
    <url>:WMA link:
    https://reference.wolfram.com/language/ref/LanguageIdentify.html</url>

    <dl>
      <dt>'LanguageIdentify'[$text$]
      <dd>returns the name of the language used in $text$.
    </dl>

    >> LanguageIdentify["eins zwei drei"]
     = German
    """

    summary_text = "determine the predominant human language in a string"

    def eval(self, text: String, evaluation: Evaluation) -> Union[Symbol, String]:
        "LanguageIdentify[text_String]"

        # an alternative: https://github.com/Mimino666/langdetect

        code, _ = langid.classify(text.value)
        language = pycountry.languages.get(alpha_2=code)
        if language is None:
            return SymbolFailed
        return String(language.name)


# FIXME generalize
class WordTranslation(Builtin):
    """
    <url>:WMA link:
    https://reference.wolfram.com/language/ref/WordTranslation.html</url>

    <dl>
      <dt>'WordTranslation'[word, $lang$]
      <dd>returns a list of translation for $word$ into $lang$.
    </dl>

    >> WordTranslation["dog", "French"]
     = ...
    """

    requires = ("lgn",)

    # Set checking that the number of arguments required to exactly two.
    eval_error = Builtin.generic_argument_error
    expected_args = 2

    summary_text = "give word translations"

    def eval(
        self, word: String, lang: String, evaluation: Evaluation
    ) -> ListExpression:
        "WordTranslation[word_String, lang_String]"
        return eval_WordTranslation(word.value, lang.value)


def eval_WordTranslation(word: str, language_name: str):
    """
    Return a list of translations of `word` in English to `language_name`.
    """

    # Convert "language_name" using NLTK's langnames utility
    # to its 3-letter ISO 639-3 code.
    iso_code = lgn.langcode(language_name, typ=3)

    if iso_code is None:
        return SymbolFailed

    synsets = wn.synsets(word)
    translations = set()

    for ss in synsets:
        # Pass the converted code to WordNet
        try:
            for lemma in ss.lemmas(lang=iso_code):
                translations.add(lemma.name())
        except WordNetError:
            return SymbolFailed

    return ListExpression(*[String(word) for word in translations])
