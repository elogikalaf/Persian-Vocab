import sys
import io
from os import system, name
import re


#LISTS OF DESIRED CHANGES IN THE THIS VERSION:
# edit distance between the two input words should be calculated before they're filtered
# fixed the issue in which when the user called the wordlist function it always prewrote the results into a string in order to write it\
        # to the output file. this issue caused a delay.
# use regex instead of the previous mess in the filtered function 




# Handle Persian Characters IO (I DON'T KNOW HOW IT REALLY WORKS I JUST COPY-AND-PASTED IT,
# It's Related to the Standard Output/Input Encoding of the Program)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Define the Class That Shapes the Vocabulary
class Vocab:
    def __init__(self, content):
        self.content = content
        self.dic = {}

    # Replace Non-Standard Characters
    def replace(self):
        # \n and other types of spaces are replaces with regular spaces so that they can be seperated later on too 
        dic_replace = {"ئ":"ی", "ؤ":"و", "ي":"ی", "ۀ":"ه", "ك":"ک", "أ":"ا", "إ":"ا", "\\n":" ", " ":" ", "\n":" ", "٬":" ", "َ":"", "ُ":"", "ِ":""} 
        # replaces no-break space with regular space, arabic letters with persian equivalants and line-break with space. fathe, kasre va zamme are removed too.
        for v, k in dic_replace.items():
            self.content = self.content.replace(v, k) # replaces the non-standard characters with their standard equivalent 
    
    # Filter Non-Standard Characters    
    def filtered(self):
        self.content = re.sub("[^ا-ی ‌آ]", " ", self.content) # everythhing excpet for persian letters and semi-space will be replaced with a space

    # Separate the Words
    def separate(self):
        persianwords = {}
        lst_seperatedwordsunclean = self.content.split() # words are seperated
        lst_seperatedwords = [i.strip("‌ \n") for i in lst_seperatedwordsunclean] # clear semi-spaces, spaces or new-lines from around the words
        for word in lst_seperatedwords:
            if persianwords.get(word) == None: # if the word hasn't been added before it gets add with the value of 1
                persianwords[word] = 1
            else:
                persianwords[word]+=1 # if the word has been added before its value gets increased by 1
        self.dic = persianwords # a dictionary, key = words and value = number of times repeated

    # Removes Stopwords
    def removestopwords(self):
        lst_stopwords = ["", " ", "و", "از", "در", " ", "", "\n", "اما", "آن", "ان", "او", "آی", "این", "اگر"
                        ,"بدون", "اما", "اینطور", "این‌طور", "آنطور", "آن‌طور", "انطور", "ان‌طور", "بر", "برای"
                        , "به", "بی", "تا", "را", "زیر", "سپس", "طور", "که", "هر", "همان","هیچ", "ولی", "پس"
                        , "چه", "چو", "چون", "این‌ها", "آن‌ها", "ان‌ها", "یا", "با", "هم"]

        for stopword in lst_stopwords:
            if stopword in self.dic:
                self.dic.pop(stopword) #Stopwords get removed from the dictionary

    # Delete an Item
    def deleteitem(self, word):
        if word in self.dic:
            # removes the word from the dictionary
            self.dic.pop(word)
            # you need to sort again because a word has been removed
            self.alphabeticalsort()
            self.topwordssort()
            return(f"the word '{word}' was deleted from the vocabulary")
        else:
            return(f"the word '{word}' doesn't exist")

    # Sorts all the words alphabetically
    def alphabeticalsort(self):
        self.alphabeticalwordlist = sorted(list(set(self.dic.keys()))) # makes an alphabetical list of all words  

    # Return Words That Have Been Sorted Alphabetically
    def wordlist(self):
        for i in self.alphabeticalwordlist: 
            yield i

    # Sorts the words considering how common they are
    def topwordssort(self):
        self.toppersianwords = dict(sorted(self.dic.items(), key = lambda i: i[1], reverse = True)) #sortes the dict based on the commonness of words

    #returns the n most common words
    def topwords(self, n):
        lst_topwrods = list(self.toppersianwords.keys()) 
        if n == "all": # if the user input is all, yields all words
            for i in lst_topwrods:
                yield i
        else: #if its a number returns the number of common words requested
            if len(lst_topwrods)>int(n)>0:
                for i in range(int(n)):
                    yield lst_topwrods[i]
            elif int(n)<0:
                yield("not valid. should be bigger than 0")
            elif int(n)>len(lst_topwrods):
                yield("not valid. too big.")

    #Search for a Word and Add It If It's Not Already
    def search(self, word):
        # Standarizes the seach key before the search
        dic_replace = {"ئ":"ی", "ؤ":"و", "ي":"ی", "ۀ":"ه", "ك":"ک", "أ":"ا", "إ":"ا"}
        for u, k in dic_replace.items():
            word = word.replace(u, k) #replaces the non-standard characters in the search input 
        list_filteredchars = [" ", "‌", "\n", "ژ", "آ"] # space, semi-space, line-break, zhe, and a ba kolah
        for i in word:
            if not (("ا" <= i <= "ی") or (i in list_filteredchars)): # if the characters are not standard they'll be replaces with a space
                word = word.replace(i, "")
        if word:
            if word not in self.dic:
                self.dic[word] = 1
                result = (f"the word '{word}' was added to the vocabulary")
                # you need to sort again because a new word has been added
                self.topwordssort()
                self.alphabeticalsort()
            else:
                result = f"the word '{word}' exists and it's been repeated {self.dic[word]} times"
            return(result)
        else:
            return("seach key is not valid, use standard characters")

    #Calculate the Edit Distance Between Two Words and Add Them to the Vocabulary If They're Not Added Already
    def editDistance(self, first, second):
        if len(first) > len(second): # the first word should be shorter
            first, second = second, first
        if len(first) == 0: # if the first word doesn't exist the edit distance = length of the second word
            return (len(second))
        # if the last letters are the same execute the function again but with the last letter removed
        if first[-1] == second[-1]: 
            return (self.editDistance(first[:-1], second[:-1]))
        else: # what's the most efficent way to turn first word to the second word?
            return (1 + min(
                    self.editDistance(first[:-1], second[:-1]) # replace a letter
                    , self.editDistance(first[:-1], second[:]) # remove a letter
                    , self.editDistance(first[:], second[:-1]) # insert a letter
                    ))

