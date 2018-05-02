import random

def printBoard(board):
    # This function prints board
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])


def randomLetterAssign():
    # Letter assignments
    tic = ''
    letters="XO"
    while not (tic == "X" or tic == "O"):
        tic = random.choice(letters)
        if tic == "X":
            return ["X", "O"]
        else:
            return ["O", "X"]


def selectFirstPlayer():
    if random.randint(0, 1) == 0:
        return "computer2"
    else:
        return "computer1"

def makeMove(board, letter, move):
    board[move] = letter


def checkWinner(board, le):
    return (
            (board[7] == le and board[8] == le and board[9] == le) or
            (board[4] == le and board[5] == le and board[6] == le) or
            (board[1] == le and board[2] == le and board[3] == le) or
            (board[7] == le and board[4] == le and board[1] == le) or
            (board[8] == le and board[5] == le and board[2] == le) or
            (board[9] == le and board[6] == le and board[3] == le) or
            (board[7] == le and board[5] == le and board[3] == le) or
            (board[9] == le and board[5] == le and board[1] == le))


def getBoardCopy(board):
    copyBoard = []
    for i in board:
        copyBoard.append(i)
    return copyBoard

def isSpaceFree(board, move):
    return board[move] == " "

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        #not a valid move.
        return None

def getMoveonBoard(board, letter):
    if letter == "X":
        comp1Letter = "O"
    else:
        comp1Letter = "X"

    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, letter, i)
            if checkWinner(copy, letter):
                return i

    #Check for winning move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, comp1Letter, i)
            if checkWinner(copy, comp1Letter):
                return i

    #Place in corner
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Place in Center
    if isSpaceFree(board, 5):
        return 5

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


while True:
    mainBoard = [' '] * 10
    comp1Letter, comp2Letter = randomLetterAssign()
    turn = selectFirstPlayer()
    print(turn +" Plays First")
    playGame = True

    while playGame:
        if turn == 'computer1':
            # Computer1 turn.
            move = getMoveonBoard(mainBoard, comp1Letter)
            makeMove(mainBoard, comp1Letter, move)
            if checkWinner(mainBoard, comp1Letter):
                print(" Computer 1 beats Computer 2 ")
                printBoard(mainBoard)
                playGame = False
            else:
                if isBoardFull(mainBoard):
                    printBoard(mainBoard)
                    print("It's  a tie!")
                    break
                else:
                    turn = "computer2"
                    print("After Computer 1's Turn")
                    printBoard(mainBoard)

        else:
            # Computer2  turn.
            move = getMoveonBoard(mainBoard, comp2Letter)
            makeMove(mainBoard, comp2Letter, move)
            if checkWinner(mainBoard, comp2Letter):
                print("Computer 2 beats Computer 1")
                printBoard(mainBoard)
                playGame = False
            else:
                if isBoardFull(mainBoard):
                    printBoard(mainBoard)
                    print("It's  a tie!")
                    break
                else:
                    turn = "computer1"
                    print("After Computer 2's Turn")
                    printBoard(mainBoard)

    if not raw_input("Do you want them to play again? Yes or No ").lower().startswith('y'):
        break