from collections import defaultdict
from math import sqrt
from numpy.random import choice
'''
tokeinizes the CFG line by line into the relevant tokens

lines: list of strings where each string is is a line from the
CFG.txt file

returns a list of lists of strings
'''
def tokenize_input(lines):
    result = []
    for i in lines:
        result.append(i.split())
    return result

'''
Normalizes a list of ints
'''
def normalize(relatives):
    length = sum(relatives)
    for i in range(len(relatives)):
        relatives[i] /= length
    return relatives


'''
Converts a CFG from the relative probabilities
given in the .txt file to the actual normalized probabilities
'''
def normalize_CFG(CFG):
    for i in CFG.keys():
        probabilities = []
        for j in CFG[i]:
            probabilities.append(int(j[1]))
        probabilities = normalize(probabilities)
        for j in range(len(CFG[i])):
            CFG[i][j] = CFG[i][j][0]
        CFG[i] = (CFG[i],probabilities)
    return CFG


'''
Creates a probabalistic context free grammar based
on the inputs given in the CFG.txt file
'''
def create_pCFG():
    file = open("CFG.txt","r")
    lines = file.readlines()
    CFG = defaultdict(list)
    sentences = tokenize_input(lines)
    for sentence in sentences:
        if sentence != []:
            CFG[sentence[0]].append((sentence[2:-2],sentence[-1]))
    CFG = normalize_CFG(CFG)
    return CFG

def no_upper(string):
    for j in string:
        if j.isupper():
            return False
    return True

def no_upper_in_list(strings):
    for i in strings:
        for j in i:
            if j.isupper():
                return False
    return True

'''
Helper function.
value list inserted into target list starting at index+1
'''
def insert_extend(index,target,value):
    itr = 0
    for i in range(index+1,index+len(value)+1):
        target.insert(i,value[itr])
        itr+=1
    return target

def pricing(string):
    if string[0] == "WEAPON":
        return 140
    elif string[0] == "WAND":
        return 80
    elif string[0] == "CONSUMABLE":
        return 20
    elif string[0] == "WEARABLE":
        return 125
    else:
        return 100

'''
Generates an item using a pCFG and a starter sentence called string. String's default value is ["S"] which is the default value to generate any item

NOTE: set price to have a different base value based on the weapons category.
E.G. weapons have a higher price_constant than consumables
Categories are defined as any sentence produced by "S"
'''
def generate_item(CFG,string):
    count = 0
    chance = 1
    if string != ["S"]:
        print("Incorrect starting sentence, should be 'S'")
        return
    for i in range(len(string)):
        if CFG[string[i]] != []:
            number = choice(len(CFG[string[i]][0]),p=CFG[string[i]][1]) #selects index based on probabilities determined from the relative probabilities
            if CFG[string[i]][1][number] < chance and CFG[string[i]][1][number] != 0.029411764705882353:
                chance = CFG[string[i]][1][number] #Sets chance to be the rarest option selected
            string = insert_extend(i,string,CFG[string[i]][0][number])#adds new sentence into the current sentence at the location
            string.pop(i) #delete the variable that was used to add the new sentence
    price_constant = pricing(string)
    while not no_upper_in_list(string):
        for i in range(len(string)):
            if CFG[string[i]] != []:
                number = choice(len(CFG[string[i]][0]),p=CFG[string[i]][1]) #selects index based on probabilities determined from the relative probabilities
                if CFG[string[i]][1][number] < chance and CFG[string[i]][1][number] != 0.029411764705882353:
                    chance = CFG[string[i]][1][number] #Sets chance to be the rarest option selected
                string = insert_extend(i,string,CFG[string[i]][0][number])#adds new sentence into the current sentence at the location
                string.pop(i) #delete the variable that was used to add the new sentence
        count +=1
    while "$" in string:
        string.remove("$") #removes null values from item
    #price_constant = 100 #Price can be increased or decreased by changing this value
    string.append("price: "+str(int(price_constant/chance)))
    return string

'''
Structure of pCFG

CFG['entry']: ([sentence,...],[probabilities,...])
'''
if __name__ == "__main__":
    CFG = create_pCFG()
    result = []
    for i in range(15):
        string = ["S"]
        temp = generate_item(CFG,string)
        if len(temp) > 2:
            result.append(temp)
    for i in result:
        print(i)
    
