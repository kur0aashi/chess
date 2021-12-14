#now class for the board
#see git changes
class Board:
    def __init__(self):
        self.rooms=list()
        for i in range(0,8):
            newl=list()
            self.rooms.append(newl)
            for j in range(0,8):                #initialize the whole board without pieces
                self.rooms[i].append("empty")
    def findPiece(self,x,y):                    #returns the piece palced at a cell and returns empty if no pieces
        return self.rooms[x][y]
    def setPiece(self,x,y,pName):               #places a piece at given cell
        self.rooms[x][y]=pName
    def findPos(self,pName):                    #find position of a piece returns a list with x and y position
        for ele in self.rooms:
            for item in ele:
                if item==pName:
                    return [self.rooms.index(ele),self.rooms[self.rooms.index(ele)].index(item)]
    def movePiece(self,x2,y2,name):             #this function sets a given piece in a cell and its initial position is cleared
        pos=self.findPos(name)
        x1=pos[0]
        y1=pos[1]
        self.setPiece(x1,y1,"empty")
        self.setPiece(x2,y2,name)
     #these fucntion is used to plot next point in diagonal directions   
    def lUp(self,y,x):
        #print("at lu")
        #print(y,x)
        #print(self.findPiece(y,x))
        return [y-1,x-1]
    def rUp(self,y,x):
        #print("at ru")
        #print(y,x)
        return [y-1,x+1]
    def lDown(self,y,x):
        #print("at ld")
        #print(y,x)
        return [y+1,x-1]
    def rDown(self,y,x):
        #print("at rd")
        #print(y,x)
        return [y+1,x+1]

#This function creates a initial board state with all the pieces in the default places
#the two dimensional array format is used "rooms[row][column]", the two index can be used to find if the-
#cell contains any piece or is empty
    def boardInit(self):
        for i in range(0,8):
            self.rooms[1][i]="bpawn"+str(i+1)
            self.rooms[6][i]="wpawn"+str(i+1)
        self.setPiece(0,0,"brook1")
        self.setPiece(7,0,"wrook1")
        self.setPiece(0,1,"bknight1")
        self.setPiece(7,1,"wknight1")
        self.setPiece(0,2,"bbishop1")
        self.setPiece(7,2,"wbishop1")
        self.setPiece(0,3,"bqueen0")
        self.setPiece(7,3,"wqueen0")
        self.setPiece(0,4,"bking0")
        self.setPiece(7,4,"wking0")
        self.setPiece(0,5,"bbishop2")
        self.setPiece(7,5,"wbishop2")
        self.setPiece(0,6,"bknight2")
        self.setPiece(7,6,"wknight2")
        self.setPiece(0,7,"brook2")
        self.setPiece(7,7,"wrook2")
        self.pieceSet=list()
        #create a variable "pieceSet" that contains all pieces names
        for item in self.rooms[0]:
            self.pieceSet.append(item)
        for item in self.rooms[1]:
            self.pieceSet.append(item)
        for item in self.rooms[6]:
            self.pieceSet.append(item)
        for item in self.rooms[7]:
            self.pieceSet.append(item)
        #create a dictionary to record state of a piece, state can be any of three
        #--seated---> is idle in a position
        #--dead----> has been killed
        #--selected---> is selected to move next
        self.pieceState=dict()
        for item in self.pieceSet:
            self.pieceState[item]="Idle"
        #create a dictionary that has a list of all the movesets of all the pieces
        self.allMoves=dict()
        #for cell name conversion
        self.xtoname=dict()
        for i in range(0,8):
            self.xtoname[i]=str(8-i)
        self.ytoname={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}




