#!/usr/bin/python3
# NAME: Michelle Goh
# NetId: mg2657
#
#*This program will behave like a bash-like macroprocessor that
#* prompts for and reads lines from the standard input,
#* performs the variable expansions, and
#* writes the expanded command to the standard output.
#
#
#!/usr/bin/python3
import sys
import os
import re
# os.environ

# takes in string and determines where it contains
# valid $. Returns index
def containsDollar (arg):
    while "\\\\" in arg:
        arg = arg.replace("\\\\","``",1) # replace even backslashes with ''
    while "\$" in arg:
        arg = arg.replace("\$","``",1) # escape dollar sign
    if "$" in arg:
        return arg.index("$") # valid arg
    else:
        return None

# get index of char before valid closing bracket
# error-check for uneven brackets
def getCloseIndex (arg):
    while "\\\\" in arg:
        arg = arg.replace("\\\\","``",1)
    while "\{" in arg:
        arg = arg.replace("\{","``",1)
    while "\}" in arg:
        arg = arg.replace("\}","``",1)
    bracketCount = 1
    index = 0 
    for char in arg:
        if char == '{':
            bracketCount += 1
        else:
            if char == '}':
                bracketCount -= 1
        if bracketCount == 0:
            return index;
        index += 1
    return None

# find where NAME ends
def getEndOfName (arg):
    nameEnd = re.search('\W', arg) # check for = or -
    if nameEnd == None:
        return len(arg) # return len(arg) if just name
    else:
        return arg.index(nameEnd.group(0))

# check if valid NAME
def isValidName (name):
    reName = re.search(r"(?<=^)[_a-zA-Z]+\w*", name)
    if reName is None:
        return False
    if reName.group(0) != name: #other nonalphanumeric chars in name
        return False
    if "$" in name or " " in name or "}" in name or "{" in name:
        return False
    else:
        return True

# get command based off number
# $D and ${N}
def getArg (number):
    try:
        arg = sys.argv[number]
        return parseString(arg)
    except IndexError:
        return ""

# get VALUE given NAME from os.environ
def getValue (key):
    try:
        return os.environ[key]  
    except KeyError:
        return None

# $*, get all commands
def getAllArgs ():
    buildString = ""
    for i in range (1, len(sys.argv)):
        buildString += sys.argv[i]
        buildString += " "
    return parseString(buildString[:-1])

# expand statements within braces
def expandBrackets (arg):
    endIndex = getCloseIndex(arg[1:])
    if (endIndex is None):
        return None
    else:
        endIndex += 1 # index of closing brace

    # ${N}
    if arg[1].isdigit():
        number = int(arg[1:endIndex])
        return {"expanded":getArg(number),"spanIndex": endIndex+2}
    
    # ${NAME=VALUE}, #{NAME-VALUE} or #{NAME}
    sequence = arg[1:endIndex]

    # split according to = or -
    sepEqual = sequence.split('=')
    sepDash = sequence.split('-')

    # ${NAME}
    if len(sepDash) == 1 and len(sepEqual) == 1:
        if isValidName(sequence) == False:
            return None
        value = getValue(sequence)
        if value != None: 
            return {"expanded":getValue(sequence),"spanIndex":endIndex + 2}
        return {"expanded":"","spanIndex":endIndex + 2}
    
    # {NAME-VALUE}
    if (len(sepDash[0]) < len(sepEqual[0])):
        name = sepDash[0]
        if isValidName(name) == False:
            return None
        dashIndex = sequence.index("-") + 1
        word = sequence[dashIndex:endIndex]
        value = getValue(name)
        # if NAME is defined, suppress WORD expansion/errors
        if value != None:
            return {"expanded":value,"spanIndex":endIndex + 2} 
        # expand WORD
        expanded = parseString(word)
        return {"expanded":expanded,"spanIndex":endIndex + 2}
    
    else: # {NAME=VALUE}
        name = sepEqual[0]
        if isValidName(name) == False:
            return None
        equalIndex = sequence.index("=") + 1
        word = sequence[equalIndex:endIndex]
        value = getValue(name)
        if value != None:
            return {"expanded":value,"spanIndex":endIndex +2}
        else:
            expanded = parseString(word)
            os.environ[name] = expanded
            return {"expanded":expanded,"spanIndex":endIndex +2}

# expands arg. Writes expanded in front of 
# statements that are expanded. spanIndex indicates
# up to which index the arg was expanded
def expand (arg):
    if (len(arg) == 1): # just dollar sign
        return {"expanded":arg,"spanIndex":1}
    
    if (arg[1].isdigit()): # $D
        endIndex = 1
        number = int(arg[1])
        return {"expanded":getArg(number),"spanIndex":2}
    
    if (arg[1] == '{'): # ${...
        return expandBrackets(arg[1:])
    
    if (arg[1] == '*'): # $*
        return {"expanded":getAllArgs(),"spanIndex":2}
    
    if(arg[1].isalpha()) or (arg[1]=="_"): # $NAME
        endIndex = getEndOfName (arg[1:]) + 1
        expanded = getValue(arg[1:endIndex])
        if expanded != None:
            return {"expanded":expanded,"spanIndex":endIndex}
        return {"expanded":"","spanIndex":endIndex}
    
    else: #just chars after $
        return {"expanded":arg, "spanIndex": len(arg)}

# parses string by deciding which parts to expand,
# and which parts to ignore. Returns None if error
# encountered
def parseString (line):
    line = line.replace('\n','') # remove new line char
    buildLine = ""
    currentIndex = 0; # index of line
    
    while (currentIndex != len(line)):
        repIndex = containsDollar(line[currentIndex:]) # index to start expansion
        if  repIndex!= None:
            buildLine += line[currentIndex:currentIndex + repIndex] # text before $
            expansion = expand(line[currentIndex + repIndex:])
            if expansion ==  None:
                return None
            # increment current index by previous indices and expanded index
            currentIndex = currentIndex + repIndex + expansion["spanIndex"] 
            # add expansion to result line
            expanded = expansion["expanded"]
            buildLine += expanded
        else:
            buildLine += line[currentIndex:]
            break
    return buildLine

# main function to prompt lines to expand and
# catch ctrl+d / ctrl+c
if __name__ == "__main__":
    numCmd = 1
    try:
        sys.stdout.write("("+str(numCmd)+")$ ")
        sys.stdout.flush()
        for line in sys.stdin:
            if line.isspace():
                sys.stdout.write("("+str(numCmd)+")$ ")
                sys.stdout.flush()
                continue
            buildLine = parseString(line)
            if (buildLine != None):
                if line[-1] != '\n':
                    print(">> " + buildLine, end = '')
                else:
                    print(">> " + buildLine)
                numCmd = numCmd + 1
            else:
                sys.stderr.write("invalid expansion\n")
                sys.stdout.write("("+str(numCmd)+")$ ")
                sys.stdout.flush()
                continue
            if line[-1] != '\n':
                print("("+str(numCmd)+")$ ")
                exit(0) 
            sys.stdout.write("("+str(numCmd)+")$ ")
            sys.stdout.flush()
    except (KeyboardInterrupt):
        print("")
        exit(1)
    print("") 
    exit(0)     