# clear the screen for better viewing
def clearscreen():
    if name == "nt": # use 'cls' if the user is on windows
        system("cls")
    else: # use 'clear' if the user is on mac/linux
        system("clear")

# reads the input file
def fileread():
    with open("Zoomit1.txt", "r", encoding="utf-8", errors="ignore") as theinput:
        return theinput.read()


# writes to the output file
def filewrite(written):
    with open("output.txt", "w", encoding="utf-8", errors="ignore") as theoutput:
        theoutput.write(written)

clearscreen()

def main():
    # Read the Input File and Store it In "Content"
#     str_userinputlocaiton = input("Put your input file at the same location as the code and name it 'Zoomit1.txt'.\
#  press Enter to continue, enter 0 if you want to stop the program.\n")
#     while (str_userinputlocaiton!=""): # if user presses Enter goes on with the code and reads the file
#         if str_userinputlocaiton == "0": # if the user presses 0 the program stops
#             sys.exit()
#         else:
#             clearscreen()
#             str_userinputlocaiton = input("Not Valid\nPut your input file at the same location as the code and name it 'Zoomit1.txt'.\
#  press Enter to continue, enter 0 if you want to stop the program.\n") # If the user inputs anything other he'll be prompted to input a valid response
    try: #checks if the input file exists or not
        content = fileread()
    except FileNotFoundError:
        print("'Zoomit1.txt' file doesn't exist")
        sys.exit() #stops the program if the input file doesn't `` exist
    ed = Vocab(content)
    ed.replace() #replaces the non-standard characters
    ed.filtered() #filters the remaining non-standard characters
    ed.separate() #seperates the words
    ed.removestopwords() #removes the stopwords
    ed.topwordssort()
    ed.alphabeticalsort()
    displayed = "" #the message that the user might see when he uses runs the program 
    useroptions = "" #user input
    written = "" #what gets written to the output file

    while (useroptions!="0"):
        clearscreen() #calls the clearscreen function to clear the screen for better viewing
        print(displayed, end="", flush=True) #displays a message if neccesary 
        displayed = ""
        useroptions = input("please put your file in the same location as the code and name it 'Zoomit1.txt'\
\nYou can save the Vocabulary for later use by going to the 'wordlist' section by inputting '3' and then saving\
 the result to the output file.\ninput '1' if you want to see the most common words.\
\ninput '2' if you want to search for a word.\ninput '3' if you want to \
see an alphabetical list of all words.\ninput '4' if you want to calculate the edit distance\
 between two words.\ninput '5' if you want to delete a specific word.\ninput '0' if\
 you want to end the program.\n")

        if useroptions == "1": #topwords
            written = ""
            isitstring = False # determines if the user input is a string or not
            doitquesiton = False # detemines if the uesr input is valid or not
            number = input("how many words do you want to be displayed?\
\nEnter 'all' to get all words sorted according to the number of times they've been repeated(descending).")
            try: # chekcs if the user input is a number or not
                int(number)
                isitstring = False
            except:
                isitstring = True
            if isitstring:
                if number != "all":
                    displayed = ("not valid\n")
                    doitquesiton = False # input is not valid
                else:
                    doitquesiton = True # input is valid
            elif isitstring == False:
                doitquesiton = True
            if doitquesiton: #input is valid and we can proceed
                printchecker = input("do you want the results printed? y/n\n")
                while (printchecker!="n"):
                    if printchecker == "y":
                        for i in ed.topwords(number): #prints the topwords
                            print(i) # prints the results
                        break
                    else: 
                        print("not valid")
                        printchecker = input("do you want the results printed? y/n\n")
                # for i in ed.topwords(number):
                #     written = written + i + "\n" #creates 'written' for saving it in the output file
                written = written.strip("\n")
                writechecker = input("do you want the results saved in the output file? y/n\n")
                while (writechecker!="n"):
                    if writechecker == "y":
                        for i in ed.topwords(number):
                            written = written + i + "\n" #creates 'written' for saving it in the output file
                        written = written.strip("\n")
                        filewrite(written)
                        break
                    else:
                        print("not valid")
            
        elif useroptions == "2": #search
            key = input("enter your search key. it will be standardized.\n")
            written = ed.search(key)
            print(written)
        
        elif useroptions == "3": #wordlist
            written = ""
            printchecker = input("do you want the results printed? y/n\n")
            while (printchecker!="n"):
                if printchecker == "y":
                    for i in ed.wordlist():
                        print(i)
                    break
                else:
                    print("not valid")
                    printchecker = input("do you want the results printed? y/n\n")
            writechecker = input("do you want the results saved in the output file? y/n\n")
            while (writechecker!="n"):
                if writechecker == "y":
                    for i in ed.wordlist():
                        written = written + i + "\n"
                    written = written.strip("\n")
                    filewrite(written)
                    break
                else:
                    print("not valid")
        
        elif useroptions == "4": #editdistance
            first = input("enter your first word. it will be standardized.\n")
            second = input("enter your second word. it will be standardized.\n")
            result = ""
            written = f"the edit distance between {first} and {second} is {ed.editDistance(first, second)}"
            print(written)
            dic_replace = {"ئ":"ی", "ؤ":"و", "ي":"ی", "ۀ":"ه", "ك":"ک", "أ":"ا", "إ":"ا"}
            for u, k in dic_replace.items():
                first = first.replace(u, k) #replaces the non-standard characters in the search input 
                second = second.replace(u, k)
            list_filteredchars = [" " , "‌", "\n", "ژ", "آ"] # space, semi-space, line-break, and a ba kolah
            for i in first:
                if not (("ا" <= i <= "ی") or (i in list_filteredchars)): # if the characters are not standard they'll be removed
                    first = first.replace(i, "")
            for i in second:
                if not (("ا" <= i <= "ی") or (i in list_filteredchars)): # if the characters are not standard they'll be removed
                    second = second.replace(i, "")
            if first:
                if first not in ed.dic:
                    ed.dic[first] = 1
                    result+=(f"the word '{first}' was added to the vocabulary\n")
                    # you need to sort again because a new word has been added
                    ed.topwordssort()
                    ed.alphabeticalsort()
            if second:
                if second not in ed.dic:
                    ed.dic[second] = 1
                    result+=(f"the word '{second}' was added to the vocabulary\n")
                    # you need to sort again because a new word has been added
                    ed.topwordssort()
                    ed.alphabeticalsort()
            print(result.strip("\n"))
       
        elif useroptions == "5": #delete
            deletedword = input("enter the word you want removed\n")
            written = ed.deleteitem(deletedword)
            displayed = written + "\n" # written will be displayed in the next loop of the while
     
        else:
            displayed = "Enter a Valid Input!\n" #this will be displayed in the next loop of the while
        
        clearscreen()

# Run The Main Function
if __name__ == "__main__":
    main()





