import re
from typing import List
from rapidfuzz import fuzz, process


class Autocorrect:
    def __init__(self, data: List[str]):
        self.data = data

    def correct_word(self, word: str = None, match_score: float = 85.0) -> str:
        """
        args
        word(str) : word to be corrected
        match_score(float): Score to correct the word, considering the matching score

        Returns:
        corrected word
        """
        word = word.lower()
        suggestions = process.extract(word, self.data, limit=1, scorer=fuzz.token_set_ratio)
        actual_match_score = suggestions[0][1]
        correct_word = suggestions[0][0]

        if actual_match_score > match_score:
            return correct_word

        return word

    def correct_sentence(self, sentence: str, match_score: float = 85.0) -> str:
        """
        args
        sentence(str) : sentence from which words to be corrected
        match_score(float): Score to correct the word, considering the matching score

        Returns:
        corrected sentence
        """
        sentence_ = sentence.lower().strip()
        sentence_ = re.sub("[\W\d_]+", " ", sentence_)
        tokens = sentence_.split(" ")

        for word in tokens:
            suggestions = process.extract(word, self.data, limit=1, scorer=fuzz.token_set_ratio)
            actual_match_score = suggestions[0][1]
            correct_word = suggestions[0][0]

            if actual_match_score > match_score:
                sentence = sentence.replace(word, correct_word)

        return sentence
