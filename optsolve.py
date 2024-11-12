
computer = input("Enter 0 to assist you in solving a wordle or 1 (e for all English five-letter words, a for entire English solution set, d for debug mode) to enter a solution and test the computer: ")
filename = "shuffled_real_wordles.txt"
if 'e' in computer:
    filename = "wordlist_fives.txt"
if 'a' in computer:
    filename = "words_alpha.txt"
if 'd' in computer:
    debug = True
computer = int(''.join(c for c in computer if c.isdigit())) #removes any mode indicators from computer, leaving it as either 1 or 0