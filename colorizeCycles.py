#!/usr/bin/env python3

"""
done by Julien Deantoni under EPL license on the 15th of May, 2018
"""

import sys
from os import path, access, R_OK
import networkx as nx
import re

def findCycles(pathToDot):
    longest=[]
    shortest=[]
    shortest.extend(range(1, 1000))
    print("    loading the graph")
    # read in the specified file, create a networkx DiGraph
    theGraph = nx.DiGraph(nx.nx_pydot.read_dot(pathToDot))
    allCycles = nx.simple_cycles(theGraph)
    numberOfCycle=0
    print("    enumerating cycles")
    for aCycle in allCycles:
        numberOfCycle = numberOfCycle +1
        if (numberOfCycle % 10000 == 0):
            sys.stdout.write('number of cycle computed: {}'.format(numberOfCycle)+chr(13))
        if (len(aCycle) < 2):
            continue
        if (len(aCycle) < len(shortest)):
            shortest=aCycle
        if (len(aCycle) > len(longest)):
            longest=aCycle
        if(numberOfCycle > 4000000):
            print("############# number of cycles computed > 4 000 000, stopping at {}".format(4000000))
            break
    return shortest,longest


def replaceAllLines(initialDot, resultingDotPath, newColor, linesToChange):
    with open(resultingDotPath, 'w') as res:
        with open(initialDot) as fp:  
            line = fp.readline()
            while line:
                changeDone=0
                if (line in linesToChange):
                    #print("change Done")
                    lineChanged=re.sub("penwidth=\"1\"", "penwidth=\"14\"", line)
                    lineChanged=re.sub("0000ff", "ff00ff", lineChanged)
                    lineChanged=re.sub("ff0000", "ff00ff", lineChanged)
                    lineChanged=re.sub("aaaaaa", newColor, lineChanged)
                    changeDone=1
                    res.write(lineChanged)
                else:
                    res.write(line)
                line = fp.readline()
                
def replaceAllLinesForStates(initialDot, resultingDotPath, newColor, linesToChange):
    with open(resultingDotPath, 'w') as res:
        with open(initialDot) as fp:  
            line = fp.readline()
            while line:
                if (line in linesToChange):
                    #print("change Done")
                    lineChanged=re.sub("fillcolor=\"#ff0000\"", "fillcolor=\"#ff00ff\"", line)
                    lineChanged=re.sub("fillcolor=\"#0000ff\"", "fillcolor=\"#ff00ff\"", line)
                    lineChanged=re.sub("fillcolor=\"#ffffff\"", "fillcolor=\""+str(newColor)+"\"", line)
                    lineChanged=re.sub(r"label=\".*", "label=\"\"];", lineChanged)
                    res.write(lineChanged)
                else:
                    res.write(line)
                line = fp.readline()


def collectLinesToChange(dotFilePath, cycle, alreadyComputedLinesToChange):
    linesToChange=alreadyComputedLinesToChange
    initialState=cycle[0]
    i=cycle[0]
    toRedo=0
    with open(dotFilePath) as fp:  
        line = fp.readline()
        while line:
            #index=0
            for j in cycle:
                #print(r"^"+str(i)+" -> "+str(j)+" .*")
                #print(line)
                if re.match(r"\t"+str(i)+" -> "+str(j)+" .*", line):
                    if line not in linesToChange:
                        #print("line to change {} -> {}".format(i,j))
                        linesToChange.append(line)
                        toRedo=1
                        break
                i=j
                #index=index+1
            if re.match(r"^"+str(i)+" -> "+str(initialState)+" .*", line):
                if line not in linesToChange:
                    #print("line to change2{} -> {}".format(i,initialState))
                    linesToChange.append(line)
                    toRedo=1
            line = fp.readline()
    #print(cycle)
    #print("toRedo={}".format(toRedo))
    return toRedo, linesToChange

def collectLinesToChangeForStates(dotFilePath, cycle):
    linesToChange=[]
    with open(dotFilePath) as fp:  
        line = fp.readline()
        while line:
            #index=0
            for j in cycle:
                #print(r"^"+str(i)+" -> "+str(j)+" .*")
                #print(line)
                if re.match(r"\t"+str(j)+" \[fillcolor=.*", line):
                    if line not in linesToChange:
                        #print("line to change {} -> {}".format(i,j))
                        linesToChange.append(line)
                        break
                i=j
            line = fp.readline()
    #print(cycle)
    #print("toRedo={}".format(toRedo))
    return linesToChange


