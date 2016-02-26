import sys
#import Tkinter as tk
from Tkinter import *


UNIQUE_TEAMS = 6

# Globals for graph data
winHeight = 0
winWidth = 0
################
# Graph object #
################
class Graph:
# Initialize the graph instance
    def __init__(self):
        self.baseX = 0
        self.baseY = 0
        self.height = winHeight
        self.width = winWidth

        self.graphNumber = 0
        self.xTicks = 6 # Matches
        self.yTicks = 5 # Scores
    def __init__(self, graphCount=1, matchCount=6, initalGraph=0):
        if (graphCount > 4 or graphCount < 1):
            print "Fatal error, bad graph count"
            sys.exit(10)

        if graphCount/2 == 0:
            self.height = winHeight
            self.baseY = 0
        else:
            self.height = winHeight/2
            self.baseY = winHeight/2

        if graphCount%2 == 1:
            self.width = winWidth
            self.baseX = 0
        else:
            self.width = winWidth/2
            self.baseX = winWidth/2
        self.graphNumber = initalGraph # Which graph to display
        self.xTicks = matchCount # Matches
        self.yTicks = masterGraphData[initialGraph]['tickCount'] # Scores
        self.graphID = graphID # Used to tell the graph where it appears on the screen
# Draw the graph to the screen

    def draw(self,canvas):
        # Draw a bounding box around the entire graph instance
        canvas.create_rectangle(self.baseX, self.baseY, self.baseX+self.width, self.baseY+self.height)

#########################################
# State of graphs for saving/workspaces #
#########################################
class State:
    def __init__(self):
        self.graphCount = 1
        self.teams = [0]*UNIQUE_TEAMS
        self.graphs = [0]*self.graphCount
    def getGraphCount(self):
        return self.graphCount
    def getTeams(self):
        return self.teams
    def getGraphs(self):
        return self.graphs
    def addGraph(self):
        if (self.graphCount < 4):
            self.graphCount += 1
            self.graphs.append(0)
    def removeGraph(self, index=-1):
        if (index == -1):
            index = self.graphCount - 1
        if (index > 0 and index < 4):
            print "Popping"
            self.graphCount -= 1
            self.graphs.pop(index)

######################
# Configuration file #
######################
def loadConfigFile():
    try:
        configFile = open("config.txt",'r')
        readed = configFile.read().split("\n")[:-1]
        configFile.close()

        matchCount = eval(readed[0])
        readed = readed[1:]
        # Load all of the graph data
        for i in range(len(readed)):
            tempSplit = readed[i].split("\t")

            tempD = {}
            tempD['id']            = int(tempSplit[0]) # Numerical id of graph, used in Graph as graphNumber
            tempD['name']          =     tempSplit[1]  # Name of graph, displayed in dropdown
            tempD['tickCount']     = int(tempSplit[2]) # Count of ticks on the y-axis
            tempD['solidCol']      = int(tempSplit[3]) # Column in the CSV file of the line that will be solid
            tempD['dashCol']       = int(tempSplit[4]) # Column in the CSV file of the line that will be dashed

            masterGraphData.append(tempD)

    except:
        print "Error: Invalid config file"
        sys.exit(1)


######################
# Load the team data #
######################
def loadMatchData():
    try:
        matchFile = open("matches.csv",'r')
        readed = matchFile.read().split("\n")[1:-1]
        print "len: ",len(readed)
        matchFile.close()

        # Sort the data from the teams by team/match number for easier graphing
        tempR = readed.split(",")
        while len(tempR) != 0:
            minIndex = 0
            minTeam = 0
            minMatch = -100
            for i in range(len(tempR)):
                tS = tempR[i].split(",")
                # Check if the team number is the smallest thus far
                if tS[0] < minTeam:
                    minIndex = i
                    minTeam = tS[0]
                    minMatch = tS[1]
                elif tS[0] == minTeam and tS[1] < minMatch:
                    minIndex = i
                    minMatch = tS[1]
            matchData.append(tempR.pop(minIndex))
    except:
        print "Error: Invalid match file"
        sys.exit(2)


