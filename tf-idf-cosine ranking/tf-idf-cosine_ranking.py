"""
Importing necessary libraries:
    - re for regular expressions
    - sys for system-specific parameters and functions
    - math for mathematical functions
    - collections for data structures like defaultdict
"""

import re
import sys
import math
from collections import defaultdict

"""
Class InvertedIndex: represents an inverted index data structure
    - documents: list of documents to build the index from
"""

class InvertedIndex:
    def __init__(self, documents):
        # Initialize the InvertedIndex object
        self.num_documents = len(documents)  # number of documents
        self.tokenized_documents = [self._preprocess(doc) for doc in documents]  # tokenize each document
        self.inverted_index = defaultdict(list)  # inverted index
        self.tf = defaultdict(lambda: defaultdict(int))  # term frequency (document -> term -> count)
        self.df = defaultdict(int)  # document frequency (term -> count)
        self.tfidf = defaultdict(lambda: defaultdict(float))  # TF-IDF (document -> term -> score)
        self._build_index()  # build the index
        self._tf_df()  # compute term frequencies and document frequencies
        self._compute_tfidf()  # compute TF-IDF scores

    """
    Preprocess a document by splitting it into individual tokens
    """
    def _preprocess(self, text):
        return re.split('[^a-zA-z]', text.lower())

    """
    Build the inverted index
    """
    def _build_index(self):
        for doc_id, tokens in enumerate(self.tokenized_documents):
            for token in set(tokens):
                self.inverted_index[token].append(doc_id)

    """
    Compute term frequencies and document frequencies
    """
    def _tf_df(self):
        for doc_id, tokens in enumerate(self.tokenized_documents):
            token_counts = defaultdict(int)
            for token in tokens:
                token_counts[token] += 1
            for token, count in token_counts.items():
                self.tf[doc_id][token] = count
                self.df[token] += 1

    """
    Compute TF-IDF scores
    """
    def _compute_tfidf(self):
        for doc_id, terms in self.tf.items():
            for term, count in terms.items():
                self.tfidf[doc_id][term] = (count / len(self.tokenized_documents[doc_id])) * math.log(
                    self.num_documents / (self.df[term]))

    """
    Compute the dot product of two vectors
    """
    def _dot_product(self, vec1, vec2):
        return sum(vec1[term] * vec2.get(term, 0.0) for term in vec1)

    """
    Compute the magnitude of a vector
    """
    def _magnitude(self, vec):
        return math.sqrt(sum(val ** 2 for val in vec.values()))

    """
    Compute the cosine similarity between two vectors
    """
    def _cosine_similarity(self, vec1, vec2):
        return self._dot_product(vec1, vec2) / (self._magnitude(vec1) * self._magnitude(vec2))

    """
    Search for documents matching a query
    """
    def search(self, query):
        # Preprocess the query
        query_tokens = self._preprocess(query)
        query_tf = defaultdict(int)
        for token in query_tokens:
            query_tf[token] += 1
        query_tfidf = {
            term: (count / len(query_tokens)) * math.log(self.num_documents / (self.df.get(term, self.num_documents)))
            for term, count in query_tf.items()}

        # Compute similarities between the query and each document
        similarities = {}
        for doc_id in range(self.num_documents):
            similarities[doc_id] = self._cosine_similarity(query_tfidf, self.tfidf[doc_id])

        # Return the top 10 documents with highest similarity scores
        return sorted(similarities.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python BM25_ranking.py [file_name]")
        sys.exit(1)

    # Read documents from file
    filename = sys.argv[1]
    documents = []
    with open(filename, encoding="utf8") as file:
        for line in file:
            documents.append(line.strip())

    # Create an InvertedIndex object
    ii = InvertedIndex(documents)

    # Get query from user
    query = input('Search: ')

    # Search for documents matching the query
    results = ii.search(query)
    print("Results for query '%s':" % query)
    for doc_id, score in results[0: 11]:
        print("Doc %d: score: %.5f" % (doc_id, score))