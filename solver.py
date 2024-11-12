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
computer = 0
count = 0
guesslist = []
chars = []
computer = 0
debug = False
all_english = False
all_fives = False

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

letter_frequencies = {}
alphabet = "abcdefghijklmnopqrstuvwxyz'-"
frequency_list = []

def populate_frequencies(): #goes through the entire alphabet and creates frequency scores for each letter, appends to and sorts frequency list
    global frequency_list, letter_frequencies
    if all_english or all_fives:
        letter_frequencies = letter_scores
        frequency_list = score_list
    else:
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

#word_scores is now full

def return_second(x): #returns the second item of a tuple, used in sorting the tuples in a list
    return x[1]

def print_words(): #outputs the sorted list of possible words and their scores
    global final_guesses, guesses, count
    if not computer:
        print("")
        print("%d total results out of %d possible answers (%.2f%%)." % (len(possible_words), len(word_list), 100.0 * len(possible_words) / len(word_list)))
    final_guesses = list(zip(possible_words, word_scores))
    final_guesses.sort(reverse=True, key=return_second)
    if debug:
        print("Computer:", computer)
        print("Guesses:", guesses)
    if not(computer and (guesses >= 2)): #count = 0 should be skipped only if computer is true and it is not the first guess
        count = 0
    
    for i in final_guesses[:10]: 
        count += 1
        if computer:
            print("%2d: %s (%.2f): best of %d results (%.2f%%)." % (count, i[0], i[1], len(possible_words), 100.0 * len(possible_words) / len(word_list)))
            break            
        else:
            print("%2d: %s (%.2f)" % (count, i[0], i[1]))

    #I want count to get printed at 1 and then increase every print statement if computer is false, being reset back to 0 every function call. If computer is true, I want count to get incremented, then break before the next print, but increment count, and don't reset it every function call

def print_frequencies():
    count = 1
    for i, j in zip(frequency_list, score_list):
        print(str(count) + ": " + str(i[0]) + " (" + str(i[1]) + ") English: " + str(j[0]) + " (" + str(j[1]) + ")")
        count += 1

def main():
    choose_mode()
    while True:
        global solution
        if computer:
            check_word()
        else:
            ask()
        solve()
        populate_frequencies()
        score_words()
        if debug:
            print_frequencies()
        print_words()
        if debug:
            input("\nContinue?")

def check_word():
    global included, excluded, partial_word, yellow, solution, final_guesses, guesses, guesslist, word_list
    if possible_words and solution:
        word = final_guesses[0][0] #check the most likely word in the list first
        for i in range(len(solution)): #if the letters of word and solution match, make it green. If they don't, but it is somewhere else in the word, make it yellow.
            letter = word[i]
            if letter == solution[i]:
                partial_word[i] = letter
                included.append(letter)
            elif letter in solution: #it should be scored yellow since it appears somewhere else in the word
                yellow[i] += letter #add the letter to the yellow letters in that column
                included.append(letter)
            else:
                excluded.append(word[i]) #exclude it/score it as grey
            if solution.count(word[i]) > 1 and word.count(word[i]) > 1 and not word[i] in multiples:
                multiples.append(word[i])
        if debug:
            print("I guessed %s." % (word))
            print("Included:", included)
            print("Excluded:", excluded)
            print("Partial word:", partial_word)
            print("Yellow letters:", yellow)
            print("Multiples:", multiples)
    
        guesslist.append(word)

    if not "*" in partial_word:
        print("I correctly guessed %s in %i tries." % (word, guesses))
        guessstring = ','.join(guesslist) + "\n"
        if debug:
            print("Guess string:", guessstring)
        with open('computersolves.csv', 'a') as file:
            file.write(guessstring)
        main()
    else:
        guesses += 1
        if guesses > 20 and not (solution in word_list):
            print("Your word is not an official wordle solution.")
            main()

def choose_mode():
    global computer, debug, all_english, all_fives, chars, word_list, solution
    computer = input("Enter 0 to assist you in solving a wordle or 1 (e for all English five-letter words, a for entire English solution set, d for debug mode) to enter a solution and test the computer: ")

    if 'e' in computer:
        all_fives = True
        file = open('wordlist_fives.txt', 'r')
        print("Resorting to english dictionary.")
        data = file.read()
        word_list = data.split()
        chars = list(data)
        for i in chars:
            if i == "\n":
                chars.remove(i)
        file.close()
    if 'a' in computer:
        all_english = True
        file = open('words.txt', 'r')
        print("Resorting to english dictionary.")
        data = file.read()
        word_list = []
        for word in data.split():
            print(word)
            word_list.append(word)
        #word_list = data.split()
        chars = list(data)
        for i in chars:
            if i == "\n":
                chars.remove(i)
        file.close()
    else:
        file = open('shuffled_real_wordles.txt', 'r')
        data = file.read()
        word_list = data.split()
        chars = list(data)
        for i in chars:
            if i == "\n":
                chars.remove(i)
        file.close()

    if 'd' in computer:
        debug = True

    if debug:
        print("Word list:", word_list)

    computer = ''.join(c for c in computer if c.isdigit())
    computer = int(computer)

    if computer:
        solution = input("Enter a word that you want the computer to try and find: ")
        '''if len(solution) > 5:
            solution = solution[0:5:]
            print("Your word has been shortened to %s." % (solution))
        elif len(solution) < 5:
            print("That is too short. Try again.")
            main()'''

reset()
main()

#The next step is to refactor the entire program to use local variables instead of global variables to reduce the chance of functions interfering with each other and make the program easier to debug