def drawGraph(canvas, state):
    # Draw the bounding boxes
    canvas.create_rectangle(0, 0, largeGraphDimensions[0], largeGraphDimensions[1], fill='black', outline='white')
    if state.graphCount > 1:
        canvas.create_rectangle(0, 0, smallGraphDimensions[0], largeGraphDimensions[1], outline='white')
    if state.graphCount > 2:
        canvas.create_rectangle(0, smallGraphDimensions[1], largeGraphDimensions[0], largeGraphDimensions[1], outline='white')

    # Draw each of the graphs
    if state.graphCount == 1:
        currentGraph = state.graphs[0]

        canvas.create_line(125,75,125,windowDimensions[1]-100, fill='white')
        canvas.create_line(125,windowDimensions[1]-100,largeGraphDimensions[0]-100,windowDimensions[1]-100, fill='white')
        # Horizontal ticks
        h_dist = (largeGraphDimensions[0]-225)/matchCount
        for i in range(matchCount):
            canvas.create_line(125+h_dist*(i+1),largeGraphDimensions[1]-100,125+h_dist*(i+1),largeGraphDimensions[1]-90, fill='white')
        # Vertical ticks
        v_dist = (largeGraphDimensions[1]-175)/(masterGraphData[currentGraph]['tickCount']-1)
        for i in range(masterGraphData[currentGraph]['tickCount']):
            canvas.create_line(115,75+v_dist*i,125,75+v_dist*i, fill='white')

        # TODO Add the lines for the different teams
    elif state.graphCount == 2:
        for j in range(state.graphCount):
            currentGraph = state.graphs[j]

            canvas.create_line(j*smallGraphDimensions[0]+50,75,j*smallGraphDimensions[0]+50,windowDimensions[1]-100, fill='white')
            canvas.create_line(j*smallGraphDimensions[0]+50,windowDimensions[1]-100,(j+1)*smallGraphDimensions[0]-50,windowDimensions[1]-100, fill='white')
            # Horizontal ticks
            h_dist = (smallGraphDimensions[0]-100)/matchCount
            for i in range(matchCount):
                canvas.create_line(j*smallGraphDimensions[0]+50+h_dist*(i+1),windowDimensions[1]-100,j*smallGraphDimensions[0]+50+h_dist*(i+1),windowDimensions[1]-90, fill='white')
            # Vertical ticks
            v_dist = (largeGraphDimensions[1]-175)/(masterGraphData[currentGraph]['tickCount']-1)
            print largeGraphDimensions[1]-175
            for i in range(masterGraphData[currentGraph]['tickCount']):
                canvas.create_line(j*smallGraphDimensions[0]+40,v_dist*i+75,j*smallGraphDimensions[0]+50,v_dist*i+75, fill='white')
    else:
        for j in range(2):
            for k in range(2):
                currentGraph = state.graphs[j+k*2]

                canvas.create_line(j*smallGraphDimensions[0]+50,k*smallGraphDimensions[1]+50,j*smallGraphDimensions[0]+50,(k+1)*smallGraphDimensions[1]-75, fill='white')
                canvas.create_line(j*smallGraphDimensions[0]+50,(k+1)*smallGraphDimensions[1]-75,(j+1)*smallGraphDimensions[0]-50,(k+1)*smallGraphDimensions[1]-75, fill='white')
                # Horizontal ticks
                h_dist = (smallGraphDimensions[0]-100)/matchCount
                for i in range(matchCount):
                    canvas.create_line(j*smallGraphDimensions[0]+50+h_dist*(i+1),(k+1)*smallGraphDimensions[1]-65,j*smallGraphDimensions[0]+50+h_dist*(i+1),(k+1)*smallGraphDimensions[1]-75, fill='white')
                # Vertical ticks
                v_dist = (smallGraphDimensions[1]-125)/(masterGraphData[currentGraph]['tickCount']-1)
                for i in range(masterGraphData[currentGraph]['tickCount']):
                    canvas.create_line(j*smallGraphDimensions[0]+50,k*smallGraphDimensions[1]+v_dist*i+50,j*smallGraphDimensions[0]+40,k*smallGraphDimensions[1]+v_dist*i+50, fill='white')

    # Testing solid vs dashed
    canvas.create_line(100,200,150,200, fill='red',     dash=(4,4), width=4)
    canvas.create_line(100,210,150,210, fill='red',                 width=4)
    canvas.create_line(100,250,150,250, fill='green',   dash=(4,4), width=4)
    canvas.create_line(100,260,150,260, fill='green',               width=4)
    canvas.create_line(100,300,150,300, fill='blue',    dash=(4,4), width=4)
    canvas.create_line(100,310,150,310, fill='blue',                width=4)
    canvas.create_line(100,350,150,350, fill='yellow',  dash=(4,4), width=4)
    canvas.create_line(100,360,150,360, fill='yellow',              width=4)
    canvas.create_line(100,400,150,400, fill='orange',  dash=(4,4), width=4)
    canvas.create_line(100,410,150,410, fill='orange',              width=4)
    canvas.create_line(100,450,150,450, fill='magenta', dash=(4,4), width=4)
    canvas.create_line(100,460,150,460, fill='magenta',             width=4)

def drawComments(canvas, section):
    pass

def key(event):
    if event.char == event.keysym:
        print 'Normal key %s' % event.char
    if event.char == 'w':
        print "Increasing..."
        states[currentState].addGraph()
        drawGraph(canvas,states[currentState])
    elif event.char =='s':
        print "Decreasing..."
        states[currentState].removeGraph()
        drawGraph(canvas,states[currentState])

matchData = []
masterGraphData = []
matchCount = 6
states = [State()]*9
currentState = 0

windowDimensions = (1024,576)
commentsDimensions = (224,windowDimensions[1]/6)
largeGraphDimensions = (800,windowDimensions[1])
smallGraphDimensions = (400,windowDimensions[1]/2)
root = Tk()
root.geometry("%dx%d" % windowDimensions)
root.title("Hazy Scout")
canvas = Canvas(root, width=windowDimensions[0], height=windowDimensions[1])
canvas.pack()

loadConfigFile()

states[currentState].addGraph()
states[currentState].graphs[1]=1
states[currentState].addGraph()
states[currentState].addGraph()
drawGraph(canvas,states[currentState])

#text = Text(root)
#text.insert(INSERT,"Testing things! Lots and lots of letters....a eu8fagoc u7a,f.g u78aeod uba7fcgu dthjomqeufgcdhtao emugcaoht epm.,tha pmacoth umeoauthym.,9ugth nmeu.pugchte nom.,89geh otmugoh tem.pguoeh utrmcue8arc meuoigreh tmuearogeh emuorch utcmuorc tcm.rcoe m")
#text.pack()

root.bind_all('<Key>',key)
root.mainloop()

sys.exit(0)

var = tk.StringVar(root)
var.set('red')

choices = ['red', 'green', 'blue', 'yellow', 'white', 'magenta']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)

button = tk.Button(root, text='check value selected', command=select)
button.pack(side='left', padx=20, pady=10)

root.mainloop()
