import time

def main():
	startTime = time.time()			# testing
	print(startTime)				# testing

	word = "ABCDEFGH"

	# Hardcoded minimum length word
	shortestWordLen = 4
	# Hardcoded maximum allowed word length - just to force an exception, so the below functionality will work as intended
	maxAllowedMax = 9

	# The source data to be used for reference is Lower Case
	word = word.lower()

	# The possible letters of the input word
	possibleLetters = []
	# the numeric indexes of this input word
	lettersIndexes = []
	# The main string array where all possible new words will be added to for final comparison
	newWords = set()
	# Eg how many letters there are in the word - used for many loops below
	maxPossibleIndexVal = 0

	# Generate the possible letters and indexes of these from the input work
	for wordIdx in range(0,len(word)):
		possibleLetters.append(word[wordIdx])
		lettersIndexes.append(wordIdx+1)

	lettersIndexes.sort()
	possibleLetters.sort()

	# Get the highest index value from this
	if len(lettersIndexes) > 0:
		for x in range(len(lettersIndexes), 0, -1):
			if maxPossibleIndexVal < x:
				maxPossibleIndexVal = x

	# Throw an exception as a safeguard
	if maxPossibleIndexVal > maxAllowedMax:
		s = "ERRROR : 'maxPossibleIndexVal' variable value ({}) is above the allowed 'maxAllowedMax' variable value ({}) - cannot continue with the current functionality".format(maxPossibleIndexVal, maxAllowedMax)
		raise Exception(s)

	# ************************************************************************************************************
	# Make possible numbers from the word - To be then used as indexes to loop through the string word

	# Indexes of the Word letters as strings of the value
	allowedIndexStrVals = []
	# All possible numbers generated from the indexes of the input work, to be used to create the output string words
	allPossibleWordRangeValues = set()

	# Stringify the allowed index values
	for letterIdx in lettersIndexes:
		allowedIndexStrVals.append(str(letterIdx))

	print("A = {}".format(time.time()))		# testing

	# Loop through the possible length words from the hardcoded character minimum up to the full length of the input work itself
	for wordLength in range(shortestWordLen, maxPossibleIndexVal+1, 1):
		minRange = ""
		maxRange = ""		

		# Loop through up to this current dynamic word length to get all possible index values - eg "1111" to "4444"
		for x in range(1,wordLength+1, 1):
			minRange = minRange + "1"
			maxRange = maxRange + str(maxPossibleIndexVal)
		
		# Then convert this range from a string into a number and loop through - eg 1111 up to 4444
		for rangeIdx in range(int(minRange), int(maxRange), 1):
			# Tut convert the value back into a string for text comparison
			strValue = str(rangeIdx)

			# Check for unique numeric values and must not contain invalid digits
			newValueString = ""
			for char in strValue:
				# eg 11345 is invalid because of the two 1's, as is 12349 due to the 9
				if char not in newValueString and char in allowedIndexStrVals:
					newValueString = newValueString + char
			# Must be the full length of the current loop, and not already exist in the relevant array
			if len(newValueString) == wordLength and int(newValueString) not in allPossibleWordRangeValues:
				# Add to the array if all good
				allPossibleWordRangeValues.add(int(newValueString))

	print("B = {}".format(time.time()))	# testing

	# ************************************************************************************************************
	# Generate theoretically possible string synonyms from the singular input word from these numerical indexes
	for num in allPossibleWordRangeValues:
		theLetters = []
		for thisLetterIdx in str(num):
			# Create an array of the letters of the new possible word based on the index number
			# Eg 1234 would be the first index of a four letter word
			# Eg 4321 of input "ABCD" would return "D,C,B,A" in an array
			theLetters.append(word[int(thisLetterIdx)-1])
		# And then create the string word from these individual letters
		theWord = ""
		for letter in theLetters:
			theWord = theWord + letter
		# Add to the final array if is unique
		if theWord not in newWords:
			# Note at the moment its all possible letters - so "ABCD" is included, even though is not a real word obviously
			newWords.add(theWord)

	# Just testing for now
	#print(newWords) # Main data output which will eventually be checked against a list of real words passed in
	
	endTime = time.time()	# testing
	print(endTime)			# testing

	# testing
	print("A [{}] letter work returns [{}] possible words in {:.1f} seconds".format(len(word),len(newWords),endTime - startTime))
	
	'''
	# testing
	A [4] letter work returns [24] possible words in 0.0 seconds
	A [5] letter work returns [240] possible words in 0.0 seconds
	A [6] letter work returns [1800] possible words in 0.4 seconds
	A [7] letter work returns [13440] possible words in 5.1 seconds
		1755240068.6143494
		A = 1755240068.6144867
		B = 1755240073.7377632
		1755240073.7502892
	A [8] letter work returns [109200] possible words in 70.6 seconds
		1755239954.8352754
		A = 1755239954.8354018
		B = 1755240025.3042166
		1755240025.4256907
	........
	'''
main()
