
def checkData():
    print("start printing")
    for w in wordsClean[:20]:
        print(w)
    print("--------")


def checkDups():
    numDups = 0
    print("Checking and printing duplicates...")
    for i in range(len(wordsClean)-1):
        if wordsClean[i] == wordsClean[i+1]:
            print(wordsClean[i])
            numDups = numDups + 1
    print("Total duplicates above: {}".format(numDups))


def createSignature():
    for myWord in wordsClean:
        #print("{} - {}".format(myWord, sorted(list(myWord))))
        wordsSignature[myWord] = sorted(list(myWord))

    # print(wordsSignature)


def listCompare(list1, list2):
    if len(list1) != len(list2):
        return False

    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False

    return True


def findAnagram(myWord):
    myWordSign = sorted(list(myWord.lower()))
    print(" ")
    print("Looking for anagram of \"{}\"  ".format(myWord))
    flag = False

    for k, v in wordsSignature.items():
        if k == myWord:
            continue
        if listCompare(v, myWordSign):
            print("Anagram found : {}".format(k))
            flag = True

    if not(flag):
        print("No anagram found for \"{}\" ".format(myWord))


def getCustomLists():
    for w in wordsClean:
        l = len(w)
        if l == 6:
            list6.append(w)
        elif l == 7:
            list7.append(w)
        elif l == 8:
            list8.append(w)

    print(list6[:10])


def findAnagramFromLists(listX):
    for word in listX:
        findAnagram(word)


wordFile = open("words.txt", "r")
words = wordFile.readlines()
wordsClean = sorted(
    set([word.strip().lower().replace("'", "") for word in words]))

# checkDups()
# checkData()

wordsSignature = {}
createSignature()

findAnagram("anagram")
print("====================")
print("====================")
print("====================")

list6 = []
list7 = []
list8 = []

getCustomLists()
findAnagramFromLists(list6)
