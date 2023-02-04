from tkinter import *


# constants and bools
BOARD_X = 8
BOARD_Y = 8
CUBE_X = 64
CUBE_Y = 64
TEXT_SIZE = 48
TABLE_COORDINATES = list(range(0, 8))
turn = "white"  # / "black"
swap = False    # Swapping for each turn
theocracy = False   # deactivate Queen

#         Table-Colour1, Table-Colour2, Player1, Player2
colours = ['#626160', '#C6C2C1', '#000000', '#F0ECE8']

borderColour = "red"
bkgColour = "red"

"""....................Game Board........................."""

# Chess Board variables

activePiece = []    # the active piece, i.e. with highlighted piece, egs :[1, 1, '#008000', '♟', '#510051']
activePieceBool = "NoActivePiece"  # / "ActivePiece"
cellList = []   # list that contains all the pieces and their attributes
moves = []      # list that has the possible moves for a piece

# Chess Board Constants and bools

justActivated = False   # a bool designed specifically for the pieceActivate function, to make it so that the piece doesn't re-activate after it has moved
turnChange = False      # bool to check if the turn has been changed in one round
coordList = []      # list with all the coordinates, note to self: xCoord is downward, while yCoord is vertical
kingMoved = False   # to check if the king has moved, needed for castling
castling = False

# Lists of all possible moves

# White
wPawn = []
wRook = []
wPriest = []
wKing = []
wQueen = []
wKnight = []
wMoves = [wPawn, wPriest, wKing, wQueen, wKnight, wRook]

# Black
bPawn = []
bRook = []
bPriest = []
bKing = []
bQueen = []
bKnight = []
bMoves = [bPawn, bPriest, bKing, bQueen, bKnight, bRook]


# Chess Board class

