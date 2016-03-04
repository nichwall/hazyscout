import sys
import yaml
try:
    from Tkinter import *
except:
    from tkinter import *


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
        self.graphs = [0]*self.graphCount
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
masterGraphData = []
def loadConfigFile():
    try:
        configData = yaml.load(open("config.yaml"))
        graphCount = configData['matchCount']
        for i in range(len(configData['graphs'])):
            if configData['graphs'][i]['id'] == i:
                print configData['graphs'][i]
                masterGraphData.append(configData['graphs'][i])
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
        matchFile.close()

        # Convert the read array to 2D array
        tempArr = []
        for i in readed:
            tempArr.append(i.split(","))
            tempArr[-1] = map(int, tempArr[-1]) # Converts the array to an array of ints
        readed = tempArr

        # Sort the data from the teams by team/match number for easier graphing
        while len(readed) != 0:
            print readed
            minIndex = 0
            minTeam = 0
            minMatch = 0
            for j in range(len(readed)):
                tempR = readed[j]
                print tempR
                # Check if the team number is the smallest thus far
                if tempR[0] < minTeam:
                    minIndex = i
                    minTeam = tempR[0]
                    minMatch = tempR[1]
                elif tempR[0] == minTeam and tempR[1] < minMatch:
                    minIndex = i
                    minMatch = tempR[1]
            matchData.append(readed.pop(minIndex))
            if matchData[-1][0] not in teamList:
                teamList.append(tempR[0])
    except:
        print "Error: Invalid match file"
        sys.exit(2)

def drawTeam(canvas, graphNumber, minX, minY, maxX, maxY, teamNumber, yTicks, xTicks, color):
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

    h_dist = (maxX-minX)/xTicks
    v_dist = (maxY-minY)/yTicks
    solidCol = masterGraphData[graphNumber]['solidCol']
    dashCol = masterGraphData[graphNumber]['dashCol']

    lastSolidPoint = (-10,-10)
    lastDashPoint  = (-10,-10)
    for i in range(len(matchList)):
        if (matchList[i][0] == teamNumber):
            # Solid line
            xPos = matchList[i][1]*h_dist+minX
            yPos = maxY-(matchList[i][solidCol]+yOffset)
            if (lastSolidPoint[0] > -10):
                canvas.create_line(lastSolidPoint, xPos, yPos, fill=color, width=3)
            lastSolidPoint = (xPos, yPos)

            # Dashed line
            if (dashCol != -1):
                yPos = maxY-(matchList[i][dashCol]+yOffset)
                if (lastDashPoint[0] > -10):
                    canvas.create_line(lastDashPoint, xPos, yPos, fill=color, width=3, dash=(4,4))
                lastDashPoint = (xPos, yPos)


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
        v_dist = (largeGraphDimensions[1]-175)/(masterGraphData[currentGraph]['yTickCount']-1)
        for i in range(masterGraphData[currentGraph]['yTickCount']):
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
            v_dist = (largeGraphDimensions[1]-175)/(masterGraphData[currentGraph]['yTickCount']-1)
            print largeGraphDimensions[1]-175
            for i in range(masterGraphData[currentGraph]['yTickCount']):
                canvas.create_line(j*smallGraphDimensions[0]+40,v_dist*i+75,j*smallGraphDimensions[0]+50,v_dist*i+75, fill='white')
    else:
        for z in range(state.graphCount):
            j = z/2
            k = z%2

            currentGraph = state.graphs[j*2+k]

            canvas.create_line(j*smallGraphDimensions[0]+50,k*smallGraphDimensions[1]+50,j*smallGraphDimensions[0]+50,(k+1)*smallGraphDimensions[1]-75, fill='white')
            canvas.create_line(j*smallGraphDimensions[0]+50,(k+1)*smallGraphDimensions[1]-75,(j+1)*smallGraphDimensions[0]-50,(k+1)*smallGraphDimensions[1]-75, fill='white')
            # Horizontal ticks
            h_dist = (smallGraphDimensions[0]-100)/matchCount
            for i in range(matchCount):
                canvas.create_line(j*smallGraphDimensions[0]+50+h_dist*(i+1),(k+1)*smallGraphDimensions[1]-65,j*smallGraphDimensions[0]+50+h_dist*(i+1),(k+1)*smallGraphDimensions[1]-75, fill='white')
            # Vertical ticks
            print "Current:",currentGraph
            print "Master:",masterGraphData[currentGraph]
            v_dist = (smallGraphDimensions[1]-125)/(masterGraphData[currentGraph]['yTickCount']-1)
            for i in range(masterGraphData[currentGraph]['yTickCount']):
                canvas.create_line(j*smallGraphDimensions[0]+50,k*smallGraphDimensions[1]+v_dist*i+50,j*smallGraphDimensions[0]+40,k*smallGraphDimensions[1]+v_dist*i+50, fill='white')

    # Testing solid vs dashed
    canvas.create_line(100,200,150,200, fill='red',     dash=(4,4), width=3)
    canvas.create_line(100,210,150,210, fill='red',                 width=3)
    canvas.create_line(100,250,150,250, fill='green',   dash=(4,4), width=3)
    canvas.create_line(100,260,150,260, fill='green',               width=3)
    canvas.create_line(100,300,150,300, fill='blue',    dash=(4,4), width=3)
    canvas.create_line(100,310,150,310, fill='blue',                width=3)
    canvas.create_line(100,350,150,350, fill='yellow',  dash=(4,4), width=3)
    canvas.create_line(100,360,150,360, fill='yellow',              width=3)
    canvas.create_line(100,400,150,400, fill='orange',  dash=(4,4), width=3)
    canvas.create_line(100,410,150,410, fill='orange',              width=3)
    canvas.create_line(100,450,150,450, fill='magenta', dash=(4,4), width=3)
    canvas.create_line(100,460,150,460, fill='magenta',             width=3)

