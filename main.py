import sys
import yaml
import json
import random
from pprint import pprint
from os import walk
from Tkinter import *

print "Running"


UNIQUE_TEAMS = 6

colors = ['red','green','blue','yellow','orange','magenta']

# Globals for graph data
winHeight = 0
winWidth = 0

#########################################
# State of graphs for saving/workspaces #
#########################################
class State:
    def __init__(self):
        self.graphCount = 1
        self.teams = [0]*UNIQUE_TEAMS
        self.graphs = ["Tele High Goal"]*self.graphCount
    def addGraph(self):
        if (self.graphCount < 4):
            self.graphCount += 1
            self.graphs.append("Tele High Goal")
    def removeGraph(self, index=-1):
        if (index == -1):
            index = self.graphCount - 1
        if (index > 0 and index < 4):
            print "Popping"
            self.graphCount -= 1
            self.graphs.pop(index)
    def loop(self):
        for i in range(self.graphCount):
            self.graphs[i] = graphDropdown[i].get()

######################
# Configuration file #
######################
def loadConfigFile():
    try:
        configData = yaml.load(open("config.yaml"))
        matchCount = configData['matchCount']
        for i in range(len(configData['graphs'])):
            if configData['graphs'][i]['xTickCount'] == "matchCount":
                configData['graphs'][i]['xTickCount'] = matchCount
            masterGraphData[configData['graphs'][i]['name']] = configData['graphs'][i]
            graphList.append( configData['graphs'][i]['name'] )
        pprint(masterGraphData)
    except:
        print "Error: Invalid config file"
        sys.exit(1)

##############
# Parse JSON #
##############
def getFiles(path):
    return next(walk(path))[2]


def recurse(d, array, configData):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            array = recurse(v, array, configData)
        else:
            for i, data in enumerate(configData):
                if k == data:
                    array[i] = int(v)
                    break
    return array


def getMatchDataFromJson():
    arr = []

    # Load config
    configData = open("jsonConfig.txt").read().split('\n')

    jsonPath = "jsonFiles/"
    files = getFiles(jsonPath)
    files.sort()

    # Loop through all of the json files and convert them into a nice csv
    for f in files:
        js = json.load(open(jsonPath+f))
        arr.append(recurse(js, [0]*len(configData), configData))

    pprint(arr)
    return arr

######################
# Load the team data #
######################
def loadMatchData():
#    try:
        # Get the array from the JSONs
        data = getMatchDataFromJson()
        # Create all the teamList stuff
        for i in data:
            if i[0] not in teamList:
                teamList.append(i[0])

        print "Data:"
        pprint(data)

        # Create the teamList elements for matchData
        for i in teamList:
            teamMatches = {}
            for j in graphList:
                teamMatches[j] = {}
                teamMatches[j]['solid'] = []
                teamMatches[j]['dashed'] = []
            matchData[i] = teamMatches

        print "Team list: ",teamList
        # Looping through data/graphs
        for i in data:
            currentTeam = i[0]
            print i
            for j in graphList:
                currentGraph = matchData[currentTeam][j]
# Check if we are adding data to a graph that uses the match count
                if ( masterGraphData[j]['usesMatch'] == 1 ):
                    # Solid line
                    currentGraph['solid'].append( [ len(currentGraph['solid'])+1 , i[masterGraphData[j]['solidCol']] ] )
                    # Dashed line?
                    if ( masterGraphData[j]['dashCol'] != -1 ):
                        currentGraph['dashed'].append( [ len(currentGraph['dashed'])+1 , i[masterGraphData[j]['dashCol']] ] )
# Otherwise, do the math for match data (need to fix this for future games, but it works for now)
                else:
                    # Check if we need to make the empyt array for the graphData
                    if ( len(currentGraph['solid']) == 0 ):
                        currentGraph['solid'] = [0]*len(masterGraphData[j]['xCols'])
                    # Loop through xCols
                    for k in range(len(masterGraphData[j]['xCols'])):
                        currentGraph['solid'][k] += i[masterGraphData[j]['xCols'][k]]
                matchData[currentTeam][j] = currentGraph
#    except:
#        print "Error: Invalid match file"
#        sys.exit(2)