#this function returns a list of all the positions where the piece can move to next-
# the list contains list of x and ypositons
#if there are no places to move it returns an empty list
#it recognizes the type of piece from the name and returns appropriate movesets
    def moves(self,name):
        posit=self.findPos(name)
        x=posit[1]
        y=posit[0]
        moveset=list()
        if name[0]=="w":
            faction="white"
            enemy="b"           #if encounterd, attack that piece
        else:
            faction="black"
            enemy="w"
        for l in name:
            if l =="1" or l=="2" or l=="0" or l=="3" or l=="4" or l=="5" or l=="6" or l=="7" or l=="8":
                ind=name.index(l)
        types=name[1:ind]
        #print("a "+types+" detected at "+str(x),str(y))
        if types=="pawn":
            if faction=="black":
                if y==1:
                    pos=self.findPiece(y+2,x)
                    if pos[0]=='e':
                        moveset.append([y+2,x])
                pos=self.findPiece(y+1,x)
                if pos[0]=='e':
                    moveset.append([y+1,x])
                if x>0 and y<7:
                    pos=self.findPiece(y+1,x-1)
                    if pos[0]==enemy:
                        moveset.append([y+1,x-1])
                if x<7 and y<7:
                    pos=self.findPiece(y+1,x+1)
                    if pos[0]==enemy:
                        moveset.append([y+1,x+1])
            #this if for white where piece travel upwards, x and y are inverted to m,ake it similar to cordinate system

            if faction=="white":
                    if y==6:
                        pos=self.findPiece(y-2,x)   #check if pawn is in first room, then it moves two step
                        if pos[0]=='e':                #move if the room is empty
                            moveset.append([y-2,x])
                    pos=self.findPiece(y-1,x)           
                    if pos[0]=='e':
                        moveset.append([y-1,x])
                    if x>0 and y>0:
                        pos=self.findPiece(y-1,x-1)
                        if pos[0]==enemy:
                            moveset.append([y-1,x-1])
                    if x<7 and y>0:
                        pos=self.findPiece(y-1,x+1)
                        if pos[0]==enemy:
                            moveset.append([y-1,x+1])
            return moveset
        #rook moves in horizontal and vertical direction until enemy or ally is encountered in path
        #check for collisions while traversing into different directions
        if types=="rook":
            for i in range(y+1,8):                     #downwards
                item=self.findPiece(i,x)              
                #print(item+" found")
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([i,x])
                    if item[0]==enemy:
                        break
                    #print(item+" found")            #upwards
            for i in range(y-1,-1,-1):
                item=self.findPiece(i,x)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([i,x])
                    if item[0]==enemy:
                        break
            for i in range(x+1,8):                  #right
                item=self.findPiece(y,i)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([y,i])
                    if item[0]==enemy:
                        break
            for i in range(x-1,-1,-1):                  #left
                item=self.findPiece(y,i)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([y,i])
                    if item[0]==enemy:
                        break
            return moveset
            
        if types=="knight":                 #knight has 8 possible moves given that all fall under the 8x8 limit
            direc=[(y+2,x-1),(y+2,x+1),(y+1,x+2),(y-1,x+2),(y-2,x-1),(y-2,x+1),(y-1,x-2),(y+1,x-2)]
            for items in direc:
                if items[0]<8 and items[0]>-1:
                    if items[1]<8 and items[1]>-1:
                        pos=self.findPiece(items[0],items[1])
                        if pos[0]=='e' or pos[0]==enemy:
                            moveset.append([items[0],items[1]])
            return moveset
        if types=="bishop":
            
            #plot points in a direction untill endpoint is reached
            
            #left up
            Y=y
            X=x
            while Y>0 and X>0:
                nextPoint=self.lUp(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #right up
            Y=y
            X=x
            while Y>0 and X<7:
                nextPoint=self.rUp(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #left down
            Y=y
            X=x
            while Y<7 and X>0:
                nextPoint=self.lDown(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #right down
            Y=y
            X=x
            while Y<7 and X<7:
                nextPoint=self.rDown(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            return moveset
        if types=="king":
            if y>0:
                pos=self.findPiece(y-1,x)
                #print(y-1,x)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y-1,x])
            if y>0 and x<7:
                pos=self.findPiece(y-1,x+1)
                #print(y-1,x+1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y-1,x+1])
            if x<7:
                pos=self.findPiece(y,x+1)
                #print(y,x+1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y,x+1])
            if y<7 and x<7:
                pos=self.findPiece(y+1,x+1)
                #print(y+1,x+1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y+1,x+1])
            if y<7:
                pos=self.findPiece(y+1,x)
                #print(y+1,x)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y+1,x])
            if y<7 and x>0:
                pos=self.findPiece(y+1,x-1)
                #print(y+1,x-1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y+1,x-1])
            if x>0:
                pos=self.findPiece(y,x-1)
                #print(y,x-1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y,x-1])
            if x>0 and y>0:
                pos=self.findPiece(y-1,x-1)
                #print(y-1,x-1)
                #print(pos)
                if pos[0]=="e" or pos[0]==enemy:
                    moveset.append([y-1,x-1])
            return moveset
        if types=="queen":
            for i in range(y+1,8):                     #downwards
                item=self.findPiece(i,x)              
                #print(item+" found")
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([i,x])
                    if item[0]==enemy:
                        break
                    #print(item+" found")            #upwards
            for i in range(y-1,-1,-1):
                item=self.findPiece(i,x)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([i,x])
                    if item[0]==enemy:
                        break
            for i in range(x+1,8):                  #right
                item=self.findPiece(y,i)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([y,i])
                    if item[0]==enemy:
                        break
            for i in range(x-1,-1,-1):                  #left
                item=self.findPiece(y,i)
                if item[0]==faction[0]:
                    break
                if item[0]=="e" or item[0]==enemy:
                    moveset.append([y,i])
                    if item[0]==enemy:
                        break
            Y=y
            X=x
            while Y>-1 and X>-1:
                nextPoint=self.lUp(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #right up
            Y=y
            X=x
            while Y>-1 and X<7:
                nextPoint=self.rUp(Y,X)
                #print("points or queen")
                #print(nextPoint)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #left down
            Y=y
            X=x
            while Y<7 and X>-1:
                nextPoint=self.lDown(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            #right down
            Y=y
            X=x
            while Y<7 and X<7:
                nextPoint=self.rDown(Y,X)
                found=self.findPiece(nextPoint[0],nextPoint[1])
                if found[0]==faction[0]:
                    break
                if found[0]==enemy:
                    moveset.append([nextPoint[0],nextPoint[1]])
                    break
                if found[0]=='e':
                    moveset.append([nextPoint[0],nextPoint[1]])
                    Y=nextPoint[0]
                    X=nextPoint[1]
            return moveset   

    def canMoveHere(self,x,y,pName):
        avail=self.moves(pName)
        found=False
        for item in avail:
            if item[0]==x and item[1]==y:
                found=True
        return found
    #creating a function that update allMoves dictionary
    # which records all movesets of all the dictionary
    def updateMovesList(self):
        for item in self.rooms:
            for pieces in item:
                if pieces!="empty":
                    self.allMoves[pieces]=self.moves(pieces)
    #this function retuns all the pieces that has it marked
    def isChecked(self,pName):
        pos=self.findPos(pName)
        if pName[0]=='w':
            enemy='b'
        else:
            enemy='w'
        checkedBy=list()
        for key in self.allMoves:
            if key[0]==enemy:
                for items in self.allMoves[key]:
                    if pos==items:
                        checkedBy.append(key)
        return checkedBy
    #name conversion
    def ctoname(self,cord):
        first=self.ytoname[cord[1]]
        second=self.xtoname[cord[0]]
        return first+second
    def nametoc(self,name):
        xx=name[1]
        yy=name[0]
        for key in self.xtoname:
            if xx==self.xtoname[key]:
                xc=key
        for key in self.ytoname:
            if yy==self.ytoname[key]:
                yc=key
        return [xc,yc]

    def get_board_state(self):
        bs=dict()
        for i in range(0,len(self.rooms)):
            for j in range(0,len(self.rooms[0])):
                bs[self.ctoname([i,j])]=self.rooms[i][j]
        return bs                       
    def move_to(self,cell,pname):
        pos=self.nametoc(cell)
        self.movePiece(pos[0],pos[1],pname)
    def find_cell(self,nameOfPiece):
        return self.ctoname(self.findPos(nameOfPiece))
    
#initialization
#---make the object using Board()
#pieceSet variable contains name of all the pieces

    
                    
#IMPORTANT METHODS
#----boardInit() ---->initializes the board to default positions
#----movePiece(x,y,nameOfPiece) ------> moves a piece to set positions and clears the original positions
#----moves(nameOfPiece) ------->returns a list eg.[(x1,y1),(x2,y2).....(xn,yn)] of all the possible moves
#----findpiece(x,y)-----> returns the string which can be name of piece at that position or "empty"
#----findpos(nameOfPiece)------> returns the postion eg[x,y] of the given piece as a list of x and y
#----canMoveHere(x,y,nameOfPiece)-----> checks if a position is valid for a piece to move to
#----updateMovesList()----> updates the dictionary "allMoves" with current set of movesets for all the pieces
#----isChecked(nameOfPiece)----> returns the list of enemy pieces that is checking the piece
#-----ctoname([x,y])---> returns cell name
#-----nametoc(cellName)---> returns array address of a cell
#------move_to(cellName,nameOfPiece)----> move a piece by giving cell name for simplicity


