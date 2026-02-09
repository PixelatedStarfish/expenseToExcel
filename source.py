#Since this code was written to parse an expense report of a webpage.
#I think you should get to see what my code actually does with your info.
#It is designed to takes the text off a webpage, filter out web artifacts,
#and output the table from the webpage as a spreadsheet compatible .csv file.
#No funny business: no accounts, no tracking, no selling
CSV = ""

def charFilter(s):
    banned = ",=|" #reserved chars are deleted from the file

    for c in banned:
        s = s.replace(c, " ")

    s = s.replace("/", "-")#all dates get '-' as delimiter
    return s
    

def parse(l, ignore = []):
    out = []
    l = charFilter(l)
        #print(l)
    l = lineSplitter(l)
    if l == None or l[0] == "<>": #skip noise and stuff marked "<>" 
        return
    if not ignores(l[1], ignore):
        liner = []
            
        for f in l:
            f = f.strip()
            out.append(f)
    return out

def ignores(line, ignore):
    for i in ignore:
        if i in line:
            return True #ignore
    return False

def lineSplitter(line):
    if (not '-' in line[0:7]): #dates get a '-' as a delimiter. 
        return None #no date field means noise

    try:
        dateSliceEnd = 0
        priceSliceStart = len(line) -1

        while line[dateSliceEnd] != " ":
            dateSliceEnd += 1
        
        while line[priceSliceStart] != " ":
            priceSliceStart -=1

        slicer1 = line[0:dateSliceEnd]
        slicer2 = line[dateSliceEnd:priceSliceStart]
        slicer3 = line[priceSliceStart:len(line)]


        return [slicer1, slicer2, slicer3]
    except IndexError:
        return None #if some gobbledygook starts with a digit, prevent a crash 

#tallies up the prices, with an array for ignoring specific substrings
def addup(lines):
    #assuming lines is whatever parse generates
    result = 0

    for line in lines:
        #print(line)
        try:
            result += float(line[2]) #adds up prices
        except ValueError:
            print("Bad parse on \"" + line[2] + "\". Format table rows with DATE, TRANSACTION, PRICE")
            exit(1)
    out = round(result, 2) #rounding off noise form floating point math

    return out

def doFile(file, ignoreList = []):
    global CSV
    
    p = []
    for line in file.split("\n"):
        q = parse(line, ignoreList)
        if not q == None:
            p.append(q)
    p.append(["Total", "  ", str(addup(p))])
    delim = "\t"
    for line in p:
        print(line[0] + delim + line[1] + delim + line[2])
        CSV += line[0]+","+line[1]+","+line[2]+"\n"

    ignoreString = "\nNothing Ignored"
    if len(ignoreList) > 0:
        ignoreString = "\nIgnoring: "
        for i in ignoreList:
            ignoreString += i + ',  '

def multiInput():
    #s = "1/1 LUCKYLAND PLAYINGCARDS NT 1,001.23"

    print("Paste your tables here to get a .csv file for a spreadsheet."\
          + "\nLines that do not start with a digit will be ignored to filter out noise."\
          + "\nPlease note that each row of a table needs to be formatted as:"\
          +"\nDATE, TRANSACTION, PRICE\n"\
          +"with space between fields."\
          +"\nEnter a double colon \"::\" to continue.\n>")
    contents = []
    while True:
        try:
            line = input()
            if line.strip() == "::":
                break
        except EOFError:
            break
        contents.append(line)
    s = ""
    for line in contents:
        s = s + (line + "\n")
    return s

def main():
    doFile(multiInput())
    

    global CSV
    f = open("out.csv", "w")
    f.write(CSV)
    f.close()
    print("Table written to 'out.csv' for importing to a spreadsheet.")

main()
