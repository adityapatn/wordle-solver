with open("shuffled_real_wordles.txt", 'r') as file:
        word_list = [line.strip() for line in file]

letter_frequencies = {'e': 45.72, 'a': 36.3, 'r': 33.33, 'o': 27.96, 't': 27.03, 'l': 26.66, 'i': 24.88, 's': 24.81, 'n': 21.32, 'c': 17.69, 'u': 17.32, 'y': 15.76, 'd': 14.57, 'h': 14.42, 'p': 13.61, 'm': 11.72, 'g': 11.53, 'b': 10.42, 'f': 8.53, 'k': 7.79, 'w': 7.23, 'v': 5.67, 'z': 1.48, 'x': 1.37, 'q': 1.08, 'j': 1.0, "'": 0.0, '-': 0.0}

#a function that takes previous values of a variable, input from the user, and returns a list green, a list yellow, and a string excluded
def ask(green_start, yellow_start, excluded_start):
    yellow = yellow_start
    green = green_start
    excluded = excluded_start
    excluded += input("Enter any excluded letters: ").strip().lower()
    green_input = input("Enter the letters of the word you know are in the correct position, using any non-alphabetic character as a wildcard: ").strip().lower()
    while len(green_input) < 5:
        green_input += "*"
    
    #green_input is now a five-character string
    for i in range(5):
        if green_input[i].isalpha():
            green[i] = green_input[i]

    yellow[0] += input("Yellow letters in column 1:").strip().lower()
    yellow[1] += input("Yellow letters in column 2:").strip().lower()
    yellow[2] += input("Yellow letters in column 3:").strip().lower()
    yellow[3] += input("Yellow letters in column 4:").strip().lower()
    yellow[4] += input("Yellow letters in column 5:").strip().lower()

    return green, yellow, excluded

#a function that takes a guess and the solution and evaluates the guess
def evaluate(green_start, yellow_start, excluded_start, guess, solution):
    green = green_start
    yellow = yellow_start
    excluded = excluded_start

    for i, j, k in zip(guess, solution, range(5)):
        if i == j: #it's in the correct spot
            green[k] = i
        elif i in solution: #it's in the word, but not in this spot
            yellow[k] += i
        elif not i in excluded: #the letter isn't in the word at all, and we haven't excluded it yet
            excluded += i
    
    return green, yellow, excluded

#a function that takes green, yellow, excluded, and a word to evaluate and returns whether it is a possible solution   
def check_word(green, yellow, excluded, word):
    global letter_frequencies
    for i, j in zip(word, green):
        if j and j.isalpha():
            if i != j:
                return False
    
    for i in word:
        if i in excluded:
            return False
    
    for i in range(len(yellow)):
        for j in yellow[i]:
            if word[i] == j:
                return False
            if not j in word:
                return False

    #the word has passed all the checks, and we need to "score" the word based on its letters
    score = 0
    checked_letters = ""
    for i in word:
        if not i in checked_letters:
            score += letter_frequencies[i]
            checked_letters += i
    return (word, score)

#a function that takes green, yellow, and excluded and returns a list of possible next guesses (random/alphabetic order)
def next_guess(green, yellow, excluded):
    global word_list
    possible_solutions = []

    for word in word_list:
        evaluation = check_word(green, yellow, excluded, word)
        if evaluation:
            possible_solutions.append(evaluation)
    
    #possible_solutions is now populated, but we need to sort it.
    possible_solutions = sorted(possible_solutions, key=lambda x: x[1], reverse=True)
    return possible_solutions

def assist_wordle():
    green = [""] * 5
    yellow = [""] * 5
    excluded = ""
    solved = False

    while not solved:
        green, yellow, excluded = ask(green, yellow, excluded)
        if not "" in green:
            solved = True
        #print("Green:", green, "Yellow:", yellow, "Grey:", excluded)
        solutions = next_guess(green, yellow, excluded)
        print("")
        print("%d total results out of %d possible answers (%3.2f%%)." % (len(solutions), len(word_list), 100.0 * len(solutions) / len(word_list)))
        print("")
        for i in range(5):
            print("%d: %s (%0.2f)" % (i + 1, solutions[i][0], solutions[i][1]))

# a function that takes a solution word and an optional first guess, and tries to guess the word.
#eventually I want this function to print the evaluated guess in green, yellow, and gray
def solve_wordle():
    green = [""] * 5
    yellow = [""] * 5
    excluded = ""
    solution = input("Enter the solution: ").strip().lower()
    first_guess = input("Enter an optional first guess: ").strip().lower()
    guesses = []

    if first_guess:
        guess = first_guess
        green, yellow, excluded = evaluate(green, yellow, excluded, first_guess, solution)
    else:
        guess = next_guess(green, yellow, excluded)[0]
    guesses.append(guess)
    
    while guess[0] != solution:
        green, yellow, excluded = evaluate(green, yellow, excluded, guess[0], solution)
        guess = next_guess(green, yellow, excluded)[0]
        guesses.append(guess)
    
    for i in range(len(guesses)):
        print("%d: %s (%3.2f)" % (i + 1, guesses[i][0], guesses[i][1]))
    
    print("")
    print("I guessed the word in %d guesses." % (len(guesses)))
    raise KeyboardInterrupt()

try:
    solve_wordle()
except KeyboardInterrupt:
    print("\nExiting program.")