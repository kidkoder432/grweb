import heapq, pathlib, os
os.chdir(pathlib.Path(__file__).parent.absolute())
RAGAS = []
NOTES = list('SRGMPDNrgmdn')
f = open('raga-index.txt')
c = str(f.read())
for x in c.split('\n'):
    if x:
        RAGAS.append(x[:x.index(':')])
def tri(n): #triangular number calculator
    t = 0
    for i in range(n, n-6, -1):
        t += i
    return t
def loadDictionary(): # open raga database
    dictionaryFile = open("raga-index.txt")
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = 0
    dictionaryFile.close()
    return englishWords    
def getRagas(message, threshold=0.5, joiner=' or '): # guessing code
    SAPTAKS = loadDictionary()
    for x in range(1, 6):
        for i in range(len(message) - x + 1):
            for saptak in list(SAPTAKS.keys()):
                if ''.join(message[i:i + x]) in saptak[saptak.index(': '):]:
                    SAPTAKS[saptak] += 1
                    # print(''.join(message[i:i + x]), saptak)
                elif x == 1:
                    del SAPTAKS[saptak]
                    # print('Deleted %s' %(saptak))
    # g = heapq.nlargest(1, SAPTAKS, SAPTAKS.get)
    # return joiner.join(g)
    # print(g)
    # print([SAPTAKS[x] for x in g])    
    guesses = []           
    keys = list(SAPTAKS.keys())
    for guess in keys:
        # print(guess, SAPTAKS[guess] / tri(len(message)))
        if SAPTAKS[guess] / tri(len(message)) >= threshold and guess in heapq.nlargest(1, SAPTAKS, SAPTAKS.get):
            guesses.append(guess[:guess.index(':')])
    guesses = joiner.join(guesses)        
    return guesses


def main():   # main interface
    phrase = input('Enter a phrase and I will guess what raga it is in! > ')  
    threshold = 0.5 # threshold at which guesser algorithm starts guessing ragas
    if len(phrase) == 0:
        return 'Your phrase is empty.'
    for note in phrase:
        if note not in 'SrRgGMmPdDnN- ':
            return 'Your phrase has a letter which is not a note. Please reenter your phrase.'
    while '-' in phrase:
        phrase.replace('-', '')
        
    if len(phrase) < 5:
        return 'Your phrase is too short. Please enter a longer phrase.'
    guesses = getRagas(phrase, threshold, '/')
    if guesses:
        print('I think your phrase is a ' + guesses + ' phrase.')
    else:
        print('I\'m not sure which raga your phrase is in.')

if __name__ == '__main__':
    while True:
        print(main())