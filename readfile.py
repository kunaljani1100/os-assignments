import os
import threading
import subprocess
import wordCountOperations as wco

# This function reads the input, creates the threads, and writes the output to the file by calling functions in the wordCountOperations module.

def readInputAndCountWords():

	# Accept the number of threads and the file path as input.
	n = int(input('Number of threads:'))
	filePath = input('File path:')
	
	# Get the count of the number of words in the file.
	wcCommandOutput = subprocess.check_output("wc -w " + filePath, shell = True).decode('utf-8').split()
	numWords = int(wcCommandOutput[0])

	# Open the file in read mode.
	fd = open(filePath, 'r')

	# Based on the word count and the number of threads, we compute the number of words in each segment.
	wordsPerSegment = wco.computeWordsPerSegment(numWords, n)

	# This part is based on making the division of work as equal as possible between all the threads. Since the total number of words is not always divisible by 
	# the total number of threads.
	wordsReadByThread = []
	wordsParsed = 0

	# Append the number of words to be read by each thread in the wordsReadBythread list.
	partitionsRead = 0
	while True:
		
		# If the partition is not the last partition, then we read the number of words to be read by each segment
		if partitionsRead != n - 1:
			wordsReadByThread.append(wordsPerSegment)
			wordsParsed += wordsPerSegment
		
		# Otherwise, we read all the remaining words.
		else:
			wordsReadByThread.append(numWords - wordsParsed)
			break
		partitionsRead += 1

	words = wco.getWordsFromParagraph(fd)
	
	# We append the word count dictionary that was computed by each partition.
	wordCountDictionaries = []
	for i in range(n):
		wordCountDictionaries.append(wco.countWordsInPartition(words[i*wordsPerSegment:i*wordsPerSegment + wordsReadByThread[i]]))
	
	# From the list of appended dictionaries, we compute the final dictionary.
	finalDictionary = wco.computeFinalWordCountDictionary(wordCountDictionaries)	
	
	fd.close()
	
	# Write the output too output.txt
	wco.writeToOutput(finalDictionary)
	
if __name__ == "__main__":
	readInputAndCountWords()