def drawTeam(canvas, graphName, minX, minY, maxX, maxY, teamNumber, yTicks, xTicks, color):
    # Offset each of the teams a little bit so that they don't overlap
    yOffset = 0
    if color == 'red':
        yOffset = -5
    elif color == 'green':
        yOffset = -3
    elif color == 'blue':
        yOffset = -1
    elif color == 'yellow':
        yOffset = 1
    elif color == 'orange':
        yOffset = 3
    elif color == 'magenta':
        yOffset = 5

    h_dist = (maxX-minX)/xTicks # Distance to move on X diff
    v_dist = (maxY-minY)/yTicks # Distance to move on Y diff

    # Loop through the solid lines
    lastPoint  = (minX,maxY+yOffset)
    for i in matchData[teamNumber][graphName]['solid']:
        newPoint = ( minX+i[0]*h_dist, maxY-i[1]*v_dist+yOffset  )
        if (lastPoint != (minX, maxY+yOffset)):
            canvas.create_line(lastPoint, newPoint, fill=color, width=3)
        lastPoint  = newPoint
    # Loop through the dashed lines
    lastPoint  = (minX,maxY+yOffset)
    for i in matchData[teamNumber][graphName]['dashed']:
        newPoint = ( minX+i[0]*h_dist, maxY-i[1]*v_dist+yOffset  )
        canvas.create_line(lastPoint, newPoint, fill=color, width=3, dash=(4,4))
        lastPoint  = newPoint


def drawGraph(canvas, state):
    # Draw the bounding boxes
    canvas.create_rectangle(0, 0, largeGraphDimensions[0], largeGraphDimensions[1], fill='black', outline='white')
    if state.graphCount > 1:
        canvas.create_rectangle(0, 0, largeGraphDimensions[0]/2, largeGraphDimensions[1], outline='white')
    if state.graphCount > 2:
        canvas.create_rectangle(0, largeGraphDimensions[1]/2, largeGraphDimensions[0], largeGraphDimensions[1], outline='white')

    # Better draw method
    xCount = 1
    if (state.graphCount != 1):
        xCount = 2
    yCount = (state.graphCount+1)/2
    for z in range(state.graphCount):
            j = z%2
            k = z/2

            currentGraph = state.graphs[j+k*2]
            print "Current Graph: ",currentGraph
# Added graph selectors
            if (k == 0):
                graphSelection[z].place(x = j*largeGraphDimensions[0]/2, y= k*largeGraphDimensions[1]/2)
            else:
                graphSelection[z].place(x = j*largeGraphDimensions[0]/2, y= (k+1)*largeGraphDimensions[1]/2-30)

            minX =  j   *largeGraphDimensions[0]/xCount+50
            maxX = (j+1)*largeGraphDimensions[0]/xCount-50
            minY =  k   *largeGraphDimensions[1]/yCount+50
            maxY = (k+1)*largeGraphDimensions[1]/yCount-75
            # Vertical line
            canvas.create_line(minX, minY, minX, maxY, fill='white')
            # Horizontal line
            canvas.create_line(minX, maxY, maxX, maxY, fill='white')
            # Horizontal ticks
            h_dist = (largeGraphDimensions[0]/xCount-100)/masterGraphData[currentGraph]['xTickCount']
            for i in range(masterGraphData[currentGraph]['xTickCount']):
                canvas.create_line( minX+h_dist*(i+1), maxY+10, minX+h_dist*(i+1), maxY, fill='white')
            # Vertical ticks
            v_dist = (largeGraphDimensions[1]/yCount-125)/(masterGraphData[currentGraph]['yTickCount']-1)
            for i in range(masterGraphData[currentGraph]['yTickCount']):
                canvas.create_line(j*largeGraphDimensions[0]/xCount+50,k*largeGraphDimensions[1]/yCount+v_dist*i+50,j*largeGraphDimensions[0]/xCount+40,k*largeGraphDimensions[1]/yCount+v_dist*i+50, fill='white')

            # Once the axis are drawn, graph the team
