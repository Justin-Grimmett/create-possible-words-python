import time
import itertools
import os
import re

def main():
	# If True, force the inputWord to be manually typed, even if the variable below has a valid word
	useInput = False

	# What would be the input word - hardcoded for now for testing
	inputWord = "abcde"
	# inputWord = "REALIGNED"	# example 9 letter word

	# If the input letters make a real word should this be included also?
	includeSourceWord = True

	# Hardcoded minimum length word
	shortestWordLen = 4
	# Hardcoded maximum allowed word length - just to force an exception, so the below functionality will work as intended
	maxAllowedMax = 9

	# "Files" directory sub-path
	fileSubDir = "\\files\\"

	# Allow the word to be typed here manually
	pattern = r"^[A-Za-z]{{{},{}}}$".format(shortestWordLen, maxAllowedMax)	# Only allow English characters between the allowed word length range
	# Force the manual input
	if useInput:
		inputWord = ""
	# Use Regex to only allow English letters, and then keep looping until this is valid
	# Note if the input word is already valid (and useInput is False) then this would be skipped
	while re.search(pattern, inputWord) == None:
		# If the length is correct, display an error regarding invalid characters
		if len(inputWord) >= shortestWordLen and len(inputWord) <= maxAllowedMax:
			print("Invalid characters entered, please try again. Only allowed to be English letters (Eg A-Z)")
		# Manual input in the CLI for the input word
		inputWord = input("Please Type some letters (between {} and {} characters): ".format(shortestWordLen,maxAllowedMax))
		
	startTime = time.time()			# Used for printline testing

	# Just for testing
	doPrintLines = True

	# The source data to be used for reference is Lower Case - and remove all white space
	inputWord = ''.join(inputWord.lower().split())

	# The possible letters of the input word
	possibleLetters = []
	# The numeric indexes of this input word
	lettersIndexes = []

	# The main string array where all possible new words will be added
	newWords = set()
	# The actual checked words - real possible words against generated letter words
	realWordOutput = set()
	# To sort the real words by length and alphabetically
	sortedWordLengthOutput = {}

	# The final sorted output
	finalRealWordOutput = []

	# Eg how many letters there are in the word - used for many loops below
	maxPossibleIndexVal = 0	# Note the value is not important, just to set it as an Int
	# Files location path
	curDir = os.getcwd()
	filesDirectory = curDir + fileSubDir
	# Just to make sure - if the folder does exist it would cause an error, but fine if it is empty
	if not os.path.exists(filesDirectory):
		os.makedirs(filesDirectory)

	# Generate the possible letters and indexes of these from the input work
	for wordIdx in range(0,len(inputWord)):
		possibleLetters.append(inputWord[wordIdx])
		lettersIndexes.append(wordIdx+1)
	# sort these
	lettersIndexes.sort()
	possibleLetters.sort()

	# Get the highest index value from this - which would be the length of the input word
	if len(lettersIndexes) > 0:
		for idx in range(len(lettersIndexes), 0, -1):
			if maxPossibleIndexVal < idx:
				maxPossibleIndexVal = idx

	# Throw an exception as a safeguard
	if maxPossibleIndexVal > maxAllowedMax:
		s = "ERRROR : 'maxPossibleIndexVal' variable value ({}) is above the allowed 'maxAllowedMax' variable value ({}) - cannot continue with the current functionality".format(maxPossibleIndexVal, maxAllowedMax)
		raise Exception(s)
	elif maxPossibleIndexVal< shortestWordLen:
		s = "ERRROR : 'maxPossibleIndexVal' variable value ({}) is below the allowed 'shortestWordLen' variable value ({})".format(maxPossibleIndexVal,shortestWordLen)
		raise Exception(s)

	# ************************************************************************************************************
	# Make possible numbers from the word - To be then used as indexes to loop through the string word
	# Eg for a 4 letter word this would go from 12345 to 54321, without duplicate digits

	# Indexes of the Word letters as strings of the value
	allowedIndexStrVals = []
	# All possible numbers generated from the indexes of the input work, to be used to create the output string words
	allPossibleWordRangeValues = set()

	# Stringify the allowed index values
	for letterIdx in lettersIndexes:
		allowedIndexStrVals.append(str(letterIdx))

	# Loop through the possible length words from the hardcoded character minimum up to the full length of the input work itself
	for wordLength in range(shortestWordLen, maxPossibleIndexVal+1):
		# Create blank object lists for each word list - to be used for the final output
		sortedWordLengthOutput[wordLength] = []
		# Generate all unique index combinations using itertools library permutations
		for indexes in itertools.permutations(lettersIndexes, wordLength):
			# For all possible index values, convert them to a string and then check that they do not contain any duplicate or invalid numbers
			# eg 11345 is invalid because of the two 1's, as is 12349 due to the 9
			intVal = int(''.join(str(idx) for idx in indexes))
			# And then store these unique valid values
			allPossibleWordRangeValues.add(intVal)

	# ************************************************************************************************************
	# Generate theoretically possible string synonyms from the singular input word from these numerical indexes

	# Basically just random strings from the letters of the input word - likley to be many thousands of possibilities for a long word
	# Eg "ABCD" though to "DCBA" for input word ABCD

	for num in allPossibleWordRangeValues:
		# Eg num = 1234 or 53214 etc
		theLetters = []
		for thisLetterIdx in str(num):
			# Create an array of the letters of the new possible word based on the index number
			# Eg 1234 would be the first index of a four letter word
			# Eg 4321 of input "ABCD" would return "D,C,B,A" in an array
			theLetters.append(inputWord[int(thisLetterIdx)-1])
		# And then create the string word from these individual letters
		theWord = ""
		for letter in theLetters:
			# Eg first loop of ["A","B","C","D"] - created from the possible letters of above "num" variable (if 1234) from original word ABCD
			theWord = theWord + letter
		# Add to the final array if is unique
		if theWord not in newWords:
			# Note at the moment its all possible letters - so "ABCD" is included, even though is not a real word obviously
			newWords.add(theWord)

	# ************************************************************************************************************
	# Compare against a static list of real existent words - to return actual read words only

	if len(newWords) > 0:
		# Loop through r files in the relevant directory
		for fileName in os.listdir(filesDirectory):
			# If is a TXT file type
			if (fileName.lower().lstrip().rstrip().endswith(".txt")):
				# Load real words from this TXT file (one word per line)
				with open((filesDirectory + fileName), "r", encoding="utf-8") as txtFile:
					# Create a List of all possible words inside these
					realWordsList = set([eachWord.strip().lower() for eachWord in txtFile if eachWord.strip()])
					# Then loop through this created list
					for realWord in realWordsList:
						# If the real word does exist in the generated "words"
						if realWord in newWords:
							# Then add to the output - That is the final output of real words - just not yet sorted
							realWordOutput.add(realWord.upper())

	# ************************************************************************************************************
	# Then sort this list of real words by length and alphabetically
	inputWord = inputWord.upper()
	if len(realWordOutput) > 0:
		# Loop through possibly word lengths
		for wordLength in range(shortestWordLen, maxPossibleIndexVal+1):
			# Set a blank list
			wordsList = []
			# Loop through the non-sorted real words Set
			for real in realWordOutput:
				# If the length of the word is this word length
				if len(real) == wordLength:
					# Then add to this list
					wordsList.append(real)
			# Then sort this alphabetically
			wordsList.sort()
			# Then add to this object attached to the word length value
			sortedWordLengthOutput[wordLength] = wordsList
	# Then loop through the alphabetically sorted word length object
	for wordLength in sortedWordLengthOutput:
		for word in sortedWordLengthOutput[wordLength]:
			# And add these words to the final output - ordered first by word length and then alphabetically
			if word != inputWord or includeSourceWord:
				finalRealWordOutput.append(word)

	endTime = time.time()	# Used for printline testing

	# Print Line for testing
	if doPrintLines:
		print()
		print(finalRealWordOutput)		# Note this is the data that will eventually be returned
		print()

		if len(finalRealWordOutput) == 0:
			print("No real words can be generated from input word : '{}'".format(inputWord))
			print()

		print("An [{}] letter input word ('{}') generates [{}] possible words, of which [{}] are actually real words - in {:.3f} seconds".format(len(inputWord),inputWord,len(newWords),len(finalRealWordOutput),endTime - startTime))
		print()

	return finalRealWordOutput

main()
