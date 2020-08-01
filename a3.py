import sys
import numpy as np
import copy

def display(state):
    new_state=""
    for i in state:
        if i == "":
            new_state+='*'
        else:
            new_state+=str(i)
    print(new_state[0],new_state[1],new_state[2])
    print(new_state[3],new_state[4],new_state[5])
    print(new_state[6],new_state[7],new_state[8])
    return
def check_three_in_a_row(state,move=None):           ##check the crosses
    if move ==None:                                  ##based on the row of the move and check the corresponding lines
        return 1                                     ##if there is three in a row due to the move, return -1
    if(state[0]==state[4]==state[8]):                ##if there is no three in a row due to the move, return  1
        return -1
    if(state[2]==state[4]==state[6]):
        return -1
    if(move<3):
        if(state[0]==state[1]==state[2]):
            return -1
        if(state[move]==state[move+3]==state[move+6]):
            return -1
        else:
            return 1
    elif(move>5):
        if(state[6]==state[7]==state[8]):
            return -1
        if(state[move]==state[move-3]==state[move-6]):
            return -1
        else:
            return 1
    else:
        if(state[3]==state[4]==state[5]):
            return -1
        if(state[move]==state[move+3]==state[move-3]):
            return -1
        else:
            return 1
        
def random_playout(state,available_move,play_times = 1000):      ##play the same board randomly 1000 times
    count =[0,0,0]
    while play_times>0:
        new_board = copy.deepcopy(state)                        ##the board for one game
        one_game_available_move = copy.deepcopy(available_move) ##the number of moves for one game
        players = True if len(one_game_available_move)%2==1 else False ##first random player is True, second random player is False
        play_times-=1
        while one_game_available_move !=[]: 
            rand_move = np.random.choice(len(one_game_available_move)) ##choose a random move
            if players ==True:
                new_board[one_game_available_move[rand_move]]= "O" ##update the board
            else:
                new_board[one_game_available_move[rand_move]]= "X" ##update the board
            value = check_three_in_a_row(new_board,one_game_available_move[rand_move])
            one_game_available_move.remove(one_game_available_move[rand_move])           ##remove the chosen move
            if value == -1 and players == True:                 ##player1 wins [0,0,0]-->][1,0,0]
                count[value+1]+= 1
                break
            elif value == -1 and players == False:              ##player1 loses [0,0,0]-->][0,1,0]
                count[value+2]+=1
                break
            elif value == 1 and len(one_game_available_move) == 0:  ##draw [0,0,0]-->][0,0,1]
                count [value+1]+=1
                break
            else:
                players = np.invert(players)                    ##switch player  
    return count

def AI_move(state,available_move):
    values = []
    AI = True if len(available_move)%2==1 else False                ##first random player is True, second random player is False
    for move in available_move:
        possible_state = copy.deepcopy(state)
        possible_moves = copy.deepcopy(available_move)
        if AI == True:
            possible_state[move]= "O"
        else:
            possible_state[move]= "X"
        value = check_three_in_a_row(possible_state,move)
        if value == -1:                                             ##100% win
            return move
        else:
            possible_moves.remove(move)
            value = random_playout(possible_state,possible_moves)   ##gather the win/lose/draw information
            values.append(value[0]*2+value[2])
    print(values)
    if AI== True:                                                   #first player
        return available_move[values.index(max(values))]            ##select the move with highest winning rate
    else:                                                           ##second player
        return available_move[values.index(min(values))]            ##select the move with lowest lossing rate

def play_a_new_game():
    print("This is a Tic-Tac-Toe game. The player will play against computer.")
    print("In order to win the game, player must place three of their marks in a horizontal, vertical or diagonal row.")
    print("The game board is the following the graph.")
    board = [1,2,3,4,5,6,7,8,9]
    legal_move = [0,1,2,3,4,5,6,7,8]                        ##based on the index of list however people thinks the board is from 1 to 9
    display(board)
    print("choose the number to place your mark on the board")
    while(True):
        user_preference = input("Do you want to play first with 'O' yes/no: ")
        if user_preference == "no":
            print("---------------------AI's turn--------------------")
            move = AI_move(board,legal_move)
            print("AI choice: ",move+1)
            board[move] = 'O'
            legal_move.remove(move)
            break
        elif user_preference == "yes":
            break
        else:
            print("Invalid input !! Enter it again !!")
    display(board)
    while True:
        
        print("---------------------Player's turn--------------------")
        print("Enter one of the number on the board")
        check = True
        while True:
            try:
                user_move = int(input("Your choice: "))                 
            except:                                       ##check if the choice is an integer
                print("user_move is not a number")
                continue
            if user_move-1 not in legal_move:                       ##check if the choice is a legal move
                print("Not a legal move !!")
                continue
            else:
                Player = True if len(legal_move)%2==1 else False    ##check if player is 1st move or 2nd move
                if Player == True:
                    board[user_move-1] = 'O'
                else:
                    board[user_move-1] = 'X'
                print(board)
                legal_move.remove(user_move-1)
                print(legal_move)
                display(board)
                value = check_three_in_a_row(board,user_move-1)
                if value == -1:
                    print("You win the game !!")
                    exit()
                elif value == 1 and len(legal_move) == 0:
                    print("Draw game !!")
                    exit()
                break
        print("---------------------AI's turn--------------------")
        move = AI_move(board,legal_move)
        print(legal_move)
        print("AI choice: ",move+1)
        AI = True if len(legal_move)%2==1 else False                ##check if AI is 1st move or 2nd move
        if AI == True:
            board[move] = 'O'
        else:
            board[move] = 'X'
        legal_move.remove(move)
        display(board)
        value = check_three_in_a_row(board,move)
        if value == -1:
            print("AI wins the game !!")
            exit()
        elif value == 1 and len(legal_move) == 0:
            print("Draw game !!")
            exit()
        
if __name__ == '__main__':
  play_a_new_game()
      

            