def printSchedule(scheduleLines):
    for line in scheduleLines:
        lineChanged=re.sub(r".*label=\"\[", "", line)
        lineChanged=re.sub(r"\]\"];", "", lineChanged)
        #print(lineChanged, end="")


def dotCleanup(dotSource, dotCleaned):
    with open(dotCleaned, 'w') as res:
        with open(dotSource) as fp:  
            line = fp.readline()
            while line:
                if re.match(r".*label=\".*", line):
                            lineChanged = re.sub(r"(.*label=\").*", r"\1", line)
                            lineChanged = lineChanged.rstrip('\n') + "\"];\n"
                            lineChanged = re.sub("style=\"solid\",", "arrowsize=0.1, size=\"0.1\", style=\"solid\",", lineChanged)
                            lineChanged = re.sub("size=\"10\", shape=\"circle\"", "shape=\"point\"", lineChanged)
                            lineChanged = re.sub("penwidth=\"14\",", "penwidth=\"3\",", lineChanged)
                            #print(lineChanged)
                            line = lineChanged
                res.write(line)
                line = fp.readline()


def usage():
    sys.stderr.write("colorizeCycle.py by Julien Deantoni \n")
    sys.stderr.write("  finds shortest and longest cycles in dot file graphs and colorize them, the result is given in a new dot\n\n")
    sys.stderr.write("create also a cleaned dot, i.e., without any label, more suitable to sfdp layout\n")
    sys.stderr.write("USAGE: colorizeCycle.py file.dot\n")

#Main


dotToColorize= ""
if (len(sys.argv) > 1):
    dotToColorize = sys.argv[1]
else:
    usage()
    sys.exit(1)

print("start looking for cycles")
shortestCycle,longestCycle=findCycles(dotToColorize)

print("\n")
print('cycles found: \n shortest {} \n longest {}'.format(shortestCycle,longestCycle))

print('start collecting line to change for shortest path')
toRedo,shortestLinesToChange=collectLinesToChange(dotToColorize, shortestCycle, [])
while toRedo == 1:
    toRedo,shortestLinesToChange=collectLinesToChange(dotToColorize, shortestCycle,shortestLinesToChange)
print("collect shortest done, number of line to change: {}".format(len(shortestLinesToChange)))

print('start replacing lines for shortest path')
replaceAllLines(dotToColorize, 'intermediateresult_'+dotToColorize, '0000ff', shortestLinesToChange)
shortestlinesToChangesForState=collectLinesToChangeForStates('intermediateresult_'+dotToColorize, shortestCycle)
replaceAllLinesForStates('intermediateresult_'+dotToColorize, 'intermediateresult2_'+dotToColorize, '0000ff', shortestLinesToChange)


print('start collecting line to change for longest path')
toRedo,longestLinesToChange=collectLinesToChange('intermediateresult2_'+dotToColorize, longestCycle, [])
while toRedo == 1:
    toRedo,longestLinesToChange=collectLinesToChange('intermediateresult2_'+dotToColorize, longestCycle,longestLinesToChange)
print("collect longest done, number of line to change: {}".format(len(longestLinesToChange)))

print('start replacing lines for shortest path')
replaceAllLines('intermediateresult2_'+dotToColorize, 'intermediateresult3_'+dotToColorize, 'ff0000', longestLinesToChange)
shortestlinesToChangesForState=collectLinesToChangeForStates('intermediateresult3_'+dotToColorize, shortestCycle)
replaceAllLinesForStates('intermediateresult3_'+dotToColorize, 'result_'+dotToColorize, '0000ff', shortestLinesToChange)

dotCleanup('result_'+dotToColorize, 'result_cleaned_'+dotToColorize)

print("######################\n shortest schedule\n######################")
printSchedule(shortestLinesToChange)
print("######################\n")

print("######################\n longest schedule\n######################")
printSchedule(longestLinesToChange)
print("######################")

