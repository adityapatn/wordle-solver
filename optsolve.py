with open("shuffled_real_wordles.txt", 'r') as file:
        word_list = [line.strip() for line in file]

#print(word_list)

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

#a function that takes green, yellow, and excluded and returns a list of possible next guesses (random/alphabetic order)
def next_guess(green, yellow, excluded):
    global word_list
    possible_solutions = []
    
    #a function that takes green, yellow, excluded, and a word to evaluate and returns whether it's possible   
    def check_word(green, yellow, excluded, word):
        for i, j in zip(word, green):
            if j:
                if i != j:
                    return False
        
        for i in word:
            if i in excluded:
                return False

        '''
        for i in range(len(word)):
            for j in yellow[i]:
                if word[i] == j:
                    return False
        '''

        return True

    for word in word_list:
        if check_word(green, yellow, excluded, word):
            possible_solutions.append(word)
    
    return possible_solutions

#testing functions

print("Evaluation:", evaluate("clang", "lunch"))
x, y, z, = evaluate("clang", "lunch")
print(next_guess(x, y, z))