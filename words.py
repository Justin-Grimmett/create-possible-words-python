# Note this really only needs to be ran once - but I'll store it for reference purposes

import os
import json
import re
import gzip

# Source word data downloaded from here : 
# [ https://diginoodles.com/projects/eowl ]
# This is free to use and redistribute EOWL even in software or games 
# BUT you must include the copyright notice and the licensing statement wherever you use or redistribute the list. 
# There are no other restrictions, and the author encourages broad distribution.

##############################################################################################################
# The folder location of where to get the (extracted) CSV files containing the Words from - manually change this as required:
dir = 'C:/Users/justi/Downloads/EOWL-v1.1.2/EOWL-v1.1.2/CSV Format/'

minAllowedLen = 4   # Shortest allowed word - set as 4 for now - change this value as required
##############################################################################################################

finalWords = []                     # temp Output
output = {}                         # final Output
MaxLen = 0                          # Variable to store the longest possible word
pattern = re.compile("^[a-z]+$")    # Only allow "a-z" format words

# Iterate over files in the above directory
for name in os.listdir(dir):
    # If is a CSV
    if (name.lower().lstrip().rstrip().endswith(".csv")):
        # Load words from these CSVs file (one word per line)
        with open((dir + name), "r", encoding="utf-8") as f:
            # Create a List of all possible words
            words = [w.strip().lower() for w in f if w.strip()]
            # Then loop through this created list
            for w in words:
                # If does not contain any invalid characters
                if pattern.fullmatch(w) is not None:
                    # If longer than the allowed shortest length word
                    if len(w) >= minAllowedLen:
                        # Add to another list as output
                        finalWords.append(w)
                        if len(w) > MaxLen:
                            # Store the longest possible word
                            MaxLen = len(w)
# Re-sort
finalWords.sort()

x = minAllowedLen
# Loop through the possible word lengths
while x <= MaxLen:
    # set temp data for each loop
    exists = False
    wordData = []
    # Loop through all words
    for w in finalWords:
        # If is the allocated lenth word
        if len(w) == x:
            # Then at least one word of this lenth exists
            exists = True
            # Add this valid word to a temp list
            wordData.append(w)
    # If is a valid length word, then add the temp list of all words for this length into a final Dictionary output attached to the value for this lenght
    if exists:
        output.update({x : wordData})
    # Loop
    x = x + 1

# If any output data exists
if len(output) > 0:
    # Store this as a real JSON file
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=5)
    # And then compress this JSON as a real GZ zipped file
    with open("words.json", 'rb') as f_in:
        with gzip.open('compressed-words.json.gz', 'wb') as f_out:
            f_out.writelines(f_in)
    print("Complete")
else:
    print("No data to store")
