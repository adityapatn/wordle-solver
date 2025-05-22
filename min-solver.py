#This program is incomplete. Do not use.
#The purpose of this file is to create a simplified version of solver.py without any of the computer option and cleaned-up functions
#I am unhappy with optsolve.py because its method is too slow and I dont wish to record every solve, I simply want the answer. Since I am building a wordle website in parallel to this program, I want to store accounts and solve data in the website. This program is intended only as a solve-accelerator.

import sys

# Open the file in read mode
with open('shuffled_real_wordles.txt', 'r') as file:
    word_list = file.read().split()

letter_frequencies = {'e': 45.72, 'a': 36.3, 'r': 33.33, 'o': 27.96, 't': 27.03, 'l': 26.66, 'i': 24.88, 's': 24.81, 'n': 21.32, 'c': 17.69, 'u': 17.32, 'y': 15.76, 'd': 14.57, 'h': 14.42, 'p': 13.61, 'm': 11.72, 'g': 11.53, 'b': 10.42, 'f': 8.53, 'k': 7.79, 'w': 7.23, 'v': 5.67, 'z': 1.48, 'x': 1.37, 'q': 1.08, 'j': 1.0, "'": 0.0, '-': 0.0}

word_length = 5
included = []
excluded = []
multiples = []
partial_word = ["*"] * word_length #list so is it is mutable as well as iterable
yellow = [""] * word_length #list so each position can contain several letters
singles = []

def ask():
    global included, excluded, multiples, partial_word, yellow, singles
    included_input = input("Enter any new included (yellow and green) letters: ").lower().strip()
    for i in included_input:
        included.append(i)
        if included_input.count(i) > 1 and not i in multiples:
            multiples.append(i)

    excluded_input = input("Enter any new excluded (dark grey) letters: ").lower().strip()
    for i in excluded_input:
        excluded.append(i)
    
    for letter in included:
        if letter in excluded:
            singles.append(letter)
    
    partial_word_input = input("Enter the letters of the word you know are in the correct position (all green letters), using * as a wildcard (no green in the column): " ).lower().strip()
    while len(partial_word_input) < word_length:
        partial_word_input += "*"
    #partial_word_input is now a five-character string of letters and placeholders
    for i in range(5):
        char = partial_word_input[i]
        if char.isalpha():
            partial_word[i] = partial_word_input[i]

    yellow_input = input("Enter the yellow letters in the word separated by commas: ").split(",")
    #print(yellow_input)
    while len(yellow_input) < 5:
        yellow_input.append("")
    
    for index in range(5):
        yellow[index] += yellow_input[index].lower().strip()

def check_word(word):
    global included, excluded, multiples, partial_word, yellow, singles

    for letter in excluded:
        if (letter in word) and not (letter in singles):
            return False

    for letter in included:
        if not letter in word:
            return False

    for letter, solution_letter in zip(word, partial_word):
        if not (solution_letter == "*" or letter == solution_letter): #not (A or B) is more computationally efficient than (not A) and (not B) because the interpreter will not evaluate the second condition of an or expression if the first is true.
            return False

    for j, k in zip(word, yellow): #i = crane, j = c, k = th
        if k: #if there are any yellow letters in the column
            for l in k: #iterate through every yellow letter in the column
                if j == l: #if the letter is one we know is yellow in that column, throw out i
                    return False
    
    for j in singles:
        if word.count(j) > 1:
            return False
    
    for j in multiples:
        if word.count(j) < 2:
            return False
    
    #print(word)
    return True

def remove_duplicates(message):
    seen = ""
    new = ""
    for char in message:
        if char not in seen:
            new += char
        seen += char
    
    return new

def solve():
    possible_solutions = []
    for possible_word in word_list:
        if check_word(possible_word): #this word is a potential solution, score it
            word_score = 0
            for letter in remove_duplicates(possible_word):
                word_score += letter_frequencies[letter]
            possible_solutions.append([possible_word, word_score])
    
    #possible_solutions is now populated, sort it
    possible_solutions = sorted(possible_solutions, key=lambda x: x[1]) #sorted sorts from least to greatest, but we need largest score first
    possible_solutions.reverse()

    #print the words to the user
    percent = round(100 * len(possible_solutions) / len(word_list), 2)
    print("\n%d total results out of %d possible answers (%.2f%%)." % (len(possible_solutions), len(word_list), percent))
    for index in range(min(10, len(possible_solutions))):
        print("%2d: %s (%.2f)" % (index + 1, possible_solutions[index][0], possible_solutions[index][1]))
    if len(possible_solutions) == 1:
        print("\nThanks for playing!\n")
        sys.exit()
    if len(possible_solutions) < 1:
        print("\nAn error occurred.\n")
        sys.exit()

while True:
    try:
        ask()
        solve()
    except KeyboardInterrupt:
        print("\nThanks for playing!\n")
        sys.exit()