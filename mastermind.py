import pygame
from random import randint
from os import path, chdir

pygame.init()

background = (158,98,61)
brown0 = (132,73,39)
brown1 = (114,63,33)
brown2 = (165,108,74)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
magenta = (255,0,255)
cyan = (0,255,255)
orange = (255,106,0)
gray = (100,100,100)
white = (255,255,255)
black = (0,0,0)

#reads settings
def settingsRead():
    with open("settings.ini") as f:
        f.read(6)
        #amount of rows 6-12
        rowVar = int(f.readline())
        f.read(20)
        #combination length 3-6
        combLenVar = int(f.readline())
        f.read(8)
        #amount of colors 2-10
        colorVar = int(f.readline())
        for i in range(7):
            f.readline()
        f.read(37)
        #All different colors in combination True/false
        differentColors = str(f.readline())
    f.closed
    return [rowVar,combLenVar,colorVar,differentColors]

#creates settings if they don't exist
chdir(path.dirname(path.realpath(__file__)))
try:
    settings = settingsRead()
except:
    with open('settings.ini','w') as f:
        f.write('Rows: 12\n'
        'Combination Length: 4\n'
        'Colors: 6\n'
        '-----------------------\n'
        'Rows should be between 6 and 12.\n'
        'Combination length should be between 3 and 10.\n'
        'Colors should be between 2 and 9.\n'
        '-----------------------\n'
        'Standard: 12 rows, 4 long, 6 colors.\n'
        '-----------------------\n'
        'All different colors in combination: False')
        f.close
    print 'Settings were not available and were set to default'
    settings = settingsRead()

rowVar = settings[0]
combLenVar = settings[1]
colorVar = settings[2]
differentColors = settings[3]

colorsAll = [red,green,blue,yellow,magenta,cyan,orange,gray,white,black]
#sets the colors available in current game
colors = []
for i in range(colorVar):
    colors.append(colorsAll[i])

#creates secret answer
def createComb():
    if 'True' in differentColors and combLenVar <= colorVar:
        answer = []
        colorRandom = randint(0,len(colors)-1)
        colorsUsed = []
        for i in range(combLenVar):
            while colorRandom in answer:
                colorRandom = randint(0,len(colors)-1)
            answer.append(colorRandom)
    else:
        if 'True' in differentColors:
            print 'Not enough colors for the combination to have none of the same.'
        answer = []
        for i in range(combLenVar):
            answer.append(randint(0,len(colors)-1))
    return answer
#creates default guess
def createDefaultGuess():
    guessCurrent = []
    for i in range(combLenVar):
        guessCurrent.append(0)
    return guessCurrent

answer = createComb()
guessCurrent = createDefaultGuess()

position = 0
rowCurrent = 0
guessMemory = []
codePegsMemory = []

win = False
loss = False

gameDisplay = pygame.display.set_mode((53+63*combLenVar,112+42*rowVar))
pygame.display.set_caption('Theo\'s Mastermind')

def codePegs():
    pegs = []
    checkedPositions = ''
    for q in range(len(guessCurrent)):
        if guessCurrent[q] == answer[q]:
            pegs.append('b')
            checkedPositions += 'guess'+str(q) + 'answer'+str(q)
    for q in range(len(guessCurrent)):
        for w in range(len(guessCurrent)):
            if guessCurrent[q] == answer[w] and 'answer'+str(w) not in checkedPositions and 'guess'+str(q) not in checkedPositions:
                pegs.append('w')
                checkedPositions += 'guess'+str(q) + 'answer'+str(w)
    return pegs

gameExit = False

