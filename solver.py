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

included = []
excluded = []
partial_word = ["*"] * 5
yellow = ["", "", "", "", ""]
possible_words = []
word_scores = []
solution = ""
singles = []
multiples = []

def reset():
    global included, excluded, partial_word, yellow, singles
    included = []
    excluded = []
    partial_word = ["*"] * 5
    yellow = ["", "", "", "", ""]
    singles = []
    multiples = []

def ask():
    global included, excluded, partial_word, yellow, multiples
    included_input = input("Enter any new included (yellow and green) letters: ").lower().strip()
    for i in included_input:
        if included_input.count(i) > 1:
            multiples.append(i)
    for i in included_input:
        included.append(i)
    excluded_input = input("Enter any new excluded (dark grey) letters: ").lower().strip()
    for i in excluded_input:
        excluded.append(i)
    partial_word_input = input("Enter the letters of the word you know are in the correct position (all green letters), using * as a wildcard (no green in the column): " ).lower().strip()
    if not partial_word_input:
        partial_word_input = "*****"
    for i in range(5):
        partial_word[i] = partial_word_input[i]
    for i in range(5):
        yellow[i] += input("Enter any new yellow letters in column " + str(i + 1) + ": ").lower().strip()

def handle_word(i): #appends all possible words to possible_words, returns nothing
    for j in excluded:
        if j in i and not j in included: #we need to include a clause here that if the letter (represented by var j) is in both included and excluded, we shouldn't throw out the word.
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
                if j == l: #if the first letter is one we know is yellow in that column, throw out i
                    return
    for j in included:
        if j in excluded:
            singles.append(j)
    
    for j in singles:
        if i.count(j) > 1:
            return
    
    for j in multiples:
        if i.count(j) < 2:
            return
            
        
    possible_words.append(i) #adds the word (if it passes all the checks) to possible_words

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
    score_words()
    print_words()
    #check_word()

possible_words = ['treat']
solution = 'treat'

def check_word():
    global included, excluded, partial_word, yellow, solution
    reset()

    word = possible_words[0]
    index = [0, 1, 2, 3, 4]
    for i in range(5): #if the letters of word and solution match, make it green. If they don't, but it is somewhere else in the word, make it yellow.
        if word[i] == solution[i]:
            partial_word[i] = word[i]
        elif word[i] in solution: #it should be scored yellow since it appears somewhere else in the word
            yellow[i] += word[i] #add the letter to the yellow letters in that column
        else:
            excluded += word[i] #exclude it/score it as grey

    #There's a problem with the original solver where if you input a guess with double letters, like 'sieve', and only the 5th letter of the solution is e, the first e in sieve will be scored as grey, and the second as green. If e is inputted as both included and excluded (although it is actually in the word), the solution set will be calculated as 0. The algorithm is not equipped to handle double letters.
             
while True:
    main()