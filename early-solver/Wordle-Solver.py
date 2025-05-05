text = open("words.txt", "r")
word_list = set(text.read().split())

print("Type in the information you receive.")

included_letters = input("Include which letters? ")
excluded_letters = input("Exclude which letters? ")
word = input("Enter the partially solved word in form of a*b*c, where * stands for any letter.")
results_1 = []

def run():
    for a in word_list: # 'break' breaks the loop on line 12

        works = True
        #if len(a) != len(word):
        #    works = False
        #    break
        

        
        for b in included_letters:
            if not b in a:
                works = False
                break
        
        if works:
            for c in excluded_letters:
                if c in a:
                    works = False
                    break
        
        if works:
            for i,j in zip(word,a):
                    
                if i.lower() != j.lower() and i != "*" and i != "":
                    works = False
                    break
                
        if works:
                results_1.append(a)

    if len(results_1) == 0:

        print("There are no possible answers like this. Did you make a mistake?")

    else:
        for d in results_1:
            print(d)

run()
