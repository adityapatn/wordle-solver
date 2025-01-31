with open("shuffled_real_wordles.txt", 'r') as file:
        word_list = [line.strip() for line in file]

letter_frequencies = [('e', 45.72), ('a', 36.3), ('r', 33.33), ('o', 27.96), ('t', 27.03), ('l', 26.66), ('i', 24.88), ('s', 24.81), ('n', 21.32), ('c', 17.69), ('u', 17.32), ('y', 15.76), ('d', 14.57), ('h', 14.42), ('p', 13.61), ('m', 11.72), ('g', 11.53), ('b', 10.42), ('f', 8.53), ('k', 7.79), ('w', 7.23), ('v', 5.67), ('z', 1.48), ('x', 1.37), ('q', 1.08), ('j', 1.0), ("'", 0.0), ('-', 0.0)]

#a function that takes input from the user and returns a list green, a list yellow, and a string excluded
def ask():
    excluded = input("Enter any excluded letters: ").strip().lower()
    green_input = input("Enter the letters of the word you know are in the correct position, using any non-alphabetic character as a wildcard: ").strip().lower()
    green = list(green_input)
    for i in green:
        if not i.isalpha():
            i = ""
    
    yellow_1 = input("Yellow letters in column 1:").strip().lower()
    yellow_2 = input("Yellow letters in column 2:").strip().lower()
    yellow_3 = input("Yellow letters in column 3:").strip().lower()
    yellow_4 = input("Yellow letters in column 4:").strip().lower()
    yellow_5 = input("Yellow letters in column 5:").strip().lower()
    yellow = [yellow_1, yellow_2, yellow_3, yellow_4, yellow_5]

    return green, yellow, excluded

#a function that takes a guess and the solution and evaluates the guess
#eventually I want this function to print the evaluated guess in green, yellow, and gray
def evaluate(guess, solution):
    green = [""] * 5
    yellow = [""] * 5
    excluded = ""

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
    #print("Checkpoint 1!")
    #print("Word:", word)
    for i, j in zip(word, green):
        if j and j.isalpha():
            if i != j:
                return False
    
    #print("Checkpoint 2!")
    for i in word:
        if i in excluded:
            return False
    
    #print("Checkpoint 3!")
    for i in range(len(yellow)):
        for j in yellow[i]:
            if word[i] == j:
                return False
            if not j in word:
                return False
    
    #print("It works!")
    return True

#a function that takes green, yellow, and excluded and returns a list of possible next guesses (random/alphabetic order)
def next_guess(green, yellow, excluded):
    global word_list
    possible_solutions = []

    for word in word_list:
        if check_word(green, yellow, excluded, word):
            possible_solutions.append(word)
    
    return possible_solutions

#x, y, z, = evaluate("fluxy", "flour")
x, y, z, = ask()
print("Green:", x, "Yellow:", y, "Grey:", z)
print(next_guess(x, y, z))
#print(check_word(x, y, z, "apnea"))