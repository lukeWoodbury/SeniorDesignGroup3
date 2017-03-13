def returnsequences(file, val):
    newline = None
    with open(file,"r") as json_file:
        line = json_file.readline()
        wordlist = line.split()
        for i in range(len(wordlist)):
            if wordlist[i] == '"return_sequences":':
                wordlist[i + 1] = val + ','
        newline = ' '.join(wordlist)
        
    with open(file,"w") as json_file:
        json_file.write(newline)

def consumeless(file,val):
    newline = None
    with open(file,"r") as json_file:
        line = json_file.readline()
        wordlist = line.split()
        for i in range(len(wordlist)):
            if wordlist[i] == '"consume_less":':
                wordlist[i + 1] = '"' + val + '",'
        newline = ' '.join(wordlist)
        
    with open(file,"w") as json_file:
        json_file.write(newline)

def stateful(file,val):
    newline = None
    with open(file,"r") as json_file:
        line = json_file.readline()
        wordlist = line.split()
        for i in range(len(wordlist)):
            if wordlist[i] == '"stateful":':
                wordlist[i + 1] = val + ','
        newline = ' '.join(wordlist)
        
    with open(file,"w") as json_file:
        json_file.write(newline)

##Examples
##returnsequences('model.json', 'true')
##
##consumeless('model.json', 'cpu')
##
##stateful('model.json', 'true')




