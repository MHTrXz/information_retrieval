import re
import sys


class InvertedIndex:
    """ A very simple inverted index. """

    def __init__(self):
        """ Create an empty inverted index. """

        self.invertedIndex = {}

    def read_from_txt(self, file_name):
        """ Construct index from given file

        >>> ii = InvertedIndex()
        >>> ii.read_from_txt('Datasets/example.txt')
        >>> ii.invertedIndex
        {'first': {1}, 'document': {1, 2, 3}, 'second': {2}, 'third': {3}}
        """
        with open(file_name, encoding="utf8") as file:
            record_id = 0
            for line in file:
                record_id += 1
                for word in re.split('[^a-zA-z]', line):
                    if len(word) > 0:
                        word = word.lower()
                        if word not in self.invertedIndex:
                            self.invertedIndex[word] = set()
                        self.invertedIndex[word].add(record_id)

    def search(self, search):
        """ Search with inverted indexes

        >>> ii = InvertedIndex()
        >>> ii.read_from_txt('Datasets/example.txt')
        >>> ii.search('first')
        {1}
        """
        search = map(lambda x: x.lower(), re.split('[^a-zA-z]', search))

        results = set()
        available_keys = self.invertedIndex.keys()
        for key in search:
            if key in available_keys:
                if len(results) == 0:
                    results = set(x for x in self.invertedIndex[key])
                else:
                    results.intersection_update(self.invertedIndex[key])
        return results


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python BM25_ranking.py [file_name]")
        sys.exit(1)

    filename = sys.argv[1]

    ii = InvertedIndex()
    ii.read_from_txt(filename)

    status = input('See inverted index [0] or search [1]: ')
    while status.isdigit() and (int(status) == 0 or int(status) == 1):
        if status == '0':
            print('inverted index')
            print('input'.ljust(30), 'repeats'.ljust(10), 'documents')
            for word, indexes in ii.invertedIndex.items():
                print(word.ljust(30), str(len(indexes)).ljust(10), indexes)
        else:
            for doc in ii.search(input('search: ')):
                print(doc)

        status = input('See inverted index [0] or search [1] or any key to exit: ')
    print('Bye')