class Board:
    def __init__(self, master, xCoord, yCoord, tileColour, pieceType, pieceColour, ACTIVE):
        self.ACTIVE = ACTIVE
        global activePiece, cellList, activePieceBool, justActivated
        self.yCoord = yCoord
        self.tileColour = tileColour
        self.pieceType = pieceType
        self.pieceColour = pieceColour

        currentCellCoord = (xCoord, yCoord)

        if len(cellList) < 64:
            cellList.append([xCoord, yCoord, tileColour, pieceType, pieceColour])

        def hoverAnimation(event=None):  # func that gives red highlight when entering a cell
            global activePiece, activePieceBool, turn
            if turn == "white":
                if pieceType in "♙♖♗♘♕♔" and activePieceBool == "NoActivePiece":
                    pieceLabel["fg"] = borderColour
            if turn == "black":
                if pieceType in "♟♜♝♞♛♚" and activePieceBool == "NoActivePiece":
                    pieceLabel["fg"] = borderColour

        def removeHover(event=None):  # func that removes red highlight when leaving a cell
            global activePiece, activePieceBool
            if pieceType in "♔♝♞♚♖♛♟♜♘♗♕♔♙" and activePieceBool == "NoActivePiece":
                pieceLabel["fg"] = pieceColour

        def blocked(x, y):
            global moves
            if pieceFromCoordinates(x, y)[4] != activePiece[4] and pieceFromCoordinates(x, y)[3] in "♔♝♞♚♖♛♟♜♘♗♕♔♙":
                if activePiece[3] not in "♙♟":
                    moves.append((x, y))
                return True  # saying that the obj is blocked
            if pieceFromCoordinates(x, y)[4] == activePiece[4] and pieceFromCoordinates(x, y)[3] in "♔♝♞♚♖♛♟♜♘♗♕♙" and x in range(
                    0, 8) and y in range(0, 8):
                return True
            else:
                return False

        def pawnMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves
            if activePiece[3] in "♟":  # black pawn
                if xCoordFrom == 6 or xCoordFrom == 1:  # initial pos can have double step or single step
                    if not blocked(xCoordFrom + 2, yCoordFrom):
                        moves.append((xCoordFrom + 2, yCoordFrom))
                    if not blocked(xCoordFrom + 1, yCoordFrom):
                        moves.append((xCoordFrom + 1, yCoordFrom))
                elif not blocked(xCoordFrom + 1, yCoordFrom):  # for all other pos, single step
                    moves.append((xCoordFrom + 1, yCoordFrom))
                if pieceFromCoordinates(xCoordFrom + 1, yCoordFrom - 1)[4] != activePiece[4] and blocked(xCoordFrom + 1,
                                                                                                    yCoordFrom - 1):
                    moves.append((xCoordFrom + 1, yCoordFrom - 1))
                if pieceFromCoordinates(xCoordFrom + 1, yCoordFrom + 1)[4] != activePiece[4] and blocked(xCoordFrom + 1,
                                                                                                    yCoordFrom + 1):
                    moves.append((xCoordFrom + 1, yCoordFrom + 1))
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True
            if activePiece[3] in "♙":  # white pawn
                if xCoordFrom == 6 or xCoordFrom == 1:
                    if not blocked(xCoordFrom - 2, yCoordFrom):
                        moves.append((xCoordFrom - 2, yCoordFrom))
                    if not blocked(xCoordFrom - 1, yCoordFrom):
                        moves.append((xCoordFrom - 1, yCoordFrom))
                elif not blocked(xCoordFrom - 1, yCoordFrom):
                    moves.append((xCoordFrom - 1, yCoordFrom))
                if pieceFromCoordinates(xCoordFrom - 1, yCoordFrom - 1)[4] != activePiece[4] and blocked(xCoordFrom - 1,
                                                                                                    yCoordFrom - 1):
                    moves.append((xCoordFrom - 1, yCoordFrom - 1))
                if pieceFromCoordinates(xCoordFrom - 1, yCoordFrom + 1)[4] != activePiece[4] and blocked(xCoordFrom - 1,
                                                                                                    yCoordFrom + 1):
                    moves.append((xCoordFrom - 1, yCoordFrom + 1))
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def rookMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList, run2, bRook, wRook
            run = True
            while run is True:
                i = 1
                j = -1
                while (xCoordFrom + j) in range(0, 8) and not blocked(xCoordFrom + j, yCoordFrom):
                    moves.append((xCoordFrom + j, yCoordFrom))
                    j += -1
                j = -1
                while (yCoordFrom + j) in range(0, 8) and not blocked(xCoordFrom, yCoordFrom + j):
                    moves.append((xCoordFrom, yCoordFrom + j))
                    j += -1
                j = -1
                while (yCoordFrom + i) in range(0, 8) and not blocked(xCoordFrom, yCoordFrom + i):
                    moves.append((xCoordFrom, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and not blocked(xCoordFrom + i, yCoordFrom):
                    moves.append((xCoordFrom + i, yCoordFrom))
                    i += 1
                i = 1
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def priestMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList
            run = True
            while run is True:
                i = 1
                while (xCoordFrom - i) in range(0, 8) and (yCoordFrom - i) in range(0, 8) and not blocked(
                        xCoordFrom - i, yCoordFrom - i):
                    moves.append((xCoordFrom - i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and (yCoordFrom - i) in range(0, 8) and not blocked(
                        xCoordFrom + i, yCoordFrom - i):
                    moves.append((xCoordFrom + i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom - i) in range(0, 8) and (yCoordFrom + i) in range(0, 8) and not blocked(
                        xCoordFrom - i, yCoordFrom + i):
                    moves.append((xCoordFrom - i, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and (yCoordFrom + i) in range(0, 8) and not blocked(
                        xCoordFrom + i, yCoordFrom + i):
                    moves.append((xCoordFrom + i, yCoordFrom + i))
                    i += 1

                i = 1
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def knightMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList
            if xCoordFrom + 2 in range(0, 8) and yCoordFrom + 1 in range(0, 8) and not blocked(xCoordFrom + 2,
                                                                                               yCoordFrom + 1):
                moves.append((xCoordFrom + 2, yCoordFrom + 1))
            if xCoordFrom + 2 in range(0, 8) and yCoordFrom - 1 in range(0, 8) and not blocked(xCoordFrom + 2,
                                                                                               yCoordFrom - 1):
                moves.append((xCoordFrom + 2, yCoordFrom - 1))
            if xCoordFrom - 2 in range(0, 8) and yCoordFrom - 1 in range(0, 8) and not blocked(xCoordFrom - 2,
                                                                                               yCoordFrom - 1):
                moves.append((xCoordFrom - 2, yCoordFrom - 1))
            if xCoordFrom - 2 in range(0, 8) and yCoordFrom + 1 in range(0, 8) and not blocked(xCoordFrom - 2,
                                                                                               yCoordFrom + 1):
                moves.append((xCoordFrom - 2, yCoordFrom + 1))
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom - 2 in range(0, 8) and not blocked(xCoordFrom + 1,
                                                                                               yCoordFrom - 2):
                moves.append((xCoordFrom + 1, yCoordFrom - 2))
            if xCoordFrom - 1 in range(0, 8) and yCoordFrom + 2 in range(0, 8) and not blocked(xCoordFrom - 1,
                                                                                               yCoordFrom + 2):
                moves.append((xCoordFrom - 1, yCoordFrom + 2))
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom + 2 in range(0, 8) and not blocked(xCoordFrom + 1,
                                                                                               yCoordFrom + 2):
                moves.append((xCoordFrom + 1, yCoordFrom + 2))
            if xCoordFrom - 1 in range(0, 8) and yCoordFrom - 2 in range(0, 8) and not blocked(xCoordFrom - 1,
                                                                                               yCoordFrom - 2):
                moves.append((xCoordFrom - 1, yCoordFrom - 2))
            if (xCoordTo, yCoordTo) in moves:
                moves = []
                return True

        def queenMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList, run2
            run = True
            while run is True:
                i = 1
                while (xCoordFrom - i) in range(0, 8) and (yCoordFrom - i) in range(0, 8) and not blocked(
                        xCoordFrom - i, yCoordFrom - i):
                    moves.append((xCoordFrom - i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and (yCoordFrom - i) in range(0, 8) and not blocked(
                        xCoordFrom + i, yCoordFrom - i):
                    moves.append((xCoordFrom + i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom - i) in range(0, 8) and (yCoordFrom + i) in range(0, 8) and not blocked(
                        xCoordFrom - i, yCoordFrom + i):
                    moves.append((xCoordFrom - i, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and (yCoordFrom + i) in range(0, 8) and not blocked(
                        xCoordFrom + i, yCoordFrom + i):
                    moves.append((xCoordFrom + i, yCoordFrom + i))
                    i += 1
                i = 1
                f = -1
                while (xCoordFrom + f) in range(0, 8) and not blocked(xCoordFrom + f, yCoordFrom):
                    moves.append((xCoordFrom + f, yCoordFrom))
                    f += -1
                f = -1
                while (yCoordFrom + f) in range(0, 8) and not blocked(xCoordFrom, yCoordFrom + f):
                    moves.append((xCoordFrom, yCoordFrom + f))
                    f += -1
                f = -1
                while (yCoordFrom + i) in range(0, 8) and not blocked(xCoordFrom, yCoordFrom + i):
                    moves.append((xCoordFrom, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0, 8) and not blocked(xCoordFrom + i, yCoordFrom):
                    moves.append((xCoordFrom + i, yCoordFrom))
                    i += 1
                i = 1
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def kingMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, cellList, kingMoved, castling
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom + 1 in range(0, 8) and not blocked(xCoordFrom + 1,
                                                                                               yCoordFrom + 1):
                moves.append((xCoordFrom + 1, yCoordFrom + 1))
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom - 1 in range(0, 8) and not blocked(xCoordFrom - 1,
                                                                                               yCoordFrom - 1):
                moves.append((xCoordFrom - 1, yCoordFrom - 1))
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom - 1 in range(0, 8) and not blocked(xCoordFrom + 1,
                                                                                               yCoordFrom - 1):
                moves.append((xCoordFrom + 1, yCoordFrom - 1))
            if xCoordFrom - 1 in range(0, 8) and yCoordFrom + 1 in range(0, 8) and not blocked(xCoordFrom - 1,
                                                                                               yCoordFrom + 1):
                moves.append((xCoordFrom - 1, yCoordFrom + 1))
            if xCoordFrom - 1 in range(0, 8) and yCoordFrom in range(0, 8) and not blocked(xCoordFrom - 1, yCoordFrom):
                moves.append((xCoordFrom - 1, yCoordFrom))
            if xCoordFrom + 1 in range(0, 8) and yCoordFrom in range(0, 8) and not blocked(xCoordFrom + 1, yCoordFrom):
                moves.append((xCoordFrom + 1, yCoordFrom))
            if xCoordFrom in range(0, 8) and yCoordFrom + 1 in range(0, 8) and not blocked(xCoordFrom, yCoordFrom + 1):
                moves.append((xCoordFrom, yCoordFrom + 1))
            if xCoordFrom in range(0, 8) and yCoordFrom - 1 in range(0, 8) and not blocked(xCoordFrom, yCoordFrom - 1):
                moves.append((xCoordFrom, yCoordFrom - 1))
            if not kingMoved:
                if activePiece[3] == "♚":
                    if (xCoordTo, yCoordTo) == (0, 6) and not blocked(0, 5) and not blocked(0, 6) and \
                            pieceFromCoordinates(0, 7)[3] == "♜":
                        pieceFromCoordinates(0, 6)[3] = "♚"
                        pieceFromCoordinates(0, 5)[3] = "♜"
                        pieceFromCoordinates(0, 7)[3] = "\u2003"
                        pieceFromCoordinates(0, 4)[3] = "\u2003"
                        castling = True
                        return True
                    if (xCoordTo, yCoordTo) == (0, 1) and not blocked(0, 1) and not blocked(0, 2) and not blocked(0, 3) and \
                            pieceFromCoordinates(0, 0)[3] == "♜":
                        pieceFromCoordinates(0, 1)[3] = "♚"
                        pieceFromCoordinates(0, 2)[3] = "♜"
                        pieceFromCoordinates(0, 0)[3] = "\u2003"
                        pieceFromCoordinates(0, 4)[3] = "\u2003"
                        castling = True
                        return True
                if activePiece[3] == "♔":
                    if (xCoordTo, yCoordTo) == (7, 6) and not blocked(7, 5) and not blocked(7, 6) and \
                            pieceFromCoordinates(7, 7)[3] == "♖":
                        pieceFromCoordinates(7, 6)[3] = "♔"
                        pieceFromCoordinates(7, 5)[3] = "♖"
                        pieceFromCoordinates(7, 7)[3] = "\u2003"
                        pieceFromCoordinates(7, 4)[3] = "\u2003"
                        castling = True
                        return True
                    if (xCoordTo, yCoordTo) == (7, 1) and not blocked(7, 1) and not blocked(7, 2) and not blocked(7, 3) and \
                            pieceFromCoordinates(7, 0)[3] == "♖":
                        pieceFromCoordinates(7, 1)[3] = "♔"
                        pieceFromCoordinates(7, 2)[3] = "♖"
                        pieceFromCoordinates(7, 0)[3] = "\u2003"
                        pieceFromCoordinates(7, 4)[3] = "\u2003"
                        castling = True
                        return True
            if (xCoordTo, yCoordTo) in moves:
                kingMoved = True
                moves = []
                return True

        def availableMove(xCoordTo, yCoordTo, xCoordFrom,
                          yCoordFrom):  # func that checks if anything is blocking the piece
            global moves, castling
            coordList = []
            [coordList.append((i[0], i[1])) for i in cellList]
            moves = []
            if activePiece[3] in "♟♙":
                return pawnMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♖♜":
                return rookMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♗♝":
                return priestMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♘♞":
                return knightMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♛♕":
                return queenMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♚♔":
                return kingMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)

        # def checkMate():    # I'm not sure that work good should be in TO DO LIST
        #     allOpponentMoves = []
        #     if activePiece[3] == "♚":
        #         return True
        #     if activePiece[3] == "♔":
        #         return True

        def pieceMovement(event=None):
            global activePiece, activePieceBool, justActivated, turn, turnChange, castling
            if turn == "white":
                if pieceType in "♙♖♗♘♕♔" and activePieceBool == "NoActivePiece":
                    activePiece = pieceFromCoordinates(currentCellCoord[0], currentCellCoord[1])
                    activePieceBool = "ActivePiece"
                    justActivated = True
            if turn == "black":
                if pieceType in "♟♜♝♞♛♚" and activePieceBool == "NoActivePiece":
                    activePiece = pieceFromCoordinates(currentCellCoord[0], currentCellCoord[1])
                    activePieceBool = "ActivePiece"
                    justActivated = True

            if activePieceBool == "ActivePiece" and not justActivated:
                clickedPiece = pieceFromCoordinates(currentCellCoord[0], currentCellCoord[1])
                # print(clickedPiece)   # for history of playing
                if castling:
                    activePiece = []
                    activePieceBool = "NoActivePiece"
                    if turn == "white" and not turnChange:
                        turn = "black"
                        turnChange = True
                    if turn == "black" and not turnChange:
                        turn = "white"
                        turnChange = True
                    turnChange = False
                    castling = False
                    baseReDraw()
                    # print(len(cellList))
                if clickedPiece[3] != "\u2003" and clickedPiece[4] != activePiece[4] and availableMove(
                        currentCellCoord[0], currentCellCoord[1], activePiece[0],
                        activePiece[1]) and not castling:  # for an opponent clicked cell
                    clickedPiece[3] = activePiece[3]
                    clickedPiece[4] = activePiece[4]
                    activePiece[3] = "\u2003"
                    activePiece = []
                    activePieceBool = "NoActivePiece"
                    if turn == "white" and not turnChange:
                        turn = "black"
                        turnChange = True
                    if turn == "black" and not turnChange:
                        turn = "white"
                        turnChange = True
                    turnChange = False
                    baseReDraw()
                if clickedPiece[3] == "\u2003" and availableMove(currentCellCoord[0], currentCellCoord[1],
                                                                 activePiece[0], activePiece[
                                                                     1]) and not castling:  # for a blank clicked cell
                    clickedPiece[3] = activePiece[3]
                    clickedPiece[4] = activePiece[4]
                    activePiece[3] = "\u2003"
                    activePiece = []
                    activePieceBool = "NoActivePiece"
                    if turn == "white" and not turnChange:
                        turn = "black"
                        turnChange = True
                    if turn == "black" and not turnChange:
                        turn = "white"
                        turnChange = True
                    turnChange = False
                    baseReDraw()
            justActivated = False
            if activePieceBool == "NoActivePiece":
                print(f"Turn: {turn}")
            else:
                if activePieceBool == "NoActivePiece":
                    print(f"Turn: {turn}")
                else:
                    print(f"{pieceType}, {turn}")

        def pieceDeactivate(event=None):
            global activePiece, activePieceBool
            if currentCellCoord == (activePiece[0], activePiece[1]):
                pieceLabel["fg"] = pieceColour
                activePiece = []
                activePieceBool = "NoActivePiece"

        # creating the label with the piece
        pieceLabel = Label(master, text=pieceType, bg=tileColour, fg=pieceColour, font=("Helvetica", TEXT_SIZE))
        pieceLabel.grid(row=xCoord, column=yCoord)

        # creating the bindings for one cell
        pieceLabel.bind("<Leave>", removeHover)
        pieceLabel.bind("<Button-1>", pieceMovement)
        pieceLabel.bind("<Button-3>", pieceDeactivate)
        pieceLabel.bind("<Enter>", hoverAnimation)


# Board initialization
board = Tk()
board.title("Chess")
icon = PhotoImage(file="Images/chess.png")
board.iconphoto(True, icon)
board.resizable(width=False, height=False)


# Board functions

def createBase():  # function that creates base for the first base
    global cellList
    patternType = "DarkLight"  # / "LightDark"

    # manually creating the initial positions for the pieces

    # black side
    Board(boardPanel, 0, 0, colours[0], "♜", colours[2], False)
    Board(boardPanel, 0, 1, colours[1], "♞", colours[2], False)
    Board(boardPanel, 0, 2, colours[0], "♝", colours[2], False)
    if not theocracy:
        Board(boardPanel, 0, 3, colours[1], "♛", colours[2], False)
    else:
        Board(boardPanel, 0, 3, colours[1], "\u2003", colours[2], False)
    Board(boardPanel, 0, 4, colours[0], "♚", colours[2], False)
    Board(boardPanel, 0, 5, colours[1], "♝", colours[2], False)
    Board(boardPanel, 0, 6, colours[0], "♞", colours[2], False)
    Board(boardPanel, 0, 7, colours[1], "♜", colours[2], False)
    for y in TABLE_COORDINATES:
        while y % 2 == 0:
            Board(boardPanel, 1, y, colours[1], "♟", colours[2], False)
            break
        while y % 2 != 0:
            Board(boardPanel, 1, y, colours[0], "♟", colours[2], False)
            break

    for x in TABLE_COORDINATES[2:6]:
        for y in TABLE_COORDINATES:
            if patternType == "DarkLight":
                while y % 2 == 0:
                    Board(boardPanel, x, y, colours[0], " ", colours[2], False)
                    break
                while y % 2 != 0:
                    Board(boardPanel, x, y, colours[1], " ", colours[3], False)
                    break
            if patternType == "LightDark":
                while y % 2 != 0:
                    Board(boardPanel, x, y, colours[0], " ", colours[2], False)
                    break
                while y % 2 == 0:
                    Board(boardPanel, x, y, colours[1], " ", colours[3], False)
                    break
        if patternType == "DarkLight":
            patternType = "LightDark"
        elif patternType == "LightDark":
            patternType = "DarkLight"

    # white side
    for y in TABLE_COORDINATES:
        while y % 2 == 0:
            Board(boardPanel, 6, y, colours[0], "♙", colours[3], False)
            break
        while y % 2 != 0:
            Board(boardPanel, 6, y, colours[1], "♙", colours[3], False)
            break
    Board(boardPanel, 7, 0, colours[1], "♖", colours[3], False)
    Board(boardPanel, 7, 1, colours[0], "♘", colours[3], False)
    Board(boardPanel, 7, 2, colours[1], "♗", colours[3], False)
    if not theocracy:
        Board(boardPanel, 7, 3, colours[0], "♕", colours[3], False)
    else:
        Board(boardPanel, 7, 3, colours[0], "\u2003", colours[3], False)
    Board(boardPanel, 7, 4, colours[1], "♔", colours[3], False)
    Board(boardPanel, 7, 5, colours[0], "♗", colours[3], False)
    Board(boardPanel, 7, 6, colours[1], "♘", colours[3], False)
    Board(boardPanel, 7, 7, colours[0], "♖", colours[3], False)


def baseReDraw():
    global cellList
    if not swap:
        for cell in cellList:
            Board(boardPanel, cell[0], cell[1], cell[2], cell[3], cell[4], False)
    else:
        for cell in cellList:
            x = False
            if cell[2] == colours[0] and not x:
                cell[2] = colours[1]
                x = True
            if cell[2] == colours[1] and not x:
                cell[2] = colours[0]
                x = True
            x = False
            Board(boardPanel, cell[0], cell[1], cell[2], cell[3], cell[4], False)


def pieceFromCoordinates(row, column):
    global cellList
    y = 0
    x = column
    if row != 0:
        y = row * 8
        return cellList[y + x]
    if row == 0:
        return cellList[y + x]


# creating the panel that has the pieces
boardPanel = PanedWindow(board, bd=5, relief="raised", bg="#464444")
boardPanel.grid(row=0, column=0, sticky=W + E + N + S)

# creating blank chessboard for the first time
createBase()

board.mainloop()
