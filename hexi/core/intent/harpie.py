from nltk.tokenize import TreebankWordTokenizer
from collections import Counter, OrderedDict
import copy
import math
import json

tokeniser = TreebankWordTokenizer()


class Skill:
    def __init__(self, name, data):
        self.name = name

        self.commands = data['commands']
        self.script = data['script']

        self.tfidf_vectors = {}


class Harpie:
    def __init__(self, intent_path):
        self._skills = []
        self._all_commands = []
        self._load_intent_library(intent_path)

        self._lexicon = self._get_lexicon()

        self._zero_vector = OrderedDict((token, 0) for token in self._lexicon)

        self._compute_tfidf()

        self._command_tokens = self._get_doc_tokens()


    def get_intent(self, message):
        tokens = tokeniser.tokenize(message)
        cosines = self._rank_relevence(tokens)
        highest_cos = max(cosines)

        return cosines[highest_cos]


    def all_skill_names(self):
        return [skill.name for skill in self._skills]


    def _load_intent_library(self, intent_path):
        with open(intent_path, "r") as json_file:
            skills = json.load(json_file)

            for name, data in skills.items():
                self._skills.append(Skill(name, data))

                for command in data['commands']:
                    self._all_commands.append(command)


    def _get_lexicon(self):
        all_tokens = set()
        for command in self._all_commands:
            [all_tokens.add(token) for token in tokeniser.tokenize(command)]
        
        return sorted(list(all_tokens))


    def _get_doc_tokens(self):
        doc_tokens = []

        for doc in self._all_commands:
            doc_tokens += [sorted(tokeniser.tokenize(doc.lower()))]

        return sum(doc_tokens, [])


    def _compute_tfidf(self):

        for skill in self._skills:
            for command in skill.commands:
                tfidf_vector = copy.copy(self._zero_vector)
                tokens = tokeniser.tokenize(command.lower())
                token_counts = Counter(tokens)      # gets the doc's tokens and counts

                # for each token in the specified doc
                for token, token_occurences in token_counts.items():
                    docs_containing_token = 0

                    # finds how many docs contain a given token (key)
                    for _command in self._all_commands:
                        if token in _command.lower():
                            docs_containing_token += 1

                    # Term Frequency
                    tf = token_occurences / len(self._lexicon)

                    # Inverse Document Frequency
                    if docs_containing_token:
                        idf = len(self._all_commands) / docs_containing_token

                    tfidf_vector[token] = tf * idf

                skill.tfidf_vectors[command] = tfidf_vector
        

    def _rank_relevence(self, tokens):
        query_vec = copy.copy(self._zero_vector)

        token_counts = Counter(tokens)

        for token, token_occurence in token_counts.items():
            docs_containing_token = 0

            for _doc in self._command_tokens:
                if token in _doc:
                    docs_containing_token += 1

            if docs_containing_token == 0:
                continue        # if the token is not in the lexicon, then skip it

            tf = token_occurence / len(tokens)
            idf = len(self._all_commands) / docs_containing_token

            query_vec[token] = tf * idf

        cosines = {}
        for skill in self._skills:
            for tfidf in list(skill.tfidf_vectors.values()):
                score = self._cosine_sim(query_vec, tfidf)

                if score in cosines.keys():
                    cosines[score].append(skill)
                else:
                    cosines[score] = [skill]

        return cosines


    def _cosine_sim(self, vec1, vec2):
        # convert dicts to lists
        vec1 = [val for val in vec1.values()]
        vec2 = [val for val in vec2.values()]

        dot_prod = 0
        for i, v in enumerate(vec1):
            dot_prod += v * vec2[i]

        mag_1 = math.sqrt(sum([x**2 for x in vec1])) + 0.001
        mag_2 = math.sqrt(sum([x**2 for x in vec2])) + 0.001

        return dot_prod / (mag_1 * mag_2)

