import os
import threading
import subprocess

# This is the function used in the thread. It counts the number of words in a partition array.

def countWordsInPartition(words):

	# Declare an empty dictionary that does not have any keys. In this dictionary, we have key-value pairs where the key is the word in the
	# text file and the value is the number of occurences of the word.
	dct = {}
	
	# Parse through the partition list and count the occurences of each word, remove the punctuation marks from the words.
	for word in words:
		editedWord = ''
		if word[-1] == '.' or word[-1] == ',' or word[-1] == '!' or word[-1] == '?':
			editedWord = word[0:-1]
		else:
			editedWord = word
		
		# If the word is not in the dictionary keys, then initialize the value of the key to 1.
		if editedWord not in dct.keys():
			dct[editedWord] = 1
		
		# Otherwise we increment the value of the key by 1.
		else:
			dct[editedWord] += 1
	
	# Return the dictionary that keeps track of the number of occurences of each word.
	return dct

# This functions accepts the dictionaries that are generated by each thread and computes the final dictionary that counts the total occurences of all the 
# words in all the threads.

def computeFinalWordCountDictionary(wordCountDictionaries):
	finalDictionary = {}
	for dictionary in wordCountDictionaries:
		for key in dictionary.keys():
			if key not in finalDictionary:
				finalDictionary[key] = dictionary[key]
			else:
				finalDictionary[key] += dictionary[key]	
	return finalDictionary

# This algorithm accepts the number of words in the file and number of threads that are to be read. Based on the values, the thread decided the number of words that are
# to be read by each segment.

def computeWordsPerSegment(numWords, n):
	wordsPerSegment = int()
	
	# If the number of words is divisible by the number of threads, then each thread is supposed to read equal number of words.
	if numWords % n == 0:
		wordsPerSegment = numWords // n
	
	# If the number of words is not divisible by the number of threads, then the last thread reads greater number of words.
	else:
		offset = numWords - (numWords % n)
		wordsPerSegment = offset // (n - 1)
	return wordsPerSegment
	
# The output is redirected to a file called output.txt which stores the occurence of each word in the input text file.

def writeToOutput(finalDictionary):
	fd = os.open('output.txt', os.O_CREAT | os.O_WRONLY)
	os.dup2(fd, 1)
	for key in finalDictionary.keys():
		print(key + ', ' + str(finalDictionary[key]))
	os.close(fd)

# This command gets input lines from the user, separated them on the occurence of the whitespace character, and separates the words to store the words in an array.

def getWordsFromParagraph(fd):
	paragraph = fd.readlines()
	words = []
	for line in paragraph:
		words += line.split()
	return words