#def drawTeam(canvas, graphName, minX, minY, maxX, maxY, teamNumber, yTicks, xTicks, color):
            for i in range(len(teamVarsForDropdown)):
                drawTeam(canvas, currentGraph, minX, minY, maxX, maxY, int(teamSelection[i].get("1.0",'end-1c')), masterGraphData[currentGraph]['yTickCount'], masterGraphData[currentGraph]['xTickCount'], colors[i])

def drawComments(canvas, state):
    for i in range(UNIQUE_TEAMS):
        canvas.create_rectangle(windowDimensions[0]-commentsDimensions[0], commentsDimensions[1]*i, windowDimensions[0], commentsDimensions[1]*(i+1), fill=colors[i], outline='white')
        teamSelection[i].place(x=1000,y=commentsDimensions[1]*i+50)
        # Update the teams in the state for graphing
        state.teams[i] = int(teamSelection[i].get("1.0",'end-1c'))
    print "Teams: ",state.teams

def key(event):
    if event.char == event.keysym:
        print "Normal key press: %s" % event.char

    if event.char == 'w':
        print "Increasing"
        states[currentState].addGraph()
    elif event.char == 's':
        print "Decreasing"
        states[currentState].removeGraph()
    elif event.char == 'q':
        print "Exit!"
        sys.exit(0)

    for s in states:
        s.loop()
    drawGraph(canvas, states[currentState])
    drawComments(canvas, states[currentState])

matchCount = 6
matchData = {}
masterGraphData = {}
states = [State()]*9
currentState = 0
teamList = [0]
graphList = []

loadConfigFile()
loadMatchData()

print "TEAMLIST:",teamList

windowDimensions = (1024,660)
commentsDimensions = (224,windowDimensions[1]/6)
largeGraphDimensions = (800,windowDimensions[1])

root = Tk()
root.geometry("%dx%d" % windowDimensions)
root.title("Hazy Scout")
canvas = Canvas(root, width=windowDimensions[0], height=windowDimensions[1])
canvas.pack()

# Team number textEntry
teamVarsForDropdown = [StringVar(root) for var in colors]
teamSelection = [Text(root, width=5, height=1) for var in teamVarsForDropdown]
for i in teamSelection:
    i.insert(END,"0")
# Graph Selector
graphDropdown = [StringVar(root) for var in range(4)]
for i in range(4):
    graphDropdown[i].set(i+1)
graphSelection = [OptionMenu(root, var, *graphList) for var in graphDropdown]
for i in graphDropdown:
    i.set("Showed Up")

drawGraph(canvas,states[currentState])
drawComments(canvas,states[currentState])

root.bind_all('<Key>',key)
root.bind_class('Text', '<Return>', lambda e: None)
root.bind_class('Text', 'a', lambda e: None)
root.bind_class('Text', 'b', lambda e: None)
root.bind_class('Text', 'c', lambda e: None)
root.bind_class('Text', 'd', lambda e: None)
root.bind_class('Text', 'e', lambda e: None)
root.bind_class('Text', 'f', lambda e: None)
root.bind_class('Text', 'g', lambda e: None)
root.bind_class('Text', 'h', lambda e: None)
root.bind_class('Text', 'i', lambda e: None)
root.bind_class('Text', 'j', lambda e: None)
root.bind_class('Text', 'k', lambda e: None)
root.bind_class('Text', 'l', lambda e: None)
root.bind_class('Text', 'm', lambda e: None)
root.bind_class('Text', 'n', lambda e: None)
root.bind_class('Text', 'o', lambda e: None)
root.bind_class('Text', 'p', lambda e: None)
root.bind_class('Text', 'q', lambda e: None)
root.bind_class('Text', 'r', lambda e: None)
root.bind_class('Text', 's', lambda e: None)
root.bind_class('Text', 't', lambda e: None)
root.bind_class('Text', 'u', lambda e: None)
root.bind_class('Text', 'v', lambda e: None)
root.bind_class('Text', 'w', lambda e: None)
root.bind_class('Text', 'x', lambda e: None)
root.bind_class('Text', 'y', lambda e: None)
root.bind_class('Text', 'z', lambda e: None)
root.bind("<Return>", lambda e: "break")
root.mainloop()

sys.exit(0)