def drawComments(canvas, state):
    teams = state.teams

    print teamSelection[0]
    for i in range(UNIQUE_TEAMS):
        canvas.create_rectangle(windowDimensions[0]-commentsDimensions[0],commentsDimensions[1]*i,windowDimensions[0],commentsDimensions[1]*(i+1), fill=colors[i], outline='white')
        teamSelection[i].place(x=1000,y=commentsDimensions[1]*i+50)

def key(event):
    if event.char == event.keysym:
        print 'Normal key %s' % event.char

    if event.char == 'w':
        print "Increasing..."
        states[currentState].addGraph()
    elif event.char == 's':
        print "Decreasing..."
        states[currentState].removeGraph()
    elif event.char == 'q':
        print "Exit!"
        sys.exit(0)

    #for var in teamVarsForDropdown:
    for var in teamVarsForDropdown:
        print var.get()
    drawGraph(canvas,states[currentState])

matchData = []
masterGraphData = []
matchCount = 6 # Default, just in case
states = [State()]*9
currentState = 0
teamList = [0]

loadConfigFile()
loadMatchData()

print "TEAMLIST:",teamList

windowDimensions = (1024,660)
commentsDimensions = (224,windowDimensions[1]/6)
largeGraphDimensions = (800,windowDimensions[1])
smallGraphDimensions = (400,windowDimensions[1]/2)

root = Tk()
root.geometry("%dx%d" % windowDimensions)
root.title("Hazy Scout")
canvas = Canvas(root, width=windowDimensions[0], height=windowDimensions[1])
canvas.pack()

teamVarsForDropdown = [StringVar(root) for var in colors]
teamSelection = [OptionMenu(root, var, *teamList) for var in teamVarsForDropdown]
for i in teamVarsForDropdown:
    i.set(0)

drawGraph(canvas,states[currentState])
drawComments(canvas,states[currentState])

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
