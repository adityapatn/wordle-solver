

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

#print(evaluate("happy", "flunk"))

#a function that takes green, yellow, and excluded and returns the next best guess