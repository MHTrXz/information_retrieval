# Import necessary modules
import re
import sys
import math
from collections import defaultdict


# Define a class to represent an inverted index
class InvertedIndex:
    def __init__(self, documents):
        # Initialize the inverted index with the given documents
        self.documents = documents
        # Create an empty index to store the token-to-document mapping
        self.index = defaultdict(list)
        # Create an empty dictionary to store the term frequencies
        self.term_freq = defaultdict(lambda: defaultdict(int))
        # Create an empty dictionary to store the document lengths
        self.doc_len = {}
        # Initialize the average document length to 0
        self.avg_dl = 0
        # Build the inverted index
        self.build_index()

    def build_index(self):
        # Iterate over the documents and tokenize them
        for doc_id, document in enumerate(self.documents):
            # Tokenize the document
            tokens = self.tokenize(document)
            # Store the length of the document
            self.doc_len[doc_id] = len(tokens)
            # Add to the total document length
            self.avg_dl += len(tokens)
            # Iterate over the tokens and update the index and term frequencies
            for token in tokens:
                # Add the document ID to the token's posting list
                self.index[token].append(doc_id)
                # Increment the term frequency for the token in the document
                self.term_freq[token][doc_id] += 1
        # Calculate the average document length
        self.avg_dl /= len(self.documents)

    def tokenize(self, text):
        # Tokenize the text by splitting on whitespace and converting to lowercase
        return re.split('[^a-zA-z]', text.lower())

    def bm25_score(self, query, doc_id):
        # Calculate the BM25 score for the query and document
        score = 0
        for token in self.tokenize(query):
            # Check if the token is in the index
            if token not in self.index:
                continue
            # Calculate the document frequency (df) of the token
            df = len(self.index[token])
            # Calculate the inverse document frequency (idf) of the token
            idf = math.log((len(self.documents) - df + 0.5) / (df + 0.5))
            # Calculate the term frequency (tf) of the token in the document
            tf = self.term_freq[token][doc_id]
            # Calculate the document length (dl) of the document
            dl = self.doc_len[doc_id]
            # Calculate the BM25 score for the token
            k1 = 1.2
            b = 0.75
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * dl / self.avg_dl)
            score += idf * (numerator / denominator)
        return score

    def search(self, query):
        # Calculate the BM25 score for the query and each document
        scores = {}
        for doc_id in range(len(self.documents)):
            scores[doc_id] = self.bm25_score(query, doc_id)
        # Return the sorted scores in descending order
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# Usage
if __name__ == '__main__':
    # Check if the script is being run from the command line
    if len(sys.argv) != 2:
        print("Usage: python BM25_ranking.py [file_name]")
        sys.exit(1)

    # Get the filename from the command-line argument
    filename = sys.argv[1]

    # Read the documents from the file
    documents = []

    with open(filename, encoding="utf8") as file:
        for line in file:
            documents.append(line.strip())

    # Create an instance of the InvertedIndex class
    ii = InvertedIndex(documents)

    # Prompt the user to enter a query
    query = input('Search: ')

    # Search for the query and get the top 10 results
    results = ii.search(query)
    print("Results for query '%s':" % query)
    for doc_id, score in results[0: 11]:
        print("Doc %d: score: %.5f" % (doc_id, score))