clock = pygame.time.Clock()

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:

            if win == False and loss == False:
                if event.key == pygame.K_1:
                    position = 0
                elif event.key == pygame.K_2 and combLenVar >= 2:
                    position = 1
                elif event.key == pygame.K_3 and combLenVar >= 3:
                    position = 2
                elif event.key == pygame.K_4 and combLenVar >= 4:
                    position = 3
                elif event.key == pygame.K_5 and combLenVar >= 5:
                    position = 4
                elif event.key == pygame.K_6 and combLenVar >= 6:
                    position = 5
                elif event.key == pygame.K_7 and combLenVar >= 7:
                    position = 6
                elif event.key == pygame.K_8 and combLenVar >= 8:
                    position = 7
                elif event.key == pygame.K_9 and combLenVar >= 9:
                    position = 8

                elif event.key == pygame.K_r:
                    guessCurrent[position] = 0
                elif event.key == pygame.K_g and colorVar >= 2:
                    guessCurrent[position] = 1
                elif event.key == pygame.K_b and colorVar >= 3:
                    guessCurrent[position] = 2
                elif event.key == pygame.K_y and colorVar >= 4:
                    guessCurrent[position] = 3
                elif event.key == pygame.K_m and colorVar >= 5:
                    guessCurrent[position] = 4
                elif event.key == pygame.K_c and colorVar >= 6:
                    guessCurrent[position] = 5
                elif event.key == pygame.K_o and colorVar >= 7:
                    guessCurrent[position] = 6
                elif event.key == pygame.K_f and colorVar >= 8:
                    guessCurrent[position] = 7
                elif event.key == pygame.K_w and colorVar >= 9:
                    guessCurrent[position] = 8
                elif event.key == pygame.K_k and colorVar >= 10:
                    guessCurrent[position] = 9

                elif event.key == pygame.K_DOWN:
                    if guessCurrent[position] == 0:
                        guessCurrent[position] = colorVar-1
                    else:
                        guessCurrent[position] -= 1
                elif event.key == pygame.K_UP:
                    if guessCurrent[position] == colorVar-1:
                        guessCurrent[position] = 0
                    else:
                        guessCurrent[position] += 1

                elif event.key == pygame.K_LEFT:
                    if position == 0:
                        position = combLenVar-1
                    else:
                        position -= 1
                elif event.key == pygame.K_RIGHT:
                    if position == combLenVar-1:
                        position = 0
                    else:
                        position += 1

                elif event.key == pygame.K_RETURN:
                    guessMemory.append(tuple(guessCurrent))
                    codePegsMemory.append(codePegs())
                    if guessCurrent == answer:
                        print 'YOU WON!'
                        win = True
                    elif rowCurrent < rowVar - 1 :
                        rowCurrent += 1
                    else:
                        print 'YOU LOST!'
                        loss = True
            if event.key == pygame.K_BACKSPACE:
                print 'Restarting...'

                answer = createComb()
                guessCurrent = createDefaultGuess()

                position = 0
                rowCurrent = 0
                guessMemory = []
                codePegsMemory = []

                win = False
                loss = False


    #print str(position)
    #print answer
    #print guessCurrent
    #print guessMemory
    #print codePegsMemory

    gameDisplay.fill(background)
    pygame.draw.rect(gameDisplay, brown0, [14,70,14+42*combLenVar,14])
    pygame.draw.rect(gameDisplay, brown0, [21,21,42*combLenVar,42])
    pygame.draw.rect(gameDisplay, brown0, [21,49+42*(rowVar-rowCurrent),42*combLenVar,42])
    pygame.draw.rect(gameDisplay, brown1, [21+42*position,49+42*(rowVar-rowCurrent),42,42])
    for x in range(len(guessCurrent)):
        pygame.draw.rect(gameDisplay, brown1, [28+42*x,28,28,28])
        for y in range(rowVar):
            pygame.draw.rect(gameDisplay, brown2, [28+42*x,98+42*y,28,28])
    #displays secret combination
    if win == True or loss == True:
        for q in range(combLenVar):
            for w in range(len(colors)):
                if answer[q] == w:
                    pygame.draw.rect(gameDisplay, colors[w], [42*q+28,28,28,28])
    #displays current guess
    for q in range(combLenVar):
        for w in range(len(colors)):
            if guessCurrent[q] == w:
                pygame.draw.rect(gameDisplay, colors[w], [42*q+28,56+42*(rowVar-rowCurrent),28,28])
    #displays previous guesses
    for x in range(rowCurrent):
        for q in range(combLenVar):
            for w in range(len(colors)):
                if guessMemory[x][q] == w:
                    pygame.draw.rect(gameDisplay, colors[w], [42*q+28,56+42*(rowVar-x),28,28])
    #displays code pegs
    lastCodePegsVar = 0
    if win == True or loss == True:
        lastCodePegsVar = 1
    for x in range(rowCurrent + lastCodePegsVar):
        if len(codePegsMemory[x]) != 0:
            pygame.draw.rect(gameDisplay, brown0, [24+42*combLenVar,66+42*(rowVar-x),21*len(codePegsMemory[x])+1,22])
        blackPegs = 0
        for q in range(len(codePegsMemory[x])):
            if codePegsMemory[x][q] == 'b':
                pygame.draw.rect(gameDisplay, black, [28+21*q+42*combLenVar,70+42*(rowVar-x),14,14])
                blackPegs += 1
            else:
                pygame.draw.rect(gameDisplay, white, [28+21*q+42*combLenVar,70+42*(rowVar-x),14,14])
    pygame.display.update()

    clock.tick(10)

pygame.quit()
quit()
