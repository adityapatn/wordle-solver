txtfile = open("words.txt", "r")
words = set(txtfile.read().split())
yletters = input("Which letters are required?").strip()
ylist = []
for i in yletters:
    ylist.append(i)

nletters = input("Which letters are banned?").strip()
nlist = []
for i in nletters:
    nlist.append(i)

length = input("How long is the word in characters?").strip()

final_words = []

for x in words:
    
    works = True

    if len(x) != length and length != "":
        works = False
        break
    
    if works:
        for i in ylist:
            if not i in x:
                works = False
                break
    
    if works:
        for i in nlist:
            if i in x:
                works = False
                break
    
    if works:
        final_words.append(x)

if len(final_words) > 1:
    for i in final_words:
        print(i)
else:
    print("There is no word like that. Idiot.")
            
