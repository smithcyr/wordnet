import collections
import string
import os
import operator

for wordLen in range(4, 9):
    with open('wordsEn.txt', 'r') as words:
        wordSet = set([word.strip() for word in words if len(word.strip()) == wordLen])

        def isConnected(w):
            for index, letter in enumerate(w):
                for sub in string.ascii_lowercase:
                    if sub != letter:
                        possible = w[:index] + sub + w[index+1:]
                        if possible in wordSet:
                            return True

        connectedWords = set([word for count, word in enumerate(wordSet) if isConnected(word)])

        # print("# " + str(wordLen) + " letter words: " + str(len(connectedWords)))

        def get_first(iterable, default=None):
            if iterable:
                for item in iterable:
                    return item
            return default

        def getConnectedWords(w):
            result = []
            for index, letter in enumerate(w):
                for sub in string.ascii_lowercase:
                    if sub != letter:
                        possible = w[:index] + sub + w[index+1:]
                        if possible in wordSet:
                            result.append(possible)
            return result

        wordGroups = []
        totalTraversed = set()
        while len(totalTraversed) < len(connectedWords):
            startingWords = connectedWords.difference(totalTraversed)
            start = get_first(startingWords)
            traversed = set()

            waveFront = set([start])
            while waveFront:
                traversed.update(waveFront)
                waveFront = set.union(*[set(getConnectedWords(word)).difference(traversed) for count, word in enumerate(waveFront)])

            totalTraversed.update(traversed)
            if len(traversed) > 50:
                wordGroups.append(traversed)
        
        print(str(wordLen) + ": " + ",".join([str(len(group)) for group in wordGroups]))
        # print(str(wordLen) + ": " + str(len(traversed)))

        print("writing to file")
        with open("Words" + str(wordLen) + ".txt", "w") as wordsList:
            for group in wordGroups:
                wordsList.write(",".join(list(group)) + "\n")