import re
import sys


class InvertedIndex:
    """ A very simple inverted index. """

    def __init__(self):
        """ Create an empty inverted index. """

        self.postings = None  # used for compressed mode
        self.indexes = None  # used for compressed mode

        self.invertedIndex = {}
        self.compressStatus = False
        self.matchCount = 1

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

    def _compress(self):
        self.indexes = ''
        current = ''  # current input to check to other
        index = 0
        setCurrent = True
        matchHistory = False
        words = list(self.invertedIndex.keys())
        while index < len(words):
            if words[index] == '':  # chck for null
                index += 1
                continue
            if setCurrent:  # set input for match to other
                current = words[index]
                self.indexes += ',' + str(len(words[index])) + words[index]
                index += 1
                setCurrent = False
                continue
            ind = -1  # match characters
            for i in range(min(len(words[index]), len(current))):
                if current[i] == words[index][i]:
                    ind = i
            if ind < self.matchCount:  # does not match
                setCurrent = True
                matchHistory = False
            else:  # match
                if matchHistory:  # first match
                    self.indexes += '@'
                else:  # other match
                    self.indexes += '*'
                    matchHistory = True
                self.indexes += str(len(words[index])) + words[index][ind + 1:]
                index += 1
        self.indexes = words[1:]
        self.compressStatus = True

    def extract_d_w(self, string):
        d = ''
        w = ''
        for i in string:
            if i.isdigit():
                d += i
            else:
                w += i
        return d, w

    def get_compress_index(self):
        return self.indexes.replace(',', '')

    def _decompress(self):
        inp = self.indexes.split(',')
        output = []
        for words in inp:
            if words == "":
                continue
            data = words.split('*')
            if len(data) == 1:
                output.append(self.extract_d_w(data[0])[1])
                continue
            count, current = self.extract_d_w(data[0])
            output.append(current)
            for string in data[1].split('@'):
                d, w = self.extract_d_w(string)
                output.append(current[: (int(d) - len(w))] + w)
        return output

    def get_decompress_index(self):
        return self._decompress()

    def compress(self):
        if self.compressStatus:
            return
        self.postings = list(self.invertedIndex.values())
        self._compress()

    def search(self, search):
        """ Search with inverted indexes

        >>> ii = InvertedIndex()
        >>> ii.read_from_txt('Datasets/example.txt')
        >>> ii.search('first')
        {1}
        """
        search = map(lambda x: x.lower(), re.split('[^a-zA-z]', search))

        results = set()

        if self.compressStatus:
            for key in search:
                index = self.indexes.index(key)
                if index > -1:
                    if len(results) == 0:
                        results = set(x for x in self.postings[index])
                    else:
                        results.intersection_update(self.postings[index])
        else:
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

    print('Search [0]')
    print('See inverted index [1]')
    print('compress indexes [2]')
    print('See compressed indexes [3]')
    print('See uncompressed indexes [4]')
    status = input('Choose action or any key to exit: ')
    while status.isdigit() and 0 <= int(status) <= 4:
        if status == '0':
            for doc in ii.search(input('search: ')):
                print(doc)
        elif status == '1':
            print('inverted index')
            print('input'.ljust(30), 'repeats'.ljust(10), 'documents')
            for word, indexes in ii.invertedIndex.items():
                print(word.ljust(30), str(len(indexes)).ljust(10), indexes)
        elif status == '2':
            ii.compress()
            print('Successfully compressed')
        elif status == '3':
            print(ii.get_compress_index())
        else:
            print(ii.get_decompress_index())

        status = input('Choose action or any key to exit: ')
    print('Bye')
