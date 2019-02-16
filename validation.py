import random
import collections
import string
import os
import time

DIFFICULTY = 14

with open('Words5.txt', 'r') as words:
    wordSet = set(words.readline().split(","))

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

def isConnected(word):
    for index, letter in enumerate(word):
        for sub in string.ascii_lowercase:
            if sub != letter:
                possible = word[:index] + sub + word[index+1:]
                if possible in wordSet:
                    return True

def getConnectedWords(word):
    result = []
    for index, letter in enumerate(word):
        for sub in string.ascii_lowercase:
            if sub != letter:
                possible = word[:index] + sub + word[index+1:]
                if possible in wordSet:
                    result.append(possible)
    return result

avg_time = 0
avg_initial_memory = 0
avg_memory = 0
avg_persisitent_memory = 0
iterations = 50

for i in range(iterations):

	start_time = time.time()
	start = get_first(random.sample(wordSet, 1))
	# print(start)
	traversed = set()

	waveFront = set([start])
	for distance in range(1, DIFFICULTY + 1):
		traversed.update(waveFront)
		waveFront = set.union(*[set(getConnectedWords(word)).difference(traversed) for count, word in enumerate(waveFront)])
	avg_initial_memory += len(traversed) + len(waveFront)
	# print(len(traversed), len(waveFront))

	end = get_first(random.sample(waveFront, 1))
	traversed = set()
	distance_to_end = {}
	distance_to_end[end] = 0

	waveFront = set([end])
	for distance in range(1, DIFFICULTY + 1):
		traversed.update(waveFront)
		waveFront = set.union(*[set(getConnectedWords(word)).difference(traversed) for count, word in enumerate(waveFront)])
		distance_to_end.update({(word, distance) for count, word in enumerate(waveFront)})
	avg_memory += len(traversed) + len(waveFront)
	avg_persisitent_memory += len(distance_to_end)
	# print(len(traversed), len(waveFront), len(distance_to_end))

	avg_time += time.time() - start_time
	# print(start + " -> " + end + ": " + str(DIFFICULTY))
	# print(time.time() - start_time)
	# print(distance_to_end)

print("time: " + str(avg_time / iterations))
print("initial mem: " + str(avg_initial_memory / iterations))
print("mem: " + str(avg_memory / iterations))
print("persistent mem: " + str(avg_persisitent_memory / iterations))