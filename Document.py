import math
from functools import cached_property

import pymorphy2


class Document:
    def __init__(self, path: str) -> None:
        self._path = path
        self.text = self.filter(self.get_text(path))
        self._term_count = 0
        self.dict_term_count = self.create_dictionary()
        self.term_weight_dictionary = dict()
        self.vector = list()

    def create_dictionary(self):
        dict_term_count = dict()
        for term in self.text.split():
            self._term_count += 1
            if term in dict_term_count:
                dict_term_count[term] += 1
            else:
                dict_term_count[term] = 1

        return dict_term_count

    @cached_property
    def term_count(self) -> int:
        return self._term_count

    def has_term(self, term: str) -> bool:
        return term in self.dict_term_count

    def create_term_weight_dictionary(self, dict_term_inverse_frequency: dict) -> None:
        for term in self.dict_term_count:
            self.term_weight_dictionary[term] = self.calculate_term_weight(term, dict_term_inverse_frequency[term])

    def calculate_term_weight(self, term: str, inverse_frequency: float) -> float:
        return self.dict_term_count[term] * inverse_frequency

    @staticmethod
    def get_text(document_path: str) -> str:
        text = ""
        with open(document_path, "r", encoding='UTF-8') as document:
            for line in document:
                for term in line.lower().split():
                    for symbol in term:
                        if symbol.isalpha():
                            text += symbol

                    if text[-1] != ' ':
                        text += " "

        return text.strip()

    @staticmethod
    def filter(text: str) -> str:
        filter_list = list()
        with open("stop_words.txt", "r", encoding='UTF-8') as document:
            for term in document:
                filter_list.append(term.strip())

        words = list(text.split())

        morph = pymorphy2.MorphAnalyzer(lang='ru')

        new_text = ''
        for word in words:
            if morph.normal_forms(word)[0] not in filter_list:
                new_text += morph.normal_forms(word)[0] + ' '

        return new_text.strip()

    def calculate_vector(self, dictionary: dict, document_count: int) -> tuple:
        vector = list()
        for key in dictionary:
            weight = float()
            for term in self.dict_term_count:
                weight += (self.dict_term_count[term] * math.log(document_count / dictionary[term])) ** 2
            weight **= 0.5

            if key in self.dict_term_count:
                vector.append(self.dict_term_count[key] * math.log(document_count / dictionary[key]))
            else:
                vector.append(0)

        return tuple(vector)

    @cached_property
    def path(self) -> str:
        return self._path

    def get_info_about_word_in_the_document(self, word):
        count = 0
        if does_contains := self.contains_word(word):
            count = self.get_count_of_word(word)
        return {'document': self.path, 'contains': does_contains, 'count': count}

    def contains_word(self, word: str) -> bool:
        return word in self.dict_term_count.keys()

    def get_count_of_word(self, word: str) -> int:
        return self.dict_term_count.get(word)
