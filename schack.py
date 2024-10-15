import itertools

def cartesian_product():
    range1 = range(1,9)
    range2 = range(1,9)
    
    return list(itertools.product(range1, range2))

class piece:
    def __init__(self, pjäs, color, coordinate):
        self.pjäs = pjäs
        self.color = color
        self.coordinate = coordinate

def draw_board(dict1):
    for e in range(8, -1, -1):
        for i in squares[e*8:(e+1)*8]:
            if i in dict1:
                print("|"+returnSymbol(dict1[i]), end="")
            else:
                print("| ", end="")
        print()

def placePiecesOnBoard():
    listOfPieces = []
    listOfPieces.append(piece("pawn", "white", (2, 1)))
    listOfPieces.append(piece("pawn", "white", (2, 2)))
    listOfPieces.append(piece("pawn", "white", (2, 3)))
    listOfPieces.append(piece("pawn", "white", (2, 4)))
    listOfPieces.append(piece("pawn", "white", (2, 5)))
    listOfPieces.append(piece("pawn", "white", (2, 6)))
    listOfPieces.append(piece("pawn", "white", (2, 7)))
    listOfPieces.append(piece("pawn", "white", (2, 8)))
    listOfPieces.append(piece("rook", "white", (1, 1)))
    listOfPieces.append(piece("knight", "white", (1, 2)))
    listOfPieces.append(piece("bishop", "white", (1, 3)))
    listOfPieces.append(piece("king", "white", (1, 4)))
    listOfPieces.append(piece("queen", "white", (1, 5)))
    listOfPieces.append(piece("bishop", "white", (1,6)))
    listOfPieces.append(piece("knight", "white", (1, 7)))
    listOfPieces.append(piece("rook", "white", (1, 8)))
    listOfPieces.append(piece("pawn", "black", (7, 1)))
    listOfPieces.append(piece("pawn", "black", (7, 2)))
    listOfPieces.append(piece("pawn", "black", (7, 3)))
    listOfPieces.append(piece("pawn", "black", (7, 4)))
    listOfPieces.append(piece("pawn", "black", (7, 5)))
    listOfPieces.append(piece("pawn", "black", (7, 6)))
    listOfPieces.append(piece("pawn", "black", (7, 7)))
    listOfPieces.append(piece("pawn", "black", (7, 8)))
    listOfPieces.append(piece("rook", "black", (8, 1)))
    listOfPieces.append(piece("knight", "black", (8, 2)))
    listOfPieces.append(piece("bishop", "black", (8, 3)))
    listOfPieces.append(piece("king", "black", (8, 4)))
    listOfPieces.append(piece("queen", "black", (8, 5)))
    listOfPieces.append(piece("bishop", "black", (8,6)))
    listOfPieces.append(piece("knight", "black", (8, 7)))
    listOfPieces.append(piece("rook", "black", (8, 8)))
    for i in listOfPieces:
        squaresWithPiecesOnThem.append(i.coordinate)
    return listOfPieces

def dictionaryWithPieces(list1, listaOfPieces):
    dict1 = {}
    for e in list1:
        if e in squaresWithPiecesOnThem:
            for i in listaOfPieces:
                if i.coordinate == e:
                    dict1[e] = i
    return dict1

def returnSymbol(apiece):
    if apiece.color == "white":
        if apiece.pjäs == "pawn":
            return "P"
        elif apiece.pjäs == "rook":
            return "R"
        elif apiece.pjäs == "knight":
            return "K"
        elif apiece.pjäs == "bishop":
            return "B"
        elif apiece.pjäs == "king":
            return "#"
        else:
            return "Q"
    else:
        if apiece.pjäs == "pawn":
            return "p"
        elif apiece.pjäs == "rook":
            return "r"
        elif apiece.pjäs == "knight":
            return "k"
        elif apiece.pjäs == "bishop":
            return "b"
        elif apiece.pjäs == "king":
            return "#"
        else:
            return "q"




squares = cartesian_product()
squaresWithPiecesOnThem = []
pieces = placePiecesOnBoard()
squaresDict = dictionaryWithPieces(squares, pieces)
draw_board(squaresDict)

user_input = input()
