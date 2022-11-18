import math

import pymorphy2

from Document import Document


class Analyzer:
    def __init__(self, documents_path: list):
        self.documents = list()
        for document_path in documents_path:
            self.documents.append(Document(document_path))
        self.cosines = list()
        self.dictionary = self.create_dictionary()
        self.dict_term_inverse_frequency = self.create_term_inverse_frequency_dictionary()
        self.create_term_weight_dictionaries()

    def analyze(self, query: str) -> None:
        query_vector = self.calculate_query_vector(query)

        for document in self.documents:
            self.cosines.append(
                (document.path, document.term_count,
                 self.calculate_cosines(document.calculate_vector(self.dictionary, len(self.documents)), query_vector)))

        self.cosines = sorted(self.cosines, key=lambda x: -x[2])

    def create_dictionary(self):
        dictionary = dict()

        for term in self.get_unique_terms():
            amount_documents_with_term = 0
            for document in self.documents:
                if document.has_term(term):
                    amount_documents_with_term += 1

            dictionary[term] = amount_documents_with_term

        return dictionary

    def get_unique_terms(self) -> set:
        terms = set()
        for document in self.documents:
            for term in document.dict_term_count.keys():
                terms.add(term)

        return terms

    # Calculating B
    def create_term_inverse_frequency_dictionary(self):
        term_inverse_frequency_dictionary = dict()

        for term in self.get_unique_terms():
            term_inverse_frequency_dictionary[term] = math.log(len(self.documents) / self.dictionary[term])

        return term_inverse_frequency_dictionary

    def create_term_weight_dictionaries(self) -> None:
        for document in self.documents:
            document.create_term_weight_dictionary(self.dict_term_inverse_frequency)

    def calculate_query_vector(self, query: str) -> tuple:
        query = self.filter(self.clean_text(query))
        print(query)

        query_vector = list()

        for term in self.dictionary:
            if term in query:
                query_vector.append(1)
            else:
                query_vector.append(0)

        return tuple(query_vector)

    @staticmethod
    def calculate_cosines(a: tuple, b: tuple) -> float:
        mod_a = float()
        mod_b = float()
        cosines = float()
        for i in range(len(a)):
            mod_a += a[i] ** 2
            mod_b += b[i] ** 2
            cosines += a[i] * b[i]

        if (mod_a ** 0.5) * (mod_b ** 0.5) == 0:
            return 1
        else:
            return float(cosines / ((mod_a ** 0.5) * (mod_b ** 0.5)))

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned_text = ''
        for term in text.lower().split():
            for symbol in term:
                if symbol.isalpha():
                    cleaned_text += symbol

            if cleaned_text[-1] != ' ':
                cleaned_text += " "

        return cleaned_text.strip()

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

    def get_documents_as_str(self):
        res = ''
        for doc in self.documents:
            res += doc.text + "\n*****************************************************\n"
        return res
