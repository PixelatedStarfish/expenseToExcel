#Since this code was written to parse an expense report of a webpage.
#I think you should get to see what my code actually does with your info.
#It is designed to takes the text off a webpage, filter out web artifacts,
#and output the table from the webpage as a spreadsheet compatible .csv file.
#No funny business: no accounts, no tracking, no selling
CSV = ""

def parse(l, ignore = []):
    #print(lines)
    out = []
    l = l.replace(",", "") #commas are evil
        #print(l)
    l = lineSplitter(l)
    if l == None: #kip noise
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
    #print(line)
    if not line[0:1].isdigit():
        return None #no date field means noise
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

#tallies up the prices, with an array for ignoring specific substrings
def addup(lines):
    #assuming lines is whatever parse generates
    result = 0

    for line in lines:
        result += float(line[2]) #adds up prices
    out = round(result, 2) #rounding off noise form floating point math

    return out

def doFile(file, ignoreList = []):
    global CSV
    
    p = []
    for line in file.split("\n"):
        q = parse(line, ignoreList)
        if not q == None:
            p.append(q)
    p.append(["Total", "->", str(addup(p))])
    #print("\nFile", file + ":")
    #print()
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

    print("Paste your tables here to get a .csv file for a spreadsheet.\nLines that do not start with a digit will be ignored to filter out noise.\nEnter a double colon \"::\" to continue.\n>\n")
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
    print("Written to 'out.csv' for importing to excel")

main()
