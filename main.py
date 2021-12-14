import pygame, sys
from pygame.locals import *
from board import Board
import time
#**************Resources**************************
#this section will collect resources such as images 
#create a dict that stores images
images=dict()
for i in range(1,9):
    images['bpawn'+str(i)]=pygame.image.load('images/bpawn.png')
for i in range(1,9):
    images['wpawn'+str(i)]=pygame.image.load('images/wpawn.png')
images['bknight1']= pygame.image.load('images/bknight.png')
images['bknight2']= pygame.image.load('images/bknight.png')
images['brook1']= pygame.image.load('images/brook.png')
images['brook2']= pygame.image.load('images/brook.png')
images['bbishop1']= pygame.image.load('images/bbishop.png')
images['bbishop2']= pygame.image.load('images/bbishop.png')
images['bqueen0']= pygame.image.load('images/bqueen.png')
images['bking0']= pygame.image.load('images/bking.png')
images['wknight1']= pygame.image.load('images/wknight.png')
images['wknight2']= pygame.image.load('images/wknight.png')
images['wrook1']= pygame.image.load('images/wrook.png')
images['wrook2']= pygame.image.load('images/wrook.png')
images['wbishop1']= pygame.image.load('images/wbishop.png')
images['wbishop2']= pygame.image.load('images/wbishop.png')
images['wqueen0']= pygame.image.load('images/wqueen.png')
images['wking0']= pygame.image.load('images/wking.png')
turn_board=pygame.image.load('images/turn.png')
t_board=pygame.transform.smoothscale(turn_board,(220,200))
tray2=pygame.image.load('images/t22.png')
pygame.mixer.init()
release = pygame.mixer.Sound('release.wav')
cut = pygame.mixer.Sound('cut.wav')
announcement=['off','none']
turn="white"
def set_text(string,fontSize): #Function to set text

    font = pygame.font.Font('fonts/pt.otf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (200,45,2)) 
    return text
def announce(msg):
    totalText = set_text(msg,50)
    mainWindow.blit(totalText,(280,300))
#**********Resources*****************************
#****pygame initialization*******
pygame.init()
winWidth=1300
winHeight=700
mainWindow=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption('Chess')
chess=Board()
chess.boardInit()
death_list=[[],[]] #this variable contains piece that are dead, first list for black and second list for white
#************draw the tray that shows dead pieces
def draw_tray(dl):
    global mainWindow
    tray1x=1055
    tray1y=30
    tray2x=1055
    tray2y=511
    tray1_color=(50,50,50)
    tray2_color=(200,200,200)
    # pygame.draw.rect(mainWindow,tray1_color,(tray1x,tray1y,240,160))
    # pygame.draw.rect(mainWindow,tray2_color,(tray2x,tray2y,240,160))
    mainWindow.blit(tray2,(tray1x,tray1y))
    mainWindow.blit(tray2,(tray2x,tray2y))
    x=tray1x
    y=tray1y+50
    for item in dl[0]:
        if x>1290:
            x=tray1x
            y=y+40
        mainWindow.blit(item,(x,y))
        x=x+30
    x=tray2x
    y=tray2y+50
    for item in dl[1]:
        if x>1290:
            x=tray1x
            y=y+40
        mainWindow.blit(item,(x,y))
        x=x+30
    mainWindow.blit(t_board,(1065,250))
    font = pygame.font.Font('fonts/nas.otf', 30) 
    #(0, 0, 0) is black, to make black text
    ttext = font.render("Turn", True, (200,200,200))
    mainWindow.blit(ttext,(1140,335))
    if turn=="white":
        tIndicator=(255,255,255)
    else:
        tIndicator=(0,0,0)
    pygame.draw.circle(mainWindow,tIndicator,(1175,400),30)
#*****************make dictionary with board coardinates for each cell

boardMap=dict()
b=30
a=250
row=[8,7,6,5,4,3,2,1,0]
col=['a','b','c','d','e','f','g','h']
color=[(181,167,125),(71,145,131)]
color_index=0
for x in range(0,8):
    a=250
    rowname=row[x]
    for y in range(0,8):
        colname=col[y]
        if colname!='a':
            color_index=(color_index+1)%2
        boardMap[colname+str(rowname)]=[a,b,color[color_index],color[color_index]]
        a=a+100
    b=b+80
#*************************************************
def drawBoard(state,selectionrecord):
    global boardMap
    global images
    global selected
    for key in boardMap:
        
        if state[key]!="empty":
            pygame.draw.rect(mainWindow,boardMap[key][3],(boardMap[key][0],boardMap[key][1],100,80))
            if selectionrecord!=key:
                mainWindow.blit(images[state[key]],((boardMap[key][0],boardMap[key][1])))
        

        else:
            pygame.draw.rect(mainWindow,boardMap[key][3],(boardMap[key][0],boardMap[key][1],100,80))
#****************************************
def get_clicked_cell(pos):
    X=pos[0]
    Y=pos[1]
    for key in boardMap:
        x=boardMap[key][0]
        y=boardMap[key][1]
        if (X>x and X<x+100) and (Y>y and Y<y+80):
            return key
#****************************************

def on_select(piece):
    selectTracker=[chess.find_cell(piece),piece]  #after selecting a piece keep track of its original
    return selectTracker                   #position and its image
selectionrecord="none"
selected=False
placed=False
def pieceSelection():
    global selected
    global announcement
    global selected_piece
    global turn
    announcement[0]="off"
    mouse_pos=pygame.mouse.get_pos()
    try:
        if selected==False:
            clicked_cell=get_clicked_cell(mouse_pos)
            piece=chess.get_board_state()[clicked_cell]
            if piece!='empty' and selected==False:
                if piece[0]!=turn[0]:
                    return
                selected_piece=on_select(piece)
                selected=True
    except:
        print("clicked outside")


#********main loop starts here***********
while True:
    mainWindow.fill((23,19,19))
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if selected==False and event.type==pygame.MOUSEBUTTONDOWN:
            pieceSelection()
        try:
            if event.type==MOUSEBUTTONUP and selected==True:
                chess.updateMovesList()
               
                mouse_pos=pygame.mouse.get_pos()
                clicked_cell=get_clicked_cell(mouse_pos)
                pos=chess.nametoc(clicked_cell)
                print(clicked_cell+" clicked now moving "+selected_piece[1])
                
                if chess.canMoveHere(pos[0],pos[1],selected_piece[1]):
                    if chess.findPiece(pos[0],pos[1])!="empty":
                        piece_at_pos=chess.findPiece(pos[0],pos[1])
                        deathpic=pygame.transform.smoothscale(images[piece_at_pos],(30,40))
                        if piece_at_pos[0]=='w':
                            death_list[0].append(deathpic)
                            announcement[0]="on"
                            for l in piece_at_pos:
                                if l =="1" or l=="2" or l=="0" or l=="3" or l=="4" or l=="5" or l=="6" or l=="7" or l=="8":
                                    ind=piece_at_pos.index(l)
                            type=piece_at_pos[1:ind]
                            pygame.mixer.Sound.play(cut)
                            announcement[1]="A white "+type+" has been cut"
                        else:
                            death_list[1].append(deathpic)
                            announcement[0]="on"
                            for l in piece_at_pos:
                                if l =="1" or l=="2" or l=="0" or l=="3" or l=="4" or l=="5" or l=="6" or l=="7" or l=="8":
                                    ind=piece_at_pos.index(l)
                            type=piece_at_pos[1:ind]
                            pygame.mixer.Sound.play(cut)
                            announcement[1]="A black "+type+" has been cut"
                    chess.move_to(clicked_cell,selected_piece[1])
                    if turn=="black":
                        turn="white"
                    else:
                        turn="black"
                    chess.updateMovesList()
                    print(death_list)
                    print("The new location of "+selected_piece[1]+" : "+clicked_cell)
                    selected=False
                    selected_piece="none"
                    selectionrecord="none"
                    
                else:
                    pygame.mixer.Sound.play(release)
                    selected=False
                    selected_piece="none"
                    selectionrecord="none"
        except Exception as e:
            print("An error has occured:")
            print(e)

        if event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
            pygame.mixer.Sound.play(release)
            selected=False
            selected_piece="none"
            selectionrecord="none"
    drawBoard(chess.get_board_state(),selectionrecord)
    
    if selected==True:
        selectionrecord=selected_piece[0]
        mousePos=pygame.mouse.get_pos()
        selpic=pygame.transform.scale(images[selected_piece[1]],(60,50))
        mainWindow.blit(selpic,(mousePos[0]-30,mousePos[1]-25))
    draw_tray(death_list)
    if announcement[0]=="on":
        announce(announcement[1])   
    pygame.display.update()                           #<------------------MAIN DISPLAY UPDATES HERE
