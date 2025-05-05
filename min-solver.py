#This program is incomplete. Do not use.
#The purpose of this file is to create a simplified version of solver.py without any of the computer option and cleaned-up functions
#I am unhappy with optsolve.py because its method is too slow and I dont wish to record every solve, I simply want the answer. Since I am building a wordle website in parallel to this program, I want to store accounts and solve data in the website. This program is intended only as a solve-accelerator

import sys
# Open the file in read mode

included = []
excluded = []
partial_word = []
yellow = ["", "", "", "", ""]
possible_words = []
word_scores = []
solution = "treat"
singles = []
multiples = []
final_guesses = []
guesses = 0
count = 0
guesslist = []
chars = []
debug = False
all_english = False
all_fives = False

def return_second(x): #returns the second item of a tuple, used in sorting the tuples in a list
    return x[1]

def reset():
    global included, excluded, partial_word, yellow, singles, multiples
    included = []
    excluded = []
    partial_word = ["*"] * len(solution)
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
        partial_word_input = "*" * len(solution)
    for i in range(len(solution)):
        partial_word[i] = partial_word_input[i]
    for i in range(len(solution)):
        yellow[i] += input("Enter any new yellow letters in column " + str(i + 1) + ": ").lower().strip()

def handle_word(i): #appends a word to possible_words, returns nothing
    if len(i) != len(solution):
        return
    for j in excluded:
        if j in i and not j in included: #we need to include a clause here that if the letter (represented by var j) is in both included and excluded for the word i, we shouldn't throw out the word.
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

def solve(): #possible_words is now full
    global possible_words
    possible_words = []
    for i in word_list:
        handle_word(i)

letter_scores = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23, 'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59, 'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39, 'j': 1.00, 'q': 1.00, "'": 1, "-": 1}
score_list = list(letter_scores.items())

def calculate_frequency(letter):
    count = 0
    for i in chars:
        if i == letter:
            count += 1
    total = len(chars)
    percent = round((count / total) * (1/0.00233), 2)
    return percent

letter_frequencies = {'e': 45.72, 'a': 36.3, 'r': 33.33, 'o': 27.96, 't': 27.03, 'l': 26.66, 'i': 24.88, 's': 24.81, 'n': 21.32, 'c': 17.69, 'u': 17.32, 'y': 15.76, 'd': 14.57, 'h': 14.42, 'p': 13.61, 'm': 11.72, 'g': 11.53, 'b': 10.42, 'f': 8.53, 'k': 7.79, 'w': 7.23, 'v': 5.67, 'z': 1.48, 'x': 1.37, 'q': 1.08, 'j': 1.0, "'": 0.0, '-': 0.0}
alphabet = "abcdefghijklmnopqrstuvwxyz'-"
frequency_list = list(letter_frequencies.items())


frequency_list.sort(reverse=True, key=return_second)

def populate_frequencies(): #goes through the entire alphabet and creates frequency scores for each letter, appends to and sorts frequency list
    global frequency_list, letter_frequencies
    if all_english or all_fives:
        letter_frequencies = letter_scores
        frequency_list = score_list
    else:
        for i in alphabet:
            letter_frequencies[i] = calculate_frequency(i)

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

#word_scores is now full

def print_words(): #outputs the sorted list of possible words and their scores
    global final_guesses, guesses, count
    print("")
    print("%d total results out of %d possible answers (%3.2f%%)." % (len(possible_words), len(word_list), 100.0 * len(possible_words) / len(word_list)))
    final_guesses = list(zip(possible_words, word_scores))
    final_guesses.sort(reverse=True, key=return_second)
    
    for i in final_guesses[:10]: 
        count += 1      
        print("%2d: %s (%.2f)" % (count, i[0], i[1]))

def main():
    populate_frequencies()
    while True:
        global solution
        ask()
        solve()
        score_words()
        print_words()

reset()
main()