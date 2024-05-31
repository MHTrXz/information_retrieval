# Import necessary modules
import re
import sys
import math
from collections import defaultdict


# Define a class for the Inverted Index
class InvertedIndex:
    def __init__(self):
        # Initialize an empty inverted index (a dictionary where each key is a term and the value is a list of
        # document IDs)
        self.index = defaultdict(list)
        # Initialize an empty dictionary to store the IDF (Inverse Document Frequency) values for each term
        self.idf = {}

    # Method to add a document to the index
    def add_document(self, doc_id, terms):
        # Iterate over the unique terms in the document
        for term in set(terms):
            # Add the document ID to the list of document IDs for the term
            self.index[term].append(doc_id)

    # Method to calculate the IDF values for each term
    def calculate_idf(self):
        # Get the total number of documents (i.e., the number of unique terms)
        N = len(self.index)
        # Iterate over each term in the index
        for term, doc_ids in self.index.items():
            # Calculate the document frequency (DF) for the term
            df = len(doc_ids)
            # Calculate the IDF value using the formula: IDF = log(N / DF)
            idf = math.log(N / df)
            # Store the IDF value in the idf dictionary
            self.idf[term] = idf

    # Method to rank documents based on a query
    def rank_documents(self, query_terms):
        # Initialize a dictionary to store the scores for each document
        scores = defaultdict(float)
        # Iterate over each term in the query
        for term in query_terms:
            # Check if the term is in the index (i.e., if it's a valid term)
            if term in self.idf:
                # Iterate over each document ID that contains the term
                for doc_id in self.index[term]:
                    # Add the IDF value of the term to the score of the document
                    scores[doc_id] += self.idf[term]
        # Return a sorted list of documents by their scores in descending order
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# Usage
if __name__ == '__main__':
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python tf-idf-cosine_ranking.py [file_name]")
        sys.exit(1)

    # Get the filename from the command-line argument
    filename = sys.argv[1]

    # Create an instance of the InvertedIndex class
    index = InvertedIndex()

    # Add documents from the file to the index
    with open(filename, encoding="utf8") as file:
        record_id = 0
        for line in file:
            record_id += 1
            # Split the line into terms using a regular expression and convert to lowercase
            terms = re.split('[^a-zA-z]', line.lower())
            # Add the document to the index
            index.add_document(record_id, terms)

    # Calculate the IDF values for each term
    index.calculate_idf()

    # Prompt the user to enter a query
    query = re.split('[^a-zA-z]', input('Search: ').lower())

    # Rank documents for the query
    ranked_docs = index.rank_documents(query)

    # Print the search results
    print(f"Search results for query '{' '.join(query)}':")
    for doc_id, score in ranked_docs[0: 11]:
        print(f"Document {doc_id}: TF-IDF score = {score:.4f}")
