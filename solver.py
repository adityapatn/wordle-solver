import sys
# Open the file in read mode

file = open('shuffled_real_wordles.txt', 'r')
data = file.read()
word_list = data.split()
chars = list(data)
for i in chars:
    if i == "\n":
        chars.remove(i)
file.close()
#print(chars)
#print(word_list)

included = ""
excluded = ""
partial_word = ""
yellow = ["", "", "", "", ""]
possible_words = []
word_scores = []

def reset():
    global included, excluded, partial_word, yellow
    included = ""
    excluded = ""
    partial_word = ""
    yellow = ["", "", "", "", ""]

def ask():
    global included, excluded, partial_word, yellow
    included += input("Enter any new included (yellow and green) letters: ").lower()
    excluded += input("Enter any new excluded (dark grey) letters: ").lower()
    partial_word = input("Enter the letters of the word you know are in the correct position (all green letters), using * as a wildcard (no green in the column): " ).lower()
    for i in range(5):
        yellow[i] += input("Enter any new yellow letters in column " + str(i + 1) + ": ")



def handle_word(i): #appends all possible words to possible_words, returns nothing
    for j in excluded:
        if j in i:
            return

    for j in included:
        if not j in i:
            return

    for j, k in zip(i, partial_word):
        if not (k == "*" or j == k):
            return

    for j, k in zip(i, yellow): #i = crane, j = c, k = th
        if k: #if there are any yellow letters in the column
            for l in k: #iterate through every yellow letter in the column
                if j == l: #if the first letter is one we know is yellow in that column, throw out i and start again from the outermost for loop
                    return
        
    possible_words.append(i)

def solve():
    global possible_words
    possible_words = []
    for i in word_list:
        handle_word(i)

#possible_words is now full

letter_scores = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23, 'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59, 'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39, 'j': 1.00, 'q': 1.00}
score_list = list(letter_scores.items())

def calculate_frequency(letter):
    count = 0
    for i in chars:
        if i == letter:
            count += 1
    
    total = len(chars)
    percent = round((count / total) * (1/0.00233), 2)
    return percent

letter_frequencies = {}
alphabet = "abcdefghijklmnopqrstuvwxyz"
frequency_list = []

def populate_frequencies():
    global frequency_list
    for i in alphabet:
        letter_frequencies[i] = calculate_frequency(i)
    
    frequency_list = list(letter_frequencies.items())
    frequency_list.sort(reverse=True, key=return_second)

def score_words(): #takes all words in possible_words and assigns scores to them, appends scores to word_scores
    global word_scores
    word_scores = []
    for i in possible_words:
        word_score = 0
        letters_in_word = ""
        for j in i:
            if j not in letters_in_word:
                word_score += letter_frequencies[j]
                letters_in_word += j
        word_score = round(word_score, 4)
        word_scores.append(word_score)
    #print("Word scores:", word_scores)

#word_scores is now full

def return_second(x): #returns the second item of a tuple, used in sorting the tuples in a list
    return x[1]

def print_words(): #outputs the sorted list of possible words and their scores
    print("")
    #print(str(len(possible_words)) + " total results out of 2315 possible answers (" + str( + "%).".format(round((len(possible_words) / 2315) * 100), 2)))
    print("%d total results out of 2315 possible answers (%.2f%%)." % (len(possible_words), 100.0 * len(possible_words) / 2315))
    final_guesses = list(zip(possible_words, word_scores))
    final_guesses.sort(reverse=True, key=return_second)
    count = 1
    for i in final_guesses[:10]:
        #print("%2d: %s" + str(i[0]) + " (" + str(i[1]) + ")" % (count))
        print("%2d: %s (%.2f)" % (count, i[0], i[1]))
        count += 1

def print_frequencies():
    count = 1
    for i, j in zip(frequency_list, score_list):
        print(str(count) + ": " + str(i[0]) + " (" + str(i[1]) + ") English: " + str(j[0]) + " (" + str(j[1]) + ")")
        count += 1

def main():
    ask()
    solve()
    populate_frequencies()
    #print_frequencies()
    score_words()
    print_words()
    
    

while True:
    